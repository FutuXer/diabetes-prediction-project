import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from sklearn.naive_bayes import GaussianNB  # 使用 GaussianNB 适用于连续型数据
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    roc_curve,
    confusion_matrix
)
from sklearn.model_selection import GridSearchCV

# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 1. 定义文件路径
TRAIN_DATA_PATH = "data/processed/diabetes_train_normalized.csv"
TEST_DATA_PATH = "data/processed/diabetes_test_normalized.csv"

# NB 实验新命名文件
MODEL_SAVE_PATH = "analysis/models/disease_classifier_nb.pkl"
METRICS_REPORT_PATH = "docs/classification_model_report_nb.txt"
ROC_CURVE_PATH = "docs/images/roc_curve_nb.png"
CONF_MATRIX_PATH = "docs/images/confusion_matrix_nb.png"


def load_data_with_ohe(train_path, test_path, target_col='Outcome'):
    """加载数据，对分类特征进行独热编码 (One-Hot Encoding)"""
    # 此函数与 V2 脚本中的一致
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


def train_nb_model(X_train, Y_train):
    """训练高斯朴素贝叶斯模型"""
    print("--- 2. 训练朴素贝叶斯模型 ---")

    # GaussianNB 默认没有需要调整的超参数，直接实例化并训练
    # var_smoothing 是唯一可选的参数，用于稳定性
    nb_model = GaussianNB()

    # 也可以使用 GridSearchCV 来调优 var_smoothing，但通常直接训练即可
    # param_grid = {'var_smoothing': np.logspace(0,-9, num=100)}
    # grid_search = GridSearchCV(nb_model, param_grid, cv=5, scoring='roc_auc', n_jobs=-1, verbose=0)
    # grid_search.fit(X_train, Y_train)
    # best_model = grid_search.best_estimator_
    # print(f"最佳 var_smoothing: {grid_search.best_params_}")

    nb_model.fit(X_train, Y_train)

    print("朴素贝叶斯模型训练完成。")
    return nb_model, X_train.columns.tolist()


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
        f.write("=== 朴素贝叶斯 (GaussianNB) 分类模型评估报告 (包含OHE特征) ===\n\n")
        f.write(f"测试集准确率 (Accuracy): {accuracy:.4f}\n")
        f.write(f"测试集AUC得分 (AUC Score): {auc:.4f}\n\n")
        f.write("--- 分类报告 (Classification Report) ---\n")
        f.write(report)
        f.write("\n--- 混淆矩阵 (Confusion Matrix) ---\n")
        f.write(str(conf_mat) + "\n\n")

        # 朴素贝叶斯没有直接的“系数”或“特征重要性”
        f.write("--- 特征重要性说明 ---\n")
        f.write("朴素贝叶斯模型不提供直接的特征系数，其重要性基于特征的概率分布。\n")

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
    plt.plot(fpr, tpr, label=f'Gaussian Naive Bayes (AUC = {auc:.4f})')
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
        best_nb_model, feature_names = train_nb_model(X_train, Y_train)

        evaluate_model(best_nb_model, X_test, Y_test, feature_names)

        save_model(best_nb_model, MODEL_SAVE_PATH)