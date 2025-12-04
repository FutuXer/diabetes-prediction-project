"""
糖尿病数据集 - 可视化分析模块（终极修复版）
作者: 成员A
功能: 探索性数据分析（EDA）、模式识别、异常值检测
"""

import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('Agg')  # 使用非交互式后端，不显示图形窗口
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')


# ============ 配置中文字体 ============
def setup_chinese_font():
    """配置中文字体 - 每次绘图前调用"""
    fm._load_fontmanager(try_read_cache=False)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False


# 初始化设置
setup_chinese_font()
sns.set_style("whitegrid")
sns.set_palette("husl")

print("\n" + "=" * 60)
print("中文字体配置完成：Microsoft YaHei")
print("=" * 60 + "\n")


class DiabetesVisualizer:
    """糖尿病数据可视化类"""

    def __init__(self, data_path='./data/raw/diabetes.csv'):
        """初始化并加载数据"""
        self.df = pd.read_csv(data_path)
        self.feature_names = self.df.columns[:-1].tolist()
        self.target = 'Outcome'

        # 特征中文名映射
        self.feature_names_cn = {
            'Pregnancies': '怀孕次数',
            'Glucose': '血糖浓度',
            'BloodPressure': '舒张压',
            'SkinThickness': '皮褶厚度',
            'Insulin': '胰岛素',
            'BMI': '体质指数',
            'DiabetesPedigreeFunction': '遗传函数',
            'Age': '年龄'
        }

    def plot_overview(self):
        """数据概览可视化"""
        setup_chinese_font()  # 确保字体设置生效

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('数据集整体概览', fontsize=16, fontweight='bold')

        # 1. 目标变量分布
        ax1 = axes[0, 0]
        outcome_counts = self.df[self.target].value_counts()
        colors = ['#2ecc71', '#e74c3c']
        ax1.pie(outcome_counts, labels=['未患病', '患病'], autopct='%1.1f%%',
                colors=colors, startangle=90, textprops={'fontsize': 12})
        ax1.set_title(f'患病率: {self.df[self.target].mean() * 100:.1f}%',
                      fontsize=13, fontweight='bold')

        # 2. 样本数量
        ax2 = axes[0, 1]
        ax2.bar(['总样本', '未患病', '患病'],
                [len(self.df), outcome_counts[0], outcome_counts[1]],
                color=['#3498db', '#2ecc71', '#e74c3c'])
        ax2.set_ylabel('样本数量', fontsize=12)
        ax2.set_title('样本分布统计', fontsize=13, fontweight='bold')
        for i, v in enumerate([len(self.df), outcome_counts[0], outcome_counts[1]]):
            ax2.text(i, v + 10, str(v), ha='center', fontsize=11, fontweight='bold')

        # 3. 特征数据类型
        ax3 = axes[1, 0]
        ax3.axis('off')
        info_text = f"""
        数据集基本信息:

        • 样本数量: {len(self.df)} 行
        • 特征数量: {len(self.feature_names)} 个
        • 目标变量: {self.target}
        • 数据类型: 全部为数值型
        • 缺失值: {'无' if self.df.isnull().sum().sum() == 0 else '有'}
        • 数据大小: {self.df.memory_usage(deep=True).sum() / 1024:.2f} KB
        """
        ax3.text(0.1, 0.5, info_text, fontsize=11, verticalalignment='center',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        # 4. 特征列表
        ax4 = axes[1, 1]
        ax4.axis('off')
        features_text = "特征列表:\n\n" + "\n".join([
            f"{i + 1}. {name:25s} ({self.feature_names_cn.get(name, name)})"
            for i, name in enumerate(self.feature_names)
        ])
        ax4.text(0.1, 0.5, features_text, fontsize=10, verticalalignment='center',
                 bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

        plt.tight_layout()
        plt.savefig('./docs/images/01_overview.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✓ 数据概览图已保存")

    def plot_distributions(self):
        """特征分布可视化"""
        setup_chinese_font()  # 确保字体设置生效

        fig, axes = plt.subplots(4, 2, figsize=(14, 16))
        fig.suptitle('各特征分布分析', fontsize=16, fontweight='bold', y=0.995)

        for idx, feature in enumerate(self.feature_names):
            ax = axes[idx // 2, idx % 2]

            # 绘制直方图和KDE
            self.df[feature].hist(bins=30, alpha=0.6, color='skyblue',
                                  edgecolor='black', ax=ax, density=True)
            self.df[feature].plot.kde(ax=ax, color='red', linewidth=2)

            # 添加均值和中位数线
            mean_val = self.df[feature].mean()
            median_val = self.df[feature].median()
            ax.axvline(mean_val, color='green', linestyle='--', linewidth=2, label=f'均值: {mean_val:.1f}')
            ax.axvline(median_val, color='orange', linestyle='--', linewidth=2, label=f'中位数: {median_val:.1f}')

            ax.set_title(f'{feature} ({self.feature_names_cn.get(feature, feature)})',
                         fontsize=12, fontweight='bold')
            ax.set_xlabel('数值', fontsize=10)
            ax.set_ylabel('密度', fontsize=10)
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('./docs/images/02_distributions.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✓ 特征分布图已保存")

    def plot_boxplots(self):
        """箱线图 - 识别异常值"""
        setup_chinese_font()  # 确保字体设置生效

        fig, axes = plt.subplots(4, 2, figsize=(14, 16))
        fig.suptitle('箱线图分析（异常值检测）', fontsize=16, fontweight='bold', y=0.995)

        for idx, feature in enumerate(self.feature_names):
            ax = axes[idx // 2, idx % 2]

            # 绘制箱线图
            bp = ax.boxplot([self.df[feature]], vert=True, patch_artist=True,
                            labels=[feature], widths=0.5)

            # 美化箱线图
            bp['boxes'][0].set_facecolor('lightblue')
            bp['boxes'][0].set_edgecolor('blue')
            bp['medians'][0].set_color('red')
            bp['medians'][0].set_linewidth(2)

            # 计算异常值
            Q1 = self.df[feature].quantile(0.25)
            Q3 = self.df[feature].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[feature] < Q1 - 1.5 * IQR) |
                               (self.df[feature] > Q3 + 1.5 * IQR)][feature]

            ax.set_title(f'{self.feature_names_cn.get(feature, feature)}\n异常值: {len(outliers)} 个',
                         fontsize=11, fontweight='bold')
            ax.set_ylabel('数值', fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')

            # 添加统计信息
            stats_text = f"Q1={Q1:.1f}\nQ3={Q3:.1f}\nIQR={IQR:.1f}"
            ax.text(1.15, Q1, stats_text, fontsize=8,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

        plt.tight_layout()
        plt.savefig('./docs/images/03_boxplots.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✓ 箱线图已保存")

    def plot_outcome_comparison(self):
        """患病vs非患病组对比"""
        setup_chinese_font()  # 确保字体设置生效

        fig, axes = plt.subplots(4, 2, figsize=(14, 16))
        fig.suptitle('患病 vs 非患病组特征对比', fontsize=16, fontweight='bold', y=0.995)

        for idx, feature in enumerate(self.feature_names):
            ax = axes[idx // 2, idx % 2]

            # 分组数据
            data_0 = self.df[self.df[self.target] == 0][feature]
            data_1 = self.df[self.df[self.target] == 1][feature]

            # 绘制小提琴图
            parts = ax.violinplot([data_0, data_1], positions=[1, 2],
                                  showmeans=True, showmedians=True)

            # 美化小提琴图
            for pc in parts['bodies']:
                pc.set_facecolor('lightblue')
                pc.set_alpha(0.6)

            # 添加箱线图
            bp = ax.boxplot([data_0, data_1], positions=[1, 2], widths=0.3,
                            patch_artist=True, showfliers=False)
            for patch, color in zip(bp['boxes'], ['green', 'red']):
                patch.set_facecolor(color)
                patch.set_alpha(0.5)

            ax.set_xticks([1, 2])
            ax.set_xticklabels(['非患病', '患病'], fontsize=10)
            ax.set_title(f'{self.feature_names_cn.get(feature, feature)}',
                         fontsize=12, fontweight='bold')
            ax.set_ylabel('数值', fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')

            # 添加均值差异
            mean_diff = data_1.mean() - data_0.mean()
            color = 'red' if mean_diff > 0 else 'green'
            ax.text(1.5, ax.get_ylim()[1] * 0.95, f'差异: {mean_diff:+.1f}',
                    ha='center', fontsize=9, color=color, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

        plt.tight_layout()
        plt.savefig('./docs/images/04_outcome_comparison.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✓ 分组对比图已保存")

    def plot_correlation_heatmap(self):
        """相关系数热力图"""
        setup_chinese_font()  # 确保字体设置生效

        plt.figure(figsize=(12, 10))

        # 计算相关系数
        corr_matrix = self.df.corr()

        # 绘制热力图
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                    cmap='coolwarm', center=0, square=True, linewidths=1,
                    cbar_kws={"shrink": 0.8})

        plt.title('特征相关性热力图', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('./docs/images/05_correlation_heatmap.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✓ 相关性热力图已保存")

        # 打印强相关特征对
        print("\n强相关特征对（|r| > 0.3）:")
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.3:
                    print(
                        f"  • {corr_matrix.columns[i]:25s} <-> {corr_matrix.columns[j]:25s}: {corr_matrix.iloc[i, j]:+.3f}")

    def plot_pairplot(self):
        """散点图矩阵（选择关键特征）"""
        setup_chinese_font()  # 确保字体设置生效

        # 选择最重要的特征
        key_features = ['Glucose', 'BMI', 'Age', 'Insulin', self.target]

        plt.figure(figsize=(12, 10))
        pair_plot = sns.pairplot(self.df[key_features], hue=self.target,
                                 palette={0: 'green', 1: 'red'},
                                 diag_kind='kde', plot_kws={'alpha': 0.6})
        pair_plot.fig.suptitle('关键特征散点图矩阵', y=1.02, fontsize=16, fontweight='bold')

        plt.savefig('./docs/images/06_pairplot.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✓ 散点图矩阵已保存")

    def generate_summary_report(self):
        """生成分析总结报告"""
        report = []
        report.append("=" * 60)
        report.append("糖尿病数据集 - 可视化分析总结报告")
        report.append("=" * 60)
        report.append("")

        # 1. 数据集概况
        report.append("【1. 数据集概况】")
        report.append(f"  • 样本总数: {len(self.df)}")
        report.append(f"  • 特征数量: {len(self.feature_names)}")
        report.append(f"  • 患病样本: {self.df[self.target].sum()} ({self.df[self.target].mean() * 100:.1f}%)")
        report.append(
            f"  • 非患病样本: {len(self.df) - self.df[self.target].sum()} ({(1 - self.df[self.target].mean()) * 100:.1f}%)")
        report.append("")

        # 2. 异常值统计
        report.append("【2. 异常值统计】")
        for feature in self.feature_names:
            Q1 = self.df[feature].quantile(0.25)
            Q3 = self.df[feature].quantile(0.75)
            IQR = Q3 - Q1
            outliers = len(self.df[(self.df[feature] < Q1 - 1.5 * IQR) |
                                   (self.df[feature] > Q3 + 1.5 * IQR)])
            report.append(f"  • {feature:25s}: {outliers:3d} 个异常值 ({outliers / len(self.df) * 100:.1f}%)")
        report.append("")

        # 3. 零值统计
        report.append("【3. 零值统计（可能的隐藏缺失值）】")
        zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
        for col in zero_cols:
            zero_count = (self.df[col] == 0).sum()
            report.append(f"  • {col:25s}: {zero_count:3d} 个零值 ({zero_count / len(self.df) * 100:.1f}%)")
        report.append("")

        # 4. 特征与目标变量的相关性
        report.append("【4. 特征与患病风险的相关性】")
        correlations = self.df.corr()[self.target].sort_values(ascending=False)[1:]
        for feature, corr in correlations.items():
            report.append(f"  • {feature:25s}: {corr:+.3f}")
        report.append("")

        # 5. 关键发现
        report.append("【5. 关键发现】")
        report.append(f"  • 血糖（Glucose）与患病相关性最强: {correlations['Glucose']:.3f}")
        report.append(f"  • BMI与患病相关性次之: {correlations['BMI']:.3f}")
        report.append(f"  • 年龄也是重要因素: {correlations['Age']:.3f}")
        report.append(f"  • 胰岛素数据存在大量零值: {(self.df['Insulin'] == 0).sum()} 个")
        report.append("")

        # 6. 建议
        report.append("【6. 数据预处理建议】")
        report.append("  • 需要处理Insulin、SkinThickness等列的零值（作为缺失值）")
        report.append("  • 异常值需要进一步检查其医学合理性")
        report.append("  • 建议对数值特征进行标准化")
        report.append("  • 可以考虑创建衍生特征（如BMI分类、年龄分组等）")
        report.append("")

        report.append("=" * 60)

        # 保存报告
        report_text = "\n".join(report)
        with open('./docs/visualization_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(report_text)
        print("\n✓ 分析报告已保存到 ./docs/visualization_report.txt")

    def run_all_analysis(self):
        """运行所有可视化分析"""
        import os
        os.makedirs('./docs/images', exist_ok=True)

        print("\n开始执行可视化分析...")
        print("-" * 60)

        print("\n[1/7] 数据概览...")
        self.plot_overview()

        print("\n[2/7] 特征分布分析...")
        self.plot_distributions()

        print("\n[3/7] 箱线图分析...")
        self.plot_boxplots()

        print("\n[4/7] 分组对比分析...")
        self.plot_outcome_comparison()

        print("\n[5/7] 相关性分析...")
        self.plot_correlation_heatmap()

        print("\n[6/7] 散点图矩阵...")
        self.plot_pairplot()

        print("\n[7/7] 生成分析报告...")
        self.generate_summary_report()

        print("\n" + "=" * 60)
        print("✓ 所有可视化分析已完成！")
        print("✓ 图表保存位置: ./docs/images/")
        print("✓ 报告保存位置: ./docs/visualization_report.txt")
        print("=" * 60)


if __name__ == '__main__':
    # 创建可视化对象
    visualizer = DiabetesVisualizer('./data/raw/diabetes.csv')

    # 运行所有分析
    visualizer.run_all_analysis()