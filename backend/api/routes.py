"""
API 路由 —— 定义所有 REST 接口
"""
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from models.schemas import (
    GenerateExamRequest, AnswerSheet,
    ExamPaper, GradeReport, AnswerKey, APIResponse,
)
from services.exam_service import generate_exam, grade_exam, generate_answer_key, get_exam

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["exam"])


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "LLM Interview Agent is running"}


@router.post("/generate", response_model=APIResponse)
async def api_generate_exam(req: GenerateExamRequest):
    """生成面试模拟试卷"""
    try:
        paper = await generate_exam(req)
        return APIResponse(
            success=True,
            data=paper.model_dump(),
            message=f"试卷生成成功，共 {len(paper.questions)} 题，满分 {paper.total_score} 分",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("生成试卷失败")
        raise HTTPException(status_code=500, detail=f"生成试卷失败: {str(e)}")


@router.get("/exam/{exam_id}", response_model=APIResponse)
async def api_get_exam(exam_id: str):
    """获取已生成的试卷"""
    paper = await get_exam(exam_id)
    if not paper:
        raise HTTPException(status_code=404, detail=f"试卷不存在: {exam_id}")
    return APIResponse(
        success=True,
        data=paper.model_dump(),
        message="ok",
    )


@router.post("/grade/{exam_id}", response_model=APIResponse)
async def api_grade_exam(exam_id: str, sheet: AnswerSheet):
    """批改答卷"""
    if sheet.exam_id != exam_id:
        raise HTTPException(status_code=400, detail="答卷的 exam_id 与 URL 不匹配")
    try:
        report = await grade_exam(exam_id, sheet)
        return APIResponse(
            success=True,
            data=report.model_dump(),
            message=f"批改完成，得分 {report.total_score}/{report.max_score}",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("批改试卷失败")
        raise HTTPException(status_code=500, detail=f"批改失败: {str(e)}")


@router.get("/answer-key/{exam_id}", response_model=APIResponse)
async def api_get_answer_key(exam_id: str):
    """获取标准答案与解析"""
    try:
        key = await generate_answer_key(exam_id)
        return APIResponse(
            success=True,
            data=key.model_dump(),
            message="答案生成成功",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("生成答案失败")
        raise HTTPException(status_code=500, detail=f"生成答案失败: {str(e)}")
