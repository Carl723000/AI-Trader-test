@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo AI-Trader 故障诊断工具
echo ========================================
echo.
echo 正在检查系统配置...
echo.

set ERROR_COUNT=0

REM 检查Python
echo [1/8] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    set /a ERROR_COUNT+=1
) else (
    python --version
    echo ✅ Python已安装
)
echo.

REM 检查pip
echo [2/8] 检查pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip不可用
    set /a ERROR_COUNT+=1
) else (
    echo ✅ pip可用
)
echo.

REM 检查依赖包
echo [3/8] 检查Python依赖包...
set MISSING_PACKAGES=0

python -c "import langchain" 2>nul
if errorlevel 1 (
    echo ❌ langchain 未安装
    set /a MISSING_PACKAGES+=1
)

python -c "import aiohttp" 2>nul
if errorlevel 1 (
    echo ❌ aiohttp 未安装
    set /a MISSING_PACKAGES+=1
)

python -c "import dotenv" 2>nul
if errorlevel 1 (
    echo ❌ python-dotenv 未安装
    set /a MISSING_PACKAGES+=1
)

if !MISSING_PACKAGES! GTR 0 (
    echo ⚠️ 缺少 !MISSING_PACKAGES! 个依赖包
    echo 建议运行：pip install -r requirements.txt
    set /a ERROR_COUNT+=1
) else (
    echo ✅ 核心依赖包已安装
)
echo.

REM 检查配置文件
echo [4/8] 检查配置文件...
if not exist ".env" (
    echo ❌ .env 文件不存在
    echo 建议运行：config_wizard.bat
    set /a ERROR_COUNT+=1
) else (
    echo ✅ .env 文件存在
)

if not exist "configs\live_config.json" (
    echo ❌ configs\live_config.json 不存在
    set /a ERROR_COUNT+=1
) else (
    echo ✅ live_config.json 存在
)
echo.

REM 检查API密钥
echo [5/8] 检查API密钥配置...
if exist ".env" (
    findstr "^OPENAI_API_KEY=" .env | findstr "your_" >nul
    if not errorlevel 1 (
        echo ⚠️ OpenAI API密钥未配置（仍为示例值）
        set /a ERROR_COUNT+=1
    )

    findstr "^ALPACA_API_KEY=" .env | findstr "your_" >nul
    if not errorlevel 1 (
        echo ⚠️ Alpaca API密钥未配置
    )

    findstr "^BINANCE_API_KEY=" .env | findstr "your_" >nul
    if not errorlevel 1 (
        echo ⚠️ Binance API密钥未配置
    )

    echo ℹ️ 请确保至少配置了一个交易平台的API密钥
) else (
    echo ⚠️ 无法检查（.env不存在）
)
echo.

REM 检查目录结构
echo [6/8] 检查目录结构...
set MISSING_DIRS=0

if not exist "data" (
    echo ❌ data 目录不存在
    mkdir data
    set /a MISSING_DIRS+=1
)

if not exist "agent_tools" (
    echo ❌ agent_tools 目录不存在
    set /a MISSING_DIRS+=1
)

if not exist "configs" (
    echo ❌ configs 目录不存在
    set /a MISSING_DIRS+=1
)

if !MISSING_DIRS! EQU 0 (
    echo ✅ 目录结构完整
) else (
    echo ⚠️ 缺少 !MISSING_DIRS! 个目录
    set /a ERROR_COUNT+=1
)
echo.

REM 检查网络连接
echo [7/8] 检查网络连接...
ping api.openai.com -n 1 -w 1000 >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 无法连接到 api.openai.com
    echo    可能是网络问题或防火墙阻止
) else (
    echo ✅ OpenAI API可访问
)

ping api.alpaca.markets -n 1 -w 1000 >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 无法连接到 api.alpaca.markets
) else (
    echo ✅ Alpaca API可访问
)
echo.

REM 检查日志文件
echo [8/8] 检查日志目录...
if not exist "data\live_logs" mkdir data\live_logs
if not exist "data\risk_logs" mkdir data\risk_logs
if not exist "data\position_logs" mkdir data\position_logs
echo ✅ 日志目录已创建
echo.

REM 诊断总结
echo ========================================
echo 诊断总结
echo ========================================
echo.

if !ERROR_COUNT! EQU 0 (
    echo 🎉 系统配置正常！
    echo.
    echo 您可以运行：
    echo 1. test_connection.bat - 测试连接
    echo 2. start_paper_trading.bat - 开始Paper Trading
) else (
    echo ⚠️ 发现 !ERROR_COUNT! 个问题
    echo.
    echo 建议操作：
    echo.

    python --version >nul 2>&1
    if errorlevel 1 (
        echo 1. 安装Python 3.8+
        echo    下载：https://www.python.org/downloads/
        echo.
    )

    if not exist ".env" (
        echo 2. 运行配置向导
        echo    双击：config_wizard.bat
        echo.
    )

    if !MISSING_PACKAGES! GTR 0 (
        echo 3. 安装依赖包
        echo    双击：install.bat
        echo.
    )
)

echo ========================================
echo.

REM 显示系统信息
echo 系统信息：
echo - 操作系统：%OS%
echo - 用户：%USERNAME%
echo - 当前目录：%CD%
python --version 2>nul
echo.

pause
