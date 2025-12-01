import pandas as pd
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "processed", "diabetes_train.csv")
df = pd.read_csv(csv_path)

print("生成有用的列联表")
print("=" * 60)

output_dir = os.path.join(base_dir, "data_analysis", "contingency_tables")
os.makedirs(output_dir, exist_ok=True)

# 只生成这三种有用的列联表
table_combinations = [
    ('Age_category', 'BMI_category', '年龄×BMI'),
    ('Age_category', 'Pregnancies_category', '年龄×怀孕次数'),
    ('BMI_category', 'Pregnancies_category', 'BMI×怀孕次数')
]

for row_col, col_col, label in table_combinations:
    print(f"\n{label} 列联表")
    print("-" * 40)

    # 1. 总人数表
    total_count = pd.crosstab(df[row_col], df[col_col], margins=True)
    print("\n总人数:")
    print(total_count)

    # 保存
    output_path = os.path.join(output_dir, f"{row_col}_{col_col}_total_count.csv")
    total_count.to_csv(output_path, encoding='utf-8')
    print(f"  保存: {output_path}")

    # 2. 糖尿病患者数表
    diabetes_df = df[df['Outcome'] == 1]
    diabetes_count = pd.crosstab(diabetes_df[row_col], diabetes_df[col_col], margins=True)
    print("\n糖尿病患者数:")
    print(diabetes_count)

    output_path = os.path.join(output_dir, f"{row_col}_{col_col}_diabetes_count.csv")
    diabetes_count.to_csv(output_path, encoding='utf-8')
    print(f"  保存: {output_path}")

    # 3. 糖尿病率表
    diabetes_rate = pd.crosstab(df[row_col], df[col_col],
                                values=df['Outcome'],
                                aggfunc='mean',
                                margins=True) * 100
    print("\n糖尿病率 (%):")
    print(diabetes_rate.round(1))

    output_path = os.path.join(output_dir, f"{row_col}_{col_col}_diabetes_rate.csv")
    diabetes_rate.round(1).to_csv(output_path, encoding='utf-8')
    print(f"  保存: {output_path}")

print(f"\n所有有用的列联表已保存到: {output_dir}")