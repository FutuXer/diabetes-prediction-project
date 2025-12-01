import pandas as pd
import numpy as np
import os

# -------------------------
#   加载数据
# -------------------------
base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "processed", "diabetes_with_categories.csv")

print(f"正在加载数据集：{csv_path}")
df = pd.read_csv(csv_path)

print(f"数据形状：{df.shape}")
print(f"数据列：{list(df.columns)}")

# -------------------------
#   定义需要处理的列
# -------------------------
# 这些列中的0值应该被视为缺失（医学上不可能为0）
zero_to_fill_cols = [
    'Glucose',  # 血糖
    'BloodPressure',  # 血压
    'SkinThickness',  # 皮肤厚度
    'BMI',  # BMI
    'Insulin'  # 胰岛素
]

# -------------------------
#   统计原始0值数量
# -------------------------
print("\n原始数据0值统计：")
print("-" * 50)

zero_counts_before = {}
for col in zero_to_fill_cols:
    zero_count = (df[col] == 0).sum()
    zero_counts_before[col] = zero_count
    percentage = (zero_count / len(df)) * 100
    print(f"{col:<20} {zero_count:>4}个0值 ({percentage:>5.1f}%)")

# -------------------------
#   按年龄分组计算中位数
# -------------------------
print("\n按年龄组计算中位数：")
print("-" * 50)

# 获取所有唯一的年龄组
age_groups = df['Age_category'].unique()
print(f"年龄组：{list(age_groups)}")

# 为每个年龄组计算各列的中位数（排除0值）
age_group_medians = {}

for age_group in age_groups:
    # 筛选该年龄组的数据（排除0值）
    age_mask = df['Age_category'] == age_group
    age_group_data = df[age_mask]

    medians = {}
    for col in zero_to_fill_cols:
        # 只计算非0值的中位数
        non_zero_values = age_group_data[col][age_group_data[col] > 0]
        if len(non_zero_values) > 0:
            medians[col] = non_zero_values.median()
        else:
            # 如果该年龄组所有值都是0，则使用全局中位数
            medians[col] = df[col][df[col] > 0].median()

    age_group_medians[age_group] = medians

    # 打印该年龄组的中位数
    print(f"\n{age_group}:")
    for col, median_val in medians.items():
        print(f"  {col:<20} 中位数: {median_val:.2f}")

# -------------------------
#   填充0值
# -------------------------
print("\n开始填充0值...")
print("-" * 50)

# 创建数据副本
df_filled = df.copy()
filled_counts = {}

for col in zero_to_fill_cols:
    filled_count = 0
    # 找出该列为0的行
    zero_mask = df_filled[col] == 0

    for idx in df_filled[zero_mask].index:
        age_group = df_filled.loc[idx, 'Age_category']
        median_val = age_group_medians[age_group][col]

        # 填充中位数
        df_filled.loc[idx, col] = median_val
        filled_count += 1

    filled_counts[col] = filled_count
    print(f"{col:<20} 填充了 {filled_count:>4} 个0值")

# -------------------------
#   验证填充结果
# -------------------------
print("\n填充后验证：")
print("-" * 50)

for col in zero_to_fill_cols:
    zero_after = (df_filled[col] == 0).sum()
    zero_before = zero_counts_before[col]
    filled_count = filled_counts[col]

    print(f"{col:<20} 填充前: {zero_before:>4}个0值 | 填充后: {zero_after:>4}个0值 | 已填充: {filled_count:>4}个")

# -------------------------
#   统计描述性变化
# -------------------------
print("\n填充前后统计对比：")
print("-" * 50)

for col in zero_to_fill_cols:
    print(f"\n{col}:")
    print(f"  填充前 - 平均值: {df[col].mean():.2f}, 中位数: {df[col].median():.2f}")
    print(f"  填充后 - 平均值: {df_filled[col].mean():.2f}, 中位数: {df_filled[col].median():.2f}")

    # 计算变化百分比
    mean_change = ((df_filled[col].mean() - df[col].mean()) / df[col].mean()) * 100
    print(f"  平均值变化: {mean_change:+.1f}%")

# -------------------------
#   保存填充后的数据
# -------------------------
output_path = os.path.join(base_dir, "data", "processed", "diabetes_filled_by_age.csv")
df_filled.to_csv(output_path, index=False, encoding='utf-8')

print(f"\n填充后的数据已保存到：{output_path}")

# -------------------------
#   创建详细报告
# -------------------------
report_path = os.path.join(base_dir, "data_pre_process", "zero_filling_report.txt")

with open(report_path, "w", encoding="utf-8") as f:
    f.write("0值填充报告（按年龄组中位数填充）\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"原始数据行数: {len(df)}\n")
    f.write(f"填充时间: {pd.Timestamp.now()}\n\n")

    f.write("处理的列:\n")
    for col in zero_to_fill_cols:
        f.write(f"  - {col}\n")
    f.write("\n")

    f.write("各年龄组中位数:\n")
    f.write("-" * 40 + "\n")
    for age_group, medians in age_group_medians.items():
        f.write(f"\n{age_group}:\n")
        for col, median_val in medians.items():
            f.write(f"  {col:<20} {median_val:.2f}\n")

    f.write("\n填充统计:\n")
    f.write("-" * 40 + "\n")
    f.write(f"{'列名':<20} {'填充前0值':>10} {'填充数':>10} {'填充后0值':>10}\n")
    f.write("-" * 60 + "\n")

    for col in zero_to_fill_cols:
        f.write(f"{col:<20} {zero_counts_before[col]:>10} {filled_counts[col]:>10} {(df_filled[col] == 0).sum():>10}\n")

    f.write("\n保存文件: diabetes_filled_by_age.csv\n")

print(f"\n详细报告已保存到：{report_path}")

# -------------------------
#   显示填充示例
# -------------------------
print("\n" + "=" * 60)
print("填充示例（前10个被填充的记录）:")
print("=" * 60)

# 找出被修改的记录
modified_records = []
for col in zero_to_fill_cols:
    zero_indices = df[df[col] == 0].index
    for idx in zero_indices[:2]:  # 每列显示2个示例
        if idx not in [r[0] for r in modified_records]:
            original_val = df.loc[idx, col]
            filled_val = df_filled.loc[idx, col]
            age_group = df.loc[idx, 'Age_category']
            modified_records.append((idx, col, original_val, filled_val, age_group))

# 显示示例
print(f"\n{'行号':<6} {'列名':<15} {'原始值':<10} {'填充值':<10} {'年龄组':<10}")
print("-" * 50)
for idx, col, original, filled, age_group in modified_records[:10]:
    print(f"{idx:<6} {col:<15} {original:<10} {filled:<10.2f} {age_group:<10}")

print("\n填充完成！")