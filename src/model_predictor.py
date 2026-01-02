import pandas as pd
import numpy as np
import joblib
import os
import streamlit as st  # 在 Streamlit 应用中，可以使用 st.cache_resource

# =================================================================
# ⭐⭐⭐ 模型和常量配置区 ⭐⭐⭐
# =================================================================

# 1. 定义最优模型路径
MODEL_PATH = "analysis/models/disease_classifier_ohe_new.pkl"

# 原始训练数据路径 (用于计算标准化参数)
RAW_TRAIN_DATA_PATH = "data/processed/diabetes_train.csv"

# 2. 定义最佳分类阈值
OPTIMAL_THRESHOLD = 0.45

# 3. 定义模型期望的最终特征列表 (从模型文件中提取的准确顺序)
FINAL_FEATURES = [
    'Pregnancies_category_4-7次', 'BMI', 'Pregnancies', 'Insulin',
    'Pregnancies_category_≥8次', 'Age', 'Age_category_≥40岁', 'BloodPressure',
    'Glucose', 'DiabetesPedigreeFunction', 'Age_category_30-40岁',
    'BMI_category_32-37', 'SkinThickness', 'BMI_category_<27',
    'BMI_category_≥37', 'Pregnancies_category_1-3次'
]

# 4. 定义标准化器路径和数值特征
NUMERICAL_FEATURES = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]


# 参数加载函数

@st.cache_resource
def load_standardization_params():
    """
    加载原始训练数据，计算数值特征的均值和标准差 (mu 和 sigma)。
    由于 StandardSclaer 对象缺失，此函数用于手动计算参数。
    """
    if not os.path.exists(RAW_TRAIN_DATA_PATH):
        st.error(f"致命错误：原始训练数据文件未找到，请检查路径: {RAW_TRAIN_DATA_PATH}")
        return None, None

    try:
        # 使用原始训练数据计算均值和标准差
        df_raw_train = pd.read_csv(RAW_TRAIN_DATA_PATH)

        # 结果以字典形式返回，方便在 preprocess_data 中查找
        means = df_raw_train[NUMERICAL_FEATURES].mean().to_dict()
        stds = df_raw_train[NUMERICAL_FEATURES].std().to_dict()

        return means, stds

    except Exception as e:
        st.error(f"加载或计算标准化参数失败。错误: {e}")
        return None, None


# 5. 模型加载函数
@st.cache_resource
def load_model():
    """加载已保存的模型，并提取优势比用于结果解读"""
    if not os.path.exists(MODEL_PATH):
        st.error(f"错误：模型文件未找到，请检查路径: {MODEL_PATH}")
        return None, None

    try:
        model = joblib.load(MODEL_PATH)
        # 提取优势比 (Odds Ratio)
        if hasattr(model, 'coef_') and hasattr(model, 'feature_names_in_'):
            coefs = pd.DataFrame({
                'Feature': model.feature_names_in_,
                'Coefficient': model.coef_[0]
            })
            coefs['Odds_Ratio'] = np.exp(coefs['Coefficient'])
            key_odds_ratios = coefs.set_index('Feature')['Odds_Ratio'].to_dict()
        else:
            key_odds_ratios = {}

        return model, key_odds_ratios

    except Exception as e:
        st.error(f"模型加载或解析失败: {e}")
        return None, None


# 5. 数据预处理函数
def preprocess_data(raw_data: dict) -> pd.DataFrame:
    """
    对用户输入数据进行预处理（分类、OHE、特征对齐）。
    """
    df = pd.DataFrame([raw_data])

    # 第一步：加载参数并执行手动标准化 (Z-score)
    means, stds = load_standardization_params()

    if means is None or stds is None:
        # 阻止继续执行
        raise RuntimeError("无法加载标准化参数，无法进行预测。")

    # 对数值特征执行 Z-score (X - mu) / sigma
    for feature in NUMERICAL_FEATURES:
        mu = means[feature]
        sigma = stds[feature]
        # X_std = (X - mu) / sigma
        df[feature] = (df[feature] - mu) / sigma

    # --- 分类函数（保持与训练时一致）---
    def categorize_pregnancies(p):
        if p == 0:
            return '0次'
        elif 1 <= p <= 3:
            return '1-3次'
        elif 4 <= p <= 7:
            return '4-7次'
        else:
            return '≥8次'

    def categorize_bmi(b):
        if b < 27.0:
            return '<27'
        elif 27.0 <= b < 32.0:
            return '27-32'
        elif 32.0 <= b < 37.0:
            return '32-37'
        else:
            return '≥37'

    def categorize_age(a):
        if a < 30:
            return '<30岁'
        elif 30 <= a < 40:
            return '30-40岁'
        else:
            return '≥40岁'

    df['Pregnancies_category'] = df['Pregnancies'].apply(categorize_pregnancies)
    df['BMI_category'] = df['BMI'].apply(categorize_bmi)
    df['Age_category'] = df['Age'].apply(categorize_age)

    # 2. 执行独热编码 (OHE)
    # drop_first=False 确保生成所有 OHE 列，然后再通过 FINAL_FEATURES 筛选掉参考列
    df_ohe = pd.get_dummies(df, columns=['Pregnancies_category', 'BMI_category', 'Age_category'], drop_first=False)

    # 3. 特征对齐（解决 ValueError 的关键）
    for col in FINAL_FEATURES:
        if col not in df_ohe.columns:
            df_ohe[col] = 0

    # 严格按照 FINAL_FEATURES 列表的顺序和列名来排列列
    X_final = df_ohe[FINAL_FEATURES]

    return X_final.astype(float)


# 7. 概率转换函数
def adjust_probability_display(raw_probability):
    """
    根据阈值调整概率显示，让大于0.45的概率显示为大于0.5
    转换逻辑：
    - prob ≤ 0.45: 映射到 0-0.5 范围
    - prob > 0.45: 映射到 0.5-1.0 范围
    """
    if raw_probability <= OPTIMAL_THRESHOLD:
        # 线性映射到 0-0.5 范围
        adjusted_prob = raw_probability * (0.5 / OPTIMAL_THRESHOLD)
    else:
        # 线性映射到 0.5-1.0 范围
        adjusted_prob = 0.5 + (raw_probability - OPTIMAL_THRESHOLD) * (0.5 / (1.0 - OPTIMAL_THRESHOLD))

    return adjusted_prob

# 8. 核心预测函数
def predict_risk(raw_data: dict):
    """
    接收原始输入，返回风险概率、诊断结果和优势比。
    """
    best_classifier, odds_ratios = load_model()

    if best_classifier is None:
        return None, None, None

    try:
        # 预处理数据
        X_final = preprocess_data(raw_data)

        # 预测概率
        prediction_proba = best_classifier.predict_proba(X_final)[:, 1]
        raw_probability = prediction_proba[0]  # 保持0-1范围用于分类判断

        # 应用最佳阈值进行最终诊断（使用原始概率）
        final_prediction = 1 if raw_probability >= OPTIMAL_THRESHOLD else 0

        # 转换显示概率（用于前端展示）
        display_probability = adjust_probability_display(raw_probability) * 100  # 转换为百分比

        return display_probability, final_prediction, odds_ratios

    except Exception as e:
        st.error(f"预测失败：特征对齐或模型计算出错。详细错误: {e}")
        return None, None, None