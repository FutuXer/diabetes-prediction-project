import pandas as pd
import os

# 加载数据
base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "processed", "diabetes_filled_by_age.csv")
df = pd.read_csv(csv_path)

# 需要处理的列
process_cols = ['SkinThickness', 'Insulin', 'BloodPressure', 'BMI',
                'DiabetesPedigreeFunction', 'Glucose']

print("开始IQR边界处理...")

# 对每列应用IQR边界
for col in process_cols:
    if col in df.columns:
        # 计算IQR边界
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        # 记录修改前的值
        original_min = df[col].min()
        original_max = df[col].max()

        # 将所有超出边界的值拉到边界
        df[col] = df[col].clip(lower=lower, upper=upper)

        # 打印简单信息
        print(f"{col}: 边界[{lower:.1f}, {upper:.1f}] | "
              f"修改前[{original_min:.1f}, {original_max:.1f}] | "
              f"修改后[{df[col].min():.1f}, {df[col].max():.1f}]")

# 保存数据
output_path = os.path.join(base_dir, "data", "processed", "diabetes_eliminate_outlier.csv")
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"\n处理完成！保存到: {output_path}")