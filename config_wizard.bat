@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo AI-Trader 配置向导
echo ========================================
echo.
echo 本向导将帮助您完成系统配置
echo 适合首次使用的新手用户
echo.
pause
cls

REM 选择交易平台
:CHOOSE_PLATFORM
echo ========================================
echo [步骤 1/5] 选择交易平台
echo ========================================
echo.
echo 请选择您要使用的交易平台：
echo.
echo 1. Alpaca Markets（美股）
echo    - 适合：美国股票交易
echo    - 优点：0佣金，支持Paper Trading测试
echo    - 注册：https://alpaca.markets/
echo.
echo 2. Binance（加密货币）
echo    - 适合：比特币、以太坊等加密货币
echo    - 优点：24/7交易，支持Testnet测试
echo    - 注册：https://www.binance.com/
echo.
set /p platform_choice="请输入选项 (1 或 2): "

if "%platform_choice%"=="1" (
    set BROKER_TYPE=alpaca
    set PLATFORM_NAME=Alpaca Markets
    goto CHOOSE_MODE
)
if "%platform_choice%"=="2" (
    set BROKER_TYPE=binance
    set PLATFORM_NAME=Binance
    goto CHOOSE_MODE
)
echo ❌ 无效选项，请重新选择
timeout /t 2 >nul
cls
goto CHOOSE_PLATFORM

REM 选择交易模式
:CHOOSE_MODE
cls
echo ========================================
echo [步骤 2/5] 选择交易模式
echo ========================================
echo.
echo 已选择平台：%PLATFORM_NAME%
echo.
echo 请选择交易模式：
echo.
echo 1. Paper Trading（模拟交易）⭐ 推荐新手
echo    - 使用虚拟资金
echo    - 无财务风险
echo    - 用于测试策略
echo.
echo 2. Live Trading（真实交易）⚠️ 谨慎使用
echo    - 使用真实资金
echo    - 有财务风险
echo    - 仅在充分测试后使用
echo.
set /p mode_choice="请输入选项 (1 或 2): "

if "%mode_choice%"=="1" (
    set TRADING_MODE=paper
    set MODE_NAME=Paper Trading（模拟）
    goto INPUT_API_KEYS
)
if "%mode_choice%"=="2" (
    set TRADING_MODE=live
    set MODE_NAME=Live Trading（真实）
    echo.
    echo ⚠️⚠️⚠️ 警告 ⚠️⚠️⚠️
    echo 真实交易模式将使用真实资金！
    echo 请确保您已经充分测试策略！
    echo.
    set /p confirm="确认使用真实交易模式？(输入YES继续): "
    if not "!confirm!"=="YES" (
        echo 已取消，返回选择模式
        timeout /t 2 >nul
        goto CHOOSE_MODE
    )
    goto INPUT_API_KEYS
)
echo ❌ 无效选项，请重新选择
timeout /t 2 >nul
goto CHOOSE_MODE

REM 输入API密钥
:INPUT_API_KEYS
cls
echo ========================================
echo [步骤 3/5] 配置API密钥
echo ========================================
echo.
echo 平台：%PLATFORM_NAME%
echo 模式：%MODE_NAME%
echo.

if "%BROKER_TYPE%"=="alpaca" (
    echo 📝 获取Alpaca API密钥：
    echo 1. 访问 https://alpaca.markets/
    echo 2. 注册并登录账户
    echo 3. 进入 Dashboard - API Keys
    if "%TRADING_MODE%"=="paper" (
        echo 4. 生成 Paper Trading API密钥
    ) else (
        echo 4. 生成 Live Trading API密钥
    )
    echo 5. 复制 API Key 和 API Secret
    echo.
    echo 请输入您的Alpaca API密钥：
    echo.
    set /p ALPACA_API_KEY="API Key: "
    set /p ALPACA_API_SECRET="API Secret: "
)

if "%BROKER_TYPE%"=="binance" (
    echo 📝 获取Binance API密钥：
    if "%TRADING_MODE%"=="paper" (
        echo 1. 访问 https://testnet.binance.vision/
        echo 2. 使用GitHub账号登录
        echo 3. 生成测试网API密钥
    ) else (
        echo 1. 访问 https://www.binance.com/
        echo 2. 登录并完成身份验证
        echo 3. 个人中心 - API管理
        echo 4. 创建API密钥（只开启读取和现货交易权限）
    )
    echo.
    echo 请输入您的Binance API密钥：
    echo.
    set /p BINANCE_API_KEY="API Key: "
    set /p BINANCE_API_SECRET="API Secret: "
)

REM 输入AI模型API
cls
echo ========================================
echo [步骤 4/5] 配置AI模型
echo ========================================
echo.
echo 本系统需要AI模型来做交易决策
echo.
echo 推荐模型（选择其一）：
echo 1. OpenAI GPT-4
echo 2. Claude (Anthropic)
echo 3. DeepSeek
echo.
set /p model_choice="请选择模型 (1-3): "

if "%model_choice%"=="1" (
    set OPENAI_API_BASE=https://api.openai.com/v1
    echo.
    echo 📝 获取OpenAI API密钥：
    echo 1. 访问 https://platform.openai.com/
    echo 2. 注册/登录账户
    echo 3. API Keys - Create new secret key
    echo.
)
if "%model_choice%"=="2" (
    set OPENAI_API_BASE=https://api.anthropic.com/v1
    echo.
    echo 📝 获取Claude API密钥：
    echo 1. 访问 https://console.anthropic.com/
    echo 2. 注册/登录账户
    echo 3. API Keys - Create Key
    echo.
)
if "%model_choice%"=="3" (
    set OPENAI_API_BASE=https://api.deepseek.com/v1
    echo.
    echo 📝 获取DeepSeek API密钥：
    echo 1. 访问 https://platform.deepseek.com/
    echo 2. 注册/登录账户
    echo 3. API Keys - Create new key
    echo.
)

set /p OPENAI_API_KEY="请输入AI模型API密钥: "

REM 风险参数配置
cls
echo ========================================
echo [步骤 5/5] 风险管理参数
echo ========================================
echo.
echo 设置风险控制参数（建议新手使用保守设置）
echo.
echo 1. 保守型（推荐新手）⭐
echo    - 单笔最大5%%资金
echo    - 单只股票最大15%%
echo    - 日最大10笔交易
echo.
echo 2. 平衡型
echo    - 单笔最大10%%资金
echo    - 单只股票最大30%%
echo    - 日最大30笔交易
echo.
echo 3. 激进型（不推荐新手）
echo    - 单笔最大15%%资金
echo    - 单只股票最大40%%
echo    - 日最大50笔交易
echo.
echo 4. 自定义
echo.
set /p risk_choice="请选择风险级别 (1-4): "

if "%risk_choice%"=="1" (
    set MAX_SINGLE_TRADE=0.05
    set MAX_POSITION=0.15
    set MAX_DAILY_TRADES=10
    set MAX_DAILY_LOSS=0.02
)
if "%risk_choice%"=="2" (
    set MAX_SINGLE_TRADE=0.10
    set MAX_POSITION=0.30
    set MAX_DAILY_TRADES=30
    set MAX_DAILY_LOSS=0.05
)
if "%risk_choice%"=="3" (
    set MAX_SINGLE_TRADE=0.15
    set MAX_POSITION=0.40
    set MAX_DAILY_TRADES=50
    set MAX_DAILY_LOSS=0.10
)
if "%risk_choice%"=="4" (
    echo.
    set /p MAX_SINGLE_TRADE="单笔最大交易比例 (0.01-0.50, 如0.10表示10%%): "
    set /p MAX_POSITION="单只股票最大持仓比例 (0.05-0.50): "
    set /p MAX_DAILY_TRADES="日最大交易次数 (1-200): "
    set /p MAX_DAILY_LOSS="日最大亏损比例 (0.01-0.20): "
)

REM 生成配置文件
cls
echo ========================================
echo 正在生成配置文件...
echo ========================================
echo.

REM 创建.env文件
(
echo # AI-Trader 配置文件
echo # 由配置向导自动生成：%date% %time%
echo.
echo # AI模型配置
echo OPENAI_API_BASE=%OPENAI_API_BASE%
echo OPENAI_API_KEY=%OPENAI_API_KEY%
echo.
echo # 交易平台配置
echo BROKER_TYPE=%BROKER_TYPE%
echo TRADING_MODE=%TRADING_MODE%
echo.
) > .env

if "%BROKER_TYPE%"=="alpaca" (
    echo # Alpaca API密钥 >> .env
    echo ALPACA_API_KEY=%ALPACA_API_KEY% >> .env
    echo ALPACA_API_SECRET=%ALPACA_API_SECRET% >> .env
)

if "%BROKER_TYPE%"=="binance" (
    echo # Binance API密钥 >> .env
    echo BINANCE_API_KEY=%BINANCE_API_KEY% >> .env
    echo BINANCE_API_SECRET=%BINANCE_API_SECRET% >> .env
)

echo.
echo # 其他配置 >> .env
echo ALPHAADVANTAGE_API_KEY=demo >> .env
echo JINA_API_KEY= >> .env

REM 创建或更新配置JSON
set CONFIG_FILE=configs\live_config.json
if "%BROKER_TYPE%"=="binance" set CONFIG_FILE=configs\live_binance_config.json

python -c "import json; config = json.load(open('%CONFIG_FILE%')); config['trading_mode'] = '%TRADING_MODE%'; config['broker_type'] = '%BROKER_TYPE%'; config['risk_controls']['max_single_trade_pct'] = %MAX_SINGLE_TRADE%; config['risk_controls']['max_position_pct'] = %MAX_POSITION%; config['risk_controls']['max_daily_trades'] = %MAX_DAILY_TRADES%; config['risk_controls']['max_daily_loss_pct'] = %MAX_DAILY_LOSS%; json.dump(config, open('%CONFIG_FILE%', 'w'), indent=2)" 2>nul

echo ✅ 配置文件已生成
echo.

REM 显示配置摘要
echo ========================================
echo 配置摘要
echo ========================================
echo.
echo 交易平台：%PLATFORM_NAME%
echo 交易模式：%MODE_NAME%
echo.
echo 风险参数：
echo - 单笔最大：%MAX_SINGLE_TRADE%（即 %MAX_SINGLE_TRADE%0%%）
echo - 持仓最大：%MAX_POSITION%（即 %MAX_POSITION%0%%）
echo - 日最大交易：%MAX_DAILY_TRADES% 笔
echo - 日最大亏损：%MAX_DAILY_LOSS%（即 %MAX_DAILY_LOSS%0%%）
echo.
echo 配置文件位置：
echo - 环境变量：%CD%\.env
echo - 交易配置：%CD%\%CONFIG_FILE%
echo.
echo ========================================
echo 🎉 配置完成！
echo ========================================
echo.
echo 下一步建议：
echo.
echo 1. 测试连接（推荐）
echo    ▶️  双击运行：test_connection.bat
echo.
echo 2. 开始Paper Trading
echo    ▶️  双击运行：start_paper_trading.bat
echo.
echo 3. 查看详细文档
echo    📖 打开：docs\WINDOWS_SETUP_GUIDE.md
echo.
pause
