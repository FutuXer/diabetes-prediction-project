import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import json
from scipy import stats  # 用于计算 p-value


def outcome_to_risk_score(probabilities):
    return probabilities * 100


def perform_statistical_tests(X, y_true, y_pred, model):
    """
    手动计算 F 检验和各参数的 t 检验
    """
    n, p = X.shape  # 样本数, 特征数
    # 如果特征不包含截距项，需要手动加 1
    df_model = p
    df_resid = n - p - 1

    # 1. 计算基本项
    residuals = y_true - y_pred
    rss = np.sum(residuals ** 2)  # 残差平方和
    tss = np.sum((y_true - np.mean(y_true)) ** 2)  # 总平方和
    ess = tss - rss  # 回归平方和 (Explained SS)

    # 2. 整体 F 检验 (H0: 所有系数均为0)
    ms_model = ess / df_model
    ms_resid = rss / df_resid
    f_stat = ms_model / ms_resid
    f_p_value = 1 - stats.f.cdf(f_stat, df_model, df_resid)

    # 3. 各参数 t 检验
    # 注意：岭回归由于引入了 alpha，其标准差估计比 OLS 复杂。
    # 这里采用线性回归的近似估计（如果 alpha 较小，结果依然具有参考价值）
    X_with_intercept = np.hstack([np.ones((n, 1)), X])
    # 估计方差 sigma^2
    sigma_squared = rss / df_resid
    # 协方差矩阵 C = sigma^2 * (X'X)^-1
    # 对于岭回归，严格意义上应为 (X'X + alpha*I)^-1 * X'X * (X'X + alpha*I)^-1
    var_beta = sigma_squared * np.linalg.inv(X_with_intercept.T @ X_with_intercept)
    std_err = np.sqrt(np.diag(var_beta))

    # 合并系数 (intercept + coefficients)
    params = np.append(model.intercept_, model.coef_)
    t_stats = params / std_err
    p_values = [2 * (1 - stats.t.cdf(np.abs(t), df_resid)) for t in t_stats]

    return f_stat, f_p_value, std_err, t_stats, p_values


def test_ridge_with_stats():
    print("--- 1. 加载模型和测试数据 ---")
    TEST_DATA_PATH = '../data/processed/diabetes_test_normalized.csv'
    MODEL_PATH = 'models/risk_score_ridge_model.pkl'

    test_data = pd.read_csv(TEST_DATA_PATH)
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    OPTIMIZED_FEATURES = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI',
                          'DiabetesPedigreeFunction', 'Age']
    X_test = test_data[OPTIMIZED_FEATURES]
    y_risk_true = outcome_to_risk_score(test_data['Outcome'])
    y_risk_pred = model.predict(X_test)

    # --- 2. 统计检验 ---
    f_stat, f_p, std_err, t_stats, p_vals = perform_statistical_tests(X_test.values, y_risk_true.values, y_risk_pred,
                                                                      model)

    print("\n" + "=" * 50)
    print(f"{'模型整体 F 检验':^50}")
    print("-" * 50)
    print(f"F-statistic: {f_stat:.4f}")
    print(f"P-value:     {f_p:.4e} ({'显著' if f_p < 0.05 else '不显著'})")

    print("\n" + "=" * 50)
    print(f"{'参数显著性检验 (t-test)':^50}")
    print("-" * 50)
    feature_names = ['Intercept'] + OPTIMIZED_FEATURES
    results = []
    for i, name in enumerate(feature_names):
        results.append({
            'Feature': name,
            'Coeff': round(np.append(model.intercept_, model.coef_)[i], 4),
            'Std.Err': round(std_err[i], 4),
            't-stat': round(t_stats[i], 4),
            'P>|t|': f"{p_vals[i]:.4f}"
        })

    df_res = pd.DataFrame(results)
    print(df_res.to_string(index=False))
    print("=" * 50)


if __name__ == '__main__':
    test_ridge_with_stats()