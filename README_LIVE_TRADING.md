# AI-Trader 实时交易系统

> **⚠️ 重要提示**：本系统已从历史回放模式改造为可连接真实市场的实时交易系统。使用前请仔细阅读文档并充分测试。

## 🚀 新功能概述

### 核心特性
- ✅ **实时市场数据**：通过API获取真实市场价格
- ✅ **真实交易执行**：连接券商API进行真实订单交易
- ✅ **多平台支持**：Alpaca (美股) / Binance (加密货币)
- ✅ **双模式运行**：Paper Trading (模拟) 和 Live Trading (实盘)
- ✅ **多层风险管理**：交易前/中/后全方位风控
- ✅ **紧急停止机制**：一键暂停所有交易

### 系统架构

```
┌─────────────────────────────────────┐
│   AI Agent (决策层)                  │
│   - Claude / GPT-4 / DeepSeek      │
└─────────────────┬───────────────────┘
                  │ MCP Protocol
┌─────────────────▼───────────────────┐
│   MCP Tools (工具层)                 │
│   - tool_trade_live (实时交易)       │
│   - tool_get_price_live (实时价格)   │
│   - Risk Manager (风险管理)          │
└─────────────────┬───────────────────┘
                  │ REST/WebSocket API
┌─────────────────▼───────────────────┐
│   Brokers & Providers (执行层)       │
│   - AlpacaBroker / BinanceBroker    │
│   - Real-time Market Data           │
└─────────────────────────────────────┘
```

## 📋 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

新增依赖：
- `aiohttp` - 异步HTTP客户端
- `python-dotenv` - 环境变量管理
- 其他标准库

### 2. 配置API密钥

```bash
# 复制环境变量模板
cp .env.live.example .env

# 编辑并填入您的API密钥
nano .env
```

**Alpaca (美股)**：
- 注册：https://alpaca.markets/
- Paper Trading API密钥（推荐先测试）

**Binance (加密货币)**：
- 注册：https://www.binance.com/
- Testnet：https://testnet.binance.vision/

### 3. 测试连接

```bash
python test_live_connection.py
```

预期输出：
```
✅ Broker connection successful
✅ Data provider connection successful
✅ Price: $226.45
🎉 All tests passed! You're ready for live trading.
```

### 4. 运行Paper Trading

```bash
# 美股Paper Trading (Alpaca)
python main_live.py configs/live_config.json

# 加密货币Paper Trading (Binance)
python main_live.py configs/live_binance_config.json
```

## 🛡️ 风险管理

### 内置风控规则

1. **单笔交易限制**：默认不超过投资组合的10%
2. **持仓集中度**：单只股票不超过30%
3. **日内交易限制**：每日最多50笔交易
4. **日最大亏损**：触及5%自动停止交易
5. **资金验证**：交易前检查可用余额
6. **紧急停止**：一键暂停所有交易

### 风险参数配置

编辑 `configs/live_config.json`：

```json
{
  "risk_controls": {
    "max_single_trade_pct": 0.10,    // 单笔最大10%
    "max_position_pct": 0.30,         // 持仓最大30%
    "max_daily_trades": 50,           // 日最大50笔
    "max_daily_loss_pct": 0.05,       // 日最大亏损5%
    "enable_emergency_stop": true
  }
}
```

## 📁 新增文件结构

```
AI-Trader-test/
├── agent_tools/
│   ├── providers/              # 🆕 市场数据提供商
│   │   ├── base_provider.py
│   │   ├── alpaca_provider.py
│   │   └── binance_provider.py
│   ├── brokers/                # 🆕 券商集成
│   │   ├── base_broker.py
│   │   ├── alpaca_broker.py
│   │   └── binance_broker.py
│   ├── tool_trade_live.py      # 🆕 实时交易工具
│   └── tool_get_price_live.py  # 🆕 实时价格工具
├── risk_management/            # 🆕 风险管理系统
│   ├── risk_manager.py
│   ├── risk_rules.py
│   └── position_monitor.py
├── configs/
│   ├── live_config.json        # 🆕 实时交易配置
│   └── live_binance_config.json
├── docs/
│   ├── LIVE_TRADING_ARCHITECTURE.md  # 🆕 架构文档
│   └── LIVE_TRADING_GUIDE.md         # 🆕 使用指南
├── main_live.py                # 🆕 实时交易主程序
├── test_live_connection.py     # 🆕 连接测试脚本
└── .env.live.example           # 🆕 环境变量模板
```

## 🔐 支持的交易平台

### Alpaca Markets (美股)

| 特性 | Paper Trading | Live Trading |
|------|---------------|--------------|
| 市场 | 美股 (NYSE, NASDAQ) | 美股 |
| 费用 | 免费 | 0佣金 |
| 数据 | 实时 | 实时 |
| 最低资金 | 无 | $0 (建议$100+) |
| 推荐用途 | 测试 | 小额实盘 |

### Binance (加密货币)

| 特性 | Testnet | Live Trading |
|------|---------|--------------|
| 市场 | 加密货币 | 加密货币 |
| 费用 | 免费 | 0.1% 手续费 |
| 数据 | 实时 | 实时 |
| 最低资金 | 虚拟USDT | $10+ |
| 推荐用途 | 测试 | 加密货币交易 |

## 📊 运行模式对比

### Paper Trading vs Live Trading

| 对比项 | Paper Trading | Live Trading |
|--------|---------------|--------------|
| 资金性质 | 虚拟资金 | 真实资金 |
| 订单执行 | 模拟成交 | 真实成交 |
| 财务风险 | ❌ 无 | ✅ 有 |
| 市场数据 | 实时 | 实时 |
| 延迟 | 略低 | 真实延迟 |
| 滑点 | 无 | 有 |
| API限流 | 宽松 | 严格 |
| **适用场景** | **策略测试** | **真实交易** |

## ⚡ 使用示例

### 示例1: Paper Trading测试

```bash
# 1. 配置Paper Trading
export TRADING_MODE=paper
export BROKER_TYPE=alpaca

# 2. 运行
python main_live.py configs/live_config.json

# 3. 观察输出
# ✅ Connected to alpaca broker (paper mode)
# 💰 Buying Power: $100000.00
# 🚀 Starting live trading agent...
```

### 示例2: 风险管理测试

```bash
# 测试风控拦截
# 修改配置将max_single_trade_pct设为0.01 (1%)
# 系统会拒绝过大的交易
```

### 示例3: 紧急停止

```python
# AI可以调用紧急停止
emergency_stop(reason="Market volatility too high")

# 或手动停止
Ctrl+C
```

## 📖 详细文档

- **[架构设计文档](docs/LIVE_TRADING_ARCHITECTURE.md)** - 系统架构和技术细节
- **[使用指南](docs/LIVE_TRADING_GUIDE.md)** - 完整的设置和使用教程
- **原README** - 历史回放模式说明（保留）

## ⚠️ 重要警告

### 在使用真实资金前，请务必：

1. ✅ **充分理解**系统运作原理
2. ✅ **Paper Trading**模式下测试至少1-2周
3. ✅ **小额测试**：先用$100-$1000测试
4. ✅ **风险管理**：设置严格的止损和仓位限制
5. ✅ **持续监控**：定期检查系统运行状态
6. ✅ **法律合规**：遵守当地金融法规

### 法律免责

- 本软件仅供学习和研究使用
- 实盘交易风险由用户自行承担
- 开发者不对任何财务损失负责
- 算法交易存在系统性风险
- 过往表现不代表未来收益

## 🆚 与原系统的区别

| 特性 | 原系统 (历史回放) | 新系统 (实时交易) |
|------|------------------|-------------------|
| 数据源 | 本地JSONL文件 | 实时API |
| 交易执行 | 本地position.jsonl | 券商API |
| 运行模式 | 日期区间回放 | 实时循环 |
| 风险 | 无财务风险 | 真实风险 |
| 用途 | 回测/研究 | 实盘交易 |
| 时间 | 可加速 | 实时 |

## 🔧 故障排查

### 常见问题

**Q: 连接失败**
```bash
# 检查API密钥
cat .env | grep ALPACA_API_KEY

# 测试网络
ping api.alpaca.markets
```

**Q: 风控总是拦截**
```json
// 调整风控参数
"max_single_trade_pct": 0.20  // 增加到20%
```

**Q: AI不执行交易**
```bash
# 查看AI推理日志
tail -f data/live_logs/trading.log
```

更多问题请查看 [使用指南](docs/LIVE_TRADING_GUIDE.md#常见问题)

## 📈 下一步计划

- [ ] 支持更多券商（Interactive Brokers, TD Ameritrade）
- [ ] A股实时交易支持
- [ ] WebSocket实时数据流
- [ ] 高级止损策略（trailing stop, bracket orders）
- [ ] 交易监控Dashboard
- [ ] 性能分析和回测对比
- [ ] 多账户管理

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

## 📄 许可证

[根据原项目许可证]

---

**⚡ 开始您的实时交易之旅！**

```bash
# 1. 安装
pip install -r requirements.txt

# 2. 配置
cp .env.live.example .env && nano .env

# 3. 测试
python test_live_connection.py

# 4. 运行
python main_live.py configs/live_config.json
```

**祝交易顺利！ 🚀**
