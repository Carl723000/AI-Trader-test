# AI-Trader 实时交易系统使用指南

## 📚 目录

1. [系统概述](#系统概述)
2. [快速开始](#快速开始)
3. [配置说明](#配置说明)
4. [交易平台设置](#交易平台设置)
5. [运行实时交易](#运行实时交易)
6. [风险管理](#风险管理)
7. [监控和日志](#监控和日志)
8. [常见问题](#常见问题)
9. [最佳实践](#最佳实践)

---

## 系统概述

AI-Trader 实时交易系统是从历史回放模式改造的真实市场交易系统，具备以下特性：

### ✅ 核心功能
- **实时数据**：通过API获取实时市场价格
- **真实交易**：连接券商API执行真实订单
- **风险管理**：多层次风险控制系统
- **多平台支持**：Alpaca（美股）、Binance（加密货币）
- **双模式运行**：Paper Trading（模拟）和 Live Trading（实盘）

### ⚠️ 重要警告

**在开始之前，请务必理解：**
1. 实时交易涉及真实资金，可能导致财务损失
2. 务必先在Paper Trading模式下充分测试
3. 算法交易存在技术风险（网络延迟、系统故障等）
4. 遵守所在地区的金融法规和税务规定
5. 建议咨询专业财务顾问

---

## 快速开始

### 步骤1: 安装依赖

```bash
# 克隆或进入项目目录
cd AI-Trader-test

# 安装Python依赖
pip install -r requirements.txt
```

### 步骤2: 配置环境变量

```bash
# 复制环境变量模板
cp .env.live.example .env

# 编辑.env文件，填入您的API密钥
nano .env  # 或使用其他编辑器
```

### 步骤3: 注册交易平台账户

#### 选项A: Alpaca (美股)
1. 访问 [Alpaca Markets](https://alpaca.markets/)
2. 注册账户
3. 在Dashboard中生成API密钥
4. **推荐先使用Paper Trading账户**

#### 选项B: Binance (加密货币)
1. 访问 [Binance](https://www.binance.com/)
2. 注册并完成KYC验证
3. 生成API密钥（只开启读取和交易权限，不要开启提现权限）
4. **推荐先使用Testnet**

### 步骤4: 测试连接

```bash
# 测试Alpaca连接
python test_connection_alpaca.py

# 或测试Binance连接
python test_connection_binance.py
```

### 步骤5: 运行Paper Trading

```bash
# 美股Paper Trading
python main_live.py configs/live_config.json

# 加密货币Paper Trading
python main_live.py configs/live_binance_config.json
```

---

## 配置说明

### 配置文件结构

配置文件位于 `configs/` 目录：

#### `live_config.json` - 美股配置

```json
{
  "trading_mode": "paper",        // "paper" 或 "live"
  "broker_type": "alpaca",         // 券商类型

  "model": {
    "name": "claude-3.7-sonnet",  // AI模型
    "basemodel": "anthropic/claude-3.7-sonnet"
  },

  "risk_controls": {
    "max_single_trade_pct": 0.10,    // 单笔最大10%
    "max_position_pct": 0.30,         // 单只股票最大30%
    "max_daily_trades": 50,           // 日最大交易数
    "max_daily_loss_pct": 0.05,       // 日最大亏损5%
    "enable_emergency_stop": true     // 紧急停止开关
  },

  "trading_config": {
    "max_iterations": 1000,           // 最大循环次数
    "iteration_wait_seconds": 60      // 循环间隔（秒）
  }
}
```

### 环境变量说明

编辑 `.env` 文件：

```bash
# AI模型API
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-key-here

# Alpaca API（Paper Trading）
ALPACA_API_KEY=PKxxxxx
ALPACA_API_SECRET=xxxxx

# Binance API（Testnet）
BINANCE_API_KEY=xxxxx
BINANCE_API_SECRET=xxxxx

# 交易模式
BROKER_TYPE=alpaca
TRADING_MODE=paper
```

---

## 交易平台设置

### Alpaca Markets 设置

#### 1. 注册和获取API密钥

```
1. 访问 https://alpaca.markets/
2. 注册账户（支持国际用户）
3. 登录 → Dashboard → API Keys
4. 生成Paper Trading API密钥
```

#### 2. API权限配置
- ✅ Account (READ)
- ✅ Trading (WRITE)
- ❌ 不要开启提现权限

#### 3. 限制说明
- Paper Trading: 无限制，免费使用
- Live Trading: 需要存入资金
- 数据访问: 实时数据需要订阅

#### 4. 环境变量配置

```bash
# Paper Trading
ALPACA_API_KEY=PKxxxxxxxxxxxxx
ALPACA_API_SECRET=xxxxxxxxxxxxxxxxx
BROKER_TYPE=alpaca
TRADING_MODE=paper
```

---

### Binance 设置

#### 1. 注册和KYC

```
1. 访问 https://www.binance.com/
2. 注册账户并完成身份验证
3. 启用双因素认证（2FA）
```

#### 2. Testnet设置（推荐测试用）

```
1. 访问 https://testnet.binance.vision/
2. 使用GitHub账号登录
3. 生成测试网API密钥
4. 获取测试USDT
```

#### 3. 正式API密钥生成

```
1. 登录Binance → 个人中心 → API管理
2. 创建API密钥
3. 权限设置：
   ✅ 启用现货交易
   ✅ 启用读取
   ❌ 禁用提现
4. IP白名单：绑定您的服务器IP（推荐）
```

#### 4. 环境变量配置

```bash
# Testnet
BINANCE_API_KEY=xxxxxxxxx
BINANCE_API_SECRET=xxxxxxxxx
BROKER_TYPE=binance
TRADING_MODE=paper

# Live Trading (谨慎使用!)
# BROKER_TYPE=binance
# TRADING_MODE=live
```

---

## 运行实时交易

### Paper Trading Mode（推荐先测试）

#### 美股Paper Trading

```bash
# 1. 确保配置正确
cat .env | grep ALPACA
cat .env | grep TRADING_MODE

# 2. 运行
python main_live.py configs/live_config.json

# 3. 观察日志输出
# ✅ Connected to alpaca broker (paper mode)
# ✅ Connected to alpaca data provider
# ✅ Risk manager initialized
# 🚀 Starting live trading agent...
```

#### 加密货币Paper Trading

```bash
# 1. 切换到Binance配置
python main_live.py configs/live_binance_config.json

# 2. 系统会自动使用testnet
```

### Live Trading Mode（真实交易）

⚠️ **只有在Paper Trading充分测试后才进行实盘交易！**

#### 步骤1: 修改配置

编辑 `configs/live_config.json`：

```json
{
  "trading_mode": "live",  // 改为 live
  ...
}
```

#### 步骤2: 更新环境变量

编辑 `.env`：

```bash
# 使用Live Trading API密钥
ALPACA_API_KEY=your_live_api_key
ALPACA_API_SECRET=your_live_api_secret
TRADING_MODE=live
```

#### 步骤3: 小额资金测试

建议先用小额资金测试（如$100-$1000）

#### 步骤4: 启动实盘交易

```bash
python main_live.py configs/live_config.json

# 系统会要求确认
⚠️  WARNING: LIVE TRADING MODE - REAL MONEY WILL BE USED!
Type 'YES' to continue with live trading:
```

---

## 风险管理

### 内置风险控制

系统包含多层风险控制：

#### 1. 交易前风控（Pre-trade）

```
✓ 单笔交易金额限制（默认10%）
✓ 持仓集中度检查（默认30%）
✓ 可用资金验证
✓ 交易时段检查（可选）
```

#### 2. 实时风控（Real-time）

```
✓ 日内交易次数限制（默认50次）
✓ 日最大亏损限制（默认5%）
✓ 持仓金额监控
✓ 异常波动熔断
```

#### 3. 交易后风控（Post-trade）

```
✓ 成交确认验证
✓ 持仓同步检查
✓ 交易日志记录
✓ 风险违规告警
```

### 风险参数配置

在 `configs/live_config.json` 中调整：

```json
{
  "risk_controls": {
    "max_single_trade_pct": 0.05,     // 降低到5%
    "max_position_pct": 0.20,          // 降低到20%
    "max_daily_trades": 20,            // 减少交易频率
    "max_daily_loss_pct": 0.03,        // 降低到3%
    "enable_emergency_stop": true
  }
}
```

### 紧急停止机制

#### 方法1: 通过API

在Agent可以调用的情况下：

```python
# AI会调用此工具
emergency_stop(reason="Market volatility too high")
```

#### 方法2: 手动停止

```bash
# 按 Ctrl+C 中断程序
# 或创建停止标志文件
touch data/emergency_stop.flag
```

#### 方法3: 修改配置

创建 `data/risk_logs/risk_state.json`：

```json
{
  "emergency_stop": true
}
```

---

## 监控和日志

### 日志位置

```
data/
├── live_logs/              # 主日志目录
│   ├── trading.log         # 交易日志
│   ├── risk_checks_*.jsonl # 风控检查记录
│   └── violations_*.jsonl  # 风险违规记录
├── risk_logs/              # 风险管理日志
│   └── risk_state.json     # 风险状态
└── position_logs/          # 持仓日志
    └── positions_*.jsonl   # 持仓变化记录
```

### 实时监控

#### 1. 查看交易日志

```bash
# 实时查看
tail -f data/live_logs/trading.log

# 查看最近交易
tail -50 data/live_logs/trading.log
```

#### 2. 检查风控状态

```bash
# 查看风控状态
cat data/risk_logs/risk_state.json

# 查看今日风控记录
cat data/live_logs/risk_checks_$(date +%Y-%m-%d).jsonl | jq .
```

#### 3. 监控账户状态

```python
# 使用Python脚本查询
from agent_tools.providers import AlpacaDataProvider
import asyncio

async def check_account():
    provider = AlpacaDataProvider(api_key, api_secret)
    await provider.connect()
    account = await provider.get_account_info()
    print(account.to_dict())

asyncio.run(check_account())
```

### 性能指标

监控以下关键指标：

```
✓ 日收益率
✓ 交易成功率
✓ 平均持仓时间
✓ 风控拦截次数
✓ API调用延迟
✓ 系统运行时间
```

---

## 常见问题

### Q1: 连接失败怎么办？

**症状**：`Failed to connect to alpaca broker`

**解决方案**：
```bash
# 1. 检查API密钥
cat .env | grep ALPACA

# 2. 检查网络连接
ping api.alpaca.markets

# 3. 验证API密钥有效性
curl -u "$ALPACA_API_KEY:$ALPACA_API_SECRET" \
  https://paper-api.alpaca.markets/v2/account
```

### Q2: 风控总是拦截交易

**症状**：`Risk check failed: Trade size exceeds maximum`

**解决方案**：
```json
// 调整风控参数
{
  "risk_controls": {
    "max_single_trade_pct": 0.20,  // 增加到20%
    "max_position_pct": 0.40        // 增加到40%
  }
}
```

### Q3: AI不执行交易

**可能原因**：
1. 市场条件不符合AI策略
2. 风控拦截
3. API密钥权限不足

**诊断**：
```bash
# 查看AI的推理过程
grep "AI response" data/live_logs/trading.log

# 查看工具调用
grep "tool_calls" data/live_logs/trading.log
```

### Q4: 如何停止运行中的系统？

```bash
# 方法1: Ctrl+C 优雅退出

# 方法2: 激活紧急停止
echo '{"emergency_stop": true}' > data/risk_logs/risk_state.json

# 方法3: Kill进程
pkill -f main_live.py
```

### Q5: Paper Trading和Live Trading的区别？

| 特性 | Paper Trading | Live Trading |
|------|--------------|--------------|
| 资金 | 虚拟资金 | 真实资金 |
| 订单执行 | 模拟成交 | 真实成交 |
| 风险 | 无财务风险 | 有真实风险 |
| 数据 | 实时数据 | 实时数据 |
| 延迟 | 可能略低 | 真实延迟 |
| API限制 | 较宽松 | 较严格 |

---

## 最佳实践

### 1. 测试流程

```
步骤1: 历史回放测试（原系统）
↓
步骤2: Paper Trading测试（1-2周）
↓
步骤3: 小额实盘测试（$100-$1000）
↓
步骤4: 增加资金规模
```

### 2. 风险管理建议

```python
# 保守型配置
{
  "max_single_trade_pct": 0.05,    # 5%
  "max_position_pct": 0.15,         # 15%
  "max_daily_trades": 10,           # 10次
  "max_daily_loss_pct": 0.02        # 2%
}

# 激进型配置（不推荐新手）
{
  "max_single_trade_pct": 0.15,    # 15%
  "max_position_pct": 0.40,         # 40%
  "max_daily_trades": 100,          # 100次
  "max_daily_loss_pct": 0.10        # 10%
}
```

### 3. 监控检查清单

每日检查：
- [ ] 账户余额和持仓
- [ ] 日收益/亏损
- [ ] 风控拦截记录
- [ ] 系统错误日志
- [ ] API调用统计

每周检查：
- [ ] 周收益率
- [ ] 交易胜率
- [ ] 最大回撤
- [ ] 策略有效性
- [ ] 系统性能

### 4. 安全建议

```
✓ 使用强密码和2FA
✓ 定期轮换API密钥
✓ 限制API权限（禁用提现）
✓ 绑定IP白名单
✓ 定期备份日志和配置
✓ 不要共享API密钥
✓ 监控异常登录
```

### 5. 性能优化

```
✓ 使用WebSocket获取实时数据（更低延迟）
✓ 缓存常用价格数据
✓ 减少不必要的API调用
✓ 优化AI推理速度
✓ 使用异步处理
```

---

## 支持和反馈

### 获取帮助

- **文档**：查看 `docs/` 目录下的其他文档
- **示例**：参考 `examples/` 目录（如果有）
- **日志**：查看 `data/live_logs/` 诊断问题

### 报告问题

如果遇到问题，请提供：
1. 错误日志
2. 配置文件（隐藏敏感信息）
3. 系统环境信息
4. 复现步骤

---

## 免责声明

**本软件仅供学习和研究使用。**

- 使用本软件进行实盘交易的所有风险由用户自行承担
- 开发者不对任何财务损失负责
- 算法交易存在系统性风险
- 过往表现不代表未来收益
- 请遵守当地金融法规

**在使用真实资金前，请务必：**
1. 充分理解系统运作原理
2. 在Paper Trading模式下充分测试
3. 咨询专业财务顾问
4. 只投入可承受损失的资金

---

**祝您交易顺利！ 🚀**
