"""
LLM Interview Agent — 后端启动管理器
支持：启动服务、检查依赖、查看配置、重启
"""
import subprocess
import sys
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent


def check_deps():
    """检查 Python 依赖"""
    print("[检查] Python 依赖...")
    try:
        import fastapi
        import uvicorn
        import pydantic
        import httpx
        import openai
        print(f"  [OK] FastAPI {fastapi.__version__}")
        print(f"  [OK] Uvicorn {uvicorn.__version__}")
        print(f"  [OK] Pydantic {pydantic.__version__}")
        print(f"  [OK] httpx {httpx.__version__}")
        print(f"  [OK] openai {openai.__version__}")
    except ImportError as e:
        print(f"  [FAIL] 缺少依赖: {e}")
        print("  请运行: pip install -r requirements.txt")
        return False
    return True


def check_env():
    """检查 .env 配置"""
    env_file = BACKEND_DIR / ".env"
    if not env_file.exists():
        print("[警告] .env 文件不存在，请从 .env.example 复制并配置")
        return False

    from dotenv import load_dotenv
    load_dotenv(env_file)

    provider = os.getenv("LLM_PROVIDER", "deepseek")
    key_map = {
        "deepseek": "DEEPSEEK_API_KEY",
        "openai": "OPENAI_API_KEY",
        "claude": "CLAUDE_API_KEY",
        "ollama": None,
    }
    key_name = key_map.get(provider)
    if key_name and not os.getenv(key_name):
        print(f"[警告] 当前 LLM Provider 为 {provider}，但未配置 {key_name}")
        return False

    print(f"[OK] LLM Provider: {provider}")
    return True


def start_server(port: int = None):
    """启动 FastAPI 服务"""
    os.chdir(BACKEND_DIR)

    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    if port is None:
        port = int(os.getenv("BACKEND_PORT", "8000"))

    print(f"\n{'='*50}")
    print(f"  启动后端服务: http://{host}:{port}")
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
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            input("\n按回车键继续...")
        elif choice == "5":
            break
        else:
            print("无效选择")


if __name__ == "__main__":
    # 如果有命令行参数，快速启动
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "start":
            check_deps()
            check_env()
            port = int(sys.argv[2]) if len(sys.argv) > 2 else None
            start_server(port)
        elif cmd == "check":
            check_deps()
            check_env()
        elif cmd == "install":
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        show_menu()
