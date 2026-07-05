"""
试卷业务逻辑 —— 生成试卷、批改、对答案的高层封装
加载 .skill 文件作为 LLM 的 system prompt
"""
import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from services.llm_service import llm_service
from models.schemas import (
    ExamPaper, GradeReport, AnswerKey,
    GenerateExamRequest, AnswerSheet,
)

logger = logging.getLogger(__name__)

# .skill 文件目录
SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

# 内存存储（生产环境可替换为数据库）
_exam_store: dict[str, ExamPaper] = {}


def _load_skill(skill_name: str) -> str:
    """加载 .skill 目录下的 SKILL.md 文件内容"""
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.exists():
        logger.warning(f"Skill 文件不存在: {skill_path}")
        return ""
    return skill_path.read_text(encoding="utf-8")


def _build_exam_prompt(req: GenerateExamRequest) -> str:
    """构建出题请求的 user message"""
    # 预设主题映射
    preset_topics = {
        "java": "Java：JVM 内存模型、垃圾回收机制、类加载机制、JIT 编译优化",
        "c++": "C++：多线程与多进程编程、内存管理、RAII、模板元编程、移动语义",
        "python": "Python：GIL 全局解释器锁、asyncio 异步编程、装饰器、生成器、内存管理",
        "mysql": "MySQL：InnoDB 索引原理、事务隔离级别、锁机制、SQL 优化、分库分表",
        "linux": "Linux：CPU 调度算法、内核态与用户态、Docker 容器原理与常用指令、文件系统",
        "llm": "LLM：MCP 协议架构、RAG 检索增强生成、Prompt Engineering、Agent 设计模式",
    }
    subject_lower = req.subject.lower().strip()
    detail = preset_topics.get(subject_lower, req.subject)

    return f"""请生成一份技术面试模拟试卷，考察领域：{detail}

要求：
- 共 {req.question_count} 道题
- 至少 {req.single_choice_min} 道单项选择题
- 题型分配建议：单选 {req.single_choice_min} 题 + 多选 3 题 + 判断 2 题 + 简答 3 题 + 论述 2 题
- 单选和多选每题 3 分，判断每题 2 分，简答每题 8 分，论述每题 12 分
- 难度比例：简单:中等:困难 ≈ 3:5:2
- 覆盖领域内的核心知识点，避免偏题怪题
- 考察点需要有区分度，能够区分初级/中级/高级水平

请严格按照下方 JSON 格式输出（不要包含 markdown 代码块标记）：

{{
  "exam_id": "{uuid.uuid4().hex[:12]}",
  "subject": "{req.subject}",
  "topic_detail": "{detail}",
  "questions": [
    {{
      "id": 1,
      "type": "single_choice",
      "subject": "领域名",
      "topic": "具体考点",
      "content": "题干内容",
      "choices": [
        {{"label": "A", "content": "选项内容"}},
        {{"label": "B", "content": "选项内容"}},
        {{"label": "C", "content": "选项内容"}},
        {{"label": "D", "content": "选项内容"}}
      ],
      "difficulty": "medium",
      "score": 3
    }}
  ],
  "total_score": 100,
  "duration_minutes": 60
}}"""


async def generate_exam(req: GenerateExamRequest) -> ExamPaper:
    """生成试卷"""
    skill_prompt = _load_skill("generate_exam.skill")
    user_prompt = _build_exam_prompt(req)

    logger.info(f"Generating exam for subject: {req.subject}")
    raw = await llm_service.chat_json(
        system_prompt=skill_prompt,
        user_message=user_prompt,
        temperature=0.8,
        max_tokens=16384,
    )

    # 填充缺失字段
    raw.setdefault("generated_at", datetime.now(timezone.utc).isoformat())
    raw.setdefault("total_score", sum(q.get("score", 5) for q in raw.get("questions", [])))
    raw.setdefault("duration_minutes", 60)

    paper = ExamPaper(**raw)
    _exam_store[paper.exam_id] = paper
    logger.info(f"Exam generated: {paper.exam_id}, {len(paper.questions)} questions")
    return paper


async def grade_exam(exam_id: str, sheet: AnswerSheet) -> GradeReport:
    """批改试卷"""
    paper = _exam_store.get(exam_id)
    if not paper:
        raise ValueError(f"试卷不存在: {exam_id}")

    skill_prompt = _load_skill("grade_exam.skill")

    # 构建试卷内容和学生作答
    questions_text = _format_questions_for_llm(paper)
    answers_text = _format_answers_for_llm(sheet)

    user_prompt = f"""请批改以下试卷的学生作答。

## 试卷内容
{questions_text}

## 学生作答
{answers_text}

请逐题批改并严格按照以下 JSON 格式输出：

{{
  "exam_id": "{exam_id}",
  "total_score": 0,
  "max_score": {paper.total_score},
  "results": [
    {{
      "question_id": 1,
      "score": 3,
      "max_score": 3,
      "comment": "批语",
      "is_correct": true
    }}
  ],
  "summary": "总体评价，分析学生的薄弱环节和优势"
}}"""

    raw = await llm_service.chat_json(
        system_prompt=skill_prompt,
        user_message=user_prompt,
        temperature=0.3,
        max_tokens=8192,
    )
    return GradeReport(**raw)


async def generate_answer_key(exam_id: str) -> AnswerKey:
    """生成标准答案与解析"""
    paper = _exam_store.get(exam_id)
    if not paper:
        raise ValueError(f"试卷不存在: {exam_id}")

    skill_prompt = _load_skill("generate_answer.skill")
    questions_text = _format_questions_for_llm(paper)

    user_prompt = f"""请为以下试卷生成标准答案和详细解析。

## 试卷内容
{questions_text}

请严格按照以下 JSON 格式输出：

{{
  "exam_id": "{exam_id}",
  "items": [
    {{
      "question_id": 1,
      "correct_answer": "标准答案（选择题填选项字母如A，多选如ABD，简答/论述写完整答案）",
      "explanation": "详细解析，说明对在哪里、错在哪里",
      "key_points": ["采分点1", "采分点2"]
    }}
  ]
}}"""

    raw = await llm_service.chat_json(
        system_prompt=skill_prompt,
        user_message=user_prompt,
        temperature=0.3,
        max_tokens=16384,
    )
    return AnswerKey(**raw)


async def get_exam(exam_id: str) -> Optional[ExamPaper]:
    """获取已生成的试卷"""
    return _exam_store.get(exam_id)


# ────────────────── 辅助函数 ──────────────────
def _format_questions_for_llm(paper: ExamPaper) -> str:
    """将试卷题目格式化为 LLM 可读文本"""
    lines = []
    type_names = {
        "single_choice": "单选",
        "multi_choice": "多选",
        "true_false": "判断",
        "short_answer": "简答",
        "essay": "论述",
    }
    for q in paper.questions:
        type_name = type_names.get(q.type.value if hasattr(q.type, 'value') else q.type, "未知")
        lines.append(f"### 第{q.id}题 [{type_name}] ({q.score}分) - {q.topic}")
        lines.append(q.content)
        if q.choices:
            for c in q.choices:
                lines.append(f"  {c.label}. {c.content}")
        lines.append("")
    return "\n".join(lines)


def _format_answers_for_llm(sheet: AnswerSheet) -> str:
    """将学生作答格式化为 LLM 可读文本"""
    lines = []
    for a in sheet.answers:
        lines.append(f"第{a.question_id}题: {a.answer}")
    return "\n".join(lines)
