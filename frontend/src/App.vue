<script setup>
import { ref, computed } from 'vue'
import TopicSelector from './components/TopicSelector.vue'
import ExamPaper from './components/ExamPaper.vue'
import AnswerSheet from './components/AnswerSheet.vue'
import GradeView from './components/GradeView.vue'
import AnswerKeyView from './components/AnswerKeyView.vue'
import { generateExam, gradeExam, getAnswerKey } from './api/index.js'

// ── State ──
const step = ref('select')  // select | exam | answer | grade | key
const loading = ref(false)
const error = ref('')

const examData = ref(null)
const gradeData = ref(null)
const answerKeyData = ref(null)
const userAnswers = ref([])

// ── Steps definition ──
const steps = [
  { key: 'select', label: '选择范围' },
  { key: 'exam', label: '查看试卷' },
  { key: 'answer', label: '在线作答' },
  { key: 'grade', label: '批改结果' },
  { key: 'key', label: '查看答案' },
]

const currentStepIdx = computed(() => steps.findIndex(s => s.key === step.value))

// ── Actions ──
async function handleGenerate(subject) {
  loading.value = true
  error.value = ''
  try {
    const res = await generateExam(subject)
    if (res.success) {
      examData.value = res.data
      step.value = 'exam'
    } else {
      error.value = res.message || '生成失败'
    }
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || '生成试卷失败，请检查后端服务'
  } finally {
    loading.value = false
  }
}

function handleStartAnswer() {
  step.value = 'answer'
}

function handleSubmitAnswers(answers) {
  userAnswers.value = answers
  gradeExamAndKey(examData.value.exam_id, answers)
}

async function gradeExamAndKey(examId, answers) {
  loading.value = true
  error.value = ''
  try {
    // 并行请求批改和答案
    const [gradeRes, keyRes] = await Promise.all([
      gradeExam(examId, answers),
      getAnswerKey(examId),
    ])
    if (gradeRes.success) {
      gradeData.value = gradeRes.data
    }
    if (keyRes.success) {
      answerKeyData.value = keyRes.data
    }
    step.value = 'grade'
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || '批改失败'
  } finally {
    loading.value = false
  }
}

function handleViewKey() {
  step.value = 'key'
}

function handleBackToExam() {
  step.value = 'exam'
}

function handleBackToGrade() {
  step.value = 'grade'
}

function handleReset() {
  step.value = 'select'
  examData.value = null
  gradeData.value = null
  answerKeyData.value = null
  userAnswers.value = []
  error.value = ''
}
</script>

<template>
  <div class="app-container">
    <!-- Header -->
    <header class="header">
      <h1>LLM Interview Agent</h1>
      <p>智能面试备考系统 — 生成试卷、在线作答、AI 批改、查看解析</p>
    </header>

    <!-- Steps Indicator -->
    <div class="steps">
      <template v-for="(s, idx) in steps" :key="s.key">
        <div
          class="step"
          :class="{
            active: currentStepIdx === idx,
            done: currentStepIdx > idx,
          }"
        >
          <span class="step-num">{{ currentStepIdx > idx ? '✓' : idx + 1 }}</span>
          <span class="step-text">{{ s.label }}</span>
        </div>
        <div v-if="idx < steps.length - 1" class="step-divider"></div>
      </template>
    </div>

    <!-- Error Banner -->
    <div v-if="error" class="status-bar error">
      <span style="font-size:18px">⚠️</span>
      <span>{{ error }}</span>
      <button class="btn btn-sm btn-outline" style="margin-left:auto" @click="error=''">关闭</button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <div>正在调用 LLM 处理中，请稍候...</div>
    </div>

    <!-- Step 1: Topic Selector -->
    <TopicSelector
      v-if="step === 'select' && !loading"
      @generate="handleGenerate"
    />

    <!-- Step 2: Exam Paper -->
    <ExamPaper
      v-if="step === 'exam' && examData && !loading"
      :paper="examData"
      @start-answer="handleStartAnswer"
      @reset="handleReset"
    />

    <!-- Step 3: Answer Sheet -->
    <AnswerSheet
      v-if="step === 'answer' && examData && !loading"
      :paper="examData"
      @submit="handleSubmitAnswers"
      @back="handleBackToExam"
    />

    <!-- Step 4: Grade View -->
    <GradeView
      v-if="step === 'grade' && gradeData && !loading"
      :grade="gradeData"
      :paper="examData"
      @view-key="handleViewKey"
      @reset="handleReset"
    />

    <!-- Step 5: Answer Key -->
    <AnswerKeyView
      v-if="step === 'key' && answerKeyData && examData && !loading"
      :answer-key="answerKeyData"
      :paper="examData"
      :grade="gradeData"
      @back="handleBackToGrade"
      @reset="handleReset"
    />
  </div>
</template>
