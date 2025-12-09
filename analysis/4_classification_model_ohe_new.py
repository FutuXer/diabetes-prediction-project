import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    recall_score,  # 引入召回率计算
    precision_score  # 引入精确率计算
)

# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 1. 定义文件路径
TRAIN_DATA_PATH = "data/processed/diabetes_train_normalized.csv"
TEST_DATA_PATH = "data/processed/diabetes_test_normalized.csv"

# V2 New 命名文件
MODEL_SAVE_PATH = "analysis/models/disease_classifier_ohe_new.pkl"
METRICS_REPORT_PATH = "docs/classification_model_report_ohe_new.txt"
ROC_CURVE_PATH = "docs/images/roc_curve_ohe_new.png"
CONF_MATRIX_PATH = "docs/images/confusion_matrix_ohe_new.png"

# 定义要测试的阈值范围
THRESHOLDS_TO_TEST = [0.50, 0.48, 0.45, 0.42, 0.40, 0.35]


def load_data_with_ohe(train_path, test_path, target_col='Outcome'):
    """加载数据，对分类特征进行独热编码 (One-Hot Encoding)"""
    print("--- 1. 加载数据并进行独热编码 ---")
    try:
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)

        CATEGORY_COLS = ['Pregnancies_category', 'BMI_category', 'Age_category']

        # 独热编码处理
        df_train_ohe = pd.get_dummies(df_train, columns=CATEGORY_COLS, drop_first=True)
        df_test_ohe = pd.get_dummies(df_test, columns=CATEGORY_COLS, drop_first=True)

        # 特征对齐
        common_cols = list(set(df_train_ohe.columns) & set(df_test_ohe.columns))
        common_cols.remove(target_col)

        X_train = df_train_ohe[common_cols]
        Y_train = df_train_ohe[target_col]

        X_test = df_test_ohe[common_cols]
        Y_test = df_test_ohe[target_col]

        print(f"独热编码后训练集大小: {X_train.shape[0]}，特征数: {X_train.shape[1]}")
        return X_train, Y_train, X_test, Y_test

    except FileNotFoundError:
        print("错误: 数据文件未找到，请检查路径。")
        return None, None, None, None


def train_and_tune_model(X_train, Y_train):
    """使用GridSearchCV进行超参数调优和模型训练 (与 V2 保持一致)"""
    print("--- 2. 超参数调优和训练 (GridSearchCV) ---")

    log_reg = LogisticRegression(solver='liblinear', random_state=42)
    param_grid = {
        'C': np.logspace(-4, 4, 20),
        'penalty': ['l1', 'l2']
    }

    grid_search = GridSearchCV(log_reg, param_grid, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, Y_train)

    best_model = grid_search.best_estimator_
    print(f"最佳超参数: {grid_search.best_params_}")
    print(f"最佳交叉验证AUC: {grid_search.best_score_:.4f}")

    return best_model, X_train.columns.tolist()


def evaluate_model_with_thresholds(model, X_test, Y_test, feature_names, thresholds):
    """评估模型性能，并迭代测试不同的分类阈值"""
    print("\n--- 3. 模型评估与多阈值测试 ---")

    Y_proba = model.predict_proba(X_test)[:, 1]

    # ----------------------------------------------------
    # ⭐ 多阈值性能统计
    results = []

    for t in thresholds:
        Y_pred_t = (Y_proba >= t).astype(int)

        # 患病类 (1) 的召回率 (我们主要关注的指标)
        recall = recall_score(Y_test, Y_pred_t, pos_label=1)

        # 患病类 (1) 的精确率 (需要权衡的指标)
        precision = precision_score(Y_test, Y_pred_t, pos_label=1, zero_division=0)

        # 混淆矩阵用于计算 FN 和 FP
        conf_mat = confusion_matrix(Y_test, Y_pred_t)
        # FN (假阴性/漏诊) 是混淆矩阵的 (1, 0) 位置
        # FP (假阳性/误诊) 是混淆矩阵的 (0, 1) 位置
        fn = conf_mat[1, 0]
        fp = conf_mat[0, 1]

        results.append({
            'Threshold (T)': f'{t:.2f}',
            'Recall (患病召回率)': f'{recall:.4f}',
            'Precision (患病精确率)': f'{precision:.4f}',
            'FN (漏诊)': fn,
            'FP (误诊)': fp,
            'Accuracy': f'{(Y_pred_t == Y_test).mean():.4f}'
        })

    results_df = pd.DataFrame(results)
    # ----------------------------------------------------

    # --- 保存报告（包含多阈值分析） ---

    # 获取默认阈值 (0.50) 下的完整报告和混淆矩阵
    Y_pred_default = (Y_proba >= 0.50).astype(int)
    auc_score = roc_auc_score(Y_test, Y_proba)
    report_default = classification_report(Y_test, Y_pred_default, target_names=['非患病 (0)', '患病 (1)'])
    conf_mat_default = confusion_matrix(Y_test, Y_pred_default)

    with open(METRICS_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("=== 逻辑回归分类模型评估报告 (OHE + 阈值分析) ===\n\n")
        f.write(f"测试集 AUC 得分 (AUC Score): {auc_score:.4f}\n\n")

        f.write("--- A. 默认阈值 (0.50) 性能 ---\n")
        f.write(f"准确率 (Accuracy): {(Y_pred_default == Y_test).mean():.4f}\n")
        f.write(report_default)
        f.write("混淆矩阵:\n" + str(conf_mat_default) + "\n\n")

        f.write("--- B. 多阈值性能对比 (重点关注召回率) ---\n")
        f.write("目标：提高 Recall (降低 FN)，同时控制 FP 增加。\n")
        f.write(results_df.to_string(index=False))
        f.write("\n\n")

        # 提取特征系数（与 V2 脚本一致）
        coefs = pd.DataFrame({'Feature': feature_names, 'Coefficient': model.coef_[0]})
        coefs['Odds_Ratio'] = np.exp(coefs['Coefficient'])
        coefs = coefs.sort_values(by='Odds_Ratio', ascending=False)
        f.write("--- C. 特征系数 (Coefficient) 与 优势比 (Odds Ratio) ---\n")
        f.write(coefs.to_string(index=False, float_format='%.4f'))

    print(f"评估报告和阈值分析已保存至: {METRICS_REPORT_PATH}")

    # --- 绘制和保存默认阈值下的图表（与 V2 保持一致） ---

    # 混淆矩阵图
    plt.figure(figsize=(6, 5))
    sns.heatmap(conf_mat_default, annot=True, fmt='d', cmap='Blues',
                xticklabels=['非患病', '患病'], yticklabels=['非患病', '患病'])
    plt.title(f'Confusion Matrix (Default Threshold 0.50)')
    plt.ylabel('实际值 (True Label)')
    plt.xlabel('预测值 (Predicted Label)')
    plt.savefig(CONF_MATRIX_PATH)
    plt.close()
    print(f"默认混淆矩阵图表已保存至: {CONF_MATRIX_PATH}")

    # ROC 曲线图 (AUC 不变)
    fpr, tpr, thresholds = roc_curve(Y_test, Y_proba)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f'Logistic Regression (AUC = {auc_score:.4f})')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlabel('假阳性率 (False Positive Rate)')
    plt.ylabel('真阳性率 (True Positive Rate)')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.savefig(ROC_CURVE_PATH)
    plt.close()
    print(f"ROC曲线图表已保存至: {ROC_CURVE_PATH}")


def save_model(model, path):
    """保存训练好的模型"""
    print("--- 4. 保存模型 ---")
    joblib.dump(model, path)
    print(f"模型已保存至: {path}")


# 主执行函数
if __name__ == "__main__":
    X_train, Y_train, X_test, Y_test = load_data_with_ohe(TRAIN_DATA_PATH, TEST_DATA_PATH)

    if X_train is not None:
        best_log_reg_model, feature_names = train_and_tune_model(X_train, Y_train)

        # 调用新的评估函数
        evaluate_model_with_thresholds(best_log_reg_model, X_test, Y_test, feature_names, THRESHOLDS_TO_TEST)

        # 保存模型（注意：我们保存的模型是未调整阈值的，阈值调整在前端应用时实现）
        save_model(best_log_reg_model, MODEL_SAVE_PATH)