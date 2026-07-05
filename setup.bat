@echo off
chcp 65001 >nul
title LLM Interview Agent - Backend Setup

echo ============================================
echo   LLM Interview Agent - Backend Setup
echo ============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo [OK] Python: %%i

echo.
echo ============================================
echo   Installing Python dependencies...
echo ============================================
cd /d "%~dp0backend"
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Python dependency installation failed
    pause
    exit /b 1
)
echo [OK] Python dependencies installed

echo.
echo ============================================
echo   Checking .env configuration...
echo ============================================
if not exist .env (
    if exist .env.example (
        echo [INFO] Copying from .env.example...
        copy .env.example .env >nul
        echo [OK] Created .env. Please edit backend\.env with your API Key
    ) else (
        echo [INFO] Creating default .env...
        python -c "open('.env','w',encoding='utf-8').write('LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
OPENAI_API_KEY=your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
CLAUDE_API_KEY=your-key-here
CLAUDE_BASE_URL=https://api.anthropic.com
CLAUDE_MODEL=claude-sonnet-4-20250514
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
')"
        echo [OK] Created .env. Please edit backend\.env with your API Key
    )
) else (
    echo [OK] .env exists
)

echo.
echo ============================================
echo   Setup complete!
echo ============================================
echo.
echo   Start backend:  python launch.py
echo   Start frontend: launch.bat
echo.
echo   Edit backend\.env to set your API Key first!
echo.
pause
