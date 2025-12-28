"""
糖尿病预测项目 - 个人风险评估页面
作者: 成员C（回归建模）+ 成员D（分类建模）
功能: 输入8项体检指标，获取风险评分和患病诊断
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from src.model_predictor import predict_risk, OPTIMAL_THRESHOLD
import plotly.figure_factory as ff

warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="个人风险评估 - 糖尿病预测",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 导入统一的UI样式系统
from src.ui_styles import (
    apply_flat_theme, create_hero_section, create_risk_level_display,
    DiabetesUITheme
)

def create_risk_gauge(risk_score):
    """创建风险评分仪表盘"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "糖尿病风险评分"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 30], 'color': "#d1fae5"},
                {'range': [30, 70], 'color': "#fef3c7"},
                {'range': [70, 100], 'color': "#fee2e2"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))

    fig.update_layout(
        height=400,
        font={'color': "#1f2937", 'family': "Arial, sans-serif"}
    )

    return fig


def get_risk_level(score, threshold):  # ✅ 接受 2 个参数
    """根据风险评分和阈值确定风险等级和建议"""

    # 评分通常是 0-100 的百分比，阈值是 0-1 的小数
    if score < threshold * 100:
        risk_level = "低风险"
        risk_icon = "🟢"
        risk_advice = "您的风险评分较低，建议保持健康的生活方式，定期体检。"
    elif score < 70:  # 使用了一个中间值作为中等风险的参考
        risk_level = "中风险"
        risk_icon = "🟡"
        risk_advice = "您的风险评分中等，建议关注各项指标，特别是血糖和BMI，并改善生活习惯。"
    else:
        risk_level = "高风险"
        risk_icon = "🔴"
        risk_advice = "您的风险评分较高，建议立即咨询医生并进行进一步的医学检查。"

    return risk_level, risk_icon, risk_advice

def main():
    """主函数"""

    # 应用扁平化主题
    apply_flat_theme()

    # 页面标题
    create_hero_section(
        title="个人风险评估",
        subtitle="输入8项体检指标，获取个性化风险评估"
    )

    # 侧边栏导航
    st.sidebar.markdown("""
    <div style="background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
                padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
        <h4 style="color: #1f2937; margin-bottom: 0.5rem;">📋 页面导航</h4>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    border-radius: 8px; border-left: 3px solid #667eea;
                    background: white;">
            <span style="color: #374151;">📝 当前：个人风险评估</span>
        </div>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    border-radius: 8px; cursor: pointer;
                    border-left: 3px solid transparent;"
                    onclick="window.location.href='/?page=personal_assessment'">
            <span style="color: #374151;">📊 批量数据筛查</span>
        </div>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    border-radius: 8px; cursor: pointer;
                    border-left: 3px solid transparent;"
                    onclick="window.location.href='/?page=data_observation'">
            <span style="color: #374151;">📈 数据可视化分析</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 主要内容
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📋 输入体检指标")

        # 创建输入表单
        with st.form("risk_assessment_form"):

            st.markdown('<div class="input-container">', unsafe_allow_html=True)

            # 怀孕次数
            pregnancies = st.slider(
                "怀孕次数",
                min_value=0,
                max_value=20,
                value=1,
                help="怀孕次数，未怀孕请输入0"
            )

            # 血糖浓度
            glucose = st.slider(
                "血糖浓度 (mg/dL)",
                min_value=0,
                max_value=300,
                value=120,
                help="空腹血糖浓度，正常值通常在70-100之间"
            )

            # 血压
            blood_pressure = st.slider(
                "舒张压 (mmHg)",
                min_value=0,
                max_value=150,
                value=80,
                help="舒张压，正常值通常在60-80之间"
            )

            # 皮肤厚度
            skin_thickness = st.slider(
                "皮褶厚度 (mm)",
                min_value=0,
                max_value=100,
                value=20,
                help="三头肌皮褶厚度，用于评估体脂"
            )

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="input-container">', unsafe_allow_html=True)

            # 胰岛素
            insulin = st.slider(
                "胰岛素水平 (μU/mL)",
                min_value=0,
                max_value=500,
                value=80,
                help="血清胰岛素水平"
            )

            # BMI
            bmi = st.slider(
                "体质指数 (BMI)",
                min_value=0.0,
                max_value=50.0,
                value=25.0,
                step=0.1,
                help="体重指数，正常范围18.5-24.9"
            )

            # 糖尿病家族史
            diabetes_pedigree = st.slider(
                "糖尿病家族史函数",
                min_value=0.0,
                max_value=2.5,
                value=0.5,
                step=0.01,
                help="糖尿病家族史遗传风险评估"
            )

            # 年龄
            age = st.slider(
                "年龄",
                min_value=1,
                max_value=100,
                value=35,
                help="实际年龄"
            )

            st.markdown('</div>', unsafe_allow_html=True)

            # 提交按钮
            submitted = st.form_submit_button("🔍 开始风险评估", use_container_width=True)

    with col2:
        st.markdown("### 📊 评估结果")

        if submitted:
            # 1. 收集原始数据
            raw_input_data = {
                'Pregnancies': pregnancies,
                'Glucose': glucose,
                'BloodPressure': blood_pressure,
                'SkinThickness': skin_thickness,
                'Insulin': insulin,
                'BMI': bmi,
                'DiabetesPedigreeFunction': diabetes_pedigree,
                'Age': age
            }

            # 2. 调用核心预测函数
            risk_score, final_prediction, odds_ratios = predict_risk(raw_input_data)

            if risk_score is None:
                # 预测函数已在内部显示错误，这里直接返回
                return

            # 获取风险等级
            risk_level, risk_icon, risk_advice = get_risk_level(risk_score, OPTIMAL_THRESHOLD)

            # 限制在0-100范围内
            risk_score = min(100, max(0, risk_score))

            # 显示结果
            st.markdown(f'<div class="result-card">', unsafe_allow_html=True)

            # 风险评分仪表盘
            fig = create_risk_gauge(risk_score)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # 风险等级和建议
            advice_details = {
                "低风险": [
                    "继续保持健康的生活方式",
                    "每年进行一次健康检查",
                    "均衡饮食，适量运动"
                ],
                "中等风险": [
                    "建议每6个月检查一次血糖",
                    "控制体重，增加运动量",
                    "减少高糖食物摄入",
                    "咨询医生制定预防计划"
                ],
                "高风险": [
                    "<strong>立即就医</strong>，进行详细检查",
                    "严格执行饮食控制",
                    "加强血糖监测",
                    "遵从医生的治疗建议"
                ]
            }

            # 使用新的风险等级显示组件
            create_risk_level_display(risk_score, risk_level, risk_advice)

            # 显示详细建议
            if risk_level in advice_details:
                st.markdown("#### 💡 详细建议")
                for advice in advice_details[risk_level]:
                    st.markdown(f"• {advice}")

            # 详细指标分析
            st.markdown("### 📈 指标分析")

            st.markdown(f"基于逻辑回归模型，模型识别出以下关键指标的风险贡献（优势比 **Odds Ratio**）：")

            # 仅展示最重要的几个特征的优势比
            key_risk_data = {
                '指标': ['血糖 (Glucose)', '年龄分类 (Age_category_≥40岁)', 'BMI', '家族史 (DiabetesPedigreeFunction)'],
                '您的值': [glucose, age, bmi, diabetes_pedigree],
                '优势比 (OR)': [
                    f"{odds_ratios.get('Glucose', 1.0):.3f}",
                    f"{odds_ratios.get('Age_category_≥40岁', 1.0):.3f}",
                    f"{odds_ratios.get('BMI', 1.0):.3f}",
                    f"{odds_ratios.get('DiabetesPedigreeFunction', 1.0):.3f}",
                ],
                '风险解释': [
                    '每增加一个单位，患病几率增加',
                    '对比30岁以下人群，患病几率增加',
                    '每增加一个单位，患病几率增加',
                    '每增加一个单位，患病几率增加',
                ]
            }

            df_metrics = pd.DataFrame(key_risk_data)
            st.dataframe(df_metrics, use_container_width=True, hide_index=True)

        else:
            st.info("💡 请在左侧输入体检指标，然后点击'开始风险评估'按钮")

    # 底部说明
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 2rem 0;'>
        <p style='font-size: 0.9rem; margin: 0;'>⚠️ 本评估仅供参考，不能替代专业医疗诊断</p>
        <p style='font-size: 0.85rem; margin: 0.5rem 0;'>如有健康疑虑，请咨询专业医生</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()