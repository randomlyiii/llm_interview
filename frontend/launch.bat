@echo off
chcp 65001 >nul
title LLM Interview Agent - Frontend

cd /d "%~dp0"

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo [INFO] Installing frontend dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed
        pause
        exit /b 1
    )
)

echo.
echo ============================================
echo   LLM Interview Agent - Frontend
echo ============================================
echo   URL:  http://localhost:5173
echo   Make sure backend is running (port 8000)
echo   Press Ctrl+C to stop
echo ============================================
echo.

call npm run dev
pause
