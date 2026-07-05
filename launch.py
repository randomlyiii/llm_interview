"""
LLM Interview Agent — 后端启动管理器 (项目根目录)
支持：启动服务、检查依赖、查看配置、安装依赖
"""
import subprocess
import sys
import os
from pathlib import Path

# 项目根目录 = 当前脚本所在目录
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"


def check_deps():
    """检查 Python 依赖"""
    print("[检查] Python 依赖...")
    missing = []
    try:
        import fastapi; print(f"  [OK] FastAPI {fastapi.__version__}")
    except ImportError: print("  [FAIL] FastAPI 未安装"); missing.append("fastapi")
    try:
        import uvicorn; print(f"  [OK] Uvicorn {uvicorn.__version__}")
    except ImportError: print("  [FAIL] Uvicorn 未安装"); missing.append("uvicorn")
    try:
        import pydantic; print(f"  [OK] Pydantic {pydantic.__version__}")
    except ImportError: print("  [FAIL] Pydantic 未安装"); missing.append("pydantic")
    try:
        import httpx; print(f"  [OK] httpx {httpx.__version__}")
    except ImportError: print("  [FAIL] httpx 未安装"); missing.append("httpx")
    try:
        import openai; print(f"  [OK] openai {openai.__version__}")
    except ImportError: print("  [FAIL] openai 未安装"); missing.append("openai")
    try:
        import anthropic; print("  [OK] anthropic")
    except ImportError: print("  [FAIL] anthropic 未安装"); missing.append("anthropic")
    try:
        from pydantic_settings import BaseSettings; print("  [OK] pydantic-settings")
    except ImportError: print("  [FAIL] pydantic-settings 未安装"); missing.append("pydantic-settings")
    try:
        from dotenv import load_dotenv; print("  [OK] python-dotenv")
    except ImportError: print("  [FAIL] python-dotenv 未安装"); missing.append("python-dotenv")

    if missing:
        print(f"\n  缺少 {len(missing)} 个依赖，请运行: pip install -r backend/requirements.txt")
        return False
    return True


def check_env():
    """检查 .env 配置"""
    env_file = BACKEND_DIR / ".env"
    if not env_file.exists():
        print("[警告] backend/.env 文件不存在")
        print("  请复制 backend/.env.example 为 backend/.env 并填入 API Key")
        return False

    from dotenv import load_dotenv
    load_dotenv(env_file, override=True)

    provider = os.getenv("LLM_PROVIDER", "deepseek")
    key_map = {
        "deepseek": "DEEPSEEK_API_KEY",
        "openai": "OPENAI_API_KEY",
        "claude": "CLAUDE_API_KEY",
        "ollama": None,
    }
    key_name = key_map.get(provider)
    if key_name:
        key_value = os.getenv(key_name, "")
        if not key_value or "your-" in key_value.lower():
            print(f"[警告] 当前 LLM Provider 为 {provider}，但 {key_name} 未正确配置")
            print(f"  请编辑 backend/.env 填入有效的 API Key")
            return False

    print(f"[OK] LLM Provider: {provider}")
    print(f"[OK] API Key 已配置")
    return True


def start_server(port: int = None):
    """启动 FastAPI 服务"""
    # 将 backend 目录加入 sys.path，确保导入正确
    sys.path.insert(0, str(BACKEND_DIR))
    os.chdir(BACKEND_DIR)

    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    if port is None:
        port = int(os.getenv("BACKEND_PORT", "8000"))

    print(f"\n{'='*50}")
    print(f"  启动后端服务: http://localhost:{port}")
    print(f"  API 文档: http://localhost:{port}/docs")
    print(f"  按 Ctrl+C 停止")
    print(f"{'='*50}\n")

    import uvicorn
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )


def show_menu():
    """显示管理菜单"""
    while True:
        print(f"\n{'='*50}")
        print("  LLM Interview Agent — 后端管理器")
        print(f"{'='*50}")
        print("  1. 启动服务")
        print("  2. 检查依赖")
        print("  3. 检查配置")
        print("  4. 安装依赖")
        print("  5. 退出")
        print(f"{'='*50}")

        choice = input("  请选择 [1-5]: ").strip()

        if choice == "1":
            if check_deps() and check_env():
                start_server()
            else:
                input("\n按回车键继续...")
        elif choice == "2":
            check_deps()
            input("\n按回车键继续...")
        elif choice == "3":
            check_env()
            input("\n按回车键继续...")
        elif choice == "4":
            print("[安装] 正在安装 Python 依赖...")
            req_path = BACKEND_DIR / "requirements.txt"
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_path)])
            input("\n按回车键继续...")
        elif choice == "5":
            print("再见！")
            break
        else:
            print("无效选择，请输入 1-5")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "start":
            if check_deps() and check_env():
                port = int(sys.argv[2]) if len(sys.argv) > 2 else None
                start_server(port)
        elif cmd == "check":
            check_deps()
            check_env()
        elif cmd == "install":
            print("[安装] 正在安装 Python 依赖...")
            req_path = BACKEND_DIR / "requirements.txt"
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_path)])
    else:
        show_menu()
