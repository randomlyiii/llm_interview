@echo off
chcp 65001 >nul
title LLM Interview Agent - Frontend

cd /d "%~dp0"

REM === Check Node.js ===
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

REM === Check node_modules ===
if not exist "node_modules" (
    echo [提示] 未找到 node_modules，正在安装依赖...
    call npm install
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

REM === Launch ===
echo.
echo ============================================
echo   LLM Interview Agent - 前端启动
echo ============================================
echo   地址: http://localhost:5173
echo   确保后端已启动 (port 8000)
echo   按 Ctrl+C 停止
echo ============================================
echo.

call npm run dev
pause
