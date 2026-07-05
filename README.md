# LLM Interview Agent

基于大语言模型的智能面试备考系统，支持多技术栈的模拟面试题生成、在线作答、智能批改与答案解析。

## 技术栈

- **前端**: Vue 3 + Vite + JavaScript
- **后端**: Python FastAPI
- **LLM**: 支持 DeepSeek V4 / OpenAI / Claude / Ollama 多后端切换

## 支持的考察范围

| 领域 | 考点 |
|------|------|
| Java | JVM、内存模型、垃圾回收 |
| C++ | 多线程、多进程、内存管理 |
| Python | 语言特性、GIL、异步编程 |
| MySQL | 索引、事务、锁、优化 |
| Linux | CPU调度、内核、Docker、常用指令 |
| LLM | MCP协议、RAG、Prompt Engineering |

支持在前端自定义考察范围。

## 快速开始

### 1. 一键安装

双击运行 `setup.bat`，自动安装后端 Python 依赖和前端 npm 依赖。

### 2. 配置 API Key

编辑 `backend/.env`，填入你的 LLM API Key：

```ini
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-key-here
```

### 3. 启动服务

**后端**:
```bash
cd backend
python launch.py
```

**前端**:
```bash
cd frontend
launch.bat
```

浏览器访问 `http://localhost:5173` 即可使用。

## 项目结构

```
llm_interview/
├── setup.bat                  # 一键环境安装
├── backend/
│   ├── launch.py              # 后端启动管理
│   ├── main.py                # FastAPI 入口
│   ├── config.py              # 配置管理
│   ├── requirements.txt       # Python 依赖
│   ├── api/routes.py          # API 路由
│   ├── services/
│   │   ├── llm_service.py     # LLM 调用服务
│   │   └── exam_service.py    # 试卷业务逻辑
│   ├── models/schemas.py      # 数据模型
│   └── skills/                # 规范化 .skill 文件
│       ├── generate_exam.skill/   # 出题
│       ├── grade_exam.skill/      # 批改
│       └── generate_answer.skill/ # 生成答案
└── frontend/
    ├── launch.bat             # 前端启动管理
    ├── vite.config.js
    └── src/
        ├── App.vue
        ├── components/
        │   ├── TopicSelector.vue
        │   ├── ExamPaper.vue
        │   ├── AnswerSheet.vue
        │   ├── GradeView.vue
        │   └── AnswerKey.vue
        └── api/index.js
```

## 使用流程

1. 前端选择考察领域（或自定义输入）
2. 系统调用 LLM 生成 20 题全题型试卷（单选、多选、判断、简答、论述）
3. 在线作答提交
4. LLM 自动批改并生成标准答案
5. 查看评分结果与答案解析
