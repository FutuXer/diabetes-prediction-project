import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import json
import pickle
import os


# --- 辅助函数：目标转换 ---
def outcome_to_risk_score(probabilities):
    """将预测概率转换为 0-100 的风险评分。"""
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
def save_model_and_explanation(model, feature_names, filename_prefix="risk_score", model_type="ridge"):
    """保存模型、提取系数并保存为 JSON。"""
    model_path = f'models/{filename_prefix}_model.pkl'
    os.makedirs('models', exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ 模型已保存到: {model_path}")

    explanation_data = {
        'model_type': model_type,
        'features': feature_names.tolist(),
        'intercept': float(model.intercept_),
        'coefficients': model.coef_.tolist()
    }

    explanation_path = f'models/{filename_prefix}_explanation.json'
    with open(explanation_path, 'w') as f:
        json.dump(explanation_data, f, indent=4)
    print(f"✅ 模型解释数据已保存到: {explanation_path}")


def train_and_evaluate_ridge_only():
    print("--- 1. 加载和准备数据 ---")
    DATA_PATH = '../data/processed/diabetes_train_normalized.csv'

    try:
        train_data = pd.read_csv(DATA_PATH)
        print(f"数据加载成功，样本数: {len(train_data)}")
    except FileNotFoundError:
        print(f"❌ 错误：未找到数据文件 {DATA_PATH}，请检查路径。")
        return

    # 定义特征和目标
    NUMERIC_FEATURES = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]
    X = train_data[NUMERIC_FEATURES]
    y_risk_score = outcome_to_risk_score(train_data['Outcome'])

    # --- 2. 训练岭回归 (Ridge) ---
    print("\n--- 2. 训练岭回归 (Ridge) ---")
    # 使用 GridSearchCV 寻找最优正则化参数 alpha
    ridge_params = {'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}
    ridge_gscv = GridSearchCV(
        Ridge(random_state=42),
        ridge_params,
        cv=5,
        scoring='neg_mean_squared_error'
    )
    ridge_gscv.fit(X, y_risk_score)

    best_ridge_model = ridge_gscv.best_estimator_
    print(f"最优参数 alpha: {ridge_gscv.best_params_['alpha']}")

    # --- 3. 评估与保存 ---
    ridge_pred = best_ridge_model.predict(X)
    ridge_metrics = evaluate_regression_model(y_risk_score, ridge_pred, "Ridge Regression")

    # 保存唯一的岭回归模型
    save_model_and_explanation(
        best_ridge_model,
        X.columns,
        filename_prefix="risk_score_ridge",
        model_type="ridge"
    )

    # 保存评估指标
    os.makedirs('../docs', exist_ok=True)
    pd.DataFrame([ridge_metrics]).to_csv('../docs/ridge_metrics.csv', index=False)
    print(f"✅ 指标已保存到: ../docs/ridge_metrics.csv")

    return ridge_metrics


if __name__ == '__main__':
    metrics = train_and_evaluate_ridge_only()
    print("\n✅ 岭回归模型训练与保存完成！")