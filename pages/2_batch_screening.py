"""
糖尿病预测项目 - 批量数据筛查页面
作者: 成员B（数据预处理）+ 成员C/D（模型应用）
功能: 上传CSV文件进行批量预测，生成筛查报告
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import warnings
from src.model_predictor import predict_risk, OPTIMAL_THRESHOLD

warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="批量数据筛查 - 糖尿病预测",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 导入统一的UI样式系统
from src.ui_styles import apply_flat_theme, create_hero_section

def calculate_risk_score(row):
    """使用训练好的回归模型计算风险评分"""
    try:
        # 将行数据转换为字典格式
        input_data = {
            'Pregnancies': row.get('Pregnancies', 1),
            'Glucose': row.get('Glucose', 100),
            'BloodPressure': row.get('BloodPressure', 70),
            'SkinThickness': row.get('SkinThickness', 20),
            'Insulin': row.get('Insulin', 80),
            'BMI': row.get('BMI', 25.0),
            'DiabetesPedigreeFunction': row.get('DiabetesPedigreeFunction', 0.5),
            'Age': row.get('Age', 35)
        }

        # 使用模型预测
        risk_score, final_prediction, odds_ratios = predict_risk(input_data)

        if risk_score is None:
            # 如果模型预测失败，使用备用方案
            return calculate_backup_score(row)

        return min(100, max(0, risk_score))

    except Exception as e:
        st.warning(f"模型预测失败，使用备用计算方法: {str(e)}")
        return calculate_backup_score(row)

def calculate_backup_score(row):
    """备用风险评分计算（当模型不可用时）"""
    score = 20  # 基础分

    # 血糖因子
    glucose = row.get('Glucose', 100)
    if glucose > 140:
        score += 30
    elif glucose > 120:
        score += 15
    elif glucose > 100:
        score += 5

    # BMI因子
    bmi = row.get('BMI', 25)
    if bmi > 30:
        score += 20
    elif bmi > 25:
        score += 10

    # 年龄因子
    age = row.get('Age', 35)
    if age > 60:
        score += 15
    elif age > 45:
        score += 10
    elif age > 30:
        score += 5

    # 家族史因子
    diabetes_pedigree = row.get('DiabetesPedigreeFunction', 0.5)
    if diabetes_pedigree > 1.0:
        score += 15
    elif diabetes_pedigree > 0.5:
        score += 8

    return min(100, max(0, score))

def get_risk_category(score):
    """获取风险分类"""
    if score < 30:
        return "低风险"
    elif score < 70:
        return "中等风险"
    else:
        return "高风险"

def validate_csv_format(df):
    """验证CSV格式"""
    required_columns = [
        'Pregnancies', 'Glucose', 'BloodPressure',
        'SkinThickness', 'Insulin', 'BMI',
        'DiabetesPedigreeFunction', 'Age'
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        missing_cols_str = ', '.join(missing_columns)
        return False, "缺少必需的列: " + missing_cols_str

    if len(df) == 0:
        return False, "文件为空"

    return True, "格式验证通过"

def main():
    """主函数"""

    # 应用扁平化主题
    apply_flat_theme()

    # 页面标题
    create_hero_section(
        title="批量数据筛查",
        subtitle="上传CSV文件进行批量预测，生成详细筛查报告"
    )

    # 侧边栏导航
    st.sidebar.markdown("""
    <div style="background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
                padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
        <h4 style="color: #1f2937; margin-bottom: 0.5rem;">📋 页面导航</h4>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    border-radius: 8px; cursor: pointer;
                    border-left: 3px solid transparent;"
                    onclick="window.location.href='/?page=personal_assessment'">
            <span style="color: #374151;">📝 个人风险评估</span>
        </div>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    border-radius: 8px; border-left: 3px solid #667eea;
                    background: white;">
            <span style="color: #374151;">📊 当前：批量数据筛查</span>
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
    st.markdown("### 🔄 批量筛查流程")

    # 步骤1: 文件上传
    st.markdown("""
    <div class="step-container">
        <h4>步骤 1: 上传数据文件</h4>
        <p>请上传包含体检数据的CSV文件。文件应包含以下列：Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age</p>
    </div>
    """, unsafe_allow_html=True)

    # 文件上传区域
    uploaded_file = st.file_uploader(
        "📁 选择CSV文件",
        type=['csv'],
        help="请上传包含8个必需列的CSV文件"
    )

    if uploaded_file is not None:
        try:
            # 读取CSV文件
            df = pd.read_csv(uploaded_file)

            # 验证格式
            is_valid, message = validate_csv_format(df)

            if is_valid:
                st.success("✅ " + message)
                st.info("📄 文件信息：" + str(df.shape[0]) + " 行 × " + str(df.shape[1]) + " 列")

                # 显示数据预览
                st.markdown("#### 📋 数据预览")
                st.dataframe(df.head(), use_container_width=True)

                # 步骤2: 数据验证
                st.markdown("---")
                st.markdown("""
                <div class="step-container">
                    <h4>步骤 2: 数据质量检查</h4>
                    <p>检查数据完整性和异常值</p>
                </div>
                """, unsafe_allow_html=True)

                # 数据质量统计
                col1, col2, col3 = st.columns(3)

                with col1:
                    # 缺失值统计
                    missing_stats = df.isnull().sum()
                    total_missing = missing_stats.sum()
                    st.metric("缺失值", str(total_missing), "需要处理" if total_missing > 0 else "完整")

                with col2:
                    # 重复值统计
                    duplicates = df.duplicated().sum()
                    st.metric("重复行", str(duplicates), "需要处理" if duplicates > 0 else "无重复")

                with col3:
                    # 零值统计（针对生理学不可能的特征）
                    zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
                    zero_count = 0
                    for col in zero_cols:
                        if col in df.columns:
                            zero_count += (df[col] == 0).sum()
                    st.metric("可疑零值", str(zero_count), "需要检查" if zero_count > 0 else "正常")

                # 步骤3: 批量预测
                st.markdown("---")
                st.markdown("""
                <div class="step-container">
                    <h4>步骤 3: 开始批量预测</h4>
                    <p>应用预测模型进行风险评估</p>
                </div>
                """, unsafe_allow_html=True)

                # 预测按钮
                if st.button("🚀 开始批量预测", type="primary", use_container_width=True):
                    with st.spinner("正在进行风险评估..."):
                        # 复制数据用于预测
                        result_df = df.copy()

                        # 使用模型进行批量预测
                        risk_scores = []
                        disease_probabilities = []
                        predictions = []

                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        for i, (_, row) in enumerate(result_df.iterrows()):
                            progress = (i + 1) / len(result_df)
                            progress_bar.progress(progress)
                            status_text.text(f"正在处理第 {i+1}/{len(result_df)} 个样本...")

                            # 构建输入数据
                            input_data = {
                                'Pregnancies': row.get('Pregnancies', 1),
                                'Glucose': row.get('Glucose', 100),
                                'BloodPressure': row.get('BloodPressure', 70),
                                'SkinThickness': row.get('SkinThickness', 20),
                                'Insulin': row.get('Insulin', 80),
                                'BMI': row.get('BMI', 25.0),
                                'DiabetesPedigreeFunction': row.get('DiabetesPedigreeFunction', 0.5),
                                'Age': row.get('Age', 35)
                            }

                            # 使用模型预测
                            risk_score, prediction, odds_ratios = predict_risk(input_data)

                            if risk_score is not None:
                                risk_scores.append(risk_score)
                                disease_probabilities.append(risk_score / 100)  # 归一化到0-1
                                predictions.append("有糖尿病" if prediction == 1 else "无糖尿病")
                            else:
                                # 备用计算
                                backup_score = calculate_backup_score(row)
                                risk_scores.append(backup_score)
                                disease_probabilities.append(backup_score / 100)
                                predictions.append("有糖尿病" if backup_score > 50 else "无糖尿病")

                        progress_bar.empty()
                        status_text.empty()

                        # 添加预测结果到数据框
                        result_df['风险评分'] = risk_scores
                        result_df['患病概率'] = disease_probabilities
                        result_df['预测结果'] = predictions
                        result_df['风险等级'] = result_df['风险评分'].apply(get_risk_category)

                        st.success("✅ 预测完成！")

                # 如果已经进行了预测，显示结果
                if '风险评分' in locals() and 'result_df' in locals():
                    # 步骤4: 结果展示
                    st.markdown("---")
                    st.markdown("""
                    <div class="step-container">
                        <h4>步骤 4: 预测结果分析</h4>
                        <p>查看批量筛查的统计结果和详细报告</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # 统计概览
                    st.markdown("#### 📊 筛查统计概览")

                    risk_counts = result_df['风险等级'].value_counts()
                    disease_counts = result_df['预测结果'].value_counts()

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("总样本数", len(result_df))

                    with col2:
                        diabetes_count = disease_counts.get('有糖尿病', 0)
                        diabetes_pct = round(diabetes_count / len(result_df) * 100, 1)
                        st.metric("预测患病", str(diabetes_count) + " (" + str(diabetes_pct) + "%)")

                    with col3:
                        healthy_count = disease_counts.get('无糖尿病', 0)
                        healthy_pct = round(healthy_count / len(result_df) * 100, 1)
                        st.metric("预测健康", str(healthy_count) + " (" + str(healthy_pct) + "%)")

                    with col4:
                        avg_risk = round(result_df['风险评分'].mean(), 1)
                        st.metric("平均风险评分", str(avg_risk) + "分")

                    # 风险分布图
                    st.markdown("#### 📈 风险分布")

                    fig_pie = go.Figure(data=[go.Pie(
                        labels=risk_counts.index,
                        values=risk_counts.values,
                        hole=0.3,
                        marker_colors=['#10b981', '#f59e0b', '#ef4444']
                    )])

                    fig_pie.update_layout(
                        title="风险等级分布",
                        height=400,
                        showlegend=True
                    )

                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.plotly_chart(fig_pie, use_container_width=True)

                    with col2:
                        # 风险评分分布直方图
                        fig_hist = go.Figure(data=[go.Histogram(
                            x=result_df['风险评分'],
                            nbinsx=20,
                            marker_color='#667eea',
                            opacity=0.7
                        )])

                        fig_hist.update_layout(
                            title="风险评分分布",
                            xaxis_title="风险评分",
                            yaxis_title="人数",
                            height=400
                        )

                        st.plotly_chart(fig_hist, use_container_width=True)

                    # 详细结果表格
                    st.markdown("#### 📋 详细筛查结果")

                    # 添加颜色编码的风险等级
                    def color_risk_level(val):
                        if val == "高风险":
                            return 'background-color: #fee2e2; color: #dc2626; font-weight: bold'
                        elif val == "中等风险":
                            return 'background-color: #fef3c7; color: #d97706; font-weight: bold'
                        else:
                            return 'background-color: #d1fae5; color: #059669; font-weight: bold'

                    display_df = result_df.copy()
                    display_df = display_df.round(2)

                    st.dataframe(
                        display_df.style.applymap(color_risk_level, subset=['风险等级']),
                        use_container_width=True,
                        height=400
                    )

                    # 导出功能
                    st.markdown("---")
                    st.markdown("#### 💾 导出筛查报告")

                    col1, col2 = st.columns(2)

                    with col1:
                        # 导出为CSV
                        csv = result_df.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="📊 下载筛查结果 (CSV)",
                            data=csv,
                            file_name="diabetes_screening_results_" + pd.Timestamp.now().strftime('%Y%m%d_%H%M%S') + ".csv",
                            mime="text/csv",
                            use_container_width=True
                        )

                    with col2:
                        # 导出为Excel
                        buffer = StringIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            result_df.to_excel(writer, index=False, sheet_name='筛查结果')

                            # 添加统计汇总表
                            summary_data = {
                                '指标': ['总样本数', '高风险人数', '中等风险人数', '低风险人数', '平均风险评分'],
                                '数值': [
                                    len(result_df),
                                    risk_counts.get('高风险', 0),
                                    risk_counts.get('中等风险', 0),
                                    risk_counts.get('低风险', 0),
                                    result_df['风险评分'].mean()
                                ]
                            }
                            summary_df = pd.DataFrame(summary_data)
                            summary_df.to_excel(writer, index=False, sheet_name='统计汇总')

                        st.download_button(
                            label="📈 下载完整报告 (Excel)",
                            data=buffer.getvalue(),
                            file_name="diabetes_screening_report_" + pd.Timestamp.now().strftime('%Y%m%d_%H%M%S') + ".xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )

            else:
                st.error("❌ " + message)

                # 提供示例数据格式
                st.markdown("#### 📝 数据格式示例")
                sample_data = {
                    'Pregnancies': [1, 2, 0, 3],
                    'Glucose': [120, 140, 85, 165],
                    'BloodPressure': [80, 70, 75, 90],
                    'SkinThickness': [20, 25, 15, 35],
                    'Insulin': [80, 100, 60, 200],
                    'BMI': [25.0, 28.5, 22.1, 35.0],
                    'DiabetesPedigreeFunction': [0.5, 0.8, 0.2, 1.2],
                    'Age': [35, 45, 28, 55]
                }
                sample_df = pd.DataFrame(sample_data)
                st.dataframe(sample_df, use_container_width=True)

        except Exception as e:
            st.error("❌ 处理文件时发生错误: " + str(e))
            st.markdown("#### 💡 建议检查")
            st.markdown("- 文件格式是否正确（UTF-8编码的CSV文件）")
            st.markdown("- 列名是否包含所有必需的特征")
            st.markdown("- 数据是否包含非数值内容")

    else:
        # 显示上传区域
        st.markdown("""
        <div class="upload-container">
            <h3>📁 上传您的数据文件</h3>
            <p>拖拽CSV文件到此处，或点击下方按钮选择文件</p>
            <p><small>支持格式：CSV | 最大文件大小：200MB</small></p>
        </div>
        """, unsafe_allow_html=True)

        # 示例数据展示
        st.markdown("#### 📋 期望的数据格式")

        example_data = {
            '列名': ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'],
            '说明': ['怀孕次数', '血糖浓度(mg/dL)', '舒张压(mmHg)', '皮褶厚度(mm)', '胰岛素水平(μU/mL)', '体质指数', '糖尿病家族史函数', '年龄'],
            '数据类型': ['整数', '整数', '整数', '整数', '整数', '浮点数', '浮点数', '整数'],
            '示例值': [1, 120, 80, 20, 80, 25.0, 0.5, 35]
        }

        example_df = pd.DataFrame(example_data)
        st.dataframe(example_df, use_container_width=True, hide_index=True)

        st.info("💡 **提示**：请确保您的CSV文件包含上述所有8个必需列，列名需要完全匹配（区分大小写）。")

    # 底部说明
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 2rem 0;'>
        <p style='font-size: 0.9rem; margin: 0;'>⚠️ 本筛查仅供参考，不能替代专业医疗诊断</p>
        <p style='font-size: 0.85rem; margin: 0.5rem 0;'>批量筛查结果仅供健康管理参考</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()