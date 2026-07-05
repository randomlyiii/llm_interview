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

### 1. 安装 Python 依赖

双击运行 `setup.bat`，自动安装后端 Python 依赖并生成 `.env` 配置文件。

### 2. 配置 API Key

编辑 `backend/.env`，填入你的 LLM API Key：

```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-key-here
```

### 3. 启动服务

**后端** (项目根目录):
```bash
python launch.py start
```

**前端** (项目根目录):
```bash
launch.bat
```

首次启动前端会自动执行 `npm install` 安装依赖。浏览器访问 `http://localhost:5173` 即可使用。

## 项目结构

```
llm_interview/
├── setup.bat                       # 一键安装 Python 后端依赖
├── launch.py                       # 后端启动管理（根目录）
├── launch.bat                      # 前端启动管理（根目录）
├── backend/
│   ├── main.py                     # FastAPI 入口
│   ├── config.py                   # 多 LLM 配置管理
│   ├── requirements.txt            # Python 依赖
│   ├── api/routes.py               # REST API 路由
│   ├── services/
│   │   ├── llm_service.py          # LLM 统一调用服务
│   │   └── exam_service.py         # 试卷业务逻辑
│   ├── models/schemas.py           # Pydantic 数据模型
│   └── skills/                     # 规范化 .skill 文件
│       ├── generate_exam.skill/    # 出题规范
│       ├── grade_exam.skill/       # 批改规范
│       └── generate_answer.skill/  # 答案规范
└── frontend/
    ├── launch.bat                  # 前端启动（子目录独立运行）
    ├── vite.config.js              # Vite 配置（含 API 代理）
    └── src/
        ├── App.vue                 # 主页面（5 步向导流程）
        ├── components/
        │   ├── TopicSelector.vue   # 选题范围
        │   ├── ExamPaper.vue       # 试卷展示
        │   ├── AnswerSheet.vue     # 在线作答
        │   ├── GradeView.vue       # 批改结果
        │   └── AnswerKeyView.vue   # 标准答案与解析
        └── api/index.js            # API 客户端
```

## 使用流程

1. 前端选择考察领域（Java/C++/Python/MySQL/Linux/LLM，或自定义输入）
2. 系统调用 LLM 生成 20 题全题型试卷（单选题 ≥10 + 多选 + 判断 + 简答 + 论述）
3. 在线作答并提交
4. LLM 自动批改每道题，给出逐题评价和总体评分
5. 查看标准答案、详细解析及采分点对照
