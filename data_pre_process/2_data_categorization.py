import pandas as pd
import os

# -------------------------
#   加载原始数据
# -------------------------
base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "raw", "diabetes.csv")

print(f"正在加载数据集：{csv_path}")
df = pd.read_csv(csv_path)

print(f"原始数据形状：{df.shape}")
print(f"原始数据列：{list(df.columns)}")

# -------------------------
#   定义分类函数
# -------------------------
def categorize_pregnancies(x):
    """怀孕次数分类"""
    if x == 0:
        return "0次"
    elif 1 <= x <= 3:
        return "1-3次"
    elif 4 <= x <= 7:
        return "4-7次"
    else:  # x >= 8
        return "≥8次"

def categorize_bmi(x):
    """BMI分类"""
    if x < 27:
        return "<27"
    elif 27 <= x < 32:
        return "27-32"
    elif 32 <= x < 37:
        return "32-37"
    else:  # x >= 37
        return "≥37"

def categorize_age(x):
    """年龄分类"""
    if x < 20:
        return "<20岁"
    elif 20 <= x < 30:
        return "20-30岁"
    elif 30 <= x < 40:
        return "30-40岁"
    else:  # x >= 40
        return "≥40岁"

# -------------------------
#   添加分类列
# -------------------------
print("\n正在添加分类列...")

df['Pregnancies_category'] = df['Pregnancies'].apply(categorize_pregnancies)
df['BMI_category'] = df['BMI'].apply(categorize_bmi)
df['Age_category'] = df['Age'].apply(categorize_age)

print(f"添加后数据形状：{df.shape}")
print(f"添加后数据列：{list(df.columns)}")

# -------------------------
#   保存处理后的数据
# -------------------------
output_path = os.path.join(base_dir, "data", "processed", "diabetes_with_categories.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

df.to_csv(output_path, index=False, encoding='utf-8')

print(f"\n数据已保存到：{output_path}")

# -------------------------
#   显示前几行
# -------------------------
print("\n处理后的数据前5行：")
print(df[['Pregnancies', 'Pregnancies_category',
          'BMI', 'BMI_category',
          'Age', 'Age_category',
          'Outcome']].head())

# -------------------------
#   简单的分组统计（可选）
# -------------------------
print("\n" + "="*60)
print("简单分组统计")
print("="*60)

total = len(df)

# 1. 怀孕次数分组
print("\n1. 怀孕次数分组:")
print("-"*40)
preg_counts = df['Pregnancies_category'].value_counts()
for category, count in preg_counts.items():
    percentage = (count / total) * 100
    print(f"  {category:<10} {count:>4}人 ({percentage:>5.1f}%)")

# 2. BMI分组
print("\n2. BMI分组:")
print("-"*40)
bmi_counts = df['BMI_category'].value_counts()
for category, count in bmi_counts.items():
    percentage = (count / total) * 100
    print(f"  {category:<10} {count:>4}人 ({percentage:>5.1f}%)")

# 3. 年龄分组
print("\n3. 年龄分组:")
print("-"*40)
age_counts = df['Age_category'].value_counts()
for category, count in age_counts.items():
    percentage = (count / total) * 100
    print(f"  {category:<10} {count:>4}人 ({percentage:>5.1f}%)")

print(f"\n总计: {total} 人")
print("="*60)

print("\n处理完成！")