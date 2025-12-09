import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor
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

# --- 辅助函数：模型解释与保存 (简化) ---
def save_model_and_explanation(model, feature_names, filename_prefix="risk_score", model_type="gbr"):
    """保存模型、提取特征重要性并保存为 JSON。"""

    # 1. 保存模型
    model_path = f'models/{filename_prefix}_model.pkl'
    os.makedirs('models', exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ 模型已保存到: {model_path}")

    # 2. 提取解释数据
    explanation_data = {
        'model_type': model_type,
        'features': feature_names.tolist(),
        'intercept': getattr(model, 'intercept_', None),
        'feature_importances': model.feature_importances_.tolist() # GBR 使用 feature_importances_
    }

    # 3. 保存解释数据
    explanation_path = f'models/{filename_prefix}_explanation.json'
    with open(explanation_path, 'w') as f:
        json.dump(explanation_data, f, indent=4)
    print(f"✅ 模型解释数据已保存到: {explanation_path}")

def train_optimized_gbr():
    print("--- 1. 加载和准备数据 ---")
    # 假设数据路径相对于这个新脚本
    DATA_PATH = '../data/processed/diabetes_train_normalized.csv'
    # 如果您在与 3_train_models.py 相同的目录下运行，请调整路径

    try:
        train_data = pd.read_csv(DATA_PATH)
        print(f"数据加载成功，样本数: {len(train_data)}")
    except FileNotFoundError:
        print(f"❌ 错误：未找到数据文件 {DATA_PATH}，请检查路径。")
        return

    OPTIMIZED_FEATURES = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]

    # 1. 特征集 X：只选择优化的 6 个标准化数值列
    X = train_data[OPTIMIZED_FEATURES]

    # 2. 目标变量 y_probability：选择 Outcome 列
    y_probability = train_data['Outcome']

    # ⭐ 核心步骤：转换为 0-100 风险评分
    y_risk_score = outcome_to_risk_score(y_probability)

    print(f"✅ 优化后的特征集 X 维度: {X.shape}") # 预期 (样本数, 6)

    # --- 2. 训练梯度提升回归树 (GBR) ---
    print("\n--- 2. 训练优化后的 GBR 模型 ---")

    # 定义超参数网格（与原代码保持一致）
    gbr_params = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.05, 0.1, 0.2],
        'max_depth': [3, 4]
    }

    gbr_gscv = GridSearchCV(
        GradientBoostingRegressor(random_state=42),
        gbr_params,
        cv=5,
        scoring='neg_mean_squared_error',
        verbose=1,
        n_jobs=-1
    )

    # GBR 模型训练
    gbr_gscv.fit(X, y_risk_score)
    best_gbr_model = gbr_gscv.best_estimator_
    print(f"最优 GBR 参数: {gbr_gscv.best_params_}")

    gbr_pred = best_gbr_model.predict(X)
    gbr_metrics = evaluate_regression_model(y_risk_score, gbr_pred, "Optimized GBR (6 Features)")

    # --- 3. 保存模型和解释数据 ---
    print("\n--- 3. 保存最终模型和解释 ---")
    save_model_and_explanation(best_gbr_model, X.columns, filename_prefix="risk_score", model_type="gbr")

    return gbr_metrics

if __name__ == '__main__':
    train_optimized_gbr()