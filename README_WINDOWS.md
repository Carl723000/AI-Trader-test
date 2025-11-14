# AI-Trader Windows 用户指南

> **专为Windows用户和Python新手设计的完整部署方案**

---

## 🎯 快速导航

| 你是... | 推荐开始 | 预计时间 |
|--------|---------|---------|
| 🆕 完全新手 | [5分钟快速开始](QUICKSTART.md) | 5分钟 |
| 📚 想了解详情 | [Windows详细指南](docs/WINDOWS_SETUP_GUIDE.md) | 30分钟 |
| ⚙️ 需要配置参数 | [参数配置参考](docs/PARAMETER_REFERENCE.md) | 60分钟 |
| 🔧 遇到问题 | [故障诊断](#故障诊断) | 10分钟 |

---

## 📦 一键安装流程

### 视频教程般的步骤说明

#### 1️⃣ 安装Python（如果还没有）

**检查方法**：
```cmd
按Win+R → 输入cmd → 回车
输入：python --version
```

**如果显示版本号**，说明已安装，跳到第2步 ✅

**如果提示错误**，需要安装：

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.11（推荐）或更高版本
3. 运行安装程序
4. ⚠️ **关键步骤**：勾选 "Add Python to PATH" ✅
5. 点击 "Install Now"
6. 等待安装完成

![Python安装](https://user-images.githubusercontent.com/example/python-install.png)

#### 2️⃣ 下载项目

**方式A：从GitHub下载**
1. 点击绿色按钮 "Code" → "Download ZIP"
2. 解压到合适的位置（如 `D:\AI-Trader`）

**方式B：使用Git**（如果已安装）
```cmd
git clone https://github.com/your-repo/AI-Trader-test.git
cd AI-Trader-test
```

#### 3️⃣ 双击安装

找到并双击运行：
```
install.bat
```

等待安装完成（约2-5分钟），您会看到：

```
🎉 安装完成！

下一步操作：
1. 编辑配置文件：D:\AI-Trader\.env
2. 运行配置向导：config_wizard.bat
3. 测试连接：test_connection.bat
4. 开始Paper Trading：start_paper_trading.bat
```

#### 4️⃣ 配置系统

双击运行：
```
config_wizard.bat
```

按屏幕提示操作：

**第1步**：选择交易平台
```
1. Alpaca Markets（美股）⭐ 推荐新手
2. Binance（加密货币）

请输入选项 (1 或 2): 1
```

**第2步**：选择交易模式
```
1. Paper Trading（模拟交易）⭐ 推荐新手
2. Live Trading（真实交易）⚠️ 谨慎使用

请输入选项 (1 或 2): 1
```

**第3步**：输入API密钥

需要两类API密钥：

**A. 交易平台API密钥**

- **Alpaca Paper Trading**（推荐）
  - 注册：https://alpaca.markets/
  - 免费，无需真实资金
  - Dashboard → API Keys → Paper Trading
  - 复制 API Key 和 Secret Key

- **Binance Testnet**（加密货币）
  - 访问：https://testnet.binance.vision/
  - GitHub登录即可
  - 免费测试币

**B. AI模型API密钥**

推荐：**OpenAI GPT-4**
- 注册：https://platform.openai.com/
- API Keys → Create new secret key
- 复制密钥（以`sk-`开头）
- 充值$10-20即可开始

其他选择：
- Claude：https://console.anthropic.com/
- DeepSeek：https://platform.deepseek.com/（国内可用）

**第4步**：选择风险级别
```
1. 保守型（推荐新手）⭐
2. 平衡型
3. 激进型
4. 自定义

请选择风险级别 (1-4): 1
```

配置完成后，系统会自动生成所有必需的配置文件。

#### 5️⃣ 测试连接

双击运行：
```
test_connection.bat
```

**成功的标志**：
```
🧪 AI-Trader Live Trading Connection Test
========================================

✅ Broker connection successful
💰 Buying Power: $100000.00
✅ Data provider connection successful
📈 Price: $226.45

🎉 All tests passed! You're ready for live trading.
```

如果看到 ❌ 错误，请查看[故障诊断](#故障诊断)部分。

#### 6️⃣ 开始Paper Trading

双击运行：
```
start_paper_trading.bat
```

**正常运行的标志**：
```
========================================
AI-Trader Paper Trading（模拟交易）
========================================

📊 平台：Alpaca Markets（美股）
💰 模式：Paper Trading（虚拟资金）

✅ Connected to alpaca broker (paper mode)
💰 Buying Power: $100000.00
🚀 Starting live trading agent...

--- Iteration 1 ---
💭 AI response: 正在分析市场...
```

**停止方法**：按 `Ctrl + C`

---

## 📁 文件结构（简化版）

```
AI-Trader-test/
│
├── 📝 批处理脚本（双击运行）
│   ├── install.bat ⭐ 一键安装
│   ├── config_wizard.bat ⭐ 配置向导
│   ├── test_connection.bat ⭐ 测试连接
│   ├── start_paper_trading.bat ⭐ 模拟交易
│   ├── start_live_trading.bat ⚠️ 真实交易
│   └── diagnose.bat 🔧 故障诊断
│
├── 📚 文档
│   ├── QUICKSTART.md - 5分钟快速开始
│   ├── WINDOWS_SETUP_GUIDE.md - Windows详细指南
│   ├── PARAMETER_REFERENCE.md - 参数配置参考
│   └── LIVE_TRADING_GUIDE.md - 完整使用手册
│
├── ⚙️ 配置文件（自动生成）
│   ├── .env - 环境变量
│   └── configs/
│       ├── live_config.json - Alpaca配置
│       └── live_binance_config.json - Binance配置
│
└── 📊 数据目录（自动创建）
    └── data/
        ├── live_logs/ - 交易日志
        ├── risk_logs/ - 风控记录
        └── position_logs/ - 持仓记录
```

---

## 🛡️ 风险管理

### 新手推荐配置（保守型）

系统默认使用保守配置：

| 参数 | 值 | 说明 |
|------|---|------|
| 单笔最大 | 5% | 单次买入不超过资金5% |
| 持仓最大 | 15% | 单只股票不超过15% |
| 日最大交易 | 10笔 | 每天最多10笔交易 |
| 日最大亏损 | 2% | 亏损达2%自动停止 |

### 安全检查清单

**开始交易前**：
- [ ] ✅ 在Paper Trading模式测试至少1周
- [ ] ✅ 理解AI的交易逻辑
- [ ] ✅ 设置保守的风险参数
- [ ] ✅ 阅读使用文档
- [ ] ✅ 只投入可承受损失的资金

**运行中监控**：
- [ ] ✅ 定期查看交易日志
- [ ] ✅ 监控账户余额变化
- [ ] ✅ 检查风控拦截记录
- [ ] ✅ 注意异常告警

---

## 🆘 故障诊断

### 问题1：Python命令不可用

**症状**：
```
'python' 不是内部或外部命令
```

**解决方案**：
1. 重新安装Python
2. ⚠️ 必须勾选 "Add Python to PATH"
3. 或手动添加PATH（见[详细指南](docs/WINDOWS_SETUP_GUIDE.md#q1)）

### 问题2：依赖安装失败

**症状**：
```
ERROR: Could not install packages
```

**解决方案**：
```cmd
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3：连接测试失败

**症状**：
```
❌ Broker connection failed
```

**检查清单**：
1. API密钥是否正确（没有多余空格）
2. 网络连接是否正常
3. 防火墙是否阻止

**运行诊断工具**：
```
双击：diagnose.bat
```

### 问题4：.env文件无法创建

**Windows特殊问题**：Windows不允许创建没有文件名的文件

**解决方案**：
```cmd
# 使用命令行
copy .env.live.example .env

# 或用记事本
1. 打开记事本
2. 保存时文件名填：.env
3. 文件类型选：所有文件 (*.*)
```

### 问题5：AI不执行交易

**可能原因**：
1. 市场条件不符合AI判断
2. 风控参数过严
3. AI判断当前不应交易

**排查方法**：
```cmd
# 查看日志
type data\live_logs\trading.log

# 查看最后50行
powershell -command "Get-Content data\live_logs\trading.log -Tail 50"
```

### 完整诊断工具

运行完整诊断：
```
双击：diagnose.bat
```

工具会自动检查：
- ✅ Python环境
- ✅ 依赖包
- ✅ 配置文件
- ✅ API密钥
- ✅ 网络连接
- ✅ 目录结构

并提供修复建议。

---

## 📊 查看交易结果

### 实时监控

**查看日志**：
```
打开文件夹：data\live_logs\
查看文件：trading.log
```

**用记事本打开**，或使用：
```cmd
type data\live_logs\trading.log
```

### 关键日志位置

```
data/
├── live_logs/
│   ├── trading.log - 主日志
│   └── risk_checks_*.jsonl - 风控记录
├── risk_logs/
│   └── risk_state.json - 风控状态
└── position_logs/
    └── positions_*.jsonl - 持仓变化
```

### 查看账户状态

在Python中运行：
```python
python test_live_connection.py
```

会显示：
- 💰 账户余额
- 📊 当前持仓
- 💵 可用资金

---

## 🚀 从Paper Trading到Live Trading

### 建议流程

```
第1周：Paper Trading + 学习系统
  ↓
第2周：Paper Trading + 优化参数
  ↓
第3周：Paper Trading + 最终验证
  ↓
第4周：Live Trading（小额$100-1000）
  ↓
稳定后：逐步增加资金
```

### 切换到Live Trading

**步骤**：

1. **确认准备就绪**
   - [ ] Paper Trading盈利至少2周
   - [ ] 理解AI决策逻辑
   - [ ] 设置严格风控参数

2. **获取Live API密钥**
   - Alpaca: Dashboard → Live Trading API
   - 注意：需要存入资金

3. **修改配置**

编辑 `.env` 文件：
```bash
TRADING_MODE=live
ALPACA_API_KEY=AK... (Live密钥，不是PK开头)
ALPACA_API_SECRET=... (Live密钥)
```

编辑 `configs/live_config.json`：
```json
{
  "trading_mode": "live",
  ...
}
```

4. **小额测试**
   - 建议先用$100-1000
   - 观察1-2周
   - 确认稳定后再增加

5. **启动Live Trading**
```
双击：start_live_trading.bat
```

系统会要求确认：
```
⚠️⚠️⚠️ 警告 ⚠️⚠️⚠️
您即将启动真实交易模式！
这将使用真实资金进行交易！

确认启动真实交易？(输入 YES 继续): YES
```

---

## 💡 使用技巧

### 1. 创建桌面快捷方式

常用脚本创建快捷方式：
1. 右键拖动 `.bat` 文件到桌面
2. 选择"在此处创建快捷方式"
3. 重命名为易识别的名称

推荐创建：
- "AI交易-配置" → `config_wizard.bat`
- "AI交易-测试" → `test_connection.bat`
- "AI交易-模拟" → `start_paper_trading.bat`

### 2. 定时自动运行

如果要让系统每天自动交易：

1. `Win + R` → 输入 `taskschd.msc`
2. 创建基本任务
3. 触发器：每天上午9点
4. 操作：启动程序
   - 程序：`cmd.exe`
   - 参数：`/c "D:\AI-Trader\start_paper_trading.bat"`

⚠️ 仅在充分测试后使用自动运行！

### 3. 查看实时日志

使用PowerShell：
```powershell
Get-Content data\live_logs\trading.log -Wait -Tail 50
```

相当于Linux的 `tail -f`

### 4. 备份配置

定期备份重要文件：
```
.env
configs/live_config.json
data/risk_logs/risk_state.json
```

### 5. 多账户管理

可以创建多个配置文件：
```
configs/
├── live_config_conservative.json  # 保守策略
├── live_config_aggressive.json    # 激进策略
└── live_config_test.json          # 测试策略
```

运行时指定：
```cmd
python main_live.py configs\live_config_conservative.json
```

---

## 📚 学习资源

### 文档阅读顺序

1. **入门**（第1天）
   - ✅ [QUICKSTART.md](QUICKSTART.md) - 快速上手
   - ✅ 本文档 - 完整Windows指南

2. **深入**（第2-3天）
   - 📖 [WINDOWS_SETUP_GUIDE.md](docs/WINDOWS_SETUP_GUIDE.md) - 详细部署
   - 📖 [PARAMETER_REFERENCE.md](docs/PARAMETER_REFERENCE.md) - 参数详解

3. **进阶**（第4-7天）
   - 📖 [LIVE_TRADING_GUIDE.md](docs/LIVE_TRADING_GUIDE.md) - 完整指南
   - 📖 [LIVE_TRADING_ARCHITECTURE.md](docs/LIVE_TRADING_ARCHITECTURE.md) - 架构文档

### 推荐学习路径

```
Day 1: 安装和配置 → Paper Trading
  ↓
Day 2-3: 观察AI决策 → 理解逻辑
  ↓
Day 4-7: 阅读文档 → 学习参数
  ↓
Week 2: 调整参数 → 优化策略
  ↓
Week 3-4: 持续测试 → 验证稳定性
  ↓
Month 2: 小额实盘 → 真实验证
```

---

## ⚡ 性能优化

### 提升运行速度

1. **使用SSD硬盘**
   - 日志写入更快

2. **增加Python进程优先级**
   - 任务管理器 → 详细信息
   - 右键Python进程 → 设置优先级 → 高

3. **优化AI模型选择**
   - GPT-3.5: 更快、更便宜
   - GPT-4: 更强、更慢

4. **调整循环间隔**
   ```json
   "iteration_wait_seconds": 30  // 从60秒减少到30秒
   ```

---

## 🔒 安全建议

### API密钥安全

1. **不要分享**：绝不分享API密钥
2. **定期轮换**：每月更换一次
3. **权限最小化**：只开启必需权限
4. **IP白名单**：绑定固定IP（如果支持）

### 资金安全

1. **小额开始**：$100-1000测试
2. **分散平台**：不要把所有资金放一个平台
3. **设置止损**：严格的亏损限制
4. **定期提现**：将盈利定期提出

### 系统安全

1. **杀毒软件**：保持更新
2. **防火墙**：开启Windows防火墙
3. **备份数据**：定期备份配置和日志
4. **更新系统**：保持Windows更新

---

## 🆘 获取帮助

### 自助排查

1. **运行诊断**
   ```
   diagnose.bat
   ```

2. **查看日志**
   ```
   data\live_logs\trading.log
   ```

3. **查阅文档**
   - [常见问题](docs/WINDOWS_SETUP_GUIDE.md#常见问题)
   - [参数说明](docs/PARAMETER_REFERENCE.md)

### 社区支持

- 📧 GitHub Issues
- 💬 讨论组（如果有）
- 📖 官方文档

---

## ✅ 完成检查清单

### 安装检查

- [ ] Python 3.8+ 已安装
- [ ] 运行 `install.bat` 成功
- [ ] 所有依赖包已安装
- [ ] 目录结构完整

### 配置检查

- [ ] 运行 `config_wizard.bat` 完成
- [ ] `.env` 文件已创建
- [ ] API密钥已填写
- [ ] 配置JSON文件已更新

### 测试检查

- [ ] 运行 `test_connection.bat` 通过
- [ ] 连接broker成功
- [ ] 连接data provider成功
- [ ] 能获取价格数据

### 交易检查

- [ ] Paper Trading运行正常
- [ ] AI有交易决策输出
- [ ] 日志文件正常生成
- [ ] 理解风险参数含义

---

## 🎉 恭喜！

如果您完成了上述所有步骤，现在您已经：

✅ 成功部署了AI-Trader实时交易系统
✅ 配置了Paper Trading环境
✅ 理解了基本的运行原理
✅ 掌握了故障诊断方法

**下一步建议**：

1. 📊 运行Paper Trading 1-2周
2. 📖 深入阅读参数配置文档
3. ⚙️ 根据表现调整参数
4. 💰 考虑小额实盘测试

**记住**：交易有风险，投资需谨慎！

---

**祝您使用顺利，交易成功！** 🚀

有问题随时查阅文档或运行诊断工具。
