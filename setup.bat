@echo off
chcp 65001 >nul
title LLM Interview Agent - Setup

echo ============================================
echo   LLM Interview Agent - Backend Setup
echo ============================================
echo.

REM === Check Python ===
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)
echo [OK] Python found
for /f "tokens=*" %%i in ('python --version') do echo     %%i

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
        python -c "open('.env','w',encoding='utf-8').write('# LLM Provider Configuration\nLLM_PROVIDER=deepseek\n\n# DeepSeek\nDEEPSEEK_API_KEY=your-deepseek-api-key-here\nDEEPSEEK_BASE_URL=https://api.deepseek.com\nDEEPSEEK_MODEL=deepseek-chat\n\n# OpenAI (Optional)\nOPENAI_API_KEY=your-openai-api-key-here\nOPENAI_BASE_URL=https://api.openai.com/v1\nOPENAI_MODEL=gpt-4o\n\n# Claude (Optional)\nCLAUDE_API_KEY=your-claude-api-key-here\nCLAUDE_BASE_URL=https://api.anthropic.com\nCLAUDE_MODEL=claude-sonnet-4-20250514\n\n# Ollama (Optional, local)\nOLLAMA_BASE_URL=http://localhost:11434\nOLLAMA_MODEL=qwen2.5:7b\n\n# Server\nBACKEND_HOST=0.0.0.0\nBACKEND_PORT=8000\n')"
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
