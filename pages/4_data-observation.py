"""
糖尿病预测项目 - Streamlit数据观测
作者: 成员A
功能: 交互式数据可视化探索
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import warnings

warnings.filterwarnings('ignore')


# ============ 配置中文字体 ============
def setup_chinese_font():
    """配置中文字体 - 每次绘图前调用"""
    fm._load_fontmanager(try_read_cache=False)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False


# 初始化字体
setup_chinese_font()

# 页面配置
st.set_page_config(
    page_title="数据可视化分析 - 糖尿病预测",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ 现代化扁平风格CSS ============
st.markdown("""
<style>
    /* 全局字体和背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 主容器 */
    .main > div {
        padding-top: 2rem;
    }

    /* 超级标题 */
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }

    /* 导航标签样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8fafc;
        padding: 8px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
        font-size: 15px;
        padding: 0 24px;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    /* 卡片样式 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        height: 100%;
    }

    .metric-card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-delta {
        color: #10b981;
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* 信息框 */
    .info-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }

    .success-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }

    .warning-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    /* 选择框样式 */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* 数据框样式 */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }

    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }

    [data-testid="stSidebar"] .element-container {
        transition: all 0.3s ease;
    }

    /* 分隔线 */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
    }

    /* 图表容器 */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }

    /* 徽章 */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* 统计卡片网格 */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitVisualizer:
    """Streamlit数据可视化类"""

    def __init__(self, data_path='./src/data/diabetes.csv'):
        """初始化并加载数据"""
        try:
            self.df = pd.read_csv(data_path)
        except FileNotFoundError:
            # 尝试其他可能的路径
            possible_paths = [
                './data/raw/diabetes.csv',
                '../data/raw/diabetes.csv',
                './diabetes.csv',
                '../diabetes.csv'
            ]
            for path in possible_paths:
                try:
                    self.df = pd.read_csv(path)
                    break
                except FileNotFoundError:
                    continue
            else:
                raise FileNotFoundError("无法找到糖尿病数据集文件")
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


def render_metric_card(label, value, delta=None, icon="📊", description=""):
    """渲染指标卡片"""
    delta_html = f'<div style="color: #10b981; font-size: 0.875rem; font-weight: 600; margin-top: 0.5rem;">↑ {delta}</div>' if delta else ''
    description_html = f'<div style="color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-top: 0.25rem; font-style: italic;">{description}</div>' if description else ''
    return f"""
    <div class="metric-card">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
        {description_html}
    </div>
    """


def main():
    """主函数"""

    # 页面标题
    st.markdown('<h1 class="hero-title">📈 数据可视化分析</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">深入了解糖尿病数据集的特征与分布</p>', unsafe_allow_html=True)

    # 加载数据
    try:
        viz = StreamlitVisualizer()
        df = viz.df
        st.success("数据加载成功！")
    except Exception as e:
        st.error(f"❌ 数据加载失败: {e}", icon="❌")
        st.stop()

    # 导航标签
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "数据概览",
        "数据预处理",
        "单变量分析",
        "双变量分析",
        "相关性分析",
        "风险因素排序"  # 新增
    ])

    # ==================== Tab 1: 数据概览 =====================
    with tab1:
        st.markdown("### 📌 核心指标")

        # 指标卡片
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(render_metric_card(
                "样本总数",
                f"{len(df):,}",
                icon="📦"
            ), unsafe_allow_html=True)

        with col2:
            st.markdown(render_metric_card(
                "特征数量",
                f"{len(viz.feature_names)}",
                icon="🎯"
            ), unsafe_allow_html=True)

        with col3:
            st.markdown(render_metric_card(
                "患病样本",
                f"{df[viz.target].sum():,}",
                delta=f"{df[viz.target].mean() * 100:.1f}%",
                icon="🏥"
            ), unsafe_allow_html=True)

        with col4:
            st.markdown(render_metric_card(
                "数据质量",
                "优秀",
                delta="无缺失值",
                icon="✨"
            ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 两列布局
        col1, col2 = st.columns([1.5, 1])

        with col1:
            st.markdown("### 📊 目标变量分布")

            # 确保每次绘图前设置字体
            setup_chinese_font()

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # 饼图
            outcome_counts = df[viz.target].value_counts()
            colors = ['#10b981', '#ef4444']
            wedges, texts, autotexts = ax1.pie(
                outcome_counts,
                labels=['未患病', '患病'],
                autopct='%1.1f%%',
                colors=colors,
                startangle=90,
                textprops={'fontsize': 11, 'weight': 'bold'}
            )
            ax1.set_title('患病比例', fontsize=13, fontweight='bold', pad=15)

            # 柱状图
            categories = ['总样本', '未患病', '患病']
            values = [len(df), outcome_counts[0], outcome_counts[1]]
            bars = ax2.bar(categories, values,
                           color=['#667eea', '#10b981', '#ef4444'],
                           alpha=0.8, edgecolor='white', linewidth=2)
            ax2.set_ylabel('样本数量', fontsize=11, fontweight='bold')
            ax2.set_title('样本分布统计', fontsize=13, fontweight='bold', pad=15)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.grid(axis='y', alpha=0.3, linestyle='--')

            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{int(height)}',
                         ha='center', va='bottom', fontsize=10, fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        with col2:
            st.markdown("### 📝 数据摘要")

            st.markdown(f"""
            <div class="info-box">
                <h4 style="margin-top: 0; color: #1e40af;">基本信息</h4>
                <p style="margin: 0.5rem 0;"><strong>样本数量:</strong> {len(df)} 行</p>
                <p style="margin: 0.5rem 0;"><strong>特征数量:</strong> {len(viz.feature_names)} 个</p>
                <p style="margin: 0.5rem 0;"><strong>目标变量:</strong> {viz.target}</p>
                <p style="margin: 0.5rem 0;"><strong>数据类型:</strong> 全部数值型</p>
                <p style="margin: 0.5rem 0;"><strong>缺失值:</strong> {'无' if df.isnull().sum().sum() == 0 else '有'}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="success-box">
                <h4 style="margin-top: 0; color: #059669;">患病率分析</h4>
                <p style="margin: 0.5rem 0;"><strong>患病样本:</strong> {df[viz.target].sum()} 例</p>
                <p style="margin: 0.5rem 0;"><strong>非患病样本:</strong> {len(df) - df[viz.target].sum()} 例</p>
                <p style="margin: 0.5rem 0;"><strong>患病率:</strong> {df[viz.target].mean() * 100:.1f}%</p>
                <p style="margin: 0.5rem 0; color: #dc2626;"><strong>⚠️ 数据不平衡</strong></p>
            </div>
            """, unsafe_allow_html=True)

        # 描述性统计
        st.markdown("### 📊 描述性统计表")

        # 缓存描述性统计
        @st.cache_data
        def get_descriptive_stats(dataframe):
            return dataframe.describe().T

        stats_df = get_descriptive_stats(df)
        st.dataframe(
            stats_df.style.background_gradient(cmap='Blues', subset=['mean', 'std'])
            .format("{:.2f}"),
            use_container_width=True,
            height=400
        )

        # 数据质量检查
        st.markdown("### 🔍 数据质量检查")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 缺失值检查")
            missing_counts = df.isnull().sum()
            if missing_counts.sum() == 0:
                st.markdown("""
                <div class="success-box">
                    <h4 style="margin-top: 0; color: #059669;">✅ 无标记缺失值</h4>
                    <p style="margin: 0.5rem 0;">数据集中没有显式的缺失值（NaN）</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ 发现缺失值")
                st.dataframe(missing_counts[missing_counts > 0])

        with col2:
            st.markdown("#### 异常值统计")
            outlier_counts = {}
            for feature in viz.feature_names:
                Q1 = df[feature].quantile(0.25)
                Q3 = df[feature].quantile(0.75)
                IQR = Q3 - Q1
                outliers = len(df[(df[feature] < Q1 - 1.5 * IQR) |
                                  (df[feature] > Q3 + 1.5 * IQR)])
                outlier_counts[feature] = outliers

            outlier_df = pd.DataFrame({
                '特征': list(outlier_counts.keys()),
                '异常值数量': list(outlier_counts.values()),
                '占比': [f"{v / len(df) * 100:.1f}%" for v in outlier_counts.values()]
            })

            st.dataframe(
                outlier_df.style.background_gradient(cmap='Reds', subset=['异常值数量']),
                use_container_width=True,
                hide_index=True
            )

        # 特征列表和零值检测
        st.markdown("### 📝 特征列表与数据质量")

        # 计算零值
        zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
        zero_counts = {}
        for col in viz.feature_names:
            zero_count = (df[col] == 0).sum()
            zero_counts[col] = zero_count

        feature_df = pd.DataFrame({
            '序号': range(1, len(viz.feature_names) + 1),
            '英文名称': viz.feature_names,
            '中文名称': [viz.feature_names_cn.get(f, f) for f in viz.feature_names],
            '数据类型': ['数值型'] * len(viz.feature_names),
            '零值数量': [zero_counts[f] for f in viz.feature_names],
            '零值占比': [f"{zero_counts[f] / len(df) * 100:.1f}%" for f in viz.feature_names]
        })

        # 高亮显示有零值的行
        def highlight_zeros(row):
            if row['零值数量'] > 0 and row['英文名称'] in zero_cols:
                return ['background-color: #fef3c7'] * len(row)
            return [''] * len(row)

        st.dataframe(
            feature_df.style.apply(highlight_zeros, axis=1),
            use_container_width=True,
            hide_index=True
        )

        # 零值警告摘要
        suspicious_zeros = [(col, zero_counts[col]) for col in zero_cols if zero_counts[col] > 0]
        if suspicious_zeros:
            st.markdown("""
            <div class="warning-box">
                <h4 style="margin-top: 0; color: #d97706;">⚠️ 零值检测（可能的隐藏缺失值）</h4>
            """, unsafe_allow_html=True)

            for col, count in suspicious_zeros:
                st.markdown(f"""
                <p style="margin: 0.3rem 0;">
                    • <strong>{col}</strong> ({viz.feature_names_cn.get(col, col)}): 
                    {count} 个零值 ({count / len(df) * 100:.1f}%)
                </p>
                """, unsafe_allow_html=True)

            st.markdown("""
                <p style="margin-top: 1rem; color: #92400e;">
                    <strong>💡 建议：</strong>这些特征的零值在医学上不合理，应在数据预处理阶段进行处理（如用中位数/均值填充）
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ==================== Tab 2: 数据预处理 ===================
    with tab2:
        st.markdown("### 🔍 数据预处理结果")

        # 预处理概览
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 预处理统计")

            # 缺失值处理统计
            missing_data = {
                'Insulin': 48.70,
                'SkinThickness': 29.56,
                'BloodPressure': 4.56,
                'BMI': 1.43,
                'Glucose': 0.65
            }

            setup_chinese_font()
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#ef4444' if x > 20 else '#f59e0b' if x > 5 else '#10b981' for x in missing_data.values()]
            bars = ax.bar(missing_data.keys(), missing_data.values(), color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

            ax.set_title('各特征缺失值比例（含0值）', fontsize=14, fontweight='bold', pad=15)
            ax.set_ylabel('缺失率 (%)', fontsize=12, fontweight='bold')
            ax.set_xlabel('特征名称', fontsize=12, fontweight='bold')

            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

            # 旋转x轴标签
            plt.xticks(rotation=45, ha='right')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', alpha=0.3, linestyle='--')

            st.pyplot(fig)
            plt.close()

            st.markdown(f"""
            <div class="warning-box">
                <h4 style="margin-top: 0; color: #d97706;">⚠️ 数据质量问题</h4>
                <p style="margin: 0.5rem 0;"><strong>主要问题：</strong></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                    <li><strong>Insulin</strong>缺失率最高（48.7%），将近一半数据需要处理</li>
                    <li><strong>SkinThickness</strong>缺失率较高（29.6%），需要重点关注</li>
                    <li>其他特征缺失率相对较低，但仍有处理价值</li>
                </ul>
                <p style="margin: 0.5rem 0; color: #92400e;">
                    <strong>处理策略：</strong>使用中位数填充，保持数据分布特征
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🎯 异常值检测")

            # 异常值统计
            outlier_data = {
                'SkinThickness': 87,
                'Insulin': 72,
                'DiabetesPedigreeFunction': 29,
                'Age': 9,
                'BMI': 8,
                'BloodPressure': 14,
                'Pregnancies': 4,
                'Glucose': 0
            }

            setup_chinese_font()
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#ef4444' if x > 50 else '#f59e0b' if x > 20 else '#10b981' for x in outlier_data.values()]
            bars = ax.bar(outlier_data.keys(), outlier_data.values(), color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

            ax.set_title('各特征异常值数量（IQR方法）', fontsize=14, fontweight='bold', pad=15)
            ax.set_ylabel('异常值数量', fontsize=12, fontweight='bold')
            ax.set_xlabel('特征名称', fontsize=12, fontweight='bold')

            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

            # 旋转x轴标签
            plt.xticks(rotation=45, ha='right')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', alpha=0.3, linestyle='--')

            st.pyplot(fig)
            plt.close()

            st.markdown(f"""
            <div class="info-box">
                <h4 style="margin-top: 0; color: #1e40af;">📈 异常值分析</h4>
                <p style="margin: 0.5rem 0;"><strong>统计方法：</strong> IQR（四分位距）方法，超过Q1-1.5×IQR或Q3+1.5×IQR视为异常</p>
                <p style="margin: 0.5rem 0;"><strong>主要发现：</strong></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                    <li><strong>SkinThickness</strong>异常值最多（87个），可能与测量误差有关</li>
                    <li><strong>Insulin</strong>异常值较多（72个），存在极值情况</li>
                    <li><strong>Glucose</strong>无异常值，数据质量较好</li>
                </ul>
                <p style="margin: 0.5rem 0; color: #1e40af;">
                    <strong>处理建议：</strong>医学合理性验证，保留有临床意义的极端值
                </p>
            </div>
            """, unsafe_allow_html=True)

        # 数据完整性总结
        st.markdown("---")
        st.markdown("### 📋 数据质量评估")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(render_metric_card(
                "原始数据完整性",
                "90.57%",
                delta="9.43%缺失",
                icon="📊"
            ), unsafe_allow_html=True)

        with col2:
            st.markdown(render_metric_card(
                "重复行检测",
                "0",
                delta="无重复",
                icon="✅"
            ), unsafe_allow_html=True)

        with col3:
            st.markdown(render_metric_card(
                "异常值总数",
                "223",
                delta="需关注",
                icon="⚠️"
            ), unsafe_allow_html=True)

        with col4:
            st.markdown(render_metric_card(
                "数据质量等级",
                "良好",
                delta="可建模",
                icon="⭐"
            ), unsafe_allow_html=True)

        # 预处理流程说明
        st.markdown("---")
        st.markdown("### 🔄 数据预处理流程")

        st.info("📖 预处理步骤")
        st.markdown("**1️⃣ 缺失值处理：**")
        st.markdown("- 识别生理学不合理的0值（血糖、血压、BMI等）")
        st.markdown("- 使用中位数或分组均值填充")
        st.markdown("- 保留原始数据分布特征")

        st.markdown("**2️⃣ 异常值检测：**")
        st.markdown("- IQR方法检测统计异常值")
        st.markdown("- 医学合理性验证")
        st.markdown("- 区分测量误差与真实极值")

        st.markdown("**3️⃣ 数据标准化：**")
        st.markdown("- Z-score标准化")
        st.markdown("- 消除量纲影响")
        st.markdown("- 为建模做准备")

        st.markdown("**🎯 预处理目标：** 提高数据质量，为后续统计建模提供可靠的数据基础")

        # 预处理前后对比（如果有的话）
        st.markdown("---")
        st.markdown("### 📈 预处理效果对比")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 处理前数据")
            before_data = {
                '总数据单元': 6912,
                '缺失单元': 652,
                '完整率': '90.57%',
                '主要问题': '隐藏零值缺失'
            }

            for key, value in before_data.items():
                st.markdown(f"• **{key}**: {value}")

        with col2:
            st.markdown("#### 处理后数据")
            after_data = {
                '总数据单元': 6912,
                '填充单元': 652,
                '完整率': '100%',
                '质量提升': '无缺失值'
            }

            for key, value in after_data.items():
                st.markdown(f"• **{key}**: {value}")

        st.markdown(f"""
        <div class="success-box">
            <h4 style="margin-top: 0; color: #059669;">✅ 预处理完成</h4>
            <p style="margin: 0.5rem 0;">
                <strong>数据质量提升：</strong>从90.57%完整率提升至100%，为后续建模提供了高质量数据基础。
            </p>
            <p style="margin: 0.5rem 0;">
                <strong>下一步：</strong>基于预处理后的数据，可以进行准确的统计建模和特征分析。
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ==================== Tab 3: 单变量分析 ===================
    with tab3:
        st.markdown("### 📈 选择特征进行分析")

        selected_feature = st.selectbox(
            "选择要分析的特征",
            viz.feature_names,
            format_func=lambda x: f"{x} ({viz.feature_names_cn.get(x, x)})"
        )

        # 统计卡片
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(render_metric_card(
                "均值",
                f"{df[selected_feature].mean():.2f}",
                icon="📊"
            ), unsafe_allow_html=True)

        with col2:
            st.markdown(render_metric_card(
                "中位数",
                f"{df[selected_feature].median():.2f}",
                icon="📍"
            ), unsafe_allow_html=True)

        with col3:
            st.markdown(render_metric_card(
                "标准差",
                f"{df[selected_feature].std():.2f}",
                icon="📏"
            ), unsafe_allow_html=True)

        with col4:
            st.markdown(render_metric_card(
                "最小值",
                f"{df[selected_feature].min():.2f}",
                icon="⬇️"
            ), unsafe_allow_html=True)

        with col5:
            st.markdown(render_metric_card(
                "最大值",
                f"{df[selected_feature].max():.2f}",
                icon="⬆️"
            ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 可视化
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 分布直方图 + 密度曲线")

            setup_chinese_font()
            fig, ax = plt.subplots(figsize=(8, 6))

            # 直方图
            n, bins, patches = ax.hist(df[selected_feature], bins=30, alpha=0.6,
                                       color='#667eea', edgecolor='white',
                                       linewidth=1.5, density=True)

            # KDE曲线
            df[selected_feature].plot.kde(ax=ax, color='#ef4444', linewidth=3)

            # 统计线
            mean_val = df[selected_feature].mean()
            median_val = df[selected_feature].median()
            ax.axvline(mean_val, color='#10b981', linestyle='--', linewidth=2.5,
                       label=f'均值: {mean_val:.1f}', alpha=0.8)
            ax.axvline(median_val, color='#f59e0b', linestyle='--', linewidth=2.5,
                       label=f'中位数: {median_val:.1f}', alpha=0.8)

            ax.set_title(f'{selected_feature} 分布', fontsize=13, fontweight='bold', pad=15)
            ax.set_xlabel('数值', fontsize=11)
            ax.set_ylabel('密度', fontsize=11)
            ax.legend(fontsize=10, frameon=True, fancybox=True, shadow=True)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, linestyle='--')

            st.pyplot(fig)
            plt.close()

        with col2:
            st.markdown("#### 📦 箱线图（异常值检测）")

            setup_chinese_font()
            fig, ax = plt.subplots(figsize=(8, 6))

            bp = ax.boxplot([df[selected_feature]], vert=True,
                            labels=[selected_feature], widths=0.5,
                            patch_artist=True,
                            boxprops=dict(facecolor='#667eea', alpha=0.6),
                            medianprops=dict(color='#ef4444', linewidth=2.5),
                            whiskerprops=dict(color='#64748b', linewidth=1.5),
                            capprops=dict(color='#64748b', linewidth=1.5),
                            flierprops=dict(marker='o', markerfacecolor='#ef4444',
                                            markersize=8, alpha=0.6))

            # 计算异常值
            Q1 = df[selected_feature].quantile(0.25)
            Q3 = df[selected_feature].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[selected_feature] < Q1 - 1.5 * IQR) |
                          (df[selected_feature] > Q3 + 1.5 * IQR)][selected_feature]

            ax.set_title(f'异常值: {len(outliers)} 个', fontsize=13, fontweight='bold', pad=15)
            ax.set_ylabel('数值', fontsize=11)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, axis='y', linestyle='--')

            st.pyplot(fig)
            plt.close()

        # 零值警告
        if selected_feature in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
            zero_count = (df[selected_feature] == 0).sum()
            if zero_count > 0:
                st.markdown(f"""
                <div class="warning-box">
                    <h4 style="margin-top: 0; color: #d97706;">⚠️ 零值检测</h4>
                    <p style="margin: 0.5rem 0;">该特征存在 <strong>{zero_count}</strong> 个零值 
                    ({zero_count / len(df) * 100:.1f}%)，可能为隐藏缺失值</p>
                    <p style="margin: 0.5rem 0; color: #92400e;">建议在数据预处理阶段进行处理</p>
                </div>
                """, unsafe_allow_html=True)

    # ==================== Tab 4: 双变量分析 ===================
    with tab4:
        st.markdown("### 🔄 患病 vs 非患病组对比")

        analysis_type = st.radio(
            "选择分析类型",
            ["单特征对比", "散点图矩阵"],
            horizontal=True
        )

        if analysis_type == "单特征对比":
            selected_feature = st.selectbox(
                "选择要对比的特征",
                viz.feature_names,
                format_func=lambda x: f"{x} ({viz.feature_names_cn.get(x, x)})",
                key="bivariate_select"
            )

            col1, col2 = st.columns([1.5, 1])

            with col1:
                st.markdown("#### 📊 小提琴图 + 箱线图")

                setup_chinese_font()
                fig, ax = plt.subplots(figsize=(10, 6))

                data_0 = df[df[viz.target] == 0][selected_feature]
                data_1 = df[df[viz.target] == 1][selected_feature]

                # 小提琴图
                parts = ax.violinplot([data_0, data_1], positions=[1, 2],
                                      showmeans=True, showmedians=True)
                for pc in parts['bodies']:
                    pc.set_facecolor('#667eea')
                    pc.set_alpha(0.3)

                # 箱线图
                bp = ax.boxplot([data_0, data_1], positions=[1, 2], widths=0.3,
                                patch_artist=True, showfliers=False)
                for patch, color in zip(bp['boxes'], ['#10b981', '#ef4444']):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.6)

                ax.set_xticks([1, 2])
                ax.set_xticklabels(['非患病', '患病'], fontsize=11, fontweight='bold')
                ax.set_title(viz.feature_names_cn.get(selected_feature, selected_feature),
                             fontsize=14, fontweight='bold', pad=15)
                ax.set_ylabel('数值', fontsize=11)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.grid(True, alpha=0.2, axis='y', linestyle='--')

                st.pyplot(fig)
                plt.close()

            with col2:
                st.markdown("#### 📋 分组统计对比")

                stats_comparison = pd.DataFrame({
                    '非患病组': [
                        data_0.mean(),
                        data_0.median(),
                        data_0.std(),
                        data_0.min(),
                        data_0.max()
                    ],
                    '患病组': [
                        data_1.mean(),
                        data_1.median(),
                        data_1.std(),
                        data_1.min(),
                        data_1.max()
                    ]
                }, index=['均值', '中位数', '标准差', '最小值', '最大值'])

                stats_comparison['差异'] = stats_comparison['患病组'] - stats_comparison['非患病组']

                st.dataframe(
                    stats_comparison.style.format("{:.2f}")
                    .background_gradient(cmap='RdYlGn_r', subset=['差异']),
                    use_container_width=True
                )

                mean_diff = data_1.mean() - data_0.mean()
                if abs(mean_diff) > 0:
                    direction = "更高" if mean_diff > 0 else "更低"
                    box_class = "warning-box" if mean_diff > 0 else "success-box"
                    st.markdown(f"""
                    <div class="{box_class}">
                        <h4 style="margin-top: 0;">💡 关键洞察</h4>
                        <p style="margin: 0.5rem 0;">患病组的{viz.feature_names_cn.get(selected_feature, selected_feature)}
                        平均值比非患病组<strong>{direction} {abs(mean_diff):.2f}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)

        else:  # 散点图矩阵
            st.markdown("#### 🔍 关键特征散点图矩阵")

            key_features = st.multiselect(
                "选择要分析的特征（建议2-4个）",
                viz.feature_names,
                default=['Glucose', 'BMI', 'Age'],
                format_func=lambda x: f"{x} ({viz.feature_names_cn.get(x, x)})"
            )

            if len(key_features) >= 2:
                features_to_plot = key_features + [viz.target]

                setup_chinese_font()
                fig = plt.figure(figsize=(14, 12))
                pairplot_data = df[features_to_plot]

                g = sns.pairplot(pairplot_data, hue=viz.target,
                                 palette={0: '#10b981', 1: '#ef4444'},
                                 diag_kind='kde',
                                 plot_kws={'alpha': 0.6, 's': 30},
                                 diag_kws={'alpha': 0.7})
                g.fig.suptitle('散点图矩阵', y=1.01, fontsize=16, fontweight='bold')

                st.pyplot(g.fig)
                plt.close()
            else:
                st.warning("⚠️ 请至少选择2个特征进行分析")

    # ==================== Tab 5: 相关性分析 ===================
    with tab5:
        st.markdown("### 🔗 特征相关性分析")

        corr_matrix = df.corr()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### 🎨 相关系数热力图")

            setup_chinese_font()
            fig, ax = plt.subplots(figsize=(12, 10))

            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                        cmap='coolwarm', center=0, square=True, linewidths=1.5,
                        cbar_kws={"shrink": 0.8}, ax=ax,
                        annot_kws={'size': 10, 'weight': 'bold'})

            ax.set_title('特征相关性热力图', fontsize=14, fontweight='bold', pad=20)
            st.pyplot(fig)
            plt.close()

        with col2:
            st.markdown("#### 🎯 与患病风险的相关性")

            target_corr = corr_matrix[viz.target].drop(viz.target).sort_values(ascending=False)

            setup_chinese_font()
            fig, ax = plt.subplots(figsize=(8, 10))
            colors = ['#ef4444' if x > 0 else '#10b981' for x in target_corr]
            target_corr.plot(kind='barh', color=colors, ax=ax, alpha=0.8)
            ax.set_xlabel('相关系数', fontsize=11, fontweight='bold')
            ax.set_title('特征重要性排序', fontsize=13, fontweight='bold', pad=15)
            ax.axvline(0, color='black', linewidth=1)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='x', alpha=0.3, linestyle='--')

            st.pyplot(fig)
            plt.close()

        # 强相关特征对
        st.markdown("#### 🔍 强相关特征对 (|r| > 0.3)")

        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.3:
                    strong_corr.append({
                        '特征1': corr_matrix.columns[i],
                        '特征2': corr_matrix.columns[j],
                        '相关系数': corr_matrix.iloc[i, j],
                        '相关强度': '强' if abs(corr_matrix.iloc[i, j]) > 0.5 else '中等'
                    })

        if strong_corr:
            strong_corr_df = pd.DataFrame(strong_corr)
            st.dataframe(
                strong_corr_df.style.format({'相关系数': '{:.3f}'})
                .background_gradient(cmap='RdYlGn', subset=['相关系数']),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("📊 没有发现强相关特征对")

        # 关键发现
        st.markdown(f"""
        <div class="info-box">
            <h4 style="margin-top: 0; color: #1e40af;">💡 相关性分析关键发现</h4>
            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                <li><strong>{target_corr.index[0]}</strong> 与患病风险相关性最强 (r={target_corr.iloc[0]:.3f})</li>
                <li><strong>{target_corr.index[1]}</strong> 次之 (r={target_corr.iloc[1]:.3f})</li>
                <li><strong>{target_corr.index[2]}</strong> 也是重要因素 (r={target_corr.iloc[2]:.3f})</li>
                <li>特征间存在一定共线性，建模时需注意多重共线性问题</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ==================== Tab 6: 风险因素排序 =================
    with tab6:
        st.markdown("### 🎯 风险因素重要性排序")

        st.info("💡 此模块将展示模型训练后的特征重要性分析")

        # 方法1：从相关系数计算重要性（临时方案）
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### 📊 基于相关性的特征重要性")

            # 计算特征重要性（使用相关系数的绝对值）
            feature_importance = df.corr()[viz.target].drop(viz.target).abs().sort_values(ascending=True)

            setup_chinese_font()
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#667eea' if x > 0.3 else '#94a3b8' for x in feature_importance]
            feature_importance.plot(kind='barh', color=colors, ax=ax, alpha=0.8)
            ax.set_xlabel('重要性分数 (相关系数绝对值)', fontsize=11, fontweight='bold')
            ax.set_title('特征重要性排序', fontsize=14, fontweight='bold', pad=15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='x', alpha=0.3, linestyle='--')

            st.pyplot(fig)
            plt.close()

        with col2:
            st.markdown("#### 📋 重要性评分表")

            importance_df = pd.DataFrame({
                '特征': [viz.feature_names_cn.get(f, f) for f in feature_importance.index],
                '重要性': feature_importance.values,
                '等级': ['⭐⭐⭐' if x > 0.4 else '⭐⭐' if x > 0.2 else '⭐'
                         for x in feature_importance.values]
            }).sort_values('重要性', ascending=False).reset_index(drop=True)

            st.dataframe(
                importance_df.style.format({'重要性': '{:.3f}'})
                .background_gradient(cmap='YlOrRd', subset=['重要性']),
                use_container_width=True,
                hide_index=True
            )

        # 关键发现总结
        top_feature = feature_importance.index[-1]
        st.markdown(f"""
        <div class="success-box">
            <h4 style="margin-top: 0;">🔬 关键发现</h4>
            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                <li><strong>{viz.feature_names_cn.get(top_feature, top_feature)}</strong> 
                是最重要的风险因素（重要性: {feature_importance.iloc[-1]:.3f}）</li>
                <li>前3大风险因素占总重要性的 
                {(feature_importance.iloc[-3:].sum() / feature_importance.sum() * 100):.1f}%</li>
                <li>建议在临床筛查中优先关注这些高重要性指标</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # 临床意义解读
        st.markdown("#### 🏥 临床意义解读")

        clinical_notes = {
            'Glucose': '血糖是糖尿病诊断的金标准指标，空腹血糖≥126mg/dL或餐后2小时血糖≥200mg/dL提示糖尿病',
            'BMI': 'BMI≥30为肥胖，是糖尿病的重要危险因素，减重可显著降低发病风险',
            'Age': '年龄每增加10岁，糖尿病风险增加约1.5-2倍，45岁以上人群建议定期筛查',
            'Pregnancies': '妊娠糖尿病史是2型糖尿病的重要预测因素',
            'DiabetesPedigreeFunction': '家族遗传史显著增加患病风险，有家族史者需更频繁监测',
            'BloodPressure': '高血压与糖尿病常伴随出现，两者相互影响',
            'Insulin': '胰岛素抵抗是2型糖尿病的核心机制',
            'SkinThickness': '皮下脂肪厚度反映肥胖程度，与代谢综合征相关'
        }

        for feature in feature_importance.index[::-1]:
            if feature in clinical_notes:
                st.markdown(f"""
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                    <strong>{viz.feature_names_cn.get(feature, feature)}</strong>: 
                    {clinical_notes[feature]}
                </div>
                """, unsafe_allow_html=True)

    # 侧边栏
    with st.sidebar:
        # 页面导航
        st.markdown("### 📋 页面导航")

        if st.sidebar.button("📝 个人风险评估", use_container_width=True):
            st.switch_page("pages/1_personal_assessment.py")

        if st.sidebar.button("📊 批量数据筛查", use_container_width=True):
            st.switch_page("pages/2_batch_screening.py")

        if st.sidebar.button("📈 当前：数据可视化分析", disabled=True, use_container_width=True):
            pass

        if st.sidebar.button("🔍 交互式数据探索", use_container_width=True):
            st.switch_page("pages/interactive_data_insights.py")

        if st.sidebar.button("📖 模型说明", use_container_width=True):
            st.switch_page("pages/5_model_documentation.py")

        if st.sidebar.button("💾 数据集介绍", use_container_width=True):
            st.switch_page("pages/6_dataset_info.py")


        st.markdown("### ℹ️ 系统信息")
        st.markdown(f"""
        <div class="metric-card">
            <p><strong>数据集:</strong> Pima Indians Diabetes</p>
            <p><strong>样本数:</strong> {len(df)}</p>
            <p><strong>特征数:</strong> {len(viz.feature_names)}</p>
            <p><strong>患病率:</strong> {df[viz.target].mean() * 100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### 📖 使用指南")
        st.markdown("""
        <div style="font-size: 0.9rem; line-height: 1.6;">
        <p><strong>数据概览</strong><br>查看数据集基本信息和目标变量分布</p>

        <p><strong>单变量分析</strong><br>探索单个特征的分布特征</p>

        <p><strong>双变量分析</strong><br>对比患病组与非患病组的差异</p>

        <p><strong>相关性分析</strong><br>发现特征之间的关联关系</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.success("✅ 系统运行正常")

        # ==================== 下载功能 ====================
        st.markdown("---")
        st.markdown("### 📥 导出数据和图表")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 下载统计报告", use_container_width=True):
                # 生成统计报告
                report = []
                report.append("=" * 60)
                report.append("糖尿病数据集 - 统计分析报告")
                report.append("=" * 60)
                report.append(f"\n生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
                report.append(f"\n总样本数: {len(df)}")
                report.append(f"患病率: {df[viz.target].mean() * 100:.2f}%")
                report.append(f"\n特征统计:\n{df.describe().to_string()}")

                report_text = "\n".join(report)
                st.download_button(
                    label="💾 下载TXT报告",
                    data=report_text,
                    file_name="diabetes_analysis_report.txt",
                    mime="text/plain"
                )

        with col2:
            # 导出清洗后的数据
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📋 下载CSV数据",
                data=csv,
                file_name="diabetes_data.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col3:
            st.info("💡 离线图表已保存在 `docs/images/` 目录")

    # 页脚
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 2rem 0;'>
        <p style='font-size: 0.9rem; margin: 0;'>糖尿病预测项目 - 成员A：数据可视化分析模块</p>
        <p style='font-size: 0.85rem; margin: 0.5rem 0;'>Powered by Streamlit | 2024-2025</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()