@echo off
echo ===========================================
echo 糖尿病预测项目 - 启动脚本
echo ===========================================
echo.

cd /d %~dp0

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误：未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

echo.
echo [2/3] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告：依赖安装可能有问题，请手动检查
)

echo.
echo [3/3] 启动Streamlit应用...
echo ===========================================
echo 应用即将启动，请在浏览器中访问：
echo http://localhost:8501
echo ===========================================
echo.

streamlit run app.py

pause

