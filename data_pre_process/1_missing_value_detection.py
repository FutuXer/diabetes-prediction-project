import pandas as pd
import numpy as np
import os

# -------------------------
#   构建 CSV 文件路径（自动定位项目根目录）
# -------------------------
base_dir = os.path.dirname(os.path.dirname(__file__))  # 返回项目根目录
csv_path = os.path.join(base_dir, "data", "raw", "diabetes.csv")

print(f"正在加载数据集：{csv_path}\n")

# 读取 CSV 文件
df = pd.read_csv(csv_path)

# -------------------------
#   定义需要将0视为缺失值的列
# -------------------------
# 这些列的0值在生理学上不可能，应视为缺失值
zero_as_missing_cols = [
    'Glucose',  # 血糖为0意味着死亡
    'BloodPressure',  # 血压为0不可能
    'SkinThickness',  # 皮肤厚度为0不可能
    'BMI',  # BMI为0不可能
    'Insulin'  # 胰岛素为0可能，但通常表示未测量
]

# 注意：
# - Pregnancies：可以为0（未怀孕）
# - Age：年龄不能为0，但数据集中应该没有
# - DiabetesPedigreeFunction：遗传函数可以为0
# - Outcome：0表示无糖尿病，是正常标签值

# -------------------------
#   创建数据副本用于统计
# -------------------------
df_with_zeros_as_missing = df.copy()

# 将指定列的0值替换为NaN（视为缺失）
for col in zero_as_missing_cols:
    # 统计原始0值数量
    zero_count = (df[col] == 0).sum()
    zero_ratio = (zero_count / len(df)) * 100

    print(f"{col:25} 原始0值数量：{zero_count:3} （占比：{zero_ratio:6.2f}%）")

    # 将0替换为NaN
    df_with_zeros_as_missing[col] = df[col].replace(0, np.nan)

# -------------------------
#   计算缺失值统计（包含0值视为缺失）
# -------------------------
print("\n" + "=" * 80)
print("缺失值统计（包含0值视为缺失）")
print("=" * 80)

# 统计传统缺失值（原始的NaN）
true_missing_count = df.isnull().sum()
true_missing_ratio = (true_missing_count / len(df)) * 100

# 统计包含0值视为缺失的情况
total_missing_count = df_with_zeros_as_missing.isnull().sum()
total_missing_ratio = (total_missing_count / len(df)) * 100

# 计算由0值转为缺失的数量
zero_based_missing = total_missing_count - true_missing_count

# -------------------------
#   构建详细的报告内容
# -------------------------
report_lines = []
report_lines.append("=" * 80)
report_lines.append("医疗数据缺失值统计报告（含0值视为缺失）")
report_lines.append("=" * 80)
report_lines.append(f"数据总行数：{len(df)}\n")
report_lines.append("说明：以下列中的0值被视为缺失值（生理学上不可能）")
report_lines.append(" - Glucose（血糖）：血糖为0意味着死亡")
report_lines.append(" - BloodPressure（血压）：血压为0不可能")
report_lines.append(" - SkinThickness（皮肤厚度）：皮肤厚度为0不可能")
report_lines.append(" - BMI（体重指数）：BMI为0不可能")
report_lines.append(" - Insulin（胰岛素）：通常0值表示未测量\n")

report_lines.append("各列详细缺失统计：")
report_lines.append("-" * 80)

for col in df.columns:
    if col in zero_as_missing_cols:
        # 对于需要将0视为缺失的列
        report_lines.append(f"\n【{col}】")
        report_lines.append(f"  原始NaN缺失值：       {true_missing_count[col]:3} （{true_missing_ratio[col]:6.2f}%）")
        report_lines.append(
            f"  0值视为缺失数量：    {zero_based_missing[col]:3} （{(zero_based_missing[col] / len(df)) * 100:6.2f}%）")
        report_lines.append(f"  总缺失值（含0值）：  {total_missing_count[col]:3} （{total_missing_ratio[col]:6.2f}%）")

        # 显示有效数据比例
        valid_ratio = 100 - total_missing_ratio[col]
        report_lines.append(f"  有效数据比例：      {valid_ratio:6.2f}%")
    else:
        # 对于其他列
        report_lines.append(f"\n【{col}】")
        report_lines.append(f"  缺失值数量：         {true_missing_count[col]:3} （{true_missing_ratio[col]:6.2f}%）")

        # 如果该列有0值，但不视为缺失，也显示统计
        if (df[col] == 0).sum() > 0:
            zero_count = (df[col] == 0).sum()
            zero_ratio = (zero_count / len(df)) * 100
            report_lines.append(f"  0值数量（不视为缺失）：{zero_count:3} （{zero_ratio:6.2f}%）")

# -------------------------
#   数据质量总结
# -------------------------
report_lines.append("\n" + "=" * 80)
report_lines.append("数据质量总结")
report_lines.append("=" * 80)

# 计算整体数据完整率
total_cells = len(df) * len(df.columns)
true_missing_cells = true_missing_count.sum()
zero_as_missing_cells = zero_based_missing.sum()
total_missing_cells = total_missing_count.sum()

report_lines.append(f"总数据单元数：         {total_cells}")
report_lines.append(f"原始NaN缺失单元数：    {true_missing_cells} （{(true_missing_cells / total_cells) * 100:.2f}%）")
report_lines.append(
    f"0值视为缺失单元数：    {zero_as_missing_cells} （{(zero_as_missing_cells / total_cells) * 100:.2f}%）")
report_lines.append(f"总缺失单元数：         {total_missing_cells} （{(total_missing_cells / total_cells) * 100:.2f}%）")
report_lines.append(f"总体数据完整率：       {100 - (total_missing_cells / total_cells) * 100:.2f}%")

# 受影响最严重的列
report_lines.append(f"\n缺失值最多的列（含0值视为缺失）：")
for col in total_missing_ratio.sort_values(ascending=False).head(5).index:
    report_lines.append(f"  {col:25} {total_missing_ratio[col]:6.2f}%")

# 拼接报告文本
report_content = "\n".join(report_lines)

# -------------------------
#   保存报告
# -------------------------
output_path = os.path.join(base_dir, "data_pre_process", "missing_value_report.txt")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(report_content)

print(f"\n报告已保存至：{output_path}")
print("=" * 80)

# -------------------------
#   可选：显示数据摘要
# -------------------------
print("\n数据摘要：")
print("-" * 40)
print(f"数据集形状：{df.shape}")
print(f"原始数据集无传统缺失值")
print(f"将0值视为缺失后，受影响列：")

for col in zero_as_missing_cols:
    missing_pct = total_missing_ratio[col]
    if missing_pct > 0:
        print(f"  {col:20} {missing_pct:6.1f}% 缺失")

print("\n建议：")
print("1. SkinThickness 和 Insulin 缺失率较高，需特殊处理")
print("2. 对于缺失值，建议使用中位数或模型填充")
print("3. 考虑创建缺失值指示器（flag）")