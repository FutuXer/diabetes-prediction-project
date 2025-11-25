"""
糖尿病预测项目 - 增强版交互式数据可视化
作者: 成员A
功能: 使用Plotly实现交互式数据探索
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import warnings

warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="交互式数据探索",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 现代化CSS
st.markdown("""
<style>
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }

    .insight-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }

    .warning-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }

    .success-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class InteractiveDataAnalyzer:
    """交互式数据分析类"""

    def __init__(self):
        """初始化数据"""
        self.df = self.load_data()
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

    def load_data(self):
        """智能加载数据"""
        possible_paths = [
            './src/data/diabetes.csv',
            './data/raw/diabetes.csv',
            './diabetes.csv',
            'diabetes.csv'
        ]

        for path in possible_paths:
            try:
                return pd.read_csv(path)
            except FileNotFoundError:
                continue

        # 如果都找不到，创建示例数据
        st.warning("未找到数据文件，使用示例数据进行演示")
        return pd.DataFrame({
            'Pregnancies': np.random.randint(0, 17, 100),
            'Glucose': np.random.normal(120, 30, 100),
            'BloodPressure': np.random.normal(70, 15, 100),
            'SkinThickness': np.random.normal(20, 10, 100),
            'Insulin': np.random.normal(80, 40, 100),
            'BMI': np.random.normal(32, 8, 100),
            'DiabetesPedigreeFunction': np.random.uniform(0, 2, 100),
            'Age': np.random.randint(21, 80, 100),
            'Outcome': np.random.randint(0, 2, 100)
        })

    def create_correlation_heatmap(self):
        """创建交互式相关性热力图"""
        corr_matrix = self.df.corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False,
            colorbar=dict(title="相关系数")
        ))

        fig.update_layout(
            title="特征相关性热力图",
            width=800,
            height=700,
            xaxis_title="特征",
            yaxis_title="特征"
        )

        return fig

    def create_distribution_plot(self, feature):
        """创建交互式分布图"""
        feature_cn = self.feature_names_cn.get(feature, feature)

        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("直方图", "箱线图", "密度曲线", "分组统计"),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "bar"}]]
        )

        # 直方图
        fig.add_trace(
            go.Histogram(x=self.df[feature], name="分布", nbinsx=30,
                        marker_color='#667eea', opacity=0.7),
            row=1, col=1
        )

        # 箱线图
        fig.add_trace(
            go.Box(y=self.df[feature], name="箱线图",
                  marker_color='#ef4444'),
            row=1, col=2
        )

        # 密度曲线
        fig.add_trace(
            go.Histogram(x=self.df[feature], name="密度",
                        histnorm='probability density', nbinsx=30,
                        marker_color='#10b981', opacity=0.7),
            row=2, col=1
        )

        # 分组统计
        stats_by_outcome = self.df.groupby(self.target)[feature].mean()
        fig.add_trace(
            go.Bar(
                x=['非患病', '患病'],
                y=stats_by_outcome.values,
                name="组间均值",
                marker=dict(color=['#10b981', '#ef4444'])
            ),
            row=2, col=2
        )

        fig.update_layout(
            height=800,
            title_text=f"{feature_cn} ({feature}) - 多维度分析",
            showlegend=False
        )

        return fig

    def create_scatter_3d(self, x_feature, y_feature, z_feature):
        """创建3D散点图"""
        fig = go.Figure(data=[go.Scatter3d(
            x=self.df[x_feature],
            y=self.df[y_feature],
            z=self.df[z_feature],
            mode='markers',
            marker=dict(
                size=self.df['Age']/5,
                color=self.df[self.target],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="患病状态")
            ),
            text=[f"年龄: {age}<br>状态: {'患病' if outcome else '未患病'}"
                  for age, outcome in zip(self.df['Age'], self.df[self.target])],
            hovertemplate="<b>%{text}</b><br>" +
                         f"{self.feature_names_cn.get(x_feature, x_feature)}: %{{x:.1f}}<br>" +
                         f"{self.feature_names_cn.get(y_feature, y_feature)}: %{{y:.1f}}<br>" +
                         f"{self.feature_names_cn.get(z_feature, z_feature)}: %{{z:.1f}}<extra></extra>"
        )])

        fig.update_layout(
            title="3D特征空间可视化",
            scene=dict(
                xaxis_title=f"{x_feature} ({self.feature_names_cn.get(x_feature, x_feature)})",
                yaxis_title=f"{y_feature} ({self.feature_names_cn.get(y_feature, y_feature)})",
                zaxis_title=f"{z_feature} ({self.feature_names_cn.get(z_feature, z_feature)})"
            ),
            width=800,
            height=600
        )

        return fig

    def create_radar_chart(self, index=None):
        """创建雷达图对比"""
        if index is None:
            # 默认显示均值对比
            non_diabetic = self.df[self.df[self.target] == 0].describe().loc['mean']
            diabetic = self.df[self.df[self.target] == 1].describe().loc['mean']

            fig = go.Figure()

            # 非患病组
            fig.add_trace(go.Scatterpolar(
                r=non_diabetic[self.feature_names].values,
                theta=[self.feature_names_cn.get(f, f) for f in self.feature_names],
                fill='toself',
                name='非患病组',
                line_color='#10b981'
            ))

            # 患病组
            fig.add_trace(go.Scatterpolar(
                r=diabetic[self.feature_names].values,
                theta=[self.feature_names_cn.get(f, f) for f in self.feature_names],
                fill='toself',
                name='患病组',
                line_color='#ef4444'
            ))

        else:
            # 显示特定样本与平均值的对比
            sample = self.df.iloc[index]
            avg = self.df.describe().loc['mean']

            fig = go.Figure()

            # 样本数据
            fig.add_trace(go.Scatterpolar(
                r=sample[self.feature_names].values,
                theta=[self.feature_names_cn.get(f, f) for f in self.feature_names],
                fill='toself',
                name=f'样本 {index}',
                line_color='#667eea'
            ))

            # 平均值
            fig.add_trace(go.Scatterpolar(
                r=avg[self.feature_names].values,
                theta=[self.feature_names_cn.get(f, f) for f in self.feature_names],
                fill='toself',
                name='人群平均',
                line_color='#94a3b8'
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, self.df[self.feature_names].max().max()]
                )
            ),
            width=600,
            height=600,
            title="雷达图对比分析"
        )

        return fig

    def create_feature_importance_plot(self):
        """创建特征重要性图表"""
        # 计算特征重要性（与目标变量的相关系数绝对值）
        importance = self.df.corr()[self.target].drop(self.target).abs().sort_values(ascending=True)

        fig = go.Figure(data=[
            go.Bar(
                x=importance.values,
                y=[self.feature_names_cn.get(f, f) for f in importance.index],
                orientation='h',
                marker=dict(
                    color=importance.values,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="重要性分数")
                )
            )
        ])

        fig.update_layout(
            title="特征重要性排序（基于相关性）",
            xaxis_title="重要性分数",
            yaxis_title="特征",
            height=500,
            width=700
        )

        return fig

def main():
    """主函数"""

    # 标题
    st.markdown('<h1 class="hero-title">🔍 交互式数据探索</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">使用交互式图表深入了解糖尿病数据集</p>', unsafe_allow_html=True)

    # 加载数据
    try:
        analyzer = InteractiveDataAnalyzer()
        df = analyzer.df
        st.success("✅ 数据加载成功！", icon="✅")
    except Exception as e:
        st.error(f"❌ 数据加载失败: {e}", icon="❌")
        return

    # 侧边栏控制
    st.sidebar.markdown("## 🎛️ 可视化控制")

    # 页面导航
    st.sidebar.markdown("""
    <div style="background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
                padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
        <h4 style="color: #1f2937; margin-bottom: 0.5rem;">📋 页面导航</h4>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    border-radius: 8px; border-left: 3px solid #667eea;
                    background: white;">
            <span style="color: #374151;">🔍 当前：交互式数据探索</span>
        </div>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    border-radius: 8px; cursor: pointer;
                    border-left: 3px solid transparent;"
                    onclick="window.location.href='/?page=data_insights'">
            <span style="color: #374151;">📈 数据可视化分析</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    viz_type = st.sidebar.selectbox(
        "选择可视化类型",
        ["数据概览", "特征分布", "相关性分析", "3D散点图", "雷达图对比", "特征重要性"]
    )

    if viz_type == "特征分布":
        selected_feature = st.sidebar.selectbox(
            "选择特征",
            analyzer.feature_names,
            format_func=lambda x: f"{x} ({analyzer.feature_names_cn.get(x, x)})"
        )

    if viz_type == "3D散点图":
        x_axis = st.sidebar.selectbox("X轴", analyzer.feature_names,
                                     format_func=lambda x: analyzer.feature_names_cn.get(x, x))
        y_axis = st.sidebar.selectbox("Y轴", analyzer.feature_names,
                                     format_func=lambda x: analyzer.feature_names_cn.get(x, x))
        z_axis = st.sidebar.selectbox("Z轴", analyzer.feature_names,
                                     format_func=lambda x: analyzer.feature_names_cn.get(x, x))

    if viz_type == "雷达图对比":
        radar_type = st.sidebar.radio("对比类型", ["组间对比", "个体对比"])
        if radar_type == "个体对比":
            sample_index = st.sidebar.number_input("样本索引", 0, len(df)-1, 0)

    # 主要内容区域
    if viz_type == "数据概览":
        st.markdown("## 📊 数据集概览")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("样本总数", f"{len(df):,}")
        with col2:
            st.metric("特征数量", f"{len(analyzer.feature_names)}")
        with col3:
            st.metric("患病样本", f"{df[analyzer.target].sum()}")
        with col4:
            st.metric("患病率", f"{df[analyzer.target].mean()*100:.1f}%")

        # 患病率饼图
        col1, col2 = st.columns(2)

        with col1:
            outcome_counts = df[analyzer.target].value_counts()
            fig = px.pie(
                values=outcome_counts.values,
                names=['未患病', '患病'],
                title="患病率分布",
                color_discrete_map={'未患病': '#10b981', '患病': '#ef4444'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # 年龄分布
            fig = px.histogram(
                df, x='Age', color=analyzer.target,
                title="年龄分布（按患病状态）",
                color_discrete_map={0: '#10b981', 1: '#ef4444'},
                nbins=20
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # 描述性统计
        st.markdown("### 📋 描述性统计")
        st.dataframe(
            df.describe().T.style.background_gradient(cmap='Blues', subset=['mean', 'std'])
            .format("{:.2f}"),
            use_container_width=True
        )

    elif viz_type == "特征分布":
        st.markdown(f"## 📈 {analyzer.feature_names_cn.get(selected_feature, selected_feature)} 分布分析")

        fig = analyzer.create_distribution_plot(selected_feature)
        st.plotly_chart(fig, use_container_width=True)

        # 统计信息
        feature_data = df[selected_feature]
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("均值", f"{feature_data.mean():.2f}")
        with col2:
            st.metric("中位数", f"{feature_data.median():.2f}")
        with col3:
            st.metric("标准差", f"{feature_data.std():.2f}")
        with col4:
            # 检查零值
            zero_count = (feature_data == 0).sum()
            if zero_count > 0 and selected_feature in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
                st.metric("零值数量", f"{zero_count} ⚠️")
            else:
                st.metric("零值数量", f"{zero_count}")

    elif viz_type == "相关性分析":
        st.markdown("## 🔗 相关性分析")

        fig = analyzer.create_correlation_heatmap()
        st.plotly_chart(fig, use_container_width=True)

        # 强相关特征对
        corr_matrix = df.corr()
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.3:
                    strong_corr.append({
                        '特征1': corr_matrix.columns[i],
                        '特征2': corr_matrix.columns[j],
                        '相关系数': corr_matrix.iloc[i, j]
                    })

        if strong_corr:
            st.markdown("### 🎯 强相关特征对")
            strong_corr_df = pd.DataFrame(strong_corr)
            st.dataframe(
                strong_corr_df.style.format({'相关系数': '{:.3f}'})
                .background_gradient(cmap='RdYlGn', subset=['相关系数']),
                use_container_width=True,
                hide_index=True
            )

    elif viz_type == "3D散点图":
        st.markdown("## 🌐 3D特征空间可视化")

        fig = analyzer.create_scatter_3d(x_axis, y_axis, z_axis)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-card">
            <h4>💡 使用提示</h4>
            <ul>
                <li>点的大小代表年龄</li>
                <li>颜色代表患病状态（绿色：未患病，红色：患病）</li>
                <li>可以旋转、缩放图表进行全方位观察</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    elif viz_type == "雷达图对比":
        st.markdown("## 🎯 雷达图对比分析")

        if radar_type == "组间对比":
            fig = analyzer.create_radar_chart()
        else:
            fig = analyzer.create_radar_chart(sample_index)

        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "特征重要性":
        st.markdown("## 🏆 特征重要性分析")

        fig = analyzer.create_feature_importance_plot()
        st.plotly_chart(fig, use_container_width=True)

        # 特征重要性表格
        importance = df.corr()[analyzer.target].drop(analyzer.target).abs().sort_values(ascending=False)

        importance_df = pd.DataFrame({
            '特征': [analyzer.feature_names_cn.get(f, f) for f in importance.index],
            '重要性分数': importance.values,
            '等级': ['⭐⭐⭐' if x > 0.4 else '⭐⭐' if x > 0.2 else '⭐' for x in importance.values]
        }).reset_index(drop=True)

        st.dataframe(
            importance_df.style.format({'重要性分数': '{:.3f}'})
            .background_gradient(cmap='YlOrRd', subset=['重要性分数']),
            use_container_width=True,
            hide_index=True
        )

        # 关键发现
        st.markdown("""
        <div class="success-card">
            <h4>🔬 关键发现</h4>
            <p>基于相关性分析，血糖浓度(Glucose)是最重要的风险因素，其次是体质指数(BMI)和年龄。这些指标在临床筛查中应重点关注。</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()