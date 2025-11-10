"""
最终中文字体测试脚本
用于验证中文是否能正常显示在图表中
"""

import matplotlib
matplotlib.use('Agg')  # 不显示窗口
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 强制重新加载字体
fm._load_fontmanager(try_read_cache=False)

# 配置微软雅黑
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("="*60)
print("正在生成测试图表...")
print("="*60)

# 创建测试图表
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('中文字体测试 - 糖尿病数据分析', fontsize=20, fontweight='bold')

# 子图1：饼图
ax1 = axes[0, 0]
sizes = [65, 35]
labels = ['未患病', '患病']
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.set_title('患病率分布', fontsize=14, fontweight='bold')

# 子图2：柱状图
ax2 = axes[0, 1]
categories = ['总样本', '未患病', '患病']
values = [768, 500, 268]
ax2.bar(categories, values, color=['#3498db', '#2ecc71', '#e74c3c'])
ax2.set_ylabel('样本数量', fontsize=12)
ax2.set_title('样本统计', fontsize=14, fontweight='bold')
for i, v in enumerate(values):
    ax2.text(i, v + 10, str(v), ha='center', fontsize=11)

# 子图3：折线图
ax3 = axes[1, 0]
x = ['怀孕次数', '血糖', '血压', '皮褶厚度']
y = [3.8, 120.9, 69.1, 20.5]
ax3.plot(x, y, marker='o', linewidth=2, markersize=8)
ax3.set_ylabel('平均值', fontsize=12)
ax3.set_title('特征平均值', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=15, ha='right')

# 子图4：文本信息
ax4 = axes[1, 1]
ax4.axis('off')
info = """
数据集信息：

• 样本数量：768 行
• 特征数量：8 个
• 患病率：34.9%
• 数据类型：数值型
• 缺失值：无

特征列表：
1. 怀孕次数 (Pregnancies)
2. 血糖浓度 (Glucose)
3. 舒张压 (BloodPressure)
4. 皮褶厚度 (SkinThickness)
"""
ax4.text(0.1, 0.5, info, fontsize=11, verticalalignment='center',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

plt.tight_layout()

# 保存图表
import os
os.makedirs('test_output', exist_ok=True)
plt.savefig('test_output/chinese_font_test.png', dpi=150, bbox_inches='tight')
print("\n✓ 测试图表已保存到: test_output/chinese_font_test.png")
print("\n请打开图片查看中文是否显示正常！")
print("="*60)

# 额外信息：显示使用的字体
print("\n当前使用的字体设置：")
print(f"  font.sans-serif: {plt.rcParams['font.sans-serif']}")

print("\n可用的中文字体：")
chinese_fonts = []
for font in fm.fontManager.ttflist:
    if any(keyword in font.name for keyword in ['YaHei', 'SimHei', 'SimSun']):
        chinese_fonts.append(f"  - {font.name}: {font.fname}")

for cf in set(chinese_fonts):
    print(cf)

print("\n" + "="*60)