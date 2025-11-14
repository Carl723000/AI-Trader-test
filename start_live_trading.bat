@echo off
chcp 65001 >nul
setlocal

echo ========================================
echo AI-Trader Live Trading（真实交易）
echo ========================================
echo.
echo ⚠️⚠️⚠️ 警告 ⚠️⚠️⚠️
echo.
echo 您即将启动真实交易模式！
echo 这将使用真实资金进行交易！
echo.
echo 请确保：
echo ✅ 已在Paper Trading模式充分测试
echo ✅ 已设置合理的风险参数
echo ✅ 理解可能的财务风险
echo ✅ 只投入可承受损失的资金
echo.
echo ========================================
echo.

set /p confirm="确认启动真实交易？(输入 YES 继续，其他任意键取消): "

if not "%confirm%"=="YES" (
    echo.
    echo 已取消启动
    echo.
    pause
    exit /b 0
)

REM 检查.env文件
if not exist ".env" (
    echo.
    echo ❌ 未找到配置文件 .env
    echo.
    echo 请先运行配置向导：
    echo ▶️  双击运行：config_wizard.bat
    echo.
    pause
    exit /b 1
)

REM 检查TRADING_MODE
findstr "^TRADING_MODE=live" .env >nul
if errorlevel 1 (
    echo.
    echo ❌ 配置文件中交易模式不是 live
    echo.
    echo 请检查 .env 文件，确保设置：
    echo TRADING_MODE=live
    echo.
    pause
    exit /b 1
)

REM 读取BROKER_TYPE
for /f "tokens=2 delims==" %%a in ('findstr "^BROKER_TYPE=" .env') do set BROKER_TYPE=%%a

cls
echo ========================================
echo 启动真实交易
echo ========================================
echo.

if "%BROKER_TYPE%"=="alpaca" (
    echo 📊 平台：Alpaca Markets（美股）
    echo 💰 模式：Live Trading（真实资金）
    echo.
    python main_live.py configs\live_config.json
) else if "%BROKER_TYPE%"=="binance" (
    echo 📊 平台：Binance（加密货币）
    echo 💰 模式：Live Trading（真实资金）
    echo.
    python main_live.py configs\live_binance_config.json
) else (
    echo 📊 使用默认配置
    python main_live.py configs\live_config.json
)

echo.
echo ========================================
echo Live Trading 已停止
echo ========================================
echo.
pause
