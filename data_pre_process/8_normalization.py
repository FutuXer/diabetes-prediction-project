import pandas as pd
import os

base_dir = os.path.dirname(os.path.dirname(__file__))

# -------------------------
# 1. 读取训练集和测试集
# -------------------------
train_path = os.path.join(base_dir, "data", "processed", "diabetes_train.csv")
test_path = os.path.join(base_dir, "data", "processed", "diabetes_test.csv")

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

print(f"训练集形状: {train_df.shape}")
print(f"测试集形状: {test_df.shape}")

# -------------------------
# 2. 确定列类型
# -------------------------
numeric_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

non_numeric_cols = ['Outcome', 'Pregnancies_category', 'BMI_category', 'Age_category']

print(f"\n数值列: {numeric_cols}")
print(f"非数值列: {non_numeric_cols}")

# -------------------------
# 3. 用训练集计算均值和标准差
# -------------------------
print("\n" + "=" * 60)
print("使用训练集计算归一化参数")
print("=" * 60)

scaler_params = {}
for col in numeric_cols:
    if col in train_df.columns:
        mean = train_df[col].mean()
        std = train_df[col].std()
        scaler_params[col] = {'mean': mean, 'std': std}

        print(f"{col}: 均值 = {mean:.4f}, 标准差 = {std:.4f}")

# -------------------------
# 4. 用训练集参数归一化训练集
# -------------------------
train_normalized = train_df.copy()

for col in numeric_cols:
    if col in scaler_params:
        params = scaler_params[col]
        train_normalized[col] = (train_df[col] - params['mean']) / params['std']

print("\n" + "=" * 60)
print("训练集归一化结果验证")
print("=" * 60)

for col in numeric_cols:
    if col in train_normalized.columns:
        print(f"{col}: 均值 = {train_normalized[col].mean():.6f}, 标准差 = {train_normalized[col].std():.6f}")

# -------------------------
# 5. 用训练集参数归一化测试集（重要！）
# -------------------------
test_normalized = test_df.copy()

for col in numeric_cols:
    if col in scaler_params:
        params = scaler_params[col]
        test_normalized[col] = (test_df[col] - params['mean']) / params['std']

print("\n" + "=" * 60)
print("测试集归一化结果（用训练集参数）")
print("=" * 60)

for col in numeric_cols:
    if col in test_normalized.columns:
        mean_val = test_normalized[col].mean()
        std_val = test_normalized[col].std()
        print(f"{col}: 均值 = {mean_val:.6f}, 标准差 = {std_val:.6f}")

# -------------------------
# 6. 保存归一化的数据集
# -------------------------
train_output = os.path.join(base_dir, "data", "processed", "diabetes_train_normalized.csv")
test_output = os.path.join(base_dir, "data", "processed", "diabetes_test_normalized.csv")

train_normalized.to_csv(train_output, index=False, encoding='utf-8')
test_normalized.to_csv(test_output, index=False, encoding='utf-8')

print(f"\n归一化后的训练集保存到: {train_output}")
print(f"归一化后的测试集保存到: {test_output}")

# -------------------------
# 7. 显示对比
# -------------------------
print("\n" + "=" * 60)
print("前3行对比")
print("=" * 60)

print("\n训练集原始 vs 归一化:")
print("原始:")
print(train_df[numeric_cols[:3] + ['Outcome']].head(3))
print("\n归一化:")
print(train_normalized[numeric_cols[:3] + ['Outcome']].head(3))

print("\n测试集原始 vs 归一化:")
print("原始:")
print(test_df[numeric_cols[:3] + ['Outcome']].head(3))
print("\n归一化:")
print(test_normalized[numeric_cols[:3] + ['Outcome']].head(3))

print("\n" + "=" * 60)
print("重要说明:")
print("=" * 60)
print("1. 训练集归一化后均值为0，标准差为1（理论上）")
print("2. 测试集用训练集参数归一化，均值不为0，标准差不为1（这是正确的！）")
print("3. 这样避免了数据泄露，更符合真实场景")