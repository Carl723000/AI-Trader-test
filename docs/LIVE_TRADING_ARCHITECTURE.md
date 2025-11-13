# AI-Trader 实时交易系统架构文档

## 📋 系统概述

本文档描述从历史回放模式到实时交易系统的架构改造方案。

## 🏗️ 核心架构变更

### 1. 数据层改造

#### 原架构（历史回放）
```
本地JSONL文件 → tool_get_price_local → Agent
```

#### 新架构（实时交易）
```
实时API (WebSocket/REST) → RealTimeDataProvider → tool_get_price_live → Agent
                                                 ↓
                                            数据缓存层
```

### 2. 交易执行层改造

#### 原架构（模拟交易）
```
Agent → tool_trade.py → 更新本地position.jsonl
```

#### 新架构（真实交易）
```
Agent → tool_trade_live.py → 风险管理系统 → 券商API → 真实市场
                                  ↓
                            交易日志和审计
```

## 🔌 支持的交易平台

### 美股交易
- **Alpaca API** (推荐) - 免手续费，支持纸上交易和实盘
- **Interactive Brokers API** - 专业级，支持全球市场
- **TD Ameritrade API** - 功能完整

### A股交易
- **华泰证券API** - 支持Level-2行情
- **东方财富API** - 个人交易者友好
- **通用券商接口** - 基于OpenAPI标准

### 加密货币交易
- **Binance API** - 全球最大交易所
- **Coinbase Pro API** - 美国合规交易所
- **OKX API** - 支持多种币种

## 🛡️ 风险管理系统

### 多层风险控制

#### 1. 交易前风控（Pre-trade Risk）
- 单笔交易金额限制
- 持仓集中度检查
- 可用保证金验证
- 交易时段检查

#### 2. 实时风控（Real-time Risk）
- 日内交易次数限制
- 止损自动触发
- 持仓金额监控
- 异常波动熔断

#### 3. 交易后风控（Post-trade Risk）
- 成交确认验证
- 持仓与账户同步
- 交易日志记录
- 异常告警

### 风控配置示例
```json
{
  "risk_controls": {
    "max_single_trade_pct": 0.10,      // 单笔最大10%资金
    "max_position_pct": 0.30,           // 单只股票最大30%
    "max_daily_trades": 50,             // 日内最大50笔
    "max_daily_loss_pct": 0.05,         // 日最大亏损5%
    "stop_loss_pct": 0.15,              // 止损线15%
    "enable_emergency_stop": true       // 紧急停止开关
  }
}
```

## 📡 实时数据获取

### 数据源架构

```python
# 抽象接口
class MarketDataProvider:
    def get_realtime_price(symbol: str) -> Price
    def subscribe_quotes(symbols: List[str], callback)
    def get_account_info() -> Account

# 具体实现
- AlpacaDataProvider
- BinanceDataProvider
- TushareRealtimeProvider
```

### WebSocket实时数据流

```
市场WebSocket → 数据解析器 → 内存缓存 → Agent查询
                    ↓
                数据库持久化
```

## 🔐 安全机制

### API密钥管理
- 环境变量加密存储
- 密钥轮换机制
- 权限最小化原则

### 交易确认机制
```python
# 两步确认流程
1. AI Agent生成交易信号
2. 风控系统验证
3. （可选）人工确认
4. 执行交易
```

### 紧急停止机制
- Web界面一键停止
- 异常自动熔断
- 邮件/短信告警

## 📊 新增模块清单

### 1. 实时数据模块
- `agent_tools/providers/base_provider.py` - 抽象基类
- `agent_tools/providers/alpaca_provider.py` - Alpaca实现
- `agent_tools/providers/binance_provider.py` - Binance实现
- `agent_tools/tool_get_price_live.py` - 实时价格工具

### 2. 券商集成模块
- `agent_tools/brokers/base_broker.py` - 抽象基类
- `agent_tools/brokers/alpaca_broker.py` - Alpaca交易
- `agent_tools/brokers/binance_broker.py` - Binance交易
- `agent_tools/tool_trade_live.py` - 实时交易工具

### 3. 风险管理模块
- `risk_management/risk_manager.py` - 风控核心
- `risk_management/position_monitor.py` - 持仓监控
- `risk_management/risk_rules.py` - 风控规则引擎

### 4. 账户管理模块
- `account_management/account_sync.py` - 账户同步
- `account_management/order_tracker.py` - 订单跟踪
- `account_management/portfolio_manager.py` - 组合管理

### 5. 实时Agent模块
- `agent/live_agent/live_base_agent.py` - 实时交易Agent
- `agent/live_agent/live_agent_us.py` - 美股实时Agent
- `agent/live_agent/live_agent_crypto.py` - 加密货币实时Agent

## 🚀 部署流程

### 1. 模拟交易测试（Paper Trading）
```bash
# 使用Alpaca纸上交易账户测试
export TRADING_MODE=paper
export ALPACA_API_KEY=your_paper_key
python main_live.py --config configs/live_paper_config.json
```

### 2. 小资金实盘验证
```bash
# 使用小额资金验证策略
export TRADING_MODE=live
export INITIAL_CAPITAL=1000  # $1000测试
python main_live.py --config configs/live_small_config.json
```

### 3. 正式实盘部署
```bash
# 完整资金实盘
export TRADING_MODE=live
python main_live.py --config configs/live_production_config.json
```

## ⚠️ 重要警告

### 法律与合规
1. **证券交易许可**：确保您有权在目标市场进行交易
2. **API使用协议**：遵守券商API使用条款
3. **税务申报**：交易收益需依法纳税
4. **风险披露**：算法交易可能导致重大损失

### 技术风险
1. **网络延迟**：可能导致价格滑点
2. **API限流**：超过调用频率可能被封禁
3. **系统故障**：需要监控和告警机制
4. **数据质量**：实时数据可能有延迟或错误

### 建议实践
- ✅ 先在纸上交易环境充分测试
- ✅ 设置严格的止损和仓位限制
- ✅ 使用小额资金验证策略
- ✅ 持续监控系统运行状态
- ✅ 保留人工干预能力

## 📈 监控和可观测性

### 关键指标
- 交易延迟（下单到成交）
- API调用成功率
- 持仓与预期偏差
- 风控拦截次数
- 日收益/亏损

### 监控工具
- Prometheus + Grafana（指标可视化）
- ELK Stack（日志分析）
- 自定义Dashboard（交易面板）

## 🔄 系统扩展性

### 支持新交易所
```python
# 1. 实现Provider接口
class NewExchangeProvider(MarketDataProvider):
    pass

# 2. 实现Broker接口
class NewExchangeBroker(BaseBroker):
    pass

# 3. 配置文件注册
"broker_type": "new_exchange"
```

### 支持新策略
- 插件化策略系统
- 策略回测框架
- 策略性能对比

## 📚 参考资源

### API文档
- [Alpaca API](https://alpaca.markets/docs/)
- [Binance API](https://binance-docs.github.io/apidocs/)
- [Interactive Brokers API](https://www.interactivebrokers.com/api/)

### 风险管理
- [算法交易风险管理指南](https://www.sec.gov/files/Algo_Trading_Report_2020.pdf)
- OWASP API安全最佳实践

---

**版本**: 1.0.0
**更新日期**: 2025-11-13
**负责人**: AI-Trader Team
