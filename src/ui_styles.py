"""
糖尿病预测项目 - 统一UI样式管理
提供现代化的、统一的界面设计风格
"""

import streamlit as st
import html

# =============================================================================
# 🎨 设计系统配置
# =============================================================================

class DiabetesUITheme:
    """糖尿病预测项目UI主题配置"""

    # 颜色系统 - 现代医疗科技风格
    COLORS = {
        'primary': {
            '50': '#eff6ff',   # 极浅蓝
            '100': '#dbeafe',  # 浅蓝
            '200': '#bfdbfe',  # 中浅蓝
            '300': '#93c5fd',  # 中蓝
            '400': '#60a5fa',  # 标准蓝
            '500': '#3b82f6',  # 主色蓝
            '600': '#2563eb',  # 深蓝
            '700': '#1d4ed8',  # 更深蓝
            '800': '#1e40af',  # 深蓝
            '900': '#1e3a8a',  # 最深蓝
        },
        'success': '#10b981',   # 绿色 - 健康/正常
        'warning': '#f59e0b',   # 橙色 - 警告/注意
        'danger': '#ef4444',    # 红色 - 危险/异常
        'info': '#6b7280',      # 灰色 - 信息
        'neutral': {
            '50': '#f9fafb',
            '100': '#f3f4f6',
            '200': '#e5e7eb',
            '300': '#d1d5db',
            '400': '#9ca3af',
            '500': '#6b7280',
            '600': '#4b5563',
            '700': '#374151',
            '800': '#1f2937',
            '900': '#111827',
        }
    }

    # 风险等级颜色映射
    RISK_COLORS = {
        'low': COLORS['success'],
        'medium': COLORS['warning'],
        'high': COLORS['danger']
    }

    # 间距系统 (rem)
    SPACING = {
        'xs': '0.5rem',
        'sm': '0.75rem',
        'md': '1rem',
        'lg': '1.5rem',
        'xl': '2rem',
        '2xl': '3rem',
        '3xl': '4rem'
    }

    # 圆角系统
    BORDER_RADIUS = {
        'none': '0',
        'sm': '0.125rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
        'full': '9999px'
    }

    # 阴影系统
    SHADOWS = {
        'none': 'none',
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)'
    }

    # 字体系统
    FONT_FAMILY = "'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

    FONT_SIZES = {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem',
        '6xl': '3.75rem'
    }

    FONT_WEIGHTS = {
        'light': '300',
        'normal': '400',
        'medium': '500',
        'semibold': '600',
        'bold': '700',
        'extrabold': '800'
    }

# =============================================================================
# 🎯 核心样式函数
# =============================================================================

def get_global_styles():
    """获取全局基础样式"""
    return f"""
    /* ===== 全局基础样式 ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: {DiabetesUITheme.FONT_FAMILY};
        font-size: {DiabetesUITheme.FONT_SIZES['base']};
        line-height: 1.5;
        color: {DiabetesUITheme.COLORS['neutral']['800']};
    }}

    /* 隐藏Streamlit默认元素 */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* 响应式设计基础 */
    .main > div {{
        padding: {DiabetesUITheme.SPACING['lg']};
        max-width: 1400px;
        margin: 0 auto;
    }}

    /* ===== 动画系统 ===== */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}

    .animate-fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}

    .animate-slide-in {{
        animation: slideIn 0.4s ease-out;
    }}
    """

def get_component_styles():
    """获取组件样式"""
    return f"""
    /* ===== 卡片组件 ===== */
    .card {{
        background: white;
        border-radius: {DiabetesUITheme.BORDER_RADIUS['xl']};
        padding: {DiabetesUITheme.SPACING['xl']};
        box-shadow: {DiabetesUITheme.SHADOWS['md']};
        border: 1px solid {DiabetesUITheme.COLORS['neutral']['200']};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}

    .card:hover {{
        box-shadow: {DiabetesUITheme.SHADOWS['lg']};
        transform: translateY(-2px);
    }}

    .card-header {{
        border-bottom: 1px solid {DiabetesUITheme.COLORS['neutral']['200']};
        padding-bottom: {DiabetesUITheme.SPACING['md']};
        margin-bottom: {DiabetesUITheme.SPACING['lg']};
    }}

    .card-title {{
        font-size: {DiabetesUITheme.FONT_SIZES['xl']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['semibold']};
        color: {DiabetesUITheme.COLORS['neutral']['800']};
        margin: 0 0 {DiabetesUITheme.SPACING['sm']} 0;
    }}

    .card-subtitle {{
        font-size: {DiabetesUITheme.FONT_SIZES['base']};
        color: {DiabetesUITheme.COLORS['neutral']['600']};
        margin: 0;
    }}

    /* ===== 按钮组件 ===== */
    .btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: {DiabetesUITheme.SPACING['sm']} {DiabetesUITheme.SPACING['lg']};
        font-size: {DiabetesUITheme.FONT_SIZES['sm']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['medium']};
        border-radius: {DiabetesUITheme.BORDER_RADIUS['lg']};
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
    }}

    .btn-primary {{
        background: linear-gradient(135deg, {DiabetesUITheme.COLORS['primary']['500']}, {DiabetesUITheme.COLORS['primary']['600']});
        color: white;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1);
    }}

    .btn-primary:hover {{
        background: linear-gradient(135deg, {DiabetesUITheme.COLORS['primary']['600']}, {DiabetesUITheme.COLORS['primary']['700']});
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2);
        transform: translateY(-1px);
    }}

    .btn-secondary {{
        background: white;
        color: {DiabetesUITheme.COLORS['neutral']['700']};
        border: 1px solid {DiabetesUITheme.COLORS['neutral']['300']};
    }}

    .btn-secondary:hover {{
        background: {DiabetesUITheme.COLORS['neutral']['50']};
        border-color: {DiabetesUITheme.COLORS['neutral']['400']};
    }}

    /* ===== 表单组件 ===== */
    .form-group {{
        margin-bottom: {DiabetesUITheme.SPACING['lg']};
    }}

    .form-label {{
        display: block;
        font-size: {DiabetesUITheme.FONT_SIZES['sm']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['medium']};
        color: {DiabetesUITheme.COLORS['neutral']['700']};
        margin-bottom: {DiabetesUITheme.SPACING['sm']};
    }}

    .form-input {{
        width: 100%;
        padding: {DiabetesUITheme.SPACING['sm']} {DiabetesUITheme.SPACING['md']};
        border: 1px solid {DiabetesUITheme.COLORS['neutral']['300']};
        border-radius: {DiabetesUITheme.BORDER_RADIUS['md']};
        font-size: {DiabetesUITheme.FONT_SIZES['base']};
        transition: all 0.2s ease;
    }}

    .form-input:focus {{
        outline: none;
        border-color: {DiabetesUITheme.COLORS['primary']['500']};
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }}

    /* ===== 状态组件 ===== */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        padding: {DiabetesUITheme.SPACING['xs']} {DiabetesUITheme.SPACING['sm']};
        font-size: {DiabetesUITheme.FONT_SIZES['xs']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['medium']};
        border-radius: {DiabetesUITheme.BORDER_RADIUS['full']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .status-success {{
        background: {DiabetesUITheme.COLORS['success']}20;
        color: {DiabetesUITheme.COLORS['success']};
    }}

    .status-warning {{
        background: {DiabetesUITheme.COLORS['warning']}20;
        color: {DiabetesUITheme.COLORS['warning']};
    }}

    .status-danger {{
        background: {DiabetesUITheme.COLORS['danger']}20;
        color: {DiabetesUITheme.COLORS['danger']};
    }}

    /* ===== 网格布局 ===== */
    .grid {{
        display: grid;
        gap: {DiabetesUITheme.SPACING['lg']};
    }}

    .grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
    .grid-3 {{ grid-template-columns: repeat(3, 1fr); }}
    .grid-4 {{ grid-template-columns: repeat(4, 1fr); }}

    /* ===== 响应式断点 ===== */
    @media (max-width: 768px) {{
        .grid-2, .grid-3, .grid-4 {{
            grid-template-columns: 1fr;
        }}

        .main > div {{
            padding: {DiabetesUITheme.SPACING['md']};
        }}

        .card {{
            padding: {DiabetesUITheme.SPACING['lg']};
        }}
    }}
    """

def get_page_specific_styles():
    """获取页面特定样式"""
    return f"""
    /* ===== 首页样式 ===== */
    .hero-section {{
        background: linear-gradient(135deg, {DiabetesUITheme.COLORS['primary']['50']} 0%, {DiabetesUITheme.COLORS['primary']['100']} 100%);
        border-radius: {DiabetesUITheme.BORDER_RADIUS['3xl']};
        padding: {DiabetesUITheme.SPACING['3xl']} {DiabetesUITheme.SPACING['2xl']};
        text-align: center;
        margin-bottom: {DiabetesUITheme.SPACING['3xl']};
        position: relative;
        overflow: hidden;
    }}

    .hero-section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 70% 80%, rgba(147, 197, 253, 0.1) 0%, transparent 50%);
    }}

    .hero-title {{
        font-size: {DiabetesUITheme.FONT_SIZES['5xl']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['extrabold']};
        background: linear-gradient(135deg, {DiabetesUITheme.COLORS['primary']['700']}, {DiabetesUITheme.COLORS['primary']['500']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: {DiabetesUITheme.SPACING['lg']};
        position: relative;
        z-index: 2;
    }}

    .hero-subtitle {{
        font-size: {DiabetesUITheme.FONT_SIZES['xl']};
        color: {DiabetesUITheme.COLORS['neutral']['600']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['normal']};
        margin-bottom: {DiabetesUITheme.SPACING['2xl']};
        position: relative;
        z-index: 2;
    }}

    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: {DiabetesUITheme.SPACING['xl']};
        margin: {DiabetesUITheme.SPACING['3xl']} 0;
    }}

    .feature-card {{
        background: white;
        padding: {DiabetesUITheme.SPACING['xl']};
        border-radius: {DiabetesUITheme.BORDER_RADIUS['2xl']};
        box-shadow: {DiabetesUITheme.SHADOWS['md']};
        border: 1px solid {DiabetesUITheme.COLORS['neutral']['200']};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }}

    .feature-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.05), transparent);
        transition: left 0.6s;
    }}

    .feature-card:hover::before {{
        left: 100%;
    }}

    .feature-card:hover {{
        transform: translateY(-4px);
        box-shadow: {DiabetesUITheme.SHADOWS['lg']};
        border-color: {DiabetesUITheme.COLORS['primary']['200']};
    }}

    .feature-icon {{
        font-size: 3rem;
        margin-bottom: {DiabetesUITheme.SPACING['lg']};
        display: block;
    }}

    .feature-title {{
        font-size: {DiabetesUITheme.FONT_SIZES['lg']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['semibold']};
        color: {DiabetesUITheme.COLORS['neutral']['800']};
        margin-bottom: {DiabetesUITheme.SPACING['md']};
    }}

    .feature-desc {{
        color: {DiabetesUITheme.COLORS['neutral']['600']};
        font-size: {DiabetesUITheme.FONT_SIZES['sm']};
        line-height: 1.6;
    }}

    /* ===== 风险等级样式 ===== */
    .risk-level {{
        padding: {DiabetesUITheme.SPACING['lg']};
        border-radius: {DiabetesUITheme.BORDER_RADIUS['lg']};
        border-left: 4px solid;
        margin: {DiabetesUITheme.SPACING['md']} 0;
        position: relative;
        overflow: hidden;
    }}

    .risk-level::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0.1;
    }}

    .risk-low {{
        border-left-color: {DiabetesUITheme.RISK_COLORS['low']};
        background: linear-gradient(135deg, {DiabetesUITheme.RISK_COLORS['low']}10, {DiabetesUITheme.RISK_COLORS['low']}05);
    }}

    .risk-low::before {{
        background: {DiabetesUITheme.RISK_COLORS['low']};
    }}

    .risk-medium {{
        border-left-color: {DiabetesUITheme.RISK_COLORS['medium']};
        background: linear-gradient(135deg, {DiabetesUITheme.RISK_COLORS['medium']}10, {DiabetesUITheme.RISK_COLORS['medium']}05);
    }}

    .risk-medium::before {{
        background: {DiabetesUITheme.RISK_COLORS['medium']};
    }}

    .risk-high {{
        border-left-color: {DiabetesUITheme.RISK_COLORS['high']};
        background: linear-gradient(135deg, {DiabetesUITheme.RISK_COLORS['high']}10, {DiabetesUITheme.RISK_COLORS['high']}05);
    }}

    .risk-high::before {{
        background: {DiabetesUITheme.RISK_COLORS['high']};
    }}

    /* ===== 统计卡片 ===== */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: {DiabetesUITheme.SPACING['lg']};
        margin: {DiabetesUITheme.SPACING['2xl']} 0;
    }}

    .stat-card {{
        background: white;
        padding: {DiabetesUITheme.SPACING['xl']};
        border-radius: {DiabetesUITheme.BORDER_RADIUS['xl']};
        box-shadow: {DiabetesUITheme.SHADOWS['sm']};
        border: 1px solid {DiabetesUITheme.COLORS['neutral']['200']};
        text-align: center;
        transition: all 0.3s ease;
    }}

    .stat-card:hover {{
        transform: translateY(-2px);
        box-shadow: {DiabetesUITheme.SHADOWS['md']};
    }}

    .stat-value {{
        font-size: {DiabetesUITheme.FONT_SIZES['4xl']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['extrabold']};
        color: {DiabetesUITheme.COLORS['primary']['600']};
        margin-bottom: {DiabetesUITheme.SPACING['sm']};
    }}

    .stat-label {{
        font-size: {DiabetesUITheme.FONT_SIZES['sm']};
        color: {DiabetesUITheme.COLORS['neutral']['600']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['medium']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* ===== 导航和页眉 ===== */
    .page-header {{
        background: white;
        padding: {DiabetesUITheme.SPACING['xl']};
        border-radius: {DiabetesUITheme.BORDER_RADIUS['xl']};
        box-shadow: {DiabetesUITheme.SHADOWS['sm']};
        margin-bottom: {DiabetesUITheme.SPACING['xl']};
        border: 1px solid {DiabetesUITheme.COLORS['neutral']['200']};
    }}

    .page-title {{
        font-size: {DiabetesUITheme.FONT_SIZES['3xl']};
        font-weight: {DiabetesUITheme.FONT_WEIGHTS['extrabold']};
        color: {DiabetesUITheme.COLORS['neutral']['800']};
        margin-bottom: {DiabetesUITheme.SPACING['sm']};
    }}

    .page-subtitle {{
        font-size: {DiabetesUITheme.FONT_SIZES['lg']};
        color: {DiabetesUITheme.COLORS['neutral']['600']};
        margin: 0;
    }}

    /* ===== 表格样式 ===== */
    .data-table {{
        background: white;
        border-radius: {DiabetesUITheme.BORDER_RADIUS['lg']};
        overflow: hidden;
        box-shadow: {DiabetesUITheme.SHADOWS['sm']};
        border: 1px solid {DiabetesUITheme.COLORS['neutral']['200']};
    }}

    /* ===== 图表容器 ===== */
    .chart-container {{
        background: white;
        padding: {DiabetesUITheme.SPACING['lg']};
        border-radius: {DiabetesUITheme.BORDER_RADIUS['lg']};
        box-shadow: {DiabetesUITheme.SHADOWS['sm']};
        border: 1px solid {DiabetesUITheme.COLORS['neutral']['200']};
        margin: {DiabetesUITheme.SPACING['lg']} 0;
    }}
    """

# =============================================================================
# 🎨 样式应用函数
# =============================================================================

def apply_global_styles():
    """应用全局样式到Streamlit应用"""
    styles = get_global_styles() + get_component_styles() + get_page_specific_styles()

    st.markdown(f"""
    <style>
    {styles}
    </style>
    """, unsafe_allow_html=True)

def create_hero_section(title: str, subtitle: str = "", badge: str = ""):
    """创建英雄区域"""
    html = f"""
    <div class="hero-section animate-fade-in">
        {f'<div class="status-badge status-info" style="display: inline-block; margin-bottom: 1rem;">{badge}</div>' if badge else ''}
        <h1 class="hero-title">{title}</h1>
        {f'<p class="hero-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def create_card(title: str, content: str = "", subtitle: str = ""):
    """创建卡片组件"""
    html = f"""
    <div class="card animate-slide-in">
        {f'<div class="card-header"><h2 class="card-title">{title}</h2>{f'<p class="card-subtitle">{subtitle}</p>' if subtitle else ''}</div>' if title else ''}
        {content}
    </div>
    """
    return html

def create_risk_level_display(risk_score: float, risk_level: str, advice: str):
    """创建风险等级显示组件"""
    risk_class = f"risk-{risk_level.lower().split()[0]}"  # low, medium, high
    risk_icon = {"低风险": "🟢", "中等风险": "🟡", "高风险": "🔴"}.get(risk_level, "⚪")

    html = f"""
    <div class="{risk_class} animate-fade-in">
        <h3>{risk_icon} {risk_level}</h3>
        <p><strong>您的风险评分：{risk_score}分</strong></p>
        <p>{advice}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def create_stat_card(value: str, label: str, icon: str = ""):
    """创建统计卡片"""
    html = f"""
    <div class="stat-card">
        {f'<div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''}
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """
    return html

def create_feature_grid(features: list):
    """创建功能网格
    features: [{'icon': '📊', 'title': '标题', 'desc': '描述'}, ...]
    """
    cards = ['<div class="feature-grid">']

    for feature in features:
        icon = feature.get('icon', '')
        title = feature.get('title', '')
        desc = feature.get('desc', '')

        # 如果描述包含 HTML 标签，则以代码块形式展示，避免被当成真实 HTML 渲染
        if '<' in desc or '>' in desc:
            safe_desc = html.escape(desc)
            card_html = f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc"><pre style="white-space: pre-wrap; margin:0;">{safe_desc}</pre></div>
            </div>
            """
        else:
            card_html = f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """

        cards.append(card_html)

    cards.append('</div>')
    st.markdown('\n'.join(cards), unsafe_allow_html=True)

def create_stats_grid(stats: list):
    """创建统计网格
    stats: [{'value': '768', 'label': '训练样本'}, ...]
    """
    html = '<div class="stats-grid">'

    for stat in stats:
        html += create_stat_card(stat['value'], stat['label'], stat.get('icon', ''))

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def create_page_layout(title: str, subtitle: str = "", show_sidebar: bool = True):
    """创建标准页面布局"""
    apply_global_styles()

    # 页面标题区域
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{title}</h1>
        {f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_info_card(title: str, content: str, type: str = "info"):
    """创建信息卡片
    type: info, success, warning, danger
    """
    type_classes = {
        'info': 'info-box',
        'success': 'success-box',
        'warning': 'warning-box',
        'danger': 'danger-box'
    }

    css_class = type_classes.get(type, 'info-box')

    html = f"""
    <div class="{css_class}">
        {f'<h4>{title}</h4>' if title else ''}
        {content}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def create_metric_grid(metrics: list):
    """创建指标网格
    metrics: [{'title': '准确率', 'value': '85.3%', 'delta': '+2.1%', 'delta_color': 'success'}, ...]
    """
    html = '<div class="grid grid-2" style="gap: 1rem; margin: 1rem 0;">'

    for metric in metrics:
        delta_color = metric.get('delta_color', 'normal')
        delta_html = f'<div class="metric-delta">{metric["delta"]}</div>' if metric.get('delta') else ''

        html += f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-size: 0.875rem; color: {DiabetesUITheme.COLORS['neutral']['600']}; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">{metric['title']}</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: {DiabetesUITheme.COLORS['primary']['600']}; margin: 0.5rem 0;">{metric['value']}</div>
                    {delta_html}
                </div>
            </div>
        </div>
        """

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# =============================================================================
# 🎯 便捷函数
# =============================================================================

def style_page(title: str, subtitle: str = "", badge: str = ""):
    """为页面应用标准样式和标题"""
    apply_global_styles()

    if title:
        create_hero_section(title, subtitle, badge)

def style_metric_card(title: str, value: str, delta: str = "", delta_color: str = "normal"):
    """创建样式化的指标卡片"""
    delta_colors = {
        "normal": DiabetesUITheme.COLORS['neutral']['600'],
        "success": DiabetesUITheme.COLORS['success'],
        "warning": DiabetesUITheme.COLORS['warning'],
        "danger": DiabetesUITheme.COLORS['danger']
    }

    html = f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="font-size: 0.875rem; color: {DiabetesUITheme.COLORS['neutral']['600']}; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">{title}</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: {DiabetesUITheme.COLORS['primary']['600']}; margin: 0.5rem 0;">{value}</div>
                {f'<div style="font-size: 0.875rem; font-weight: 600; color: {delta_colors[delta_color]};">{delta}</div>' if delta else ''}
            </div>
        </div>
    </div>
    """
    return html

if __name__ == "__main__":
    # 样式测试
    apply_global_styles()
    st.title("UI样式测试")
    st.markdown("这是新的UI样式系统测试页面")


def apply_flat_theme():
    """
    插入扁平化、极简白色主题（Apple-like），并提供选中标签浮起效果。
    使用此函数替换 apply_global_styles() 在页面中调用。
    """
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #ffffff;
        color: {DiabetesUITheme.COLORS['neutral']['800']};
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .main > div {{ max-width: 1100px; margin: 0 auto; padding: 1.5rem; }}

    /* 卡片与扁平化风格 */
    .card {{ background: #ffffff; border: 1px solid {DiabetesUITheme.COLORS['neutral']['200']}; border-radius: 10px; padding: 1rem; }}

    /* 简洁统计 */
    .stat .value {{ color: {DiabetesUITheme.COLORS['primary']['500']}; font-weight: 700; }}

    /* 选中标签浮起效果（Streamlit tabs） */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        padding: 6px;
        border-radius: 8px;
        background: transparent;
    }}

    .stTabs [data-baseweb="tab"] {{
        padding: 10px 16px;
        border-radius: 8px;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        background: transparent;
        color: {DiabetesUITheme.COLORS['neutral']['700']};
        border: 1px solid transparent;
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        transform: translateY(-6px);
        box-shadow: 0 8px 20px rgba(16,24,40,0.08);
        background: linear-gradient(180deg, #ffffff, #fbfdff);
        color: {DiabetesUITheme.COLORS['primary']['600']};
        border: 1px solid {DiabetesUITheme.COLORS['border'] if 'border' in DiabetesUITheme.COLORS else DiabetesUITheme.COLORS['neutral']['200']};
    }}

    /* 按钮简化 */
    .stButton > button {{ border-radius: 8px !important; padding: .55rem 1rem !important; }}
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def safe_markdown(*args, **kwargs):
    """
    Wrapper for st.markdown that forces unsafe_allow_html=True by default.
    Use this in pages to ensure HTML fragments are rendered instead of shown as text.
    """
    kwargs.setdefault("unsafe_allow_html", True)
    return st.markdown(*args, **kwargs)
