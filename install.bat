@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo AI-Trader 实时交易系统 - Windows 一键安装
echo ========================================
echo.

REM 检查Python是否安装
echo [1/6] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python！
    echo.
    echo 请先安装Python 3.8或更高版本：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载最新版本（推荐3.11）
    echo 3. 安装时勾选"Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python已安装
echo.

REM 检查pip
echo [2/6] 检查pip包管理器...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip未安装，正在安装...
    python -m ensurepip --upgrade
)
echo ✅ pip已就绪
echo.

REM 升级pip
echo [3/6] 升级pip到最新版本...
python -m pip install --upgrade pip
echo.

REM 安装依赖
echo [4/6] 安装Python依赖包（可能需要几分钟）...
echo 正在安装核心依赖...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ⚠️ 部分依赖安装失败，尝试使用国内镜像源...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)
echo ✅ 依赖安装完成
echo.

REM 创建必要的目录
echo [5/6] 创建数据目录...
if not exist "data\live_logs" mkdir data\live_logs
if not exist "data\risk_logs" mkdir data\risk_logs
if not exist "data\position_logs" mkdir data\position_logs
echo ✅ 目录创建完成
echo.

REM 复制环境变量模板
echo [6/6] 配置环境变量...
if not exist ".env" (
    if exist ".env.live.example" (
        copy .env.live.example .env >nul
        echo ✅ 已创建.env配置文件
        echo.
        echo ⚠️ 重要：请编辑.env文件，填入您的API密钥
        echo    文件位置：%CD%\.env
    ) else (
        echo ❌ 找不到.env.live.example模板文件
    )
) else (
    echo ℹ️ .env文件已存在，跳过创建
)
echo.

echo ========================================
echo 🎉 安装完成！
echo ========================================
echo.
echo 下一步操作：
echo.
echo 1. 编辑配置文件：
echo    📝 打开文件：%CD%\.env
echo    🔑 填入API密钥（参考文档获取）
echo.
echo 2. 运行配置向导（推荐新手）：
echo    ▶️  双击运行：config_wizard.bat
echo.
echo 3. 测试连接：
echo    ▶️  双击运行：test_connection.bat
echo.
echo 4. 开始Paper Trading：
echo    ▶️  双击运行：start_paper_trading.bat
echo.
echo 📚 详细文档：
echo    - 快速开始：README_LIVE_TRADING.md
echo    - 详细指南：docs\LIVE_TRADING_GUIDE.md
echo    - Windows指南：docs\WINDOWS_SETUP_GUIDE.md
echo.
echo ========================================
echo.
pause
