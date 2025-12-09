import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import json
import pickle
import os


# --- 辅助函数：目标转换 ---
def outcome_to_risk_score(probabilities):
    """将预测概率转换为 0-100 的风险评分（基于 P(Outcome=1)）。"""
    return probabilities * 100


# --- 辅助函数：模型评估 ---
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
    print(f"\n--- {model_name} 评估结果 ---")
    print(json.dumps(metrics, indent=4))
    return metrics


# --- 核心函数：模型解释与保存 ---
def save_model_and_explanation(model, feature_names, filename_prefix="risk_score"):
    """保存模型、提取系数并保存为 JSON。"""

    # 1. 确保模型目录存在
    os.makedirs('models', exist_ok=True)

    # 2. 保存模型
    model_path = f'models/{filename_prefix}_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ 模型已保存到: {model_path}")

    # 3. 提取解释数据
    explanation_data = {
        'model_type': 'linear_regression',
        'features': feature_names.tolist(),
        'intercept': float(model.intercept_)
    }

    # 保存系数
    explanation_data['coefficients'] = model.coef_.tolist()

    # 4. 保存解释数据
    explanation_path = f'models/{filename_prefix}_explanation.json'
    with open(explanation_path, 'w') as f:
        json.dump(explanation_data, f, indent=4)
    print(f"✅ 模型解释数据已保存到: {explanation_path}")


def train_linear_regression_model():
    """训练多元线性回归模型"""
    print("=== 多元线性回归模型训练 ===")

    # --- 1. 加载和准备数据 ---
    DATA_PATH = '../data/processed/diabetes_train_normalized.csv'

    try:
        train_data = pd.read_csv(DATA_PATH)
        print(f"数据加载成功，样本数: {len(train_data)}")
    except FileNotFoundError:
        print(f"❌ 错误：未找到数据文件 {DATA_PATH}，请检查路径。")
        return None

    # 定义回归模型所需的 8 个标准化数值特征
    NUMERIC_FEATURES = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]

    # 特征集 X：只选择 8 个标准化数值列
    X = train_data[NUMERIC_FEATURES]

    # 目标变量 y_probability：选择 Outcome 列
    y_probability = train_data['Outcome']

    # 转换为 0-100 风险评分
    y_risk_score = outcome_to_risk_score(y_probability)

    # 确认特征数量是否正确
    print(f"特征集 X 维度: {X.shape}")
    print(f"目标变量 y 维度: {y_risk_score.shape}")
    print(f"\n使用的特征: {list(X.columns)}")

    # --- 2. 训练多元线性回归模型 ---
    print("\n--- 训练多元线性回归模型 ---")
    lr_model = LinearRegression()
    lr_model.fit(X, y_risk_score)

    # 输出模型基本信息
    print("✅ 模型训练完成")
    print(f"截距 (Intercept): {lr_model.intercept_:.4f}")
    print("\n系数 (Coefficients):")
    for feature, coef in zip(X.columns, lr_model.coef_):
        print(f"  {feature}: {coef:.4f}")

    # --- 3. 模型评估 ---
    lr_pred = lr_model.predict(X)
    lr_metrics = evaluate_regression_model(y_risk_score, lr_pred, "Linear Regression")

    # --- 4. 模型保存 ---
    print("\n--- 保存模型和解释数据 ---")
    save_model_and_explanation(lr_model, X.columns)

    return lr_model, lr_metrics, X.columns


if __name__ == '__main__':
    # 训练模型
    model, metrics, features = train_linear_regression_model()

    if model is not None:
        print("\n=== 训练完成 ===")
        print(f"模型评估指标:")
        print(f"  R²: {metrics['R2']}")
        print(f"  RMSE: {metrics['RMSE']}")
        print(f"  MAE: {metrics['MAE']}")

        # 生成简单的模型报告
        print("\n=== 模型报告 ===")
        print(f"模型类型: 多元线性回归")
        print(f"特征数量: {len(features)}")
        print(f"模型已保存到 models/ 目录")