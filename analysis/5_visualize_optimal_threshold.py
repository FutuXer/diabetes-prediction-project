import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
import os

# =================================================================
# ⭐⭐⭐ 配置区 ⭐⭐⭐
# =================================================================

TEST_DATA_PATH = "data/processed/diabetes_test_normalized.csv"
MODEL_PATH = "analysis/models/disease_classifier_ohe_new.pkl"

BEST_THRESHOLD = 0.45

ROC_CURVE_PATH = "docs/images/roc_curve_ohe_new.png"
CONF_MATRIX_PATH = "docs/images/confusion_matrix_ohe_new.png"

# 关键：定义分类列，必须与训练脚本中的 load_data_with_ohe 函数保持一致
CATEGORY_COLS = ['Pregnancies_category', 'BMI_category', 'Age_category']

# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def load_model_and_data(model_path, data_path):
    """
    加载模型和测试数据，并执行与训练时完全一致的 OHE 和特征对齐。
    """
    try:
        if not os.path.exists(model_path) or not os.path.exists(data_path):
            print("错误：模型文件或测试数据文件未找到。请检查路径。")
            return None, None, None

        # 1. 加载模型
        model = joblib.load(model_path)

        # 2. 加载测试数据 (包含已标准化的数值特征和原始分类特征)
        df_test = pd.read_csv(data_path)
        target_col = 'Outcome'

        # 3. 执行 OHE (关键修复点：使用 drop_first=True，与训练脚本保持一致)
        df_test_ohe = pd.get_dummies(df_test, columns=CATEGORY_COLS, drop_first=True)

        # 4. 准备 Y_test
        Y_test = df_test_ohe[target_col]

        # 5. 准备 X_test
        X_test_base = df_test_ohe.drop(columns=[target_col])

        # 6. 特征对齐和排序 (解决 KeyError 的核心)
        if hasattr(model, 'feature_names_in_'):
            feature_names = model.feature_names_in_

            # 确保 X_test 包含模型期望的所有特征（处理训练集有而测试集没有的 OHE 列）
            for col in feature_names:
                if col not in X_test_base.columns:
                    X_test_base[col] = 0  # 缺失的 OHE 列赋值 0

            # 严格按照模型期望的顺序和列名进行选择
            X_test = X_test_base[feature_names]
        else:
            print("错误：模型中缺少 feature_names_in_ 属性，无法进行特征对齐。")
            return None, None, None

        print(f"✅ 测试集特征数对齐成功: {X_test.shape[1]}")
        return model, X_test, Y_test

    except Exception as e:
        print(f"加载过程中发生错误: {e}")
        return None, None, None


def plot_and_save_visualizations(model, X_test, Y_test, best_t):
    """使用最佳阈值绘制混淆矩阵，并绘制ROC曲线"""

    Y_proba = model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(Y_test, Y_proba)

    print(f"--- 模型性能 (AUC): {auc_score:.4f} ---")

    # -----------------------------------------------
    # 1. 绘制最佳阈值下的混淆矩阵 (T=0.45)
    # -----------------------------------------------
    Y_pred_best = (Y_proba >= best_t).astype(int)
    conf_mat_best = confusion_matrix(Y_test, Y_pred_best)

    # 混淆矩阵图
    plt.figure(figsize=(6, 5))
    sns.heatmap(conf_mat_best, annot=True, fmt='d', cmap='Blues',
                xticklabels=['非患病 (0)', '患病 (1)'], yticklabels=['非患病 (0)', '患病 (1)'])
    plt.title(f'Confusion Matrix (Optimal Threshold {best_t:.2f})')
    plt.ylabel('实际值 (True Label)')
    plt.xlabel('预测值 (Predicted Label)')
    plt.savefig(CONF_MATRIX_PATH)
    plt.close()
    print(f"✅ 混淆矩阵图表已更新至: {CONF_MATRIX_PATH} (阈值: {best_t:.2f})")

    # 2. 绘制 ROC 曲线
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
    print(f"✅ ROC曲线图表已更新至: {ROC_CURVE_PATH}")


if __name__ == "__main__":
    print("--- 启动模型可视化脚本 ---")
    model, X_test, Y_test = load_model_and_data(MODEL_PATH, TEST_DATA_PATH)

    if model is not None and X_test is not None and Y_test is not None:
        plot_and_save_visualizations(model, X_test, Y_test, BEST_THRESHOLD)
    else:
        print("脚本执行失败，请检查文件路径和数据完整性。")