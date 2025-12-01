import pandas as pd
from sklearn.model_selection import train_test_split
import os

# -------------------------
# 读取数据
# -------------------------
base_dir = os.path.dirname(os.path.dirname(__file__))
input_csv = os.path.join(base_dir, "data", "processed", "diabetes_eliminate_outlier.csv")
df = pd.read_csv(input_csv)

# -------------------------
# 分割训练集和测试集（80/20），分层采样
# -------------------------
train_df, test_df = train_test_split(
    df,
    test_size=0.2,           # 测试集占20%
    random_state=42,         # 保证可复现
    stratify=df['Outcome']   # 按 Outcome 列分层
)

# -------------------------
# 保存结果
# -------------------------
train_csv = os.path.join(base_dir, "data", "processed", "diabetes_train.csv")
test_csv = os.path.join(base_dir, "data", "processed", "diabetes_test.csv")
train_df.to_csv(train_csv, index=False)
test_df.to_csv(test_csv, index=False)

# -------------------------
# 打印检查
# -------------------------
print("训练集 Outcome 分布：")
print(train_df['Outcome'].value_counts(), "\n")
print("测试集 Outcome 分布：")
print(test_df['Outcome'].value_counts())
