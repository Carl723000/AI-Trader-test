# AI-Trader 参数配置完全参考

> 本文档详细说明所有可配置参数，帮助用户根据自己的需求定制系统

---

## 目录

1. [环境变量配置](#环境变量配置-env)
2. [交易配置文件](#交易配置文件-json)
3. [风险管理参数](#风险管理参数)
4. [AI模型参数](#ai模型参数)
5. [参数调优建议](#参数调优建议)

---

## 环境变量配置 (.env)

### 基本结构

```bash
# AI模型API配置
OPENAI_API_BASE=<API服务器地址>
OPENAI_API_KEY=<您的API密钥>

# 交易平台选择
BROKER_TYPE=<alpaca|binance>
TRADING_MODE=<paper|live>

# Alpaca API
ALPACA_API_KEY=<Alpaca API Key>
ALPACA_API_SECRET=<Alpaca API Secret>

# Binance API
BINANCE_API_KEY=<Binance API Key>
BINANCE_API_SECRET=<Binance API Secret>

# 辅助API
ALPHAADVANTAGE_API_KEY=<Alpha Vantage Key>
JINA_API_KEY=<Jina AI Key>
```

### 详细参数说明

#### 1. AI模型配置

##### `OPENAI_API_BASE`

**类型**：字符串（URL）
**必需**：是
**说明**：AI模型API服务器地址

**可选值**：

| 服务商 | API Base URL | 说明 |
|--------|--------------|------|
| OpenAI | `https://api.openai.com/v1` | 官方API |
| Anthropic | `https://api.anthropic.com/v1` | Claude API |
| DeepSeek | `https://api.deepseek.com/v1` | DeepSeek API |
| 自定义代理 | `https://your-proxy.com/v1` | OpenAI兼容代理 |

**示例**：
```bash
OPENAI_API_BASE=https://api.openai.com/v1
```

##### `OPENAI_API_KEY`

**类型**：字符串
**必需**：是
**说明**：AI模型API密钥

**格式**：
- OpenAI: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (51字符)
- Anthropic: `sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- DeepSeek: 32字符十六进制

**获取方式**：
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys
- DeepSeek: https://platform.deepseek.com/api_keys

**示例**：
```bash
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678
```

#### 2. 交易平台配置

##### `BROKER_TYPE`

**类型**：枚举
**必需**：是
**可选值**：
- `alpaca` - Alpaca Markets（美股）
- `binance` - Binance（加密货币）

**说明**：选择要使用的交易平台

**影响**：
- 决定使用哪个数据提供商
- 决定使用哪个券商API
- 影响默认配置文件选择

**示例**：
```bash
BROKER_TYPE=alpaca
```

##### `TRADING_MODE`

**类型**：枚举
**必需**：是
**可选值**：
- `paper` - Paper Trading（模拟交易）
- `live` - Live Trading（真实交易）

**说明**：选择交易模式

**Paper Trading**：
- ✅ 使用虚拟资金
- ✅ 无财务风险
- ✅ 适合测试策略
- ✅ API限制较宽松

**Live Trading**：
- ⚠️ 使用真实资金
- ⚠️ 有财务风险
- ⚠️ 需谨慎使用
- ⚠️ API限制较严格

**示例**：
```bash
TRADING_MODE=paper
```

#### 3. Alpaca API配置

##### `ALPACA_API_KEY`

**类型**：字符串
**必需**：当 `BROKER_TYPE=alpaca` 时
**格式**：`PK` + 20位字母数字（Paper） 或 `AK` + 20位（Live）

**获取方式**：
1. 登录 Alpaca Dashboard
2. API Keys 页面
3. Paper Trading 或 Live Trading 区域
4. 复制 API Key

**示例**：
```bash
ALPACA_API_KEY=PKA12B34C56D78E90FGH1
```

##### `ALPACA_API_SECRET`

**类型**：字符串
**必需**：当 `BROKER_TYPE=alpaca` 时
**格式**：40位字母数字字符串

**注意**：
- ⚠️ Secret Key只显示一次
- ⚠️ 丢失需重新生成
- ⚠️ 妥善保管，不要泄露

**示例**：
```bash
ALPACA_API_SECRET=abcdefghijklmnopqrstuvwxyz1234567890abcd
```

#### 4. Binance API配置

##### `BINANCE_API_KEY`

**类型**：字符串
**必需**：当 `BROKER_TYPE=binance` 时
**格式**：64位字母数字字符串

**权限要求**：
- ✅ 读取权限（Read）
- ✅ 现货交易（Spot Trading）
- ❌ 提现权限（Withdraw）- 禁用

**获取方式**：
- Testnet: https://testnet.binance.vision/
- 正式: Binance → API管理

**示例**：
```bash
BINANCE_API_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567890abcdef12
```

##### `BINANCE_API_SECRET`

**类型**：字符串
**必需**：当 `BROKER_TYPE=binance` 时
**格式**：64位字母数字字符串

**示例**：
```bash
BINANCE_API_SECRET=fedcba098765432109876543210fedcba098765432109876543210fedcba098
```

#### 5. 辅助API配置

##### `ALPHAADVANTAGE_API_KEY`

**类型**：字符串
**必需**：否（可选）
**说明**：Alpha Vantage市场数据API

**用途**：
- 补充历史数据
- 获取公司基本面信息
- 技术指标计算

**限制**：
- 免费版：5次/分钟
- 付费版：无限制

**获取**：https://www.alphavantage.co/support/#api-key

**示例**：
```bash
ALPHAADVANTAGE_API_KEY=DEMO  # 演示密钥
ALPHAADVANTAGE_API_KEY=YOUR_KEY_HERE  # 实际密钥
```

##### `JINA_API_KEY`

**类型**：字符串
**必需**：否（推荐配置）
**说明**：Jina AI搜索和网页提取API

**用途**：
- 市场新闻搜索
- 公司公告抓取
- 市场情报收集

**获取**：https://jina.ai/

**示例**：
```bash
JINA_API_KEY=jina_abc123def456ghi789
```

---

## 交易配置文件 (JSON)

### 文件位置

- Alpaca（美股）：`configs/live_config.json`
- Binance（加密货币）：`configs/live_binance_config.json`

### 完整配置示例

```json
{
  "description": "AI-Trader实时交易配置",

  "trading_mode": "paper",
  "broker_type": "alpaca",

  "model": {
    "name": "gpt-4",
    "basemodel": "gpt-4",
    "enabled": true
  },

  "risk_controls": {
    "enable_max_single_trade": true,
    "max_single_trade_pct": 0.10,

    "enable_max_position": true,
    "max_position_pct": 0.30,

    "enable_max_daily_trades": true,
    "max_daily_trades": 50,

    "enable_max_daily_loss": true,
    "max_daily_loss_pct": 0.05,

    "enable_min_position_size": true,
    "min_position_value": 10.0,

    "enable_trading_hours": false,
    "trading_hours": [9, 16],

    "enable_emergency_stop": true
  },

  "trading_config": {
    "max_iterations": 1000,
    "iteration_wait_seconds": 60,
    "enable_auto_stop_loss": true,
    "stop_loss_pct": 0.15
  },

  "log_path": "data/live_logs",

  "notification": {
    "enable_email": false,
    "email_address": "",
    "enable_webhook": false,
    "webhook_url": ""
  }
}
```

### 参数详解

#### 1. 基本配置

##### `trading_mode`

**类型**：字符串
**可选值**：`"paper"` | `"live"`
**默认值**：`"paper"`
**说明**：交易模式（与.env中的TRADING_MODE对应）

##### `broker_type`

**类型**：字符串
**可选值**：`"alpaca"` | `"binance"`
**默认值**：`"alpaca"`
**说明**：交易平台（与.env中的BROKER_TYPE对应）

#### 2. AI模型配置

##### `model.name`

**类型**：字符串
**说明**：模型显示名称

**常用值**：
```json
"gpt-4"
"gpt-3.5-turbo"
"claude-3.7-sonnet"
"deepseek-chat"
```

##### `model.basemodel`

**类型**：字符串
**说明**：实际调用的模型ID

**OpenAI模型**：
- `gpt-4` - GPT-4（最强）
- `gpt-4-turbo` - GPT-4 Turbo（更快）
- `gpt-3.5-turbo` - GPT-3.5（便宜）

**Anthropic模型**：
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `claude-3-opus-20240229` - Claude 3 Opus

**DeepSeek模型**：
- `deepseek-chat` - DeepSeek Chat
- `deepseek-coder` - DeepSeek Coder

##### `model.enabled`

**类型**：布尔值
**默认值**：`true`
**说明**：是否启用该模型

---

## 风险管理参数

### 1. 单笔交易限制

##### `enable_max_single_trade`

**类型**：布尔值
**默认值**：`true`
**说明**：是否启用单笔交易金额限制

##### `max_single_trade_pct`

**类型**：数字（0.0-1.0）
**默认值**：`0.10` (10%)
**说明**：单笔交易不超过总资金的比例

**计算方式**：
```
允许交易金额 = 投资组合总值 × max_single_trade_pct
```

**示例**：
```json
"max_single_trade_pct": 0.05  // 5% - 保守
"max_single_trade_pct": 0.10  // 10% - 平衡
"max_single_trade_pct": 0.20  // 20% - 激进
```

**推荐值**：
| 风险偏好 | 推荐值 | 说明 |
|---------|--------|------|
| 极保守 | 0.02-0.05 | 2-5% |
| 保守 | 0.05-0.10 | 5-10% |
| 平衡 | 0.10-0.15 | 10-15% |
| 激进 | 0.15-0.25 | 15-25% |

### 2. 持仓集中度限制

##### `enable_max_position`

**类型**：布尔值
**默认值**：`true`
**说明**：是否启用持仓集中度限制

##### `max_position_pct`

**类型**：数字（0.0-1.0）
**默认值**：`0.30` (30%)
**说明**：单只股票持仓不超过总资金的比例

**计算方式**：
```
允许持仓价值 = 投资组合总值 × max_position_pct
```

**示例**：
```json
"max_position_pct": 0.15  // 15% - 高分散
"max_position_pct": 0.30  // 30% - 平衡
"max_position_pct": 0.50  // 50% - 集中（风险高）
```

**分散化策略**：
| 持仓数量 | 单只比例 | 风险等级 |
|---------|---------|---------|
| 10+ | 10% | 高度分散 ⭐ |
| 5-10 | 10-20% | 适度分散 |
| 3-5 | 20-33% | 中度集中 |
| 1-3 | 33-100% | 高度集中 ⚠️ |

### 3. 日内交易限制

##### `enable_max_daily_trades`

**类型**：布尔值
**默认值**：`true`
**说明**：是否限制日交易次数

##### `max_daily_trades`

**类型**：整数
**默认值**：`50`
**说明**：每日最大交易笔数

**目的**：
- 防止过度交易
- 控制交易成本
- 避免情绪化决策

**推荐值**：
| 交易风格 | 推荐值 | 说明 |
|---------|--------|------|
| 长期持有 | 1-5 | 很少交易 |
| 波段交易 | 5-20 | 适度交易 |
| 日内交易 | 20-100 | 频繁交易 |
| 高频交易 | 100+ | 极高频率 ⚠️ |

### 4. 日最大亏损限制

##### `enable_max_daily_loss`

**类型**：布尔值
**默认值**：`true`
**说明**：是否启用日亏损限制

##### `max_daily_loss_pct`

**类型**：数字（0.0-1.0）
**默认值**：`0.05` (5%)
**说明**：单日亏损达到此比例时自动停止交易

**计算方式**：
```
触发条件：
当日亏损 = 期初资金 - 当前资金
亏损比例 = 当日亏损 / 期初资金
if 亏损比例 >= max_daily_loss_pct:
    停止所有交易
```

**示例**：
```json
"max_daily_loss_pct": 0.02  // 2% - 非常保守 ⭐
"max_daily_loss_pct": 0.05  // 5% - 保守
"max_daily_loss_pct": 0.10  // 10% - 激进 ⚠️
"max_daily_loss_pct": 0.20  // 20% - 极高风险 ❌
```

**重要性**：
- 🛡️ 最重要的风险保护机制
- 📊 防止单日重大损失
- 🔴 触发后需人工重置

### 5. 最小仓位限制

##### `enable_min_position_size`

**类型**：布尔值
**默认值**：`true`
**说明**：是否启用最小仓位检查

##### `min_position_value`

**类型**：数字（美元或其他货币）
**默认值**：`10.0`
**说明**：单笔交易最小金额

**目的**：
- 避免"尘埃交易"（过小的交易）
- 降低交易成本占比
- 提高资金使用效率

**示例**：
```json
// 美股
"min_position_value": 10.0   // $10最小交易

// 加密货币
"min_position_value": 10.0   // 10 USDT最小交易
```

### 6. 交易时段限制

##### `enable_trading_hours`

**类型**：布尔值
**默认值**：`false`
**说明**：是否限制交易时段

##### `trading_hours`

**类型**：数组 `[start_hour, end_hour]`
**默认值**：`[9, 16]`
**说明**：允许交易的时间范围（24小时制）

**用途**：
- 避免盘前盘后交易
- 只在流动性最好的时段交易
- 符合个人作息时间

**示例**：
```json
// 美股常规交易时段（东部时间）
"trading_hours": [9, 16]  // 9:00 AM - 4:00 PM ET

// 扩展时段
"trading_hours": [4, 20]  // 包含盘前盘后

// 加密货币（24小时）
"enable_trading_hours": false  // 不限制
```

### 7. 紧急停止

##### `enable_emergency_stop`

**类型**：布尔值
**默认值**：`true`
**说明**：启用紧急停止机制

**功能**：
- 一键暂停所有交易
- 紧急情况快速响应
- 需手动解除

**触发方式**：
1. AI调用 `emergency_stop()` 工具
2. 手动修改状态文件
3. Ctrl+C中断程序

---

## AI模型参数

### 交易配置

##### `max_iterations`

**类型**：整数
**默认值**：`1000`
**说明**：最大交易循环次数

**计算**：
```
运行时间 ≈ max_iterations × iteration_wait_seconds
例如：1000 × 60秒 = 16.7小时
```

**建议值**：
- 测试：10-100
- 日内交易：100-500
- 长期运行：1000-10000

##### `iteration_wait_seconds`

**类型**：整数
**默认值**：`60`
**说明**：每次决策循环间隔（秒）

**选择依据**：
| 交易风格 | 建议间隔 | 说明 |
|---------|---------|------|
| 高频交易 | 1-10秒 | 需要强大算力 |
| 日内交易 | 30-60秒 | 平衡性能和实时性 |
| 摆动交易 | 300-600秒 | 5-10分钟检查一次 |
| 持仓交易 | 3600秒+ | 1小时或更长 |

##### `enable_auto_stop_loss`

**类型**：布尔值
**默认值**：`true`
**说明**：自动执行止损

##### `stop_loss_pct`

**类型**：数字（0.0-1.0）
**默认值**：`0.15` (15%)
**说明**：持仓亏损达到此比例时自动卖出

**示例**：
```json
"stop_loss_pct": 0.05  // 5% - 短线，严格止损
"stop_loss_pct": 0.10  // 10% - 平衡
"stop_loss_pct": 0.15  // 15% - 中长线
"stop_loss_pct": 0.20  // 20% - 长线，宽松止损
```

---

## 参数调优建议

### 场景1：新手测试

```json
{
  "trading_mode": "paper",
  "risk_controls": {
    "max_single_trade_pct": 0.05,     // 5%
    "max_position_pct": 0.15,          // 15%
    "max_daily_trades": 10,
    "max_daily_loss_pct": 0.02,        // 2%
    "min_position_value": 10.0
  },
  "trading_config": {
    "iteration_wait_seconds": 60,
    "stop_loss_pct": 0.10              // 10%
  }
}
```

**特点**：
- ✅ 极保守参数
- ✅ 适合学习系统
- ✅ 最小化风险

### 场景2：日内交易

```json
{
  "risk_controls": {
    "max_single_trade_pct": 0.10,
    "max_position_pct": 0.25,
    "max_daily_trades": 50,
    "max_daily_loss_pct": 0.05,
    "enable_trading_hours": true,
    "trading_hours": [9, 16]
  },
  "trading_config": {
    "iteration_wait_seconds": 30,
    "stop_loss_pct": 0.05
  }
}
```

**特点**：
- 🔄 频繁交易
- ⏰ 限制交易时段
- 🛡️ 严格止损

### 场景3：波段交易

```json
{
  "risk_controls": {
    "max_single_trade_pct": 0.15,
    "max_position_pct": 0.30,
    "max_daily_trades": 20,
    "max_daily_loss_pct": 0.05,
    "enable_trading_hours": false
  },
  "trading_config": {
    "iteration_wait_seconds": 300,     // 5分钟
    "stop_loss_pct": 0.12
  }
}
```

**特点**：
- 📊 中等频率
- 🔄 适度分散
- ⏱️ 不限时段

### 场景4：长期持有

```json
{
  "risk_controls": {
    "max_single_trade_pct": 0.20,
    "max_position_pct": 0.40,
    "max_daily_trades": 5,
    "max_daily_loss_pct": 0.10,
  },
  "trading_config": {
    "iteration_wait_seconds": 3600,    // 1小时
    "stop_loss_pct": 0.20
  }
}
```

**特点**：
- 📈 低频交易
- 💰 集中持仓
- 🎯 宽松止损

### 场景5：加密货币

```json
{
  "broker_type": "binance",
  "risk_controls": {
    "max_single_trade_pct": 0.08,
    "max_position_pct": 0.25,
    "max_daily_trades": 100,
    "max_daily_loss_pct": 0.10,
    "enable_trading_hours": false
  },
  "trading_config": {
    "iteration_wait_seconds": 60,
    "stop_loss_pct": 0.15
  }
}
```

**特点**：
- 🌐 24/7交易
- ⚡ 高波动性
- 📊 更高频率

---

## 参数优化策略

### 1. 渐进式调整

```
阶段1: 极保守参数（测试1周）
  ↓
阶段2: 保守参数（测试2周）
  ↓
阶段3: 平衡参数（实盘小额）
  ↓
阶段4: 根据表现调整
```

### 2. A/B测试

同时运行不同参数配置，对比表现：

```bash
# 配置A：保守
python main_live.py configs/config_conservative.json

# 配置B：激进
python main_live.py configs/config_aggressive.json
```

### 3. 参数敏感性分析

记录不同参数下的表现：

| 参数 | 值 | 收益率 | 最大回撤 | 交易次数 |
|------|---|--------|---------|---------|
| max_single_trade | 5% | +2.3% | -1.5% | 45 |
| max_single_trade | 10% | +4.1% | -3.2% | 52 |
| max_single_trade | 15% | +5.8% | -5.7% | 48 |

---

## 常见问题

### Q1: 如何找到最优参数？

**答**：
1. 从保守参数开始
2. Paper Trading测试2-4周
3. 记录关键指标
4. 逐步调整单个参数
5. 观察变化并记录

### Q2: 参数设置过于保守，AI不交易怎么办？

**答**：
1. 检查风控日志
2. 适当放宽限制
3. 但保持日亏损限制严格

### Q3: 如何平衡收益和风险？

**答**：使用夏普比率：
```
夏普比率 = (平均收益 - 无风险利率) / 收益标准差
```
目标：夏普比率 > 1.0

---

## 总结

### 核心原则

1. **安全第一**：严格的日亏损限制
2. **分散风险**：限制单只持仓
3. **控制频率**：避免过度交易
4. **渐进优化**：从保守到激进
5. **持续监控**：定期review表现

### 快速参考

**最重要的3个参数**：
1. `max_daily_loss_pct` - 日亏损限制（保命）
2. `max_position_pct` - 持仓集中度（分散）
3. `stop_loss_pct` - 止损比例（保护）

**建议配置流程**：
```
1. 复制示例配置
2. 根据风险偏好选择模板
3. 在Paper Trading测试
4. 根据表现微调
5. 小额实盘验证
```

---

**参数配置是交易成功的关键！建议花时间仔细调优。** 📊
