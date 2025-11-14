# AI-Trader Windows 部署指南

> **适用对象**：熟悉MATLAB但缺乏Python经验的用户
> **操作系统**：Windows 10/11
> **难度级别**：⭐ 初级（按步骤操作即可）

---

## 📋 目录

1. [前期准备](#前期准备)
2. [5分钟快速安装](#5分钟快速安装)
3. [详细安装步骤](#详细安装步骤)
4. [配置说明](#配置说明)
5. [常见问题](#常见问题)
6. [附录](#附录)

---

## 前期准备

### 必需软件

#### 1. Python 3.8+

**检查是否已安装**：
1. 按 `Win + R`
2. 输入 `cmd`，回车
3. 输入 `python --version`

如果显示版本号（如 `Python 3.11.5`），说明已安装。

**如何安装**：
1. 访问 https://www.python.org/downloads/
2. 点击 "Download Python 3.11.x"（最新版本）
3. 运行下载的安装程序
4. **重要**：勾选 "Add Python to PATH" ✅
5. 点击 "Install Now"
6. 等待安装完成

![Python安装](https://docs.python.org/3/_images/win_installer.png)

**验证安装**：
```cmd
python --version
pip --version
```

两个命令都应该显示版本号。

#### 2. 文本编辑器

推荐任选其一：
- **记事本**（Windows自带）- 适合简单编辑
- **Notepad++** - https://notepad-plus-plus.org/
- **VS Code** - https://code.visualstudio.com/

#### 3. 网络要求

需要稳定的网络连接以：
- 下载Python依赖包
- 访问交易平台API
- 获取实时市场数据

---

## 5分钟快速安装

### 方案A：双击安装（推荐新手）

1. **下载项目**
   - 下载整个项目文件夹到本地（如 `D:\AI-Trader`）

2. **运行安装程序**
   - 双击 `install.bat`
   - 等待安装完成（约2-5分钟）

3. **运行配置向导**
   - 双击 `config_wizard.bat`
   - 按提示输入配置信息

4. **测试连接**
   - 双击 `test_connection.bat`
   - 检查是否连接成功

5. **开始使用**
   - 双击 `start_paper_trading.bat`
   - 开始模拟交易！

### 方案B：命令行安装（熟悉终端者）

```cmd
# 1. 进入项目目录
cd D:\AI-Trader

# 2. 安装依赖
install.bat

# 3. 配置系统
config_wizard.bat

# 4. 测试连接
test_connection.bat

# 5. 启动
start_paper_trading.bat
```

---

## 详细安装步骤

### 步骤1: 下载项目

#### 方式1：从GitHub下载

1. 访问项目页面
2. 点击绿色按钮 "Code"
3. 选择 "Download ZIP"
4. 解压到本地目录（如 `D:\AI-Trader`）

#### 方式2：使用Git（如果已安装）

```cmd
git clone https://github.com/your-repo/AI-Trader-test.git
cd AI-Trader-test
```

### 步骤2: 安装Python依赖

#### 自动安装（推荐）

双击运行 `install.bat`，安装程序会自动：
- 检查Python环境
- 安装所有依赖包
- 创建必要的目录
- 生成配置文件模板

#### 手动安装

如果自动安装失败，可以手动执行：

```cmd
# 1. 打开命令提示符
# Win + R → 输入 cmd → 回车

# 2. 进入项目目录
cd D:\AI-Trader

# 3. 升级pip
python -m pip install --upgrade pip

# 4. 安装依赖
pip install -r requirements.txt

# 如果安装很慢，使用国内镜像：
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**依赖包列表**：
```
langchain==1.0.2          # AI Agent框架
langchain-openai==1.0.1   # OpenAI集成
aiohttp>=3.9.0            # 异步HTTP客户端
python-dotenv>=1.0.0      # 环境变量管理
pandas>=2.0.0             # 数据处理
numpy>=1.24.0             # 数值计算
```

### 步骤3: 注册交易平台账户

您需要至少注册一个交易平台。

#### 选项A：Alpaca Markets（美股）

**推荐用途**：美国股票交易

**注册步骤**：
1. 访问 https://alpaca.markets/
2. 点击 "Sign Up"
3. 填写邮箱、密码
4. 验证邮箱
5. 完成基本信息（可选实盘交易）

**获取Paper Trading API密钥**：
1. 登录后进入 Dashboard
2. 左侧菜单选择 "Your API Keys"
3. 在 "Paper Trading" 区域点击 "View"
4. 复制 **API Key** 和 **Secret Key**
5. ⚠️ Secret Key只显示一次，请妥善保存

**特点**：
- ✅ Paper Trading完全免费
- ✅ 0佣金交易
- ✅ 支持国际用户
- ✅ 实时美股数据
- ❌ 只能交易美股

#### 选项B：Binance（加密货币）

**推荐用途**：比特币、以太坊等加密货币

**Testnet注册（推荐测试）**：
1. 访问 https://testnet.binance.vision/
2. 用GitHub账号登录
3. 点击 "Generate HMAC_SHA256 Key"
4. 复制 **API Key** 和 **Secret Key**
5. 领取测试USDT（用于测试交易）

**正式账户注册**：
1. 访问 https://www.binance.com/
2. 注册账户
3. 完成身份验证（KYC）
4. 个人中心 → API管理 → 创建API
5. 权限设置：
   - ✅ 启用读取
   - ✅ 启用现货交易
   - ❌ 禁用提现（安全）
6. 绑定IP白名单（推荐）

**特点**：
- ✅ 24/7交易
- ✅ Testnet完全免费
- ✅ 支持多种加密货币
- ⚠️ 需要KYC验证（正式账户）

### 步骤4: 获取AI模型API密钥

系统需要AI模型来做交易决策。

#### OpenAI GPT-4（推荐）

**注册步骤**：
1. 访问 https://platform.openai.com/
2. 注册/登录账户
3. 进入 API Keys 页面
4. 点击 "Create new secret key"
5. 为密钥命名（如 "AI-Trader"）
6. 复制密钥（以 `sk-` 开头）

**费用**：按使用量计费
- GPT-4: $0.03/1K tokens (输入)
- GPT-3.5: $0.0015/1K tokens
- 建议充值$10-20测试

#### Anthropic Claude

**注册步骤**：
1. 访问 https://console.anthropic.com/
2. 注册账户
3. API Keys → Create Key
4. 复制密钥

**费用**：
- Claude 3.5: $0.003/1K tokens

#### DeepSeek（国内可用）

**注册步骤**：
1. 访问 https://platform.deepseek.com/
2. 注册账户
3. API Keys → Create
4. 复制密钥

**优势**：
- ✅ 国内可直接访问
- ✅ 价格便宜
- ✅ 中文支持好

### 步骤5: 配置系统

#### 方式1：配置向导（推荐）

双击运行 `config_wizard.bat`，按提示操作：

**屏幕示例**：

```
========================================
[步骤 1/5] 选择交易平台
========================================

请选择您要使用的交易平台：

1. Alpaca Markets（美股）
2. Binance（加密货币）

请输入选项 (1 或 2): 1

========================================
[步骤 2/5] 选择交易模式
========================================

请选择交易模式：

1. Paper Trading（模拟交易）⭐ 推荐新手
2. Live Trading（真实交易）⚠️ 谨慎使用

请输入选项 (1 或 2): 1

... (继续按提示操作)
```

配置向导会自动：
- 生成 `.env` 文件
- 更新配置JSON文件
- 设置风险参数

#### 方式2：手动编辑配置文件

如果向导无法运行，手动编辑：

**1. 创建 `.env` 文件**

在项目根目录创建 `.env` 文件（没有文件名，只有扩展名）：

**Windows创建方法**：
- 方法1：复制 `.env.live.example` 并重命名为 `.env`
- 方法2：用记事本创建，保存时文件名填 `.env`，文件类型选"所有文件"

**配置内容**：

```bash
# AI模型API
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-actual-api-key-here

# Alpaca API（如果使用）
ALPACA_API_KEY=PKxxxxxxxxxxxxxxxxx
ALPACA_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Binance API（如果使用）
BINANCE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
BINANCE_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 交易配置
BROKER_TYPE=alpaca
TRADING_MODE=paper
```

**2. 编辑配置JSON**

编辑 `configs/live_config.json`（Alpaca）或 `configs/live_binance_config.json`（Binance）：

```json
{
  "trading_mode": "paper",
  "broker_type": "alpaca",

  "model": {
    "name": "gpt-4",
    "basemodel": "gpt-4",
    "enabled": true
  },

  "risk_controls": {
    "max_single_trade_pct": 0.10,
    "max_position_pct": 0.30,
    "max_daily_trades": 50,
    "max_daily_loss_pct": 0.05
  }
}
```

### 步骤6: 测试连接

运行连接测试：

```cmd
# 方式1：双击
test_connection.bat

# 方式2：命令行
python test_live_connection.py
```

**成功示例**：

```
🧪 AI-Trader Live Trading Connection Test
========================================

========================================
Testing Alpaca Connection
========================================

📋 API Key: PKxxxxxx...

🔌 Testing broker connection...
✅ Broker connection successful
💰 Buying Power: $100000.00
📊 Current Positions: 0

🔌 Testing data provider...
✅ Data provider connection successful

📈 Testing price retrieval for AAPL...
✅ Price: $226.45
   Volume: 12,345,678
   Time: 2025-11-13 14:30:00

✅ Alpaca test completed successfully!

========================================
Test Summary
========================================
ALPACA: ✅ PASS

🎉 All tests passed! You're ready for live trading.
```

**如果失败**：
- 检查网络连接
- 确认API密钥正确
- 运行诊断工具：`diagnose.bat`

---

## 配置说明

### 核心配置参数

#### 1. 交易平台配置

```bash
# .env文件

# 选择平台：alpaca 或 binance
BROKER_TYPE=alpaca

# 选择模式：paper（模拟）或 live（真实）
TRADING_MODE=paper
```

#### 2. 风险管理参数

在 `configs/live_config.json` 中设置：

```json
{
  "risk_controls": {
    "max_single_trade_pct": 0.10,
    "max_position_pct": 0.30,
    "max_daily_trades": 50,
    "max_daily_loss_pct": 0.05
  }
}
```

**参数说明**：

| 参数 | 含义 | 推荐值（新手） | 说明 |
|------|------|----------------|------|
| `max_single_trade_pct` | 单笔最大交易比例 | 0.05 (5%) | 单次买入不超过总资金的5% |
| `max_position_pct` | 单只股票最大持仓 | 0.15 (15%) | 单只股票持仓不超过总资金的15% |
| `max_daily_trades` | 日最大交易次数 | 10-20 | 防止过度交易 |
| `max_daily_loss_pct` | 日最大亏损比例 | 0.02 (2%) | 单日亏损达2%自动停止 |

**风险等级对照表**：

```
保守型（推荐新手）:
  max_single_trade_pct: 0.05   (5%)
  max_position_pct: 0.15        (15%)
  max_daily_trades: 10
  max_daily_loss_pct: 0.02      (2%)

平衡型:
  max_single_trade_pct: 0.10   (10%)
  max_position_pct: 0.30        (30%)
  max_daily_trades: 30
  max_daily_loss_pct: 0.05      (5%)

激进型（不推荐新手）:
  max_single_trade_pct: 0.15   (15%)
  max_position_pct: 0.40        (40%)
  max_daily_trades: 50
  max_daily_loss_pct: 0.10      (10%)
```

#### 3. AI模型配置

```json
{
  "model": {
    "name": "gpt-4",
    "basemodel": "gpt-4",
    "enabled": true
  }
}
```

**可选模型**：
- `gpt-4` - OpenAI GPT-4（最强）
- `gpt-3.5-turbo` - GPT-3.5（便宜）
- `claude-3.7-sonnet` - Anthropic Claude
- `deepseek-chat` - DeepSeek（国内）

#### 4. 交易循环配置

```json
{
  "trading_config": {
    "max_iterations": 1000,
    "iteration_wait_seconds": 60
  }
}
```

**参数说明**：
- `max_iterations`: 最大循环次数（防止无限运行）
- `iteration_wait_seconds`: 每次决策间隔（秒）

**建议设置**：
- Day Trading（日内交易）：60秒
- Swing Trading（摆动交易）：300-600秒（5-10分钟）
- Position Trading（持仓交易）：3600秒（1小时）

---

## 常见问题

### 安装问题

#### Q1: Python安装后，命令行输入`python`提示"不是内部或外部命令"

**原因**：Python未添加到系统PATH

**解决方案**：

方法1（推荐）：重新安装Python
1. 卸载当前Python
2. 重新下载安装
3. ✅ 勾选 "Add Python to PATH"

方法2：手动添加PATH
1. 找到Python安装路径（如 `C:\Users\用户名\AppData\Local\Programs\Python\Python311`）
2. 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
3. 在"系统变量"中找到"Path"，点击编辑
4. 添加两个路径：
   - `C:\Users\用户名\AppData\Local\Programs\Python\Python311`
   - `C:\Users\用户名\AppData\Local\Programs\Python\Python311\Scripts`
5. 确定，重新打开命令提示符

#### Q2: pip install时报错"SSL Certificate Error"

**原因**：网络问题或防火墙

**解决方案**：

```cmd
# 方法1：使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方法2：临时禁用SSL验证（不推荐）
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### Q3: 安装时提示"Microsoft Visual C++ is required"

**原因**：缺少C++运行库（某些包需要）

**解决方案**：
1. 下载安装 Visual C++ Redistributable
2. 访问 https://aka.ms/vs/17/release/vc_redist.x64.exe
3. 安装后重新运行 `install.bat`

### 配置问题

#### Q4: 创建.env文件时，Windows不允许创建没有文件名的文件

**解决方案**：

方法1：使用命令行
```cmd
copy .env.live.example .env
```

方法2：用记事本
1. 打开记事本
2. 保存文件
3. 文件名填：`.env`（包含点号）
4. 文件类型选：`所有文件 (*.*)`
5. 保存

方法3：重命名
1. 复制 `.env.live.example`
2. 重命名为 `.env.txt`
3. 再删除 `.txt` 扩展名

#### Q5: 编辑.env文件后，系统还是提示API密钥未配置

**可能原因**：
1. .env文件保存有误
2. 路径不对（需要在项目根目录）
3. 文件编码问题

**检查方法**：
```cmd
# 在项目目录运行
type .env

# 应该显示文件内容
# 如果提示找不到文件，说明位置不对
```

**解决方案**：
1. 确保.env在项目根目录（与install.bat同级）
2. 用记事本打开，检查内容
3. 保存时选择UTF-8编码

### 运行问题

#### Q6: 运行start_paper_trading.bat后立即关闭

**原因**：Python脚本出错

**查看错误**：
```cmd
# 在命令提示符中运行，可以看到错误信息
cd D:\AI-Trader
python main_live.py configs\live_config.json
```

常见错误：
- `ModuleNotFoundError`: 依赖未安装，运行 `install.bat`
- `API key not found`: 检查 `.env` 文件
- `Connection error`: 检查网络和防火墙

#### Q7: API连接测试失败

**排查步骤**：

1. 检查网络
```cmd
ping api.alpaca.markets
ping api.binance.com
```

2. 检查API密钥
- 确认复制正确（没有多余空格）
- 确认密钥未过期
- 确认权限设置正确

3. 检查防火墙
- 临时关闭防火墙测试
- 添加Python到防火墙白名单

4. 使用诊断工具
```cmd
diagnose.bat
```

#### Q8: AI不执行任何交易

**可能原因**：
1. 市场条件不符合AI策略
2. 风控参数过于严格
3. AI判断当前不应交易
4. API额度不足

**排查方法**：

查看日志：
```cmd
type data\live_logs\trading.log
```

查看最近的AI决策：
```cmd
# 最后50行
powershell -command "Get-Content data\live_logs\trading.log -Tail 50"
```

调整风控参数（如果确认是风控原因）：
- 增加 `max_single_trade_pct`
- 增加 `max_position_pct`

#### Q9: 真实交易模式无法启动

**检查清单**：

1. `.env` 中 `TRADING_MODE=live` ✅
2. 使用正式账户的API密钥（不是Paper Trading密钥）✅
3. 账户有足够余额 ✅
4. API权限包含交易权限 ✅
5. 已在Paper Trading充分测试 ✅

**安全提示**：
- 建议先用小额资金（$100-1000）
- 设置严格的风控参数
- 持续监控系统运行

---

## 附录

### A. 文件结构说明

```
AI-Trader-test/
│
├── install.bat                  ⭐ 一键安装脚本
├── config_wizard.bat            ⭐ 配置向导
├── test_connection.bat          ⭐ 连接测试
├── start_paper_trading.bat      ⭐ 启动Paper Trading
├── start_live_trading.bat       ⭐ 启动Live Trading
├── diagnose.bat                 ⭐ 故障诊断
│
├── .env                         🔑 环境变量配置（需创建）
├── .env.live.example            📄 配置模板
├── requirements.txt             📦 依赖列表
│
├── main_live.py                 🐍 实时交易主程序
├── test_live_connection.py      🐍 连接测试程序
│
├── configs/                     ⚙️ 配置文件目录
│   ├── live_config.json         - Alpaca配置
│   └── live_binance_config.json - Binance配置
│
├── agent_tools/                 🔧 工具模块
│   ├── providers/               - 数据提供商
│   ├── brokers/                 - 券商接口
│   ├── tool_trade_live.py       - 实时交易工具
│   └── tool_get_price_live.py   - 实时价格工具
│
├── risk_management/             🛡️ 风险管理
│   ├── risk_manager.py
│   ├── risk_rules.py
│   └── position_monitor.py
│
├── data/                        📊 数据目录
│   ├── live_logs/               - 交易日志
│   ├── risk_logs/               - 风控日志
│   └── position_logs/           - 持仓日志
│
└── docs/                        📚 文档目录
    ├── WINDOWS_SETUP_GUIDE.md   - 本文档
    ├── LIVE_TRADING_GUIDE.md    - 详细指南
    └── LIVE_TRADING_ARCHITECTURE.md
```

### B. 快捷方式创建

为常用批处理文件创建桌面快捷方式：

1. 右键拖动`.bat`文件到桌面
2. 选择"在此处创建快捷方式"
3. 重命名快捷方式（如"AI交易-Paper Trading"）

推荐创建快捷方式：
- `config_wizard.bat` → "配置AI交易系统"
- `test_connection.bat` → "测试交易连接"
- `start_paper_trading.bat` → "启动模拟交易"
- `diagnose.bat` → "系统诊断工具"

### C. 计划任务设置（自动运行）

如果想让系统定时自动交易：

1. 按 `Win + R`，输入 `taskschd.msc`
2. 右侧点击"创建基本任务"
3. 名称：AI-Trader自动交易
4. 触发器：选择运行频率（如每天上午9点）
5. 操作：启动程序
   - 程序/脚本：`cmd.exe`
   - 添加参数：`/c "D:\AI-Trader\start_paper_trading.bat"`
6. 完成

**注意**：仅在充分测试后使用自动运行！

### D. 日志查看技巧

#### 实时查看日志

使用PowerShell：
```powershell
Get-Content data\live_logs\trading.log -Wait -Tail 50
```

#### 搜索关键词

```powershell
# 搜索包含"buy"的行
Select-String -Path data\live_logs\trading.log -Pattern "buy"

# 搜索错误
Select-String -Path data\live_logs\trading.log -Pattern "error|Error|ERROR"
```

#### 查看风控记录

```cmd
type data\live_logs\risk_checks_2025-11-13.jsonl
```

### E. 升级和更新

#### 更新Python依赖

```cmd
pip install --upgrade -r requirements.txt
```

#### 更新项目代码

如果从Git克隆：
```cmd
cd D:\AI-Trader
git pull
```

如果是ZIP下载：
1. 备份`.env`文件和`configs/`目录
2. 下载新版本
3. 解压并覆盖
4. 恢复`.env`和配置文件

### F. 卸载

如果需要完全移除：

1. 删除项目目录
```cmd
rd /s /q D:\AI-Trader
```

2. 卸载Python依赖（可选）
```cmd
pip uninstall -r requirements.txt -y
```

3. 卸载Python（可选）
   - 控制面板 → 程序和功能 → 卸载Python

---

## 🆘 获取帮助

如果遇到无法解决的问题：

1. **运行诊断工具**
   ```cmd
   diagnose.bat
   ```

2. **查看日志**
   ```cmd
   type data\live_logs\trading.log
   ```

3. **查看文档**
   - [详细使用指南](LIVE_TRADING_GUIDE.md)
   - [架构文档](LIVE_TRADING_ARCHITECTURE.md)

4. **常见问题**
   - 本文档"常见问题"部分

---

## ✅ 检查清单

部署前检查：

- [ ] Python 3.8+ 已安装
- [ ] 依赖包全部安装成功
- [ ] 已注册交易平台账户
- [ ] 已获取API密钥
- [ ] `.env` 文件配置正确
- [ ] 连接测试通过
- [ ] 理解风险管理参数
- [ ] 阅读使用文档

开始交易前检查：

- [ ] 在Paper Trading模式测试至少1周
- [ ] 设置保守的风控参数
- [ ] 准备小额资金测试（$100-1000）
- [ ] 理解可能的财务风险
- [ ] 设置监控和告警

---

**祝您使用顺利！如有问题，请参考本指南或运行诊断工具。** 🚀
