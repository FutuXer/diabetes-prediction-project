👤 成员A：数据可视化 + 数据洞察模块核心职责
前期数据探索 + 主应用中的"数据洞察"页面工作清单Part 1：离线数据探索分析（70%已完成）

✅ 编写 analysis/1_visualization.py

数据概览（样本统计、患病率）
单变量分析（8个特征分布图、箱线图）
双变量分析（患病组vs非患病组对比）
相关性分析（热力图、特征重要性）
⭐ 新增：为每个分析添加明确结论



✅ 生成分析报告

保存图表到 docs/images/
撰写 docs/可视化分析报告.md（包含结论）


Part 2：主应用【数据洞察模块】开发（30%）

在 app.py 中完成 render_data_insights() 函数
功能：

患病率分析（饼图+结论）
关键风险因素（柱状图+结论）
高风险人群特征（对比图+结论）
特征相关性（热力图+结论）


⭐ 重点：每个图表下方必须有文字结论框
Part 3：协助集成

调试 app.py 整体布局和样式
撰写报告中"数据可视化分析"章节
答辩PPT中"数据探索"部分
交付物清单

 analysis/1_visualization.py 完整脚本
 docs/images/ 所有可视化图表（至少10张）
 docs/可视化分析报告.md（含结论）
 app.py 中 render_data_insights() 函数
 项目报告"数据可视化"章节
Git分支

feature/visualization
feature/app-insights-module
👤 成员B：数据预处理 + 批量筛查模块核心职责
数据清洗工程 + 主应用中的"批量筛查"功能工作清单Part 1：离线数据预处理脚本

编写 analysis/2_preprocessing.py

缺失值处理

检测零值（Glucose、BloodPressure、SkinThickness、Insulin、BMI）
填充策略：中位数或KNN填充


异常值处理

IQR方法检测
医学合理性验证
决策：删除/保留/替换


特征工程

标准化（Z-score或Min-Max）
衍生特征（BMI分类、年龄分组、血糖风险等级）


数据集划分

训练集 70%
验证集 15%
测试集 15%
保持患病率分层





生成清洗后数据

data/processed/train.csv
data/processed/validation.csv
data/processed/test.csv
models/scaler.pkl（标准化器，供后续使用）



生成预处理报告

docs/预处理报告.md
记录处理前后对比
说明每个决策的理由


Part 2：工具函数库

编写 utils.py

load_data()：加载数据
handle_missing()：缺失值处理
detect_outliers()：异常值检测
standardize_features()：标准化
feature_engineering()：特征工程
这些函数供成员C、D训练模型时使用


Part 3：主应用【批量筛查模块】开发

在 app.py 中完成 render_batch_screening() 函数
功能：

上传CSV文件（多人体检数据）
调用训练好的模型批量预测
生成筛查统计

高/中/低风险人数
平均风险评分
高危人员名单


导出筛查报告Excel


Part 4：协助集成

确保预处理流程与模型训练对接顺利
撰写报告中"数据预处理"章节
答辩PPT中"数据质量"部分
交付物清单

 analysis/2_preprocessing.py 完整脚本
 utils.py 工具函数库
 data/processed/ 三个数据集
 models/scaler.pkl 标准化器
 docs/预处理报告.md
 app.py 中 render_batch_screening() 函数
 项目报告"数据预处理"章节
Git分支

feature/preprocessing
feature/app-batch-module
👤 成员C：回归建模 + 风险评分核心逻辑核心职责
训练回归模型 + 主应用中"风险评分"计算逻辑工作清单Part 1：离线回归模型训练

编写 analysis/3_train_models.py（回归部分）

任务定义

目标：预测风险评分（0-100分连续值）
方法：将Outcome转为风险评分（可用概率×100）





模型构建

模型1：多元线性回归（基线）
模型2：岭回归（处理多重共线性）
模型3：Lasso回归（特征选择）



模型训练

使用成员B提供的训练集
交叉验证选择最优超参数



模型评估

R²（决定系数）
RMSE（均方根误差）
MAE（平均绝对误差）
残差分析（Q-Q图、残差图）



模型解释

提取回归系数
计算各特征贡献度
生成系数置信区间



保存模型

models/risk_score_model.pkl
models/regression_coefficients.json（系数和贡献度）



生成模型报告

docs/回归模型报告.md
包含：模型对比、性能指标、系数解读


Part 2：主应用【风险评分逻辑】开发

在 app.py 的 predict_risk_score() 函数中实现
功能：

加载训练好的回归模型
接收用户输入的8个特征
调用模型预测风险评分
返回评分 + 贡献度分解
例如："您的风险评分68分，其中血糖贡献30分，BMI贡献20分..."


Part 3：主应用【模型说明】部分

在 app.py 的 render_model_documentation() 中完成"回归模型"部分
内容：

模型类型说明（为什么选岭回归）
评估指标展示（R²、RMSE）
回归系数解读（每个系数的医学意义）
可视化：系数柱状图


Part 4：协助集成

确保模型与成员D的分类模型协同工作
撰写报告中"回归建模"章节
答辩PPT中"风险评分"部分
交付物清单

 analysis/3_train_models.py（回归部分）
 models/risk_score_model.pkl
 models/regression_coefficients.json
 docs/回归模型报告.md
 app.py 中 predict_risk_score() 函数
 app.py 中模型说明"回归部分"
 项目报告"回归建模"章节
Git分支

feature/regression-model
feature/app-risk-score
👤 成员D：分类建模 + 患病诊断核心逻辑核心职责
训练分类模型 + 主应用中"患病诊断"计算逻辑工作清单Part 1：离线分类模型训练

编写 analysis/3_train_models.py（分类部分）

任务定义

目标：预测是否患病（0/1二分类）
重点：优先召回率（避免漏诊）





模型构建

模型1：逻辑回归（计算Odds Ratio）
模型2：线性判别分析（LDA）
模型3：朴素贝叶斯（可选）



模型训练

使用成员B提供的训练集
处理类别不平衡（类别权重或SMOTE）



模型评估

准确率（Accuracy）
精确率（Precision）
召回率（Recall）⭐ 重点
F1-Score
AUC-ROC
混淆矩阵
ROC曲线、PR曲线



阈值优化

默认0.5可能不是最优
根据召回率调整阈值



模型解释

计算Odds Ratio（比值比）
特征重要性排序



保存模型

models/disease_classifier.pkl
models/classification_metrics.json（性能指标）



生成模型报告

docs/分类模型报告.md
包含：模型对比、混淆矩阵、ROC曲线、Odds Ratio


Part 2：主应用【患病诊断逻辑】开发

在 app.py 的 predict_disease() 函数中实现
功能：

加载训练好的分类模型
接收用户输入的8个特征
调用模型预测患病概率
返回：是/否 + 概率 + 置信度


Part 3：主应用【模型说明】部分

在 app.py 的 render_model_documentation() 中完成"分类模型"部分
内容：

模型类型说明（为什么选逻辑回归+LDA）
评估指标展示（准确率、召回率、AUC）
Odds Ratio解读（各因素对患病的影响倍数）
可视化：混淆矩阵、ROC曲线


Part 4：主应用【风险评估页面】集成

与成员C协作完成完整的风险评估功能
整合：风险评分 + 患病诊断 → 综合评估报告
Part 5：协助集成

撰写报告中"分类建模"章节
答辩PPT中"患病诊断"部分
交付物清单

 analysis/3_train_models.py（分类部分）
 models/disease_classifier.pkl
 models/classification_metrics.json
 docs/分类模型报告.md
 app.py 中 predict_disease() 函数
 app.py 中模型说明"分类部分"
 项目报告"分类建模"章节
Git分支

feature/classification-model
feature/app-diagnosis