import pandas as pd
import os

# -------------------------
# 构造数据集路径（自动定位项目根目录）
# -------------------------
base_dir = os.path.dirname(os.path.dirname(__file__))  # 返回项目根目录
csv_path = os.path.join(base_dir, "data", "processed", "diabetes_eliminate_outlier.csv")

print(f"正在加载数据集：{csv_path}")

# 读取数据
df = pd.read_csv(csv_path)

# -------------------------
# 检查重复行
# -------------------------
# duplicated() 默认检查整行，除第一次出现外的重复返回 True
duplicated_index = df.duplicated()
num_duplicates = duplicated_index.sum()
total_rows = len(df)

# 打印统计信息
print(f"\n数据总行数：{total_rows}")
print(f"重复行数量：{num_duplicates}")
print(f"重复行占比：{num_duplicates / total_rows * 100:.2f}%")

# -------------------------
# 生成报告（中文内容，文件名英文）
# -------------------------
report_lines = []
report_lines.append("重复行检测报告\n")
report_lines.append(f"数据总行数：{total_rows}")
report_lines.append(f"重复行数量：{num_duplicates}")
report_lines.append(f"重复行占比：{num_duplicates / total_rows * 100:.2f}%\n")
report_lines.append("重复行索引（布尔表示，True表示重复）：")
report_lines.extend([f"{i}: {val}" for i, val in enumerate(duplicated_index)])

# 保存报告
output_path = os.path.join(base_dir, "data_pre_process", "duplicate_report.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"\n重复行报告已生成：{output_path}")
