chcp 65001 > nul
@echo off
echo 启动 Vue3 + Flask 项目...

echo.
echo 1. 启动 Flask 后端...
start "Flask Backend" cmd /k "cd backend && python app.py"

echo.
echo 2. 等待后端启动...
timeout /t 3 /nobreak > nul

echo.
echo 3. 启动 Vue 前端...
start "Vue Frontend" cmd /k "npm run dev"

echo.
echo 项目启动完成！
echo 前端地址: http://localhost:5173
echo 后端地址: http://localhost:3000
echo.
echo 按任意键退出...
pause > nul 