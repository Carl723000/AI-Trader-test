# AI-Trader Windows 快速开始指南

> **5分钟快速上手** - 适合新手的最简化部署流程

---

## 🚀 三步开始

### 第1步：安装Python

1. 下载Python：https://www.python.org/downloads/
2. 运行安装程序
3. **重要**：✅ 勾选 "Add Python to PATH"
4. 点击 "Install Now"

**验证安装**：
```cmd
python --version
```
应显示：`Python 3.11.x` 或更高版本

---

### 第2步：安装系统

1. **下载项目**
   - 解压到文件夹（如 `D:\AI-Trader`）

2. **双击运行**
   ```
   install.bat
   ```
   等待2-5分钟安装完成

---

### 第3步：配置系统

**双击运行**
```
config_wizard.bat
```

按提示输入：

#### 问题1：选择交易平台
```
1. Alpaca Markets（美股）⭐ 推荐新手
2. Binance（加密货币）
```
选择：`1`

#### 问题2：选择交易模式
```
1. Paper Trading（模拟）⭐ 推荐
2. Live Trading（真实）
```
选择：`1`

#### 问题3：输入API密钥

**获取Alpaca Paper Trading密钥**：
1. 访问：https://alpaca.markets/
2. 注册账户（免费）
3. Dashboard → API Keys
4. 复制 Paper Trading 的 API Key 和 Secret

**获取AI模型密钥（OpenAI）**：
1. 访问：https://platform.openai.com/
2. 注册/登录
3. API Keys → Create new key
4. 复制密钥（`sk-`开头）

#### 问题4：风险级别
```
1. 保守型（推荐新手）⭐
```
选择：`1`

---

## ✅ 测试和运行

### 测试连接

**双击运行**
```
test_connection.bat
```

**成功标志**：
```
✅ Broker connection successful
✅ Data provider connection successful
🎉 All tests passed!
```

### 开始Paper Trading

**双击运行**
```
start_paper_trading.bat
```

**看到这些输出说明成功**：
```
✅ Connected to alpaca broker (paper mode)
💰 Buying Power: $100000.00
🚀 Starting live trading agent...
```

---

## 📊 监控运行

### 查看日志

打开文件夹查看：
```
data\live_logs\trading.log
```

### 停止运行

在运行窗口按：
```
Ctrl + C
```

---

## 🆘 遇到问题？

### 运行诊断工具

**双击运行**
```
diagnose.bat
```

### 常见问题速查

**Q: Python未安装**
```
下载：https://www.python.org/downloads/
记得勾选"Add Python to PATH"！
```

**Q: 连接测试失败**
```
检查API密钥是否正确
检查网络连接
```

**Q: 找不到.env文件**
```
重新运行：config_wizard.bat
```

---

## 📚 深入学习

- **详细部署**：[docs/WINDOWS_SETUP_GUIDE.md](docs/WINDOWS_SETUP_GUIDE.md)
- **参数配置**：[docs/PARAMETER_REFERENCE.md](docs/PARAMETER_REFERENCE.md)
- **完整指南**：[docs/LIVE_TRADING_GUIDE.md](docs/LIVE_TRADING_GUIDE.md)

---

## ⚠️ 重要提醒

### Paper Trading（模拟）
- ✅ 安全无风险
- ✅ 适合学习测试
- ✅ 使用虚拟资金

### Live Trading（真实）
- ⚠️ 使用真实资金
- ⚠️ 有财务风险
- ⚠️ 需充分测试后使用

**建议：Paper Trading测试至少2周后，再考虑使用真实资金！**

---

## 🎯 下一步

1. ✅ 运行Paper Trading 1-2周
2. 📊 观察AI的交易决策
3. ⚙️ 调整风险参数
4. 📖 阅读详细文档
5. 💰 （可选）小额实盘测试

---

**祝您使用顺利！** 🚀

有问题随时查看文档或运行 `diagnose.bat`
