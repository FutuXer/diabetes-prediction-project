import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
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
def save_model_and_explanation(model, feature_names, filename_prefix="risk_score", model_type="linear"):
    """保存模型、提取系数或特征重要性并保存为 JSON。"""

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
        'intercept': getattr(model, 'intercept_', None)  # 尝试获取截距
    }

    if model_type in ["linear", "ridge", "lasso"]:
        # 线性模型保存系数
        explanation_data['coefficients'] = model.coef_.tolist()
    else:
        # 对于其他统计模型，如果有特征重要性可以保存
        if hasattr(model, 'feature_importances_'):
            explanation_data['feature_importances'] = model.feature_importances_.tolist()
        else:
            explanation_data['coefficients'] = "Not applicable for this model type"

    # 3. 保存解释数据
    explanation_path = f'models/{filename_prefix}_explanation.json'
    with open(explanation_path, 'w') as f:
        json.dump(explanation_data, f, indent=4)
    print(f"✅ 模型解释数据已保存到: {explanation_path}")


def train_and_evaluate_regression_models():
    print("--- 1. 加载和准备数据 ---")
    DATA_PATH = '../data/processed/diabetes_train_normalized.csv'

    try:
        train_data = pd.read_csv(DATA_PATH)
        print(f"数据加载成功，样本数: {len(train_data)}")
    except FileNotFoundError:
        print(f"❌ 错误：未找到数据文件 {DATA_PATH}，请检查路径。")
        return

    # 定义回归模型所需的 8 个标准化数值特征
    # 注意：这里排除了 'Outcome' 和所有的 '_category' 文本列
    NUMERIC_FEATURES = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]

    # **核心修改：选择特征集 X 和目标变量 y**
    # 1. 特征集 X：只选择 8 个标准化数值列
    X = train_data[NUMERIC_FEATURES]

    # 2. 目标变量 y_probability：选择 Outcome 列
    y_probability = train_data['Outcome']

    # ⭐ 核心步骤：转换为 0-100 风险评分
    y_risk_score = outcome_to_risk_score(y_probability)

    # 确认特征数量是否正确
    print(f"特征集 X 维度: {X.shape}")  # 预期 (样本数, 8)

    # --- 2. 训练和评估基线模型：多元线性回归 (LR) ---
    print("\n--- 2. 训练多元线性回归 (Baseline) ---")
    lr_model = LinearRegression()
    lr_model.fit(X, y_risk_score)
    lr_pred = lr_model.predict(X)
    lr_metrics = evaluate_regression_model(y_risk_score, lr_pred, "Linear Regression (Baseline)")

    # --- 3. 训练和评估模型 2：岭回归 (Ridge) ---
    print("\n--- 3. 训练岭回归 (Ridge) ---")
    ridge_params = {'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}
    ridge_gscv = GridSearchCV(Ridge(random_state=42), ridge_params, cv=5, scoring='neg_mean_squared_error')
    ridge_gscv.fit(X, y_risk_score)
    best_ridge_model = ridge_gscv.best_estimator_
    print(f"最优岭回归参数: {ridge_gscv.best_params_}")

    ridge_pred = best_ridge_model.predict(X)
    ridge_metrics = evaluate_regression_model(y_risk_score, ridge_pred, "Ridge Regression (Optimal)")

    # --- 4. 训练和评估模型 3：Lasso回归 (Lasso) ---
    print("\n--- 4. 训练 Lasso 回归 ---")
    lasso_params = {'alpha': [0.0001, 0.001, 0.01, 0.1, 1.0]}
    lasso_gscv = GridSearchCV(Lasso(random_state=42, max_iter=10000), lasso_params, cv=5,
                              scoring='neg_mean_squared_error')
    lasso_gscv.fit(X, y_risk_score)
    best_lasso_model = lasso_gscv.best_estimator_
    print(f"最优 Lasso 回归参数: {lasso_gscv.best_params_}")

    lasso_pred = best_lasso_model.predict(X)
    lasso_metrics = evaluate_regression_model(y_risk_score, lasso_pred, "Lasso Regression (Optimal)")

    # --- 5. 最终模型选择与保存 ---
    print("\n--- 5. 最终模型选择与保存 ---")

    # 集合所有模型的评估结果
    all_models = {
        "Linear Regression": lr_metrics,
        "Ridge Regression": ridge_metrics,
        "Lasso Regression": lasso_metrics
    }

    # 找出 R2 最高的模型作为最佳模型
    best_model_name = max(all_models, key=lambda name: all_models[name]['R2'])
    best_r2 = all_models[best_model_name]['R2']

    print(f"\n✨ 模型性能对比 ✨")
    print(f"{'=' * 40}")
    print(f"{'模型名称':<25} {'R²':<8} {'RMSE':<8} {'MAE':<8}")
    print(f"{'=' * 40}")
    for name, metrics in all_models.items():
        print(f"{name:<25} {metrics['R2']:<8} {metrics['RMSE']:<8} {metrics['MAE']:<8}")
    print(f"{'=' * 40}")

    print(f"\n📊 最佳模型: {best_model_name} (R² = {best_r2:.4f})")

    # 选择最终模型
    if best_model_name == "Linear Regression":
        final_model = lr_model
        model_type = "linear"
    elif best_model_name == "Ridge Regression":
        final_model = best_ridge_model
        model_type = "ridge"
    elif best_model_name == "Lasso Regression":
        final_model = best_lasso_model
        model_type = "lasso"

    # 保存最佳模型
    save_model_and_explanation(final_model, X.columns,
                               filename_prefix="risk_score",
                               model_type=model_type)

    # 可选：保存所有模型的评估结果供报告使用
    all_metrics_df = pd.DataFrame([
        lr_metrics,
        ridge_metrics,
        lasso_metrics
    ])

    os.makedirs('../docs', exist_ok=True)
    all_metrics_df.to_csv('../docs/regression_model_metrics.csv', index=False)
    print(f"✅ 所有模型评估指标已保存到: ../docs/regression_model_metrics.csv")

    return lr_metrics, ridge_metrics, lasso_metrics


if __name__ == '__main__':
    all_metrics = train_and_evaluate_regression_models()
    print("\n✅ 所有回归模型训练完成！")