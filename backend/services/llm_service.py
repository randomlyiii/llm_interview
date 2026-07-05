"""
LLM 调用服务 —— 统一接口，支持 DeepSeek / OpenAI / Claude / Ollama 多后端
"""
import json
import logging
from typing import Optional, AsyncGenerator

from openai import AsyncOpenAI
import anthropic

from config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """多 LLM 后端统一调用服务"""

    def __init__(self):
        self.provider = settings.llm_provider
        self._openai_client: Optional[AsyncOpenAI] = None
        self._claude_client: Optional[anthropic.AsyncAnthropic] = None
        logger.info(f"LLM Service initialized with provider: {self.provider}")

    # ────────────────── 客户端懒加载 ──────────────────
    @property
    def openai_client(self) -> AsyncOpenAI:
        if self._openai_client is None:
            if self.provider == "deepseek":
                self._openai_client = AsyncOpenAI(
                    api_key=settings.deepseek_api_key,
                    base_url=settings.deepseek_base_url,
                )
            elif self.provider == "openai":
                self._openai_client = AsyncOpenAI(
                    api_key=settings.openai_api_key,
                    base_url=settings.openai_base_url,
                )
            elif self.provider == "ollama":
                self._openai_client = AsyncOpenAI(
                    api_key="ollama",
                    base_url=f"{settings.ollama_base_url}/v1",
                )
            else:
                raise ValueError(f"不支持的 provider: {self.provider}")
        return self._openai_client

    @property
    def claude_client(self) -> anthropic.AsyncAnthropic:
        if self._claude_client is None:
            self._claude_client = anthropic.AsyncAnthropic(
                api_key=settings.claude_api_key,
                base_url=settings.claude_base_url,
            )
        return self._claude_client

    # ────────────────── 获取模型名 ──────────────────
    @property
    def model_name(self) -> str:
        provider_models = {
            "deepseek": settings.deepseek_model,
            "openai": settings.openai_model,
            "claude": settings.claude_model,
            "ollama": settings.ollama_model,
        }
        return provider_models.get(self.provider, settings.deepseek_model)

    # ────────────────── 核心调用方法 ──────────────────
    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 8192,
    ) -> str:
        """发送一次对话请求，返回完整回复文本"""
        logger.info(f"LLM call: provider={self.provider}, model={self.model_name}")

        if self.provider == "claude":
            return await self._chat_claude(system_prompt, user_message, temperature, max_tokens)
        else:
            return await self._chat_openai_compat(system_prompt, user_message, temperature, max_tokens)

    async def chat_json(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 8192,
    ) -> dict:
        """调用 LLM 并解析 JSON 返回"""
        raw = await self.chat(system_prompt, user_message, temperature, max_tokens)
        return self._extract_json(raw)

    # ────────────────── OpenAI 兼容接口 (DeepSeek / OpenAI / Ollama) ──────────────────
    async def _chat_openai_compat(
        self, system_prompt: str, user_message: str, temperature: float, max_tokens: int
    ) -> str:
        response = await self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    # ────────────────── Claude 接口 ──────────────────
    async def _chat_claude(
        self, system_prompt: str, user_message: str, temperature: float, max_tokens: int
    ) -> str:
        response = await self.claude_client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        # Claude 返回的是 ContentBlock 列表
        if response.content and len(response.content) > 0:
            return response.content[0].text
        return ""

    # ────────────────── JSON 提取 ──────────────────
    @staticmethod
    def _extract_json(text: str) -> dict:
        """从 LLM 返回文本中提取 JSON 对象"""
        text = text.strip()
        # 尝试去除 markdown 代码块标记
        if text.startswith("```"):
            lines = text.split("\n")
            # 去掉第一行 ```json 或 ```
            text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[: text.rfind("```")].strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # 尝试匹配第一个 {...}
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"无法从 LLM 响应中解析 JSON: {text[:500]}...")


# 全局单例
llm_service = LLMService()
