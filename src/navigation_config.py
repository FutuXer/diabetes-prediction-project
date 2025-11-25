"""
导航配置 - 统一页面名称和路由
确保侧边栏和主页面按钮文字保持一致
"""

# 导航配置字典
NAVIGATION_CONFIG = {
    "main": {
        "title": "女性糖尿病风险评估系统",
        "subtitle": "基于Pima Indians数据集的精准健康预测"
    },
    "pages": {
        "home": {
            "name": "系统首页",
            "icon": "🏠",
            "file": "app.py"
        },
        "personal_assessment": {
            "name": "个人风险评估",
            "icon": "📝",
            "file": "pages/personal_assessment.py",
            "description": "输入8项体检指标，获取个性化风险评分"
        },
        "batch_screening": {
            "name": "批量数据筛查",
            "icon": "📊",
            "file": "pages/batch_screening.py",
            "description": "上传CSV文件进行批量预测分析"
        },
        "data_insights": {
            "name": "数据可视化分析",
            "icon": "📈",
            "file": "pages/4_data-observation.py",
            "description": "探索数据特征分布和规律"
        },
        "interactive_insights": {
            "name": "交互式数据探索",
            "icon": "🔍",
            "file": "pages/interactive_data_insights.py",
            "description": "使用交互式图表深入分析数据"
        },
        "model_documentation": {
            "name": "模型说明",
            "icon": "📖",
            "file": "pages/model_documentation.py",
            "description": "了解模型原理和技术细节"
        },
        "dataset_info": {
            "name": "数据集介绍",
            "icon": "💾",
            "file": "pages/dataset_info.py",
            "description": "查看数据集详细信息"
        },
        "about_team": {
            "name": "关于团队",
            "icon": "👥",
            "file": "pages/about_team.py",
            "description": "项目团队和分工信息"
        }
    }
}

# 获取页面信息
def get_page_info(page_key):
    """根据页面key获取页面信息"""
    return NAVIGATION_CONFIG["pages"].get(page_key, {})

# 获取所有导航页面
def get_all_pages():
    """获取所有页面的导航信息"""
    return NAVIGATION_CONFIG["pages"]

# 生成侧边栏导航HTML
def get_sidebar_nav_html():
    """生成侧边栏导航HTML"""
    html = """
    <div style="background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
                padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
        <h4 style="color: #1f2937; margin-bottom: 0.5rem;">🎯 核心功能</h4>
    """

    # 核心功能页面
    core_pages = ["personal_assessment", "batch_screening", "data_insights", "interactive_insights"]
    for page_key in core_pages:
        page_info = get_page_info(page_key)
        if page_info:
            html += f"""
            <div style="padding: 0.5rem; margin: 0.25rem 0;
                        border-radius: 8px; cursor: pointer;
                        transition: all 0.2s ease;
                        border-left: 3px solid transparent;">
                <span style="font-size: 1.2rem;">{page_info['icon']}</span>
                <span style="margin-left: 0.5rem; color: #374151;">{page_info['name']}</span>
            </div>
            """

    html += """
        <h4 style="color: #1f2937; margin: 1rem 0 0.5rem 0;">📚 系统信息</h4>
    """

    # 系统信息页面
    info_pages = ["model_documentation", "dataset_info", "about_team"]
    for page_key in info_pages:
        page_info = get_page_info(page_key)
        if page_info:
            html += f"""
            <div style="padding: 0.5rem; margin: 0.25rem 0;
                        border-radius: 8px; cursor: pointer;
                        transition: all 0.2s ease;
                        border-left: 3px solid transparent;">
                <span style="font-size: 1.2rem;">{page_info['icon']}</span>
                <span style="margin-left: 0.5rem; color: #374151;">{page_info['name']}</span>
            </div>
            """

    html += "</div>"
    return html

# 验证配置
def validate_config():
    """验证导航配置的完整性"""
    required_keys = ["name", "icon", "file"]
    for page_key, page_info in NAVIGATION_CONFIG["pages"].items():
        for key in required_keys:
            if key not in page_info:
                print(f"⚠️ 页面 {page_key} 缺少必要字段: {key}")

if __name__ == "__main__":
    validate_config()
    print("导航配置验证完成")