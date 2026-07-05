"""
Pydantic 数据模型 —— 定义 API 请求/响应的数据结构
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# ────────────────── 题型枚举 ──────────────────
class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"       # 单选
    MULTI_CHOICE = "multi_choice"         # 多选
    TRUE_FALSE = "true_false"             # 判断
    SHORT_ANSWER = "short_answer"         # 简答
    ESSAY = "essay"                       # 论述


# ────────────────── 题目模型 ──────────────────
class Choice(BaseModel):
    """选择题选项"""
    label: str            # A / B / C / D
    content: str          # 选项内容


class Question(BaseModel):
    """单道题目"""
    id: int
    type: QuestionType
    subject: str                               # 考察领域
    topic: str                                 # 具体考点
    content: str                               # 题干
    choices: Optional[List[Choice]] = None     # 选择题选项
    difficulty: str = "medium"                 # easy / medium / hard
    score: int = 5                             # 分值


class ExamPaper(BaseModel):
    """完整试卷"""
    exam_id: str
    subject: str                               # 考察领域
    topic_detail: str                          # 具体考点描述
    questions: List[Question]
    total_score: int
    duration_minutes: int = 60
    generated_at: str                          # ISO 时间戳


# ────────────────── 作答模型 ──────────────────
class Answer(BaseModel):
    """单题作答"""
    question_id: int
    answer: str                                # 选择题: "A" / "ABD"; 简答/论述: 文本


class AnswerSheet(BaseModel):
    """完整答卷"""
    exam_id: str
    answers: List[Answer]


# ────────────────── 批改结果模型 ──────────────────
class GradeResult(BaseModel):
    """单题批改"""
    question_id: int
    score: int
    max_score: int
    comment: str                               # 批语
    is_correct: Optional[bool] = None          # 客观题正确与否


class GradeReport(BaseModel):
    """完整批改报告"""
    exam_id: str
    total_score: int
    max_score: int
    results: List[GradeResult]
    summary: str                               # 总体评价


# ────────────────── 标准答案模型 ──────────────────
class AnswerKeyItem(BaseModel):
    """单题标准答案"""
    question_id: int
    correct_answer: str
    explanation: str                           # 解析
    key_points: Optional[List[str]] = None     # 简答/论述的采分点


class AnswerKey(BaseModel):
    """完整答案与解析"""
    exam_id: str
    items: List[AnswerKeyItem]


# ────────────────── 生成试卷请求 ──────────────────
class GenerateExamRequest(BaseModel):
    subject: str = Field(
        ...,
        description="考察领域，如 'Java:JVM' / 'C++:多线程与多进程' / '自定义内容'",
        min_length=1,
        max_length=500
    )
    question_count: int = Field(
        default=20,
        ge=5,
        le=30,
        description="题目总数"
    )
    single_choice_min: int = Field(
        default=10,
        ge=5,
        description="最少选择题数量"
    )


# ────────────────── API 通用响应 ──────────────────
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: str = ""
    error: Optional[str] = None
