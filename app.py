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

# 全局修复：将包含 HTML 标签的 st.markdown 调用默认设为 unsafe_allow_html=True
# 这样可以避免页面上看到被转义的原始 HTML 字符串（会把 HTML 渲染为布局）
_orig_markdown = st.markdown
def _markdown_wrapper(body, *args, **kwargs):
    try:
        if isinstance(body, str) and ('<' in body and '>' in body) and 'unsafe_allow_html' not in kwargs:
            kwargs['unsafe_allow_html'] = True
    except Exception:
        pass
    return _orig_markdown(body, *args, **kwargs)
st.markdown = _markdown_wrapper

# 导入统一的UI样式系统
from src.ui_styles import (
    apply_flat_theme, create_hero_section, create_feature_grid,
    create_stats_grid, style_metric_card
)

def main():
    """主页面"""

    # 应用扁平化主题
    apply_flat_theme()

    # 英雄区域
    create_hero_section(
        title="女性糖尿病风险评估系统",
        subtitle="基于Pima Indians数据集的精准健康预测",
        badge="🏥 AI驱动的健康预测平台"
    )

    # 核心功能网格
    st.markdown("## 🎯 核心功能")

    features = [
        {
            'icon': '📝',
            'title': '个人风险评估',
            'desc': '输入8项体检指标，获取个性化风险评分和诊断建议'
        },
        {
            'icon': '📊',
            'title': '批量数据筛查',
            'desc': '上传CSV文件进行批量预测，生成详细筛查报告'
        },
        {
            'icon': '📈',
            'title': '数据可视化分析',
            'desc': '探索数据特征分布，发现风险因素和规律'
        },
        {
            'icon': '🔍',
            'title': '交互式数据探索',
            'desc': '使用高级交互式图表深入分析数据特征'
        }
    ]

    create_feature_grid(features)

    # 功能按钮
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📝 个人风险评估", use_container_width=True, key="personal_btn"):
            st.switch_page("pages/1_personal_assessment.py")

    with col2:
        if st.button("📊 批量数据筛查", use_container_width=True, key="batch_btn"):
            st.switch_page("pages/2_batch_screening.py")

    with col3:
        if st.button("📈 数据可视化分析", use_container_width=True, key="data_btn"):
            st.switch_page("pages/4_data-observation.py")

    with col4:
        if st.button("🔍 交互式数据探索", use_container_width=True, key="interactive_btn"):
            st.switch_page("pages/interactive_data_insights.py")

    # 系统统计信息
    st.markdown("## 📊 系统能力展示")

    stats = [
        {'value': '768', 'label': '训练样本', 'icon': '👥'},
        {'value': '77.9%', 'label': '诊断准确率', 'icon': '🎯'},
        {'value': '0.82', 'label': 'AUC得分', 'icon': '📈'},
        {'value': '8', 'label': '关键指标', 'icon': '📋'}
    ]

    create_stats_grid(stats)

    # 项目介绍
    st.markdown("---")
    st.markdown("## 💡 项目背景")

    col1, col2 = st.columns(2)

    with col1:
        # 项目背景卡片
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">🏥 研究领域</h3>
                <p class="card-subtitle">医疗健康 - 女性糖尿病风险评估</p>
            </div>
            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: #1f2937; margin-bottom: 0.5rem;">📋 核心问题</h4>
                <p style="color: #6b7280; line-height: 1.6;">
                如何基于常规体检指标，构建可解释的统计模型，对女性糖尿病风险进行量化评估和分类诊断？
                </p>
            </div>
            <div>
                <h4 style="color: #1f2937; margin-bottom: 1rem;">🎯 研究挑战</h4>
                <ul style="color: #6b7280; padding-left: 1.5rem;">
                    <li>数据质量问题：原始数据存在隐藏缺失值</li>
                    <li>模型可解释性：医疗场景需要明确临床意义</li>
                    <li>风险量化需求：同时提供评分和诊断</li>
                    <li>应用落地：转化为实用临床决策工具</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # 技术栈展示
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">🛠️ 技术栈</h3>
                <p class="card-subtitle">现代化的数据科学技术栈</p>
            </div>
        """, unsafe_allow_html=True)

        # 技术栈网格
        tech_stack = [
            {'icon': '🐍', 'name': 'Python 3.9+', 'desc': '后端开发'},
            {'icon': '🌊', 'name': 'Streamlit', 'desc': '前端框架'},
            {'icon': '📊', 'name': 'Pandas/NumPy', 'desc': '数据处理'},
            {'icon': '🧠', 'name': 'Scikit-learn', 'desc': '机器学习'},
            {'icon': '📈', 'name': 'Plotly', 'desc': '数据可视化'},
            {'icon': '🎨', 'name': 'Matplotlib', 'desc': '统计图表'}
        ]

        html = '<div class="grid grid-2" style="margin-top: 1rem;">'
        for tech in tech_stack:
            html += f"""
            <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                        padding: 1rem; border-radius: 8px; text-align: center;
                        border: 1px solid #e2e8f0; transition: all 0.3s ease;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{tech['icon']}</div>
                <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">{tech['name']}</div>
                <div style="font-size: 0.875rem; color: #6b7280;">{tech['desc']}</div>
            </div>
            """
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)

        
    # 快速导航
    st.markdown("---")
    st.markdown("## 🧭 快速导航")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📖 模型说明", use_container_width=True):
            st.switch_page("pages/5_model_documentation.py")

    with col2:
        if st.button("💾 数据集介绍", use_container_width=True):
            st.switch_page("pages/6_dataset_info.py")

    with col3:
        if st.button("👥 关于团队", use_container_width=True):
            st.switch_page("pages/7_about_team.py")

    
if __name__ == "__main__":
    main()