import pandas as pd
import numpy as np
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    roc_curve,
    confusion_matrix
)
from matplotlib import rcParams
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 1. 定义文件路径
# 注意：请确保这些路径与您的实际项目结构一致
TRAIN_DATA_PATH = "data/processed/diabetes_train_normalized.csv"
TEST_DATA_PATH = "data/processed/diabetes_test_normalized.csv"
MODEL_SAVE_PATH = "analysis/models/disease_classifier.pkl"
METRICS_REPORT_PATH = "docs/classification_model_report.txt"
ROC_CURVE_PATH = "docs/images/roc_curve.png"
CONF_MATRIX_PATH = "docs/images/confusion_matrix.png"

def load_data(train_path, test_path, target_col='Outcome'):
    """加载并划分数据集为特征X和目标Y"""
    print("--- 1. 加载数据 ---")
    try:
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)

        # 确定需要排除的非数值列 (基于您的数据示例)
        EXCLUDED_COLS = [
            target_col,
            'Pregnancies_category',
            'BMI_category',
            'Age_category'
        ]

        # 划分特征和目标变量，并排除非数值特征
        X_train = df_train.drop(columns=EXCLUDED_COLS, errors='ignore')
        Y_train = df_train[target_col]
        X_test = df_test.drop(columns=EXCLUDED_COLS, errors='ignore')
        Y_test = df_test[target_col]

        # 检查 X_train 中的数据类型，确保所有列都是 float64 或 int64
        # print("检查 X_train 数据类型:\n", X_train.dtypes)

        print(f"训练集大小: {X_train.shape[0]}，特征数: {X_train.shape[1]}")
        print("已成功排除分类特征并加载数值数据。")
        return X_train, Y_train, X_test, Y_test
    except FileNotFoundError:
        print("错误: 数据文件未找到，请检查路径。")
        return None, None, None, None

def train_and_tune_model(X_train, Y_train):
    """使用GridSearchCV进行超参数调优和模型训练"""
    print("--- 2. 超参数调优和训练 (GridSearchCV) ---")

    # 定义逻辑回归模型和待优化的参数空间
    log_reg = LogisticRegression(solver='liblinear', random_state=42)
    # 优化正则化参数 C (C越小，正则化越强)
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
        f.write("=== 逻辑回归分类模型评估报告 ===\n\n")
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


def save_model(model, path):
    """保存训练好的模型"""
    print("--- 4. 保存模型 ---")
    joblib.dump(model, path)
    print(f"模型已保存至: {path}")


# 主执行函数
if __name__ == "__main__":
    X_train, Y_train, X_test, Y_test = load_data(TRAIN_DATA_PATH, TEST_DATA_PATH)

    if X_train is not None:
        best_log_reg_model, feature_names = train_and_tune_model(X_train, Y_train)

        evaluate_model(best_log_reg_model, X_test, Y_test, feature_names)

        save_model(best_log_reg_model, MODEL_SAVE_PATH)