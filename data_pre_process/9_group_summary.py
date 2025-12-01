import pandas as pd
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "processed", "diabetes_train.csv")
df = pd.read_csv(csv_path)

print("生成三个分类的分组汇总表")
print("=" * 60)

# 定义三个分类
categories = [
    ('Age_category', '年龄分组'),
    ('BMI_category', 'BMI分组'),
    ('Pregnancies_category', '怀孕次数分组')
]

# 要统计的数值列
numeric_cols = ['Glucose', 'BloodPressure', 'SkinThickness',
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Pregnancies']

# 创建输出目录
output_dir = os.path.join(base_dir, "data_analysis", "group_summaries")
os.makedirs(output_dir, exist_ok=True)

for col, col_name in categories:
    print(f"\n正在生成 {col_name} 的分组汇总...")

    # 分组计算
    group_stats = df.groupby(col).agg({
        'Outcome': ['count', 'sum', 'mean'],  # 人数, 糖尿病患者数, 糖尿病率
    })

    # 添加各数值列的平均值
    for num_col in numeric_cols:
        if num_col in df.columns:
            group_stats[(num_col, 'mean')] = df.groupby(col)[num_col].mean()

    # 扁平化多层列索引
    group_stats.columns = [f'{col[0]}_{col[1]}' if isinstance(col, tuple) else col
                           for col in group_stats.columns]

    # 重命名列
    column_rename = {
        'Outcome_count': '总人数',
        'Outcome_sum': '糖尿病患者数',
        'Outcome_mean': '糖尿病率',
        'Glucose_mean': '平均血糖',
        'BloodPressure_mean': '平均血压',
        'SkinThickness_mean': '平均皮肤厚度',
        'Insulin_mean': '平均胰岛素',
        'BMI_mean': '平均BMI',
        'DiabetesPedigreeFunction_mean': '平均遗传函数',
        'Age_mean': '平均年龄',
        'Pregnancies_mean': '平均怀孕次数'
    }

    group_stats = group_stats.rename(columns=column_rename)

    # 格式化数据
    group_stats['总人数'] = group_stats['总人数'].astype(int)
    group_stats['糖尿病患者数'] = group_stats['糖尿病患者数'].astype(int)
    group_stats['糖尿病率'] = (group_stats['糖尿病率'] * 100).round(1)

    for col_name in ['平均血糖', '平均血压', '平均皮肤厚度', '平均胰岛素',
                     '平均BMI', '平均遗传函数', '平均年龄', '平均怀孕次数']:
        if col_name in group_stats.columns:
            group_stats[col_name] = group_stats[col_name].round(2)

    # 保存为CSV
    output_path = os.path.join(output_dir, f"{col}_summary.csv")
    group_stats.to_csv(output_path, encoding='utf-8')

    print(f"  已保存: {output_path}")
    print(f"  分组数: {len(group_stats)}")
    print(f"  总人数: {group_stats['总人数'].sum()}")

    # 在控制台显示摘要
    print(f"  {col_name}汇总:")
    for idx, row in group_stats.iterrows():
        print(f"    {idx}: {row['总人数']}人, 糖尿病率{row['糖尿病率']}%")

print(f"\n所有汇总表已保存到: {output_dir}")