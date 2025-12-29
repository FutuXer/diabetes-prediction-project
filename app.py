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

# 活泼现代的CSS样式
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 50%, #e0e7ff 100%);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hero Section Styles */
    .hero-section {
        position: relative;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.9) 0%, rgba(147, 197, 253, 0.9) 50%, rgba(165, 180, 252, 0.9) 100%);
        border-radius: 24px;
        padding: 4rem 2rem;
        margin-bottom: 3rem;
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(59, 130, 246, 0.25);
        z-index: 1;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background:
            linear-gradient(45deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 197, 253, 0.1) 100%),
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(255, 255, 255, 0.03) 10px,
                rgba(255, 255, 255, 0.03) 20px
            );
        opacity: 1;
        z-index: -1;
    }

    .hero-content {
        position: relative;
        z-index: 2;
        text-align: center;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1.5rem;
        text-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 500;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        padding: 0.75rem 2rem;
        border-radius: 50px;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.1), 0 4px 6px -2px rgba(139, 92, 246, 0.05);
        border: 2px solid rgba(139, 92, 246, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s;
    }

    .feature-card:hover::before {
        left: 100%;
    }

    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px -12px rgba(139, 92, 246, 0.25);
        border-color: rgba(139, 92, 246, 0.3);
        background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(240, 249, 255, 1) 100%);
    }

    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 50%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #1f2937 0%, #4b5563 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .feature-desc {
        color: #6b7280;
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 400;
    }

    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }

    .stat-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 12px -2px rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 25px -5px rgba(139, 92, 246, 0.2);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 50%, #93c5fd 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3) !important;
    }

    /* Content Sections */
    .content-section {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 8px 12px -2px rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.1);
    }

    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Animations */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .floating {
        animation: float 6s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """主页面"""

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-badge floating">
                🏥 AI驱动的健康预测平台
            </div>
            <h1 class="hero-title">女性糖尿病风险评估系统</h1>
            <p class="hero-subtitle">基于Pima Indians数据集的精准健康预测</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 核心功能卡片
    st.markdown("## 🎯 核心功能")

    # 第一行 - 核心功能
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
            st.switch_page("pages/1_personal_assessment.py")

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
            st.switch_page("pages/2_batch_screening.py")

    # 第二行 - 数据分析和文档功能
    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4, col5 = st.columns(3)

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
        # 模型说明
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?page=model_documentation'">
            <div class="feature-icon">📖</div>
            <div class="feature-title">模型说明</div>
            <div class="feature-desc">了解预测模型的原理、性能和技术细节</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📖 模型说明", use_container_width=True, key="model_btn"):
            st.switch_page("pages/5_model_documentation.py")

    with col5:
        # 数据集介绍
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='?page=dataset_info'">
            <div class="feature-icon">💾</div>
            <div class="feature-title">数据集介绍</div>
            <div class="feature-desc">了解Pima Indians糖尿病数据集的详细信息</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("💾 数据集介绍", use_container_width=True, key="dataset_btn"):
            st.switch_page("pages/6_dataset_info.py")


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

    col1, col2 = st.columns(2)

    with col1:
        # 左侧：研究领域和核心技术
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); color: #1e40af; padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 600; margin-bottom: 1.5rem; text-align: center;">
            🏥 医疗健康 - 女性糖尿病风险评估
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📋 问题背景")
        st.markdown("""
        糖尿病是全球重大公共卫生问题，其中女性糖尿病患者面临独特的生理和代谢特征。
        Pima印第安人群体因遗传和生活方式因素，糖尿病发病率显著高于其他人群，
        为研究女性糖尿病风险因素提供了宝贵的流行病学数据。
        """)

        st.markdown("### 🛠️ 核心技术")

        tech_col1, tech_col2 = st.columns(2)

        with tech_col1:
            st.markdown("""
            <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #3b82f6;">
                <div style="font-weight: 600; color: #1e40af; margin-bottom: 0.5rem;">📊 统计建模</div>
                <div style="color: #64748b; font-size: 0.9rem;">岭回归、逻辑回归</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 12px; border-left: 4px solid #10b981;">
                <div style="font-weight: 600; color: #065f46; margin-bottom: 0.5rem;">⚡ 风险评估</div>
                <div style="color: #64748b; font-size: 0.9rem;">个体化风险评分</div>
            </div>
            """, unsafe_allow_html=True)

        with tech_col2:
            st.markdown("""
            <div style="background: rgba(236, 72, 153, 0.1); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #ec4899;">
                <div style="font-weight: 600; color: #be185d; margin-bottom: 0.5rem;">📈 数据可视化</div>
                <div style="color: #64748b; font-size: 0.9rem;">探索性数据分析（EDA）</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background: rgba(251, 146, 60, 0.1); padding: 1rem; border-radius: 12px; border-left: 4px solid #fb923c;">
                <div style="font-weight: 600; color: #ea580c; margin-bottom: 0.5rem;">🤖 决策支持</div>
                <div style="color: #64748b; font-size: 0.9rem;">临床筛查辅助工具</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # 右侧：项目信息
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); color: #4338ca; padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 600; margin-bottom: 1.5rem; text-align: center;">
            📊 项目信息
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎯 项目目标")
        st.markdown("""
        基于Pima印第安人糖尿病数据集，构建统计模型，实现：
        - 个性化风险评估
        - 批量数据筛查
        - 数据可视化分析
        - 临床决策支持
        """)

        st.markdown("### 📈 数据集规模")

        col_info1, col_info2, col_info3 = st.columns(3)

        with col_info1:
            st.metric("样本数量", "768例")

        with col_info2:
            st.metric("特征数量", "8个")

        with col_info3:
            st.metric("患病率", "34.9%")
if __name__ == "__main__":
    main()