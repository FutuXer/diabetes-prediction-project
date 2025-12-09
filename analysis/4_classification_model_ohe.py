import pandas as pd
import numpy as np
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    roc_curve,
    confusion_matrix
)

# 解决中文乱码问题 (如果需要)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 1. 定义新的文件路径
TRAIN_DATA_PATH = "data/processed/diabetes_train_normalized.csv"
TEST_DATA_PATH = "data/processed/diabetes_test_normalized.csv"

# V2 新命名文件
MODEL_SAVE_PATH = "analysis/models/disease_classifier_ohe.pkl"
METRICS_REPORT_PATH = "docs/classification_model_report_ohe.txt"
ROC_CURVE_PATH = "docs/images/roc_curve_ohe.png"
CONF_MATRIX_PATH = "docs/images/confusion_matrix_ohe.png"


def load_data_with_ohe(train_path, test_path, target_col='Outcome'):
    """加载数据，对分类特征进行独热编码 (One-Hot Encoding)"""
    print("--- 1. 加载数据并进行独热编码 ---")
    try:
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)

        # 确定需要进行独热编码的列
        CATEGORY_COLS = ['Pregnancies_category', 'BMI_category', 'Age_category']

        # --- 独热编码处理 ---
        # 1. 对训练集进行独热编码
        df_train_ohe = pd.get_dummies(df_train, columns=CATEGORY_COLS, drop_first=True)
        # 2. 对测试集进行独热编码
        df_test_ohe = pd.get_dummies(df_test, columns=CATEGORY_COLS, drop_first=True)

        # 为了保证训练集和测试集的特征列完全一致，需要重新对齐列
        # 获取所有列名（包括原始数值特征和新的OHE特征）
        common_cols = list(set(df_train_ohe.columns) & set(df_test_ohe.columns))
        common_cols.remove(target_col)  # 排除目标列

        X_train = df_train_ohe[common_cols]
        Y_train = df_train_ohe[target_col]

        X_test = df_test_ohe[common_cols]
        Y_test = df_test_ohe[target_col]

        print(f"独热编码后训练集大小: {X_train.shape[0]}，特征数: {X_train.shape[1]}")
        print("已成功加载数据并完成独热编码。")
        return X_train, Y_train, X_test, Y_test

    except FileNotFoundError:
        print("错误: 数据文件未找到，请检查路径。")
        return None, None, None, None


# 保持 train_and_tune_model 函数不变
def train_and_tune_model(X_train, Y_train):
    """使用GridSearchCV进行超参数调优和模型训练"""
    print("--- 2. 超参数调优和训练 (GridSearchCV) ---")

    # 定义逻辑回归模型和待优化的参数空间
    log_reg = LogisticRegression(solver='liblinear', random_state=42)
    param_grid = {
        'C': np.logspace(-4, 4, 20),
        'penalty': ['l1', 'l2']
    }

    # 使用网格搜索进行5折交叉验证 (cv=5)
    grid_search = GridSearchCV(log_reg, param_grid, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, Y_train)

    best_model = grid_search.best_estimator_
    print(f"最佳超参数: {grid_search.best_params_}")
    print(f"最佳交叉验证AUC: {grid_search.best_score_:.4f}")

    return best_model, X_train.columns.tolist()


# 保持 evaluate_model 函数不变
def evaluate_model(model, X_test, Y_test, feature_names):
    """评估模型性能，并生成报告和图表"""
    print("--- 3. 模型评估与报告生成 ---")

    Y_pred = model.predict(X_test)
    Y_proba = model.predict_proba(X_test)[:, 1]

    # 计算关键指标
    accuracy = model.score(X_test, Y_test)
    auc = roc_auc_score(Y_test, Y_proba)
    report = classification_report(Y_test, Y_pred, target_names=['非患病 (0)', '患病 (1)'])
    conf_mat = confusion_matrix(Y_test, Y_pred)

    # 打印和保存报告
    with open(METRICS_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("=== 逻辑回归分类模型评估报告 (包含OHE特征) ===\n\n")
        f.write(f"测试集准确率 (Accuracy): {accuracy:.4f}\n")
        f.write(f"测试集AUC得分 (AUC Score): {auc:.4f}\n\n")
        f.write("--- 分类报告 (Classification Report) ---\n")
        f.write(report)
        f.write("\n--- 混淆矩阵 (Confusion Matrix) ---\n")
        f.write(str(conf_mat) + "\n\n")

        # 提取特征系数（作为特征重要性）
        coefs = pd.DataFrame({'Feature': feature_names, 'Coefficient': model.coef_[0]})
        coefs['Odds_Ratio'] = np.exp(coefs['Coefficient'])
        coefs = coefs.sort_values(by='Odds_Ratio', ascending=False)
        f.write("--- 特征系数 (Coefficient) 与 优势比 (Odds Ratio) ---\n")
        f.write(coefs.to_string(index=False, float_format='%.4f'))

    print(f"评估报告已保存至: {METRICS_REPORT_PATH}")

    # 绘制和保存混淆矩阵
    plt.figure(figsize=(6, 5))
    sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues',
                xticklabels=['非患病', '患病'], yticklabels=['非患病', '患病'])
    plt.title('Confusion Matrix')
    plt.ylabel('实际值 (True Label)')
    plt.xlabel('预测值 (Predicted Label)')
    plt.savefig(CONF_MATRIX_PATH)
    plt.close()
    print(f"混淆矩阵图表已保存至: {CONF_MATRIX_PATH}")

    # 绘制和保存ROC曲线
    fpr, tpr, thresholds = roc_curve(Y_test, Y_proba)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f'Logistic Regression (AUC = {auc:.4f})')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlabel('假阳性率 (False Positive Rate)')
    plt.ylabel('真阳性率 (True Positive Rate)')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.savefig(ROC_CURVE_PATH)
    plt.close()
    print(f"ROC曲线图表已保存至: {ROC_CURVE_PATH}")


# ... 保持 evaluate_model 结束

# 保持 save_model 函数不变
def save_model(model, path):
    """保存训练好的模型"""
    print("--- 4. 保存模型 ---")
    joblib.dump(model, path)
    print(f"模型已保存至: {path}")


# 主执行函数：注意这里调用了新的 load_data_with_ohe 函数
if __name__ == "__main__":
    X_train, Y_train, X_test, Y_test = load_data_with_ohe(TRAIN_DATA_PATH, TEST_DATA_PATH)

    if X_train is not None:
        best_log_reg_model, feature_names = train_and_tune_model(X_train, Y_train)

        evaluate_model(best_log_reg_model, X_test, Y_test, feature_names)

        save_model(best_log_reg_model, MODEL_SAVE_PATH)