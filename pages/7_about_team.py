"""
糖尿病预测项目 - 团队介绍页面
作者: 全体成员
功能: 展示团队成员、分工和项目信息
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="关于团队 - 糖尿病预测",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 现代化CSS样式
st.markdown("""
<style>
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }

    .team-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        text-align: center;
    }

    .team-card:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        transform: translateY(-5px);
        border-color: #667eea;
    }

    .member-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 3rem;
        color: white;
    }

    .skill-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 500;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        color: #1e40af;
        margin: 0.25rem;
        border: 1px solid #3b82f6;
    }

    .timeline-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        position: relative;
    }

    .timeline-item::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 50%;
        transform: translateY(-50%);
        width: 12px;
        height: 12px;
        background: #667eea;
        border-radius: 50%;
    }

    .tech-stack {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .tech-item {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .tech-item:hover {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-color: #3b82f6;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """主函数"""

    # 页面标题
    st.markdown('<h1 class="hero-title">👥 关于团队</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">了解我们的团队成员、分工和项目信息</p>', unsafe_allow_html=True)

    # 侧边栏导航
    st.sidebar.markdown("""
    <div style="background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
                padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
        <h4 style="color: #1f2937; margin-bottom: 0.5rem;">📋 页面导航</h4>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    cursor: pointer;
                    border-left: 3px solid transparent;"
                    onclick="window.location.href='/?page=personal_assessment'">
            <span style="color: #374151;">📝 个人风险评估</span>
        </div>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    cursor: pointer;
                    border-left: 3px solid transparent;"
                    onclick="window.location.href='/?page=batch_screening'">
            <span style="color: #374151;">📊 批量数据筛查</span>
        </div>
        <div style="padding: 0.5rem; margin: 0.25rem 0;
                    cursor: pointer;
                    border-left: 3px solid transparent;"
                    onclick="window.location.href='/?page=data_observation'">
            <span style="color: #374151;">📈 数据可视化分析</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 导航标签
    tab1, tab2, tab3, tab4 = st.tabs([
        "团队成员",
        "项目分工",
        "开发历程",
        "联系方式"
    ])

    # ==================== Tab 1: 团队成员 =====================
    with tab1:
        st.markdown("### 👨‍👩‍👧‍👦 核心团队成员")

        # 成员信息
        team_members = [
            {
                '姓名': '成员A',
                '角色': '数据可视化与探索性分析',
                '头像': '🎨',
                '专业': '数据科学',
                '技能': ['Python', 'Matplotlib', 'Plotly', 'Streamlit', '数据分析'],
                '负责': [
                    '数据可视化分析',
                    '探索性数据分析(EDA)',
                    '统计图表制作',
                    '交互式界面设计'
                ],
                '特点': '细致的数据洞察力，优秀的可视化设计能力'
            },
            {
                '姓名': '成员B',
                '角色': '数据预处理与特征工程',
                '头像': '🔧',
                '专业': '数据工程',
                '技能': ['Python', 'Pandas', 'NumPy', '数据清洗', '特征工程'],
                '负责': [
                    '缺失值处理',
                    '异常值检测',
                    '数据标准化',
                    '特征选择'
                ],
                '特点': '严谨的数据处理能力，注重数据质量'
            },
            {
                '姓名': '成员C',
                '角色': '回归模型构建（风险评分）',
                '头像': '📊',
                '专业': '机器学习',
                '技能': ['Python', 'Scikit-learn', '统计建模', 'R', '岭回归'],
                '负责': [
                    '风险评分模型',
                    '岭回归训练',
                    '模型解释',
                    '特征重要性分析'
                ],
                '特点': '深入的建模理解，优秀的算法实现能力'
            },
            {
                '姓名': '成员D',
                '角色': '分类模型构建（患病诊断）',
                '头像': '🎯',
                '专业': '机器学习',
                '技能': ['Python', 'Scikit-learn', '逻辑回归', 'AUC分析', '模型评估'],
                '负责': [
                    '分类模型训练',
                    '诊断模型优化',
                    'ROC曲线分析',
                    '模型性能评估'
                ],
                '特点': '精确的模型调优，全面的性能评估'
            }
        ]

        # 展示成员卡片
        cols = st.columns(2)

        for i, member in enumerate(team_members):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="team-card">
                    <div class="member-avatar">{member['头像']}</div>
                    <h3>{member['姓名']}</h3>
                    <h4>{member['角色']}</h4>
                    <p><strong>专业方向：</strong>{member['专业']}</p>

                    <div style="text-align: left; margin: 1rem 0;">
                        <h5>🛠️ 核心技能：</h5>
                        <div>
                            {' '.join([f'<span class="skill-tag">{skill}</span>' for skill in member['技能']])}
                        </div>
                    </div>

                    <div style="text-align: left; margin: 1rem 0;">
                        <h5>📋 主要职责：</h5>
                        <ul style="text-align: left; padding-left: 1.5rem;">
                            {' '.join([f'<li>{task}</li>' for task in member['负责']])}
                        </ul>
                    </div>

                    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 0.75rem; border-radius: 8px; margin-top: 1rem;">
                        <p style="margin: 0; font-style: italic;"><strong>个人特点：</strong>{member['特点']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # 团队优势
        st.markdown("---")
        st.markdown("### ✨ 团队优势")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="team-card">
                <h3>🎯 专业化分工</h3>
                <p>每个成员专注特定领域，发挥专业优势</p>
                <ul>
                    <li>数据处理 → 成员B</li>
                    <li>数据可视化 → 成员A</li>
                    <li>回归建模 → 成员C</li>
                    <li>分类建模 → 成员D</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="team-card">
                <h3>🤝 协作精神</h3>
                <p>团队协作紧密，知识共享</p>
                <ul>
                    <li>定期进度同步</li>
                    <li>技术方案讨论</li>
                    <li>代码质量审查</li>
                    <li>成果整合优化</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="team-card">
                <h3>📚 学习成长</h3>
                <p>持续学习新技术，共同进步</p>
                <ul>
                    <li>技术栈更新</li>
                    <li>算法优化</li>
                    <li>最佳实践</li>
                    <li>经验总结</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # ==================== Tab 2: 项目分工 =====================
    with tab2:
        st.markdown("### 📋 详细分工说明")

        # 分工总览
        st.markdown("#### 🏗️ 项目架构与分工")

        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);">
            <h4>📊 系统架构</h4>
            <p><strong>前端层：</strong>Streamlit多页面应用</p>
            <p><strong>业务逻辑：</strong>Python数据处理和模型推理</p>
            <p><strong>数据处理：</strong>Pandas + NumPy</p>
            <p><strong>机器学习：</strong>Scikit-learn</p>
            <p><strong>可视化：</strong>Matplotlib + Plotly</p>
        </div>
        """, unsafe_allow_html=True)

        # 分工详情表
        st.markdown("#### 📝 分工详情表")

        分工_data = {
            '阶段': ['需求分析', '数据收集', '数据预处理', '探索性分析', '模型开发', '系统集成', '测试验证', '文档撰写'],
            '成员A': ['✅ 参与', '❌', '❌', '✅ 负责', '❌', '✅ 参与', '✅ 参与', '✅ 负责'],
            '成员B': ['✅ 参与', '✅ 负责', '✅ 负责', '❌', '❌', '✅ 参与', '✅ 参与', '✅ 负责'],
            '成员C': ['✅ 参与', '❌', '❌', '❌', '✅ 负责', '✅ 参与', '✅ 参与', '✅ 负责'],
            '成员D': ['✅ 参与', '❌', '❌', '❌', '✅ 负责', '✅ 参与', '✅ 负责', '✅ 负责']
        }

        st.dataframe(
            pd.DataFrame(分工_data),
            use_container_width=True,
            hide_index=True
        )

        # 成员A详细分工
        st.markdown("#### 🎨 成员A - 数据可视化与探索性分析")

        member_a_tasks = {
            '离线分析': [
                '✅ 编写 analysis/1_visualization.py',
                '✅ 数据概览（样本分布、缺失值、异常值）',
                '✅ 单变量分析（8个特征的分布直方图、箱线图）',
                '✅ 双变量分析（患病组vs非患病组对比）',
                '✅ 相关性分析（相关系数热力图、散点图矩阵）',
                '✅ 生成静态图表保存至docs/images/',
                '✅ 撰写可视化分析报告'
            ],
            '在线展示': [
                '✅ 开发 pages/4_data-observation.py',
                '✅ 创建5个Tab功能（数据概览、单变量分析、双变量分析、相关性分析、风险因素排序）',
                '✅ 添加数据预处理结果展示',
                '✅ 实现交互式图表（plotly）',
                '✅ 优化用户界面和交互体验'
            ],
            '交互式探索': [
                '✅ 开发 pages/interactive_data_insights.py',
                '✅ 实现6种高级可视化（3D散点图、雷达图等）',
                '✅ 添加侧边栏控制面板',
                '✅ 提供数据探索工具'
            ],
            '交付物': [
                '✅ analysis/1_visualization.py 完整脚本',
                '✅ docs/images/ 6-8张高质量图表',
                '✅ 两个完整的页面应用',
                '✅ 项目报告数据可视化章节'
            ]
        }

        for section, tasks in member_a_tasks.items():
            st.markdown(f"**{section}：**")
            for task in tasks:
                st.markdown(f"• {task}")
            st.markdown("")

        # 成员B详细分工
        st.markdown("#### 🔧 成员B - 数据预处理与特征工程")

        member_b_tasks = {
            '离线处理': [
                '✅ 编写 data_pre_process/*.py',
                '✅ 缺失值检测（识别生理学不合理的0值）',
                '✅ 异常值检测（IQR方法）',
                '✅ 数据清洗和标准化',
                '✅ 特征工程（BMI分类、年龄分组）',
                '✅ 数据集划分和保存'
            ],
            '工具函数': [
                '✅ 开发 utils.py 工具函数库',
                '✅ 实现可复用的数据处理函数',
                '✅ 提供模型训练接口'
            ],
            '批量筛查': [
                '✅ 开发 pages/batch_screening.py',
                '✅ 实现CSV文件上传功能',
                '✅ 批量预测和报告生成',
                '✅ 结果导出（CSV/Excel）'
            ],
            '交付物': [
                '✅ 完整的数据预处理流程',
                '✅ 清洗后的高质量数据集',
                '✅ 详细的数据质量报告',
                '✅ 预处理工具函数库'
            ]
        }

        for section, tasks in member_b_tasks.items():
            st.markdown(f"**{section}：**")
            for task in tasks:
                st.markdown(f"• {task}")
            st.markdown("")

        # 成员C和D简要介绍
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="team-card">
                <h3>📊 成员C - 回归建模（风险评分）</h3>
                <p><strong>核心职责：</strong></p>
                <ul>
                    <li>训练岭回归风险评分模型</li>
                    <li>超参数调优和交叉验证</li>
                    <li>模型解释和特征重要性分析</li>
                    <li>风险评分接口开发</li>
                    <li>模型技术文档编写</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="team-card">
                <h3>🎯 成员D - 分类建模（患病诊断）</h3>
                <p><strong>核心职责：</strong></p>
                <ul>
                    <li>训练逻辑回归分类模型</li>
                    <li>计算Odds Ratio和特征重要性</li>
                    <li>ROC曲线和混淆矩阵分析</li>
                    <li>诊断概率接口开发</li>
                    <li>性能评估和阈值优化</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # ==================== Tab 3: 开发历程 =====================
    with tab3:
        st.markdown("### 📅 项目开发历程")

        # 时间线
        timeline_events = [
            {
                'date': '2024-11',
                'event': '项目启动',
                'description': '确定项目方向：基于统计建模的糖尿病预测',
                'milestone': True
            },
            {
                'date': '2024-11-15',
                'event': '团队分工',
                'description': '4人团队，明确分工方案',
                'milestone': True
            },
            {
                'date': '2024-11-20',
                'event': '数据收集',
                'description': '获取Pima Indians数据集，了解数据背景',
                'milestone': True
            },
            {
                'date': '2024-11-25',
                'event': '数据预处理',
                'description': '成员B完成数据清洗和特征工程',
                'milestone': True
            },
            {
                'date': '2024-11-30',
                'event': '可视化分析',
                'description': '成员A完成EDA和可视化页面开发',
                'milestone': True
            },
            {
                'date': '2024-12-01',
                'event': '模型开发',
                'description': '成员C和D完成回归和分类模型训练',
                'milestone': True
            },
            {
                'date': '2024-12-03',
                'event': '系统集成',
                'description': '完成所有页面开发，系统整体集成测试',
                'milestone': True
            },
            {
                'date': '2024-12-05',
                'event': '文档完善',
                'description': '完善项目文档，准备答辩材料',
                'milestone': False
            }
        ]

        # 时间线可视化
        fig_timeline = go.Figure()

        for i, event in enumerate(timeline_events):
            if event['milestone']:
                fig_timeline.add_trace(go.Scatter(
                    x=[event['date']],
                    y=[i],
                    mode='markers',
                    marker=dict(
                        size=20,
                        color='#667eea',
                        symbol='star',
                        line=dict(width=2, color='#667eea')
                    ),
                    name=event['event'],
                    hovertemplate='<b>%{text}</b><br>日期: %{x}<br>%{hovertext}'
                ))
            else:
                fig_timeline.add_trace(go.Scatter(
                    x=[event['date']],
                    y=[i],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color='#94a3b8',
                        symbol='circle'
                    ),
                    name=event['event'],
                    hovertemplate='<b>%{text}</b><br>日期: %{x}<br>%{hovertext}',
                    showlegend=False
                ))

        fig_timeline.update_layout(
            title="项目开发时间线",
            xaxis_title="时间",
            yaxis_title="事件",
            height=400,
            showlegend=True
        )

        st.plotly_chart(fig_timeline, use_container_width=True)

        # 开发阶段详情
        st.markdown("#### 🔄 开发阶段详情")

        phases = {
            '第一阶段': {
                '时间': '11月-12月初',
                '内容': '需求分析、数据收集、团队组建',
                '成果': '项目方案、数据集、分工方案'
            },
            '第二阶段': {
                '时间': '12月初-12月中',
                '内容': '数据处理、模型训练、功能开发',
                '成果': '预处理数据、训练模型、基础功能'
            },
            '第三阶段': {
                '时间': '12月中-12月底',
                '内容': '系统集成、界面优化、文档撰写',
                '成果': '完整系统、项目文档、答辩材料'
            }
        }

        for phase_name, phase_info in phases.items():
            st.markdown(f"""
            <div class="timeline-item">
                <h4>{phase_name}</h4>
                <p><strong>时间：</strong>{phase_info['时间']}</p>
                <p><strong>主要内容：</strong>{phase_info['内容']}</p>
                <p><strong>主要成果：</strong>{phase_info['成果']}</p>
            </div>
            """, unsafe_allow_html=True)

        # 技术决策
        st.markdown("#### 🛠️ 技术决策")

        decisions = {
            '前端框架': ['Streamlit', '选择理由：快速原型、易用性好、多页面支持'],
            '后端语言': ['Python', '选择理由：数据科学生态完善、机器学习库丰富'],
            '可视化库': ['Matplotlib + Plotly', '选择理由：静态图表+交互式图表互补'],
            '机器学习': ['Scikit-learn', '选择理由：统计建模友好、文档完善'],
            '模型选择': ['岭回归 + 逻辑回归', '选择理由：可解释性强、适合医疗场景']
        }

        for decision, details in decisions.items():
            st.markdown(f"**{decision}：** {' - '.join(details)}")

        # 挑战与解决方案
        st.markdown("#### ⚡ 挑战与解决方案")

        challenges = [
            {
                '挑战': '数据质量问题',
                '描述': '数据中存在大量0值，需要识别生理学不合理的缺失值',
                '解决': '医学知识指导，使用中位数或分组填充'
            },
            {
                '挑战': '可解释性要求',
                '描述': '医疗场景需要模型参数具有明确临床意义',
                '解决': '选择线性模型，强调系数解释性'
            },
            {
                '挑战': '系统集成复杂',
                '描述': '4个成员工作需要有效整合',
                '解决': '模块化设计，清晰接口定义'
            }
        ]

        for i, challenge in enumerate(challenges):
            st.markdown(f"""
            <div class="timeline-item">
                <h4>{i+1}. {challenge['挑战']}</h4>
                <p><strong>描述：</strong>{challenge['描述']}</p>
                <p><strong>解决方案：</strong>{challenge['解决']}</p>
            </div>
            """, unsafe_allow_html=True)

    # ==================== Tab 4: 联系方式 =====================
    with tab4:
        st.markdown("### 📞 联系方式")

        # 项目信息
        st.markdown("#### 📊 项目基本信息")

        project_info = {
            '项目名称': '基于统计建模的糖尿病预测与健康风险分析系统',
            '项目类型': '课程项目 - 统计建模与数据分析',
            '开发语言': 'Python',
            '技术栈': 'Streamlit, Pandas, NumPy, Scikit-learn, Matplotlib, Plotly',
            '数据集': 'Pima Indians Diabetes Dataset (NIDDK)',
            '开发周期': '2024年11月 - 12月'
        }

        for key, value in project_info.items():
            st.markdown(f"**{key}：** {value}")

        # 团队联系
        st.markdown("#### 👥 团队联系")

        st.markdown("""
        <div class="info-card">
            <h4>📧 邮箱联系方式</h4>
            <p>团队成员邮箱：[具体邮箱地址]</p>
            <p>技术支持：[技术支持邮箱]</p>
            <p>项目咨询：[咨询邮箱]</p>

            <h4>🌐 项目资源</h4>
            <p><strong>GitHub仓库：</strong> [GitHub仓库链接]</p>
            <p><strong>项目文档：</strong> 完整的文档和说明</p>
            <p><strong>在线演示：</strong> [在线演示链接]</p>
        </div>
        """, unsafe_allow_html=True)

        # 致谢
        st.markdown("---")
        st.markdown("### 🙏 致谢")

        st.markdown("""
        <div class="info-card">
            <h4>特别感谢</h4>
            <ul>
                <li><strong>数据提供方：</strong>美国国家糖尿病、消化和肾脏疾病研究所 (NIDDK)</li>
                <li><strong>指导老师：</strong>感谢老师的悉心指导和建议</li>
                <li><strong>课程支持：</strong>统计分析与建模课程组</li>
                <li><strong>技术社区：</strong>开源社区的技术支持</li>
            </ul>

            <h4>技术支持</h4>
            <ul>
                <li>Python数据科学生态</li>
                <li>Streamlit框架</li>
                <li>Scikit-learn机器学习库</li>
                <li>Plotly可视化库</li>
            </ul>

            <h4>团队成员感谢</h4>
            <p>感谢所有团队成员的辛勤付出和紧密合作，没有大家的努力就没有这个项目的成功完成！</p>
        </div>
        """, unsafe_allow_html=True)

        # 版本信息
        st.markdown("#### 📋 版本信息")

        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px; margin: 1rem 0;">
            <p><strong>项目版本：</strong>v1.0.0</p>
            <p><strong>最后更新：</strong>{datetime.now().strftime('%Y年%m月%d日')}</p>
            <p><strong>Python版本：</strong>≥3.8</p>
            <p><strong>依赖版本：</strong>见requirements.txt</p>
            <p><strong>许可证：</strong>MIT License</p>
        </div>
        """, unsafe_allow_html=True)

        # 开源信息
        st.markdown("#### 🌐 开源信息")

        st.markdown("""
        <div class="info-card">
            <h4>📜 开源许可</h4>
            <p>本项目采用MIT许可证，欢迎：</p>
            <ul>
                <li>✅ 学术用途使用</li>
                <li>✅ 学习参考</li>
                <li>✅ 贡献代码</li>
                <li>✅ 报告问题</li>
            </ul>

            <p><strong>贡献指南：</strong></p>
            <ul>
                <li>Fork项目仓库</li>
                <li>创建特性分支</li>
                <li>提交Pull Request</li>
                <li>代码审查通过后合并</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 2rem 0;'>
        <p style='font-size: 0.9rem; margin: 0;'>👥 团队成员：成员A、成员B、成员C、成员D</p>
        <p style='font-size: 0.85rem; margin: 0.5rem 0;'>📊 项目：基于统计建模的糖尿病预测系统</p>
        <p style='font-size: 0.85rem; margin: 0.5rem 0;'>🎯 目标：利用统计建模解决实际问题</p>
        <p style='font-size: 0.85rem; margin: 0.5rem 0;'>💫 持续改进中，欢迎反馈建议</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()