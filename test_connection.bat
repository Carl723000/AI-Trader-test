@echo off
chcp 65001 >nul

echo ========================================
echo AI-Trader 连接测试
echo ========================================
echo.
echo 正在测试与交易平台的连接...
echo 这将验证您的API密钥是否正确配置
echo.
pause

python test_live_connection.py

echo.
echo ========================================
echo 测试完成
echo ========================================
echo.
pause
