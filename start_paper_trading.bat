@echo off
chcp 65001 >nul
setlocal

echo ========================================
echo AI-Trader Paper Trading（模拟交易）
echo ========================================
echo.

REM 检查.env文件
if not exist ".env" (
    echo ❌ 未找到配置文件 .env
    echo.
    echo 请先运行配置向导：
    echo ▶️  双击运行：config_wizard.bat
    echo.
    pause
    exit /b 1
)

REM 读取BROKER_TYPE
for /f "tokens=2 delims==" %%a in ('findstr "^BROKER_TYPE=" .env') do set BROKER_TYPE=%%a

echo 正在启动Paper Trading...
echo.

if "%BROKER_TYPE%"=="alpaca" (
    echo 📊 平台：Alpaca Markets（美股）
    echo 💰 模式：Paper Trading（虚拟资金）
    echo.
    python main_live.py configs\live_config.json
) else if "%BROKER_TYPE%"=="binance" (
    echo 📊 平台：Binance（加密货币）
    echo 💰 模式：Paper Trading（测试网）
    echo.
    python main_live.py configs\live_binance_config.json
) else (
    echo 📊 使用默认配置
    python main_live.py configs\live_config.json
)

echo.
echo ========================================
echo Paper Trading 已停止
echo ========================================
echo.
pause
