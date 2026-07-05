"""
LLM Interview Agent — FastAPI 后端入口
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from config import settings

# 日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# FastAPI 应用
app = FastAPI(
    title="LLM Interview Agent",
    description="基于 LLM 的智能面试备考系统 API",
    version="1.0.0",
)

# CORS —— 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)


@app.on_event("startup")
async def startup():
    logger.info(f"LLM Interview Agent starting on {settings.backend_host}:{settings.backend_port}")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"API Docs: http://{settings.backend_host}:{settings.backend_port}/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
    )
