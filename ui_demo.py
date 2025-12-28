"""
UI样式系统演示
展示新的现代化UI设计风格
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 导入UI样式系统
from src.ui_styles import *

def main():
    """UI样式系统演示"""

    # 应用全局样式
    apply_global_styles()

    # 页面标题
    create_hero_section(
        title="🎨 UI样式系统演示",
        subtitle="现代化医疗科技风格界面设计",
        badge="✨ 新一代设计系统"
    )

    st.markdown("---")

    # 1. 功能卡片网格演示
    st.markdown("## 🎯 功能卡片网格")

    features = [
        {
            'icon': '📝',
            'title': '个人评估',
            'desc': '输入体检指标，获取个性化风险评估报告'
        },
        {
            'icon': '📊',
            'title': '批量筛查',
            'desc': '上传CSV文件，进行大规模健康筛查'
        },
        {
            'icon': '📈',
            'title': '数据可视化',
            'desc': '探索数据分布，发现关键风险因素'
        },
        {
            'icon': '🔍',
            'title': '交互探索',
            'desc': '高级交互式图表，深入数据洞察'
        }
    ]

    create_feature_grid(features)

    st.markdown("---")

    # 2. 统计卡片网格演示
    st.markdown("## 📊 统计信息展示")

    stats = [
        {'value': '768', 'label': '训练样本', 'icon': '👥'},
        {'value': '77.9%', 'label': '模型准确率', 'icon': '🎯'},
        {'value': '0.82', 'label': 'AUC得分', 'icon': '📈'},
        {'value': '8', 'label': '风险指标', 'icon': '📋'}
    ]

    create_stats_grid(stats)

    st.markdown("---")

    # 3. 指标网格演示
    st.markdown("## 📈 性能指标")

    metrics = [
        {'title': '准确率', 'value': '77.9%', 'delta': '+2.1%', 'delta_color': 'success'},
        {'title': '召回率', 'value': '66.7%', 'delta': '+5.3%', 'delta_color': 'success'},
        {'title': '精确率', 'value': '69.2%', 'delta': '+1.8%', 'delta_color': 'success'},
        {'title': 'AUC值', 'value': '0.82', 'delta': '+0.03', 'delta_color': 'success'}
    ]

    create_metric_grid(metrics)

    st.markdown("---")

    # 4. 风险等级显示演示
    st.markdown("## 🚨 风险等级展示")

    risk_scenarios = [
        (25.0, "低风险", "您的风险评分较低，建议保持健康的生活方式，定期体检。"),
        (55.0, "中等风险", "您的风险评分中等，建议关注各项指标，特别是血糖和BMI，并改善生活习惯。"),
        (85.0, "高风险", "您的风险评分较高，建议立即咨询医生并进行进一步的医学检查。")
    ]

    for score, level, advice in risk_scenarios:
        create_risk_level_display(score, level, advice)
        st.markdown("")

    st.markdown("---")

    # 5. 信息卡片演示
    st.markdown("## 💡 信息提示")

    create_info_card(
        "数据质量说明",
        """
        <p>本系统使用Pima Indians糖尿病数据集，经过严格的数据预处理：</p>
        <ul>
            <li>✅ 缺失值处理：使用中位数填充生理学不合理的0值</li>
            <li>✅ 异常值检测：IQR方法结合医学验证</li>
            <li>✅ 特征工程：BMI分级、年龄分组等</li>
            <li>✅ 数据完整性：最终完整率100%</li>
        </ul>
        """
    )

    create_info_card(
        "模型说明",
        """
        <h4>回归模型：岭回归 (Ridge Regression)</h4>
        <p>用于生成0-100分的连续风险评分，具有良好的抗过拟合能力。</p>

        <h4>分类模型：逻辑回归 + OHE</h4>
        <p>采用独热编码处理分类特征，阈值T=0.45，在准确率和召回率间取得最佳平衡。</p>
        """,
        "success"
    )

    st.markdown("---")

    # 6. 图表容器演示
    st.markdown("## 📊 数据可视化")

    # 示例数据
    sample_data = pd.DataFrame({
        '特征': ['血糖', 'BMI', '年龄', '家族史', '胰岛素', '血压'],
        '重要性': [0.35, 0.28, 0.18, 0.12, 0.05, 0.02],
        '颜色': ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#6b7280']
    })

    # 创建条形图
    fig = go.Figure(data=[
        go.Bar(
            x=sample_data['重要性'],
            y=sample_data['特征'],
            orientation='h',
            marker=dict(
                color=sample_data['重要性'],
                colorscale='Blues',
                showscale=True
            ),
            text=[f'{x:.1%}' for x in sample_data['重要性']],
            textposition='auto'
        )
    ])

    fig.update_layout(
        title="特征重要性分析",
        xaxis_title="重要性权重",
        yaxis_title="特征名称",
        height=400
    )

    # 使用样式化的图表容器
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 7. 表单组件演示
    st.markdown("## 📝 表单组件")

    with st.form("demo_form"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">风险评估模拟</h3></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            glucose = st.slider("血糖浓度 (mg/dL)", 70, 200, 120)
            bmi = st.slider("BMI指数", 18.0, 50.0, 25.0, 0.1)
            age = st.slider("年龄", 20, 80, 35)

        with col2:
            blood_pressure = st.slider("舒张压 (mmHg)", 50, 120, 80)
            pregnancies = st.slider("怀孕次数", 0, 15, 2)
            family_history = st.slider("家族史风险", 0.0, 1.0, 0.3, 0.1)

        submitted = st.form_submit_button("🔍 评估风险", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            # 简单的风险计算演示
            risk_score = (glucose - 100) * 0.3 + (bmi - 25) * 2 + (age - 30) * 0.5 + family_history * 10
            risk_score = min(100, max(0, risk_score))

            if risk_score < 30:
                risk_level, advice = "低风险", "保持健康生活方式"
            elif risk_score < 70:
                risk_level, advice = "中等风险", "建议定期检查"
            else:
                risk_level, advice = "高风险", "建议立即就医"

            create_risk_level_display(risk_score, risk_level, advice)

    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #6b7280;'>
        <p>🎨 <strong>UI样式系统 v1.0</strong> | 现代化医疗科技设计</p>
        <p>✨ 简洁 · 美观 · 易用 · 响应式</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

