import pandas as pd
import numpy as np
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "processed", "diabetes_filled_by_age.csv")

# 加载数据
df = pd.read_csv(csv_path)

# 需要检测的列
numeric_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

# 准备写入txt的内容
output_lines = []
output_lines.append("各列箱线图统计信息 (IQR方法)")
output_lines.append("=" * 60)
output_lines.append(f"数据文件: {csv_path}")
output_lines.append(f"数据行数: {len(df)}")
output_lines.append(f"统计时间: {pd.Timestamp.now()}\n")

for col in numeric_cols:
    # 计算四分位数
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    # 计算异常值边界
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    # 找出异常值
    outliers = df[(df[col] < lower) | (df[col] > upper)]

    # 添加到输出内容
    output_lines.append(f"\n{col}:")
    output_lines.append(f"  Q1: {Q1:.2f}, Q3: {Q3:.2f}, IQR: {IQR:.2f}")
    output_lines.append(f"  异常值边界: [{lower:.2f}, {upper:.2f}]")
    output_lines.append(f"  异常值数量: {len(outliers)}")

    # 打印异常值
    if len(outliers) > 0:
        output_lines.append(f"  异常值行: {outliers.index.tolist()}")
        output_lines.append(f"  异常值具体数值: {outliers[col].tolist()}")

# 计算总异常值数
total_outliers = 0
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    total_outliers += len(outliers)

# 添加总结
output_lines.append(f"\n{'=' * 60}")
output_lines.append(f"总计: {total_outliers} 个异常值")

# 保存到txt文件
output_path = os.path.join(base_dir, "data_pre_process", "boxplot_outlier_report.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"报告已保存到: {output_path}")

# 同时在控制台输出
print("各列箱线图统计信息 (IQR方法)")
print("=" * 60)
for line in output_lines[:10]:  # 只显示前几行
    print(line)