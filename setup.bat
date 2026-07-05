@echo off
chcp 65001 >nul
title LLM Interview Agent - Setup

echo ============================================
echo   LLM Interview Agent - 一键环境安装
echo ============================================
echo.

REM === Check Python ===
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)
echo [OK] Python 已安装
for /f "tokens=*" %%i in ('python --version') do echo     %%i

REM === Check Node.js ===
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)
echo [OK] Node.js 已安装
for /f "tokens=*" %%i in ('node --version') do echo     %%i

REM === Check npm ===
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 npm
    pause
    exit /b 1
)
echo [OK] npm 已安装
for /f "tokens=*" %%i in ('npm --version') do echo     %%i

echo.
echo ============================================
echo   安装 Python 后端依赖...
echo ============================================
cd /d "%~dp0backend"
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [错误] Python 依赖安装失败
    pause
    exit /b 1
)
echo [OK] Python 依赖安装完成

echo.
echo ============================================
echo   安装前端依赖...
echo ============================================
cd /d "%~dp0frontend"
call npm install
if %errorlevel% neq 0 (
    echo [错误] 前端依赖安装失败
    pause
    exit /b 1
)
echo [OK] 前端依赖安装完成

echo.
echo ============================================
echo   检查 .env 配置...
echo ============================================
cd /d "%~dp0backend"
if not exist .env (
    echo [提示] 未找到 backend\.env，正在从 .env.example 复制...
    if exist .env.example (
        copy .env.example .env >nul
        echo [OK] 已创建 .env，请编辑 backend\.env 填入你的 API Key
    ) else (
        echo [警告] .env.example 也不存在，将自动创建默认配置
        (
            echo # LLM Provider Configuration
            echo LLM_PROVIDER=deepseek
            echo.
            echo # DeepSeek
            echo DEEPSEEK_API_KEY=your-deepseek-api-key-here
            echo DEEPSEEK_BASE_URL=https://api.deepseek.com
            echo DEEPSEEK_MODEL=deepseek-chat
            echo.
            echo # OpenAI ^(Optional^)
            echo OPENAI_API_KEY=your-openai-api-key-here
            echo OPENAI_BASE_URL=https://api.openai.com/v1
            echo OPENAI_MODEL=gpt-4o
            echo.
            echo # Claude ^(Optional^)
            echo CLAUDE_API_KEY=your-claude-api-key-here
            echo CLAUDE_BASE_URL=https://api.anthropic.com
            echo CLAUDE_MODEL=claude-sonnet-4-20250514
            echo.
            echo # Ollama ^(Optional, local^)
            echo OLLAMA_BASE_URL=http://localhost:11434
            echo OLLAMA_MODEL=qwen2.5:7b
            echo.
            echo # Server
            echo BACKEND_HOST=0.0.0.0
            echo BACKEND_PORT=8000
        ) > .env
        echo [OK] 已创建 .env，请编辑 backend\.env 填入你的 API Key
    )
) else (
    echo [OK] .env 已存在
)

echo.
echo ============================================
echo   安装完成！
echo ============================================
echo.
echo   后端启动:  cd backend ^&^& python launch.py
echo   前端启动:  cd frontend ^&^& launch.bat
echo.
echo   首次使用请编辑 backend\.env 填入 API Key！
echo.
pause
