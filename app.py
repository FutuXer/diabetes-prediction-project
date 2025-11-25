"""
糖尿病预测项目 - Streamlit主应用
基于统计建模的女性糖尿病风险评估系统
"""

import streamlit as st
import os
import sys

# 配置页面
st.set_page_config(
    page_title="首页 - 女性糖尿病风险评估系统",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 现代化CSS样式
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.25rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }

    .feature-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 3px solid #e2e8f0;
        transition: all 0.3s ease;
        text-align: center;
        cursor: pointer;
    }

    .feature-card:hover {
        box-shadow: 0 20px 25px -5px rgba(102, 126, 234, 0.3);
        transform: translateY(-5px);
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }

    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        color: #6b7280;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 3rem 0;
    }

    .stat-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stat-label {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """主页面"""

    # 标题区域
    st.markdown('<h1 class="hero-title">🏥 女性糖尿病风险评估系统</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">基于Pima Indians数据集的精准健康预测</p>', unsafe_allow_html=True)

    # 核心功能卡片
    st.markdown("## 🎯 核心功能")

    col1, col2 = st.columns(2)

    with col1:
        # 个人风险评估
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?page=personal_assessment'">
            <div class="feature-icon">📝</div>
            <div class="feature-title">个人风险评估</div>
            <div class="feature-desc">输入8项体检指标，获取个性化风险评分和诊断建议</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📝 个人风险评估", use_container_width=True, key="personal_btn"):
            st.switch_page("pages/personal_assessment.py")

    with col2:
        # 批量数据筛查
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?page=batch_screening'">
            <div class="feature-icon">📊</div>
            <div class="feature-title">批量数据筛查</div>
            <div class="feature-desc">上传CSV文件进行批量预测，生成详细筛查报告</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📊 批量数据筛查", use_container_width=True, key="batch_btn"):
            st.switch_page("pages/batch_screening.py")

    # 第二行 - 数据分析功能
    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        # 数据可视化分析
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?page=data_observation'">
            <div class="feature-icon">📈</div>
            <div class="feature-title">数据可视化分析</div>
            <div class="feature-desc">探索数据特征分布，发现风险因素和规律</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📈 数据可视化分析", use_container_width=True, key="data_btn"):
            st.switch_page("pages/4_data-observation.py")

    with col4:
        # 交互式数据探索
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?page=interactive_insights'">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">交互式数据探索</div>
            <div class="feature-desc">使用高级交互式图表深入分析数据特征</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔍 交互式数据探索", use_container_width=True, key="interactive_btn"):
            st.switch_page("pages/interactive_data_insights.py")

    # 系统统计信息
    st.markdown("## 📊 系统能力展示")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">768</div>
            <div class="stat-label">训练样本</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">85.3%</div>
            <div class="stat-label">诊断准确率</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">0.82</div>
            <div class="stat-label">AUC得分</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">8</div>
            <div class="stat-label">关键指标</div>
        </div>
        """, unsafe_allow_html=True)

    # 项目介绍
    st.markdown("---")
    st.markdown("## 💡 项目背景")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### 研究领域
        **医疗健康 - 女性糖尿病风险评估**

        ### 问题背景
        糖尿病是全球重大公共卫生问题，其中女性糖尿病患者面临独特的生理和代谢特征。Pima印第安人群体因遗传和生活方式因素，糖尿病发病率显著高于其他人群，为研究女性糖尿病风险因素提供了宝贵的流行病学数据。

        ### 核心技术
        - **统计建模**：岭回归、逻辑回归
        - **数据可视化**：探索性数据分析（EDA）
        - **风险评估**：个体化风险评分
        - **决策支持**：临床筛查辅助工具
        """)

    with col2:
        st.markdown("""
        ### 技术栈
        - **前端**: Streamlit
        - **后端**: Python 3.9+
        - **数据处理**: Pandas, NumPy
        - **机器学习**: Scikit-learn
        - **可视化**: Matplotlib, Plotly

        ### 团队分工
        - **成员A**: 数据可视化与EDA
        - **成员B**: 数据预处理
        - **成员C**: 回归建模
        - **成员D**: 分类建模
        """)

    # 快速导航
    st.markdown("---")
    st.markdown("## 🧭 快速导航")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📖 模型说明", use_container_width=True):
            st.switch_page("pages/model_documentation.py")

    with col2:
        if st.button("💾 数据集介绍", use_container_width=True):
            st.switch_page("pages/dataset_info.py")

    with col3:
        if st.button("👥 关于团队", use_container_width=True):
            st.switch_page("pages/about_team.py")

    with col4:
        if st.button("⚙️ 系统设置", use_container_width=True):
            st.switch_page("pages/settings.py")

if __name__ == "__main__":
    main()