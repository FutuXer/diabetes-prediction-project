import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import os
import json


# --- 辅助函数：目标转换 (与训练脚本保持一致) ---
def outcome_to_risk_score(probabilities):
    """将预测概率转换为 0-100 的风险评分（基于 P(Outcome=1)）。"""
    return probabilities * 100


# --- 辅助函数：模型评估 (与训练脚本保持一致) ---
def evaluate_regression_model(y_true, y_pred, model_name):
    """计算 R²、RMSE、MAE 等指标。"""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)

    metrics = {
        'Model': model_name,
        'R2': round(r2, 4),
        'RMSE': round(rmse, 4),
        'MAE': round(mae, 4)
    }
    print(f"\n--- {model_name} 测试集评估结果 ---")
    print(json.dumps(metrics, indent=4))
    return metrics


def test_optimized_gbr_model():
    print("--- 1. 加载模型和测试数据 ---")

    # 假设数据路径与训练集在同一目录下
    TEST_DATA_PATH = '../data/processed/diabetes_test_normalized.csv'
    MODEL_PATH = 'models/risk_score_ridge_model.pkl' # <-- 修改为这个新文件名

    # 1. 加载测试数据
    try:
        test_data = pd.read_csv(TEST_DATA_PATH)
        print(f"✅ 测试数据加载成功，样本数: {len(test_data)}")
    except FileNotFoundError:
        print(f"❌ 错误：未找到数据文件 {TEST_DATA_PATH}，请检查路径。")
        return

    # 2. 加载模型
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print(f"✅ 模型加载成功: {MODEL_PATH}")
    except FileNotFoundError:
        print(f"❌ 错误：未找到模型文件 {MODEL_PATH}。请先运行 '4_train_gbr_optimized.py'。")
        return

    # --- 2. 准备特征和目标变量 ---
    OPTIMIZED_FEATURES = [
         'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]

    # 提取特征集 X 和目标变量 y
    X_test = test_data[OPTIMIZED_FEATURES]
    y_probability_test = test_data['Outcome']

    # 转换为 0-100 风险评分
    y_risk_score_test = outcome_to_risk_score(y_probability_test)

    print(f"✅ 测试特征集 X 维度: {X_test.shape}")

    # --- 3. 进行预测和评估 ---
    print("\n--- 3. 模型预测和评估 ---")

    # 进行预测
    y_pred_risk_score = model.predict(X_test)

    # 评估模型性能
    test_metrics = evaluate_regression_model(
        y_risk_score_test,
        y_pred_risk_score,
        "Optimized GBR (6 Features)"
    )

    # 可选：打印预测结果的头部
    print("\n--- 部分预测结果展示 (预测值 vs 真实风险分) ---")
    results_df = pd.DataFrame({
        'True_Risk_Score': y_risk_score_test,
        'Predicted_Risk_Score': y_pred_risk_score
    })
    print(results_df.head(50))

    return test_metrics


if __name__ == '__main__':
    test_optimized_gbr_model()