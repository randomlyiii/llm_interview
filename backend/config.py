"""
应用配置管理 —— 从 .env 读取 LLM 和服务配置
"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # --- LLM Provider ---
    llm_provider: str = os.getenv("LLM_PROVIDER", "deepseek")

    # DeepSeek
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Claude
    claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")
    claude_base_url: str = os.getenv("CLAUDE_BASE_URL", "https://api.anthropic.com")
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

    # Ollama (local)
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

    # Server
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))

    model_config = {"env_file": ".env", "extra": "allow"}


settings = Settings()
