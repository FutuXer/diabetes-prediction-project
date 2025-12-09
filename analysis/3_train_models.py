import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
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


# --- 核心函数：模型解释与保存 (简化) ---
# analysis/3_train_models.py (更新后的 save_model_and_explanation 函数)

def save_model_and_explanation(model, feature_names, filename_prefix="risk_score", model_type="linear"):
    """保存模型、提取系数或特征重要性并保存为 JSON。"""

    # 1. 保存模型
    model_path = f'models/{filename_prefix}_model.pkl'
    # ... (保存模型代码保持不变)
    os.makedirs('models', exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ 模型已保存到: {model_path}")

    # 2. 提取解释数据
    explanation_data = {
        'model_type': model_type,
        'features': feature_names.tolist(),
        'intercept': getattr(model, 'intercept_', None)  # 尝试获取截距，非线性模型可能没有
    }

    if model_type in ["linear", "ridge", "lasso"]:
        # 线性模型保存系数
        explanation_data['coefficients'] = model.coef_.tolist()
    else:
        # 非线性模型保存特征重要性
        explanation_data['feature_importances'] = model.feature_importances_.tolist()

    # 3. 保存解释数据
    explanation_path = f'models/{filename_prefix}_explanation.json'  # 注意：文件名从 coefficients 改为 explanation
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
    lr_model = LinearRegression()
    lr_model.fit(X, y_risk_score)
    lr_pred = lr_model.predict(X)
    lr_metrics = evaluate_regression_model(y_risk_score, lr_pred, "Linear Regression (Baseline)")

    # --- 3. 训练和评估模型 2：岭回归 (Ridge) ---
    # ... (使用 X 和 y_risk_score 进行 Ridge 模型训练和评估，保持不变)
    print("\n--- 3. 训练岭回归 (Ridge) ---")
    ridge_params = {'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}
    ridge_gscv = GridSearchCV(Ridge(random_state=42), ridge_params, cv=5, scoring='neg_mean_squared_error')
    ridge_gscv.fit(X, y_risk_score)
    best_ridge_model = ridge_gscv.best_estimator_
    print(f"最优岭回归参数: {ridge_gscv.best_params_}")

    ridge_pred = best_ridge_model.predict(X)
    ridge_metrics = evaluate_regression_model(y_risk_score, ridge_pred, "Ridge Regression (Optimal)")

    # --- 4. 训练和评估模型 3：Lasso回归 (Lasso) ---
    # ... (使用 X 和 y_risk_score 进行 Lasso 模型训练和评估，保持不变)
    print("\n--- 4. 训练 Lasso 回归 ---")
    lasso_params = {'alpha': [0.0001, 0.001, 0.01, 0.1, 1.0]}
    lasso_gscv = GridSearchCV(Lasso(random_state=42, max_iter=10000), lasso_params, cv=5,
                              scoring='neg_mean_squared_error')
    lasso_gscv.fit(X, y_risk_score)
    best_lasso_model = lasso_gscv.best_estimator_
    print(f"最优 Lasso 回归参数: {lasso_gscv.best_params_}")

    lasso_pred = best_lasso_model.predict(X)
    lasso_metrics = evaluate_regression_model(y_risk_score, lasso_pred, "Lasso Regression (Optimal)")

    # --- 5. 训练和评估模型 4：梯度提升回归树 (GBR) ---
    print("\n--- 5. 训练梯度提升回归树 (GBR) ---")

    # 定义超参数网格（仅选择部分关键参数进行调优）
    gbr_params = {
        'n_estimators': [50, 100, 200],  # 树的数量
        'learning_rate': [0.05, 0.1, 0.2],  # 学习率
        'max_depth': [3, 4]  # 树的最大深度
    }

    # 使用 5 折交叉验证寻找最优参数
    gbr_gscv = GridSearchCV(
        GradientBoostingRegressor(random_state=42),
        gbr_params,
        cv=5,
        scoring='neg_mean_squared_error',
        verbose=1,  # 显示进度
        n_jobs=-1  # 使用所有核心并行计算
    )

    # GBR 模型训练
    gbr_gscv.fit(X, y_risk_score)
    best_gbr_model = gbr_gscv.best_estimator_
    print(f"最优 GBR 参数: {gbr_gscv.best_params_}")

    gbr_pred = best_gbr_model.predict(X)
    gbr_metrics = evaluate_regression_model(y_risk_score, gbr_pred, "Gradient Boosting Regressor (Optimal) - FE")

    # --- 6. 最终模型选择与保存 (更新逻辑) ---
    print("\n--- 6. 最终模型选择与保存 ---")

    # 集合所有模型的评估结果
    all_models = {
        "Linear Regression": lr_metrics,
        "Ridge Regression": ridge_metrics,
        "Lasso Regression": lasso_metrics,
        "GBR": gbr_metrics
    }

    # 找出 R2 最高的模型作为最佳模型
    best_model_name = max(all_models, key=lambda name: all_models[name]['R2'])

    if best_model_name == "GBR":
        best_model = best_gbr_model
        print(f"✨ 最终选择非线性模型：{best_model_name}，R2 最高。")
    elif best_model_name == "Ridge Regression":
        best_model = best_ridge_model
        print(f"✨ 最终选择线性模型：{best_model_name}，易于解释。")
    # ... 您可以根据实际情况添加更多选择逻辑
    else:
        # 如果 GBR 优于线性模型，则选择 GBR
        best_model = best_ridge_model  # 默认为 Ridge，如果 GBR 性能提升不明显，保持易解释的线性模型
        if gbr_metrics['R2'] > ridge_metrics['R2']:
            best_model = best_gbr_model
            best_model_name = "GBR"
            print(f"✨ GBR (R2={gbr_metrics['R2']}) 性能优于 Ridge (R2={ridge_metrics['R2']})，选择 GBR。")
        else:
            print("✨ 非线性模型性能提升不显著，仍选择 Ridge Regression 以保持解释性。")
            best_model_name = "Ridge Regression"

    # 重新赋值以获取最终选择的模型对象
    if best_model_name == "Ridge Regression":
        final_model_to_save = best_ridge_model
    elif best_model_name == "GBR":
        final_model_to_save = best_gbr_model
    else:
        final_model_to_save = best_ridge_model  # 保险起见

    # 注意：GBR 没有 coef_ 属性，保存解释数据需要不同的逻辑（例如特征重要性）
    if best_model_name in ["Ridge Regression", "Lasso Regression"]:
        save_model_and_explanation(final_model_to_save, X.columns, model_type="linear")
    else:  # 非线性模型 (GBR)
        # 为 GBR 单独保存模型，并保存 Feature Importance
        save_model_and_explanation(final_model_to_save, X.columns, model_type="gbr")

    return lr_metrics, ridge_metrics, lasso_metrics, gbr_metrics


if __name__ == '__main__':
    all_metrics = train_and_evaluate_regression_models()
    # 可以在这里对 all_metrics 进行比较，并生成 docs/回归模型报告.md 的内容