<script setup>
import { ref, reactive, computed } from 'vue'

const props = defineProps({
  paper: { type: Object, required: true },
})
const emit = defineEmits(['submit', 'back'])

// Initialize answers
const answers = reactive(
  props.paper.questions.map(q => ({
    question_id: q.id,
    answer: '',
    selectedChoices: [], // for multi_choice
  }))
)

const answeredCount = computed(() =>
  answers.filter(a => a.answer.trim().length > 0 || a.selectedChoices.length > 0).length
)

function getQuestion(id) {
  return props.paper.questions.find(q => q.id === id)
}

function getAnswer(qId) {
  return answers.find(a => a.question_id === qId)
}

function selectChoice(qId, choiceLabel, isMulti) {
  const ans = getAnswer(qId)
  if (isMulti) {
    const idx = ans.selectedChoices.indexOf(choiceLabel)
    if (idx >= 0) {
      ans.selectedChoices.splice(idx, 1)
    } else {
      ans.selectedChoices.push(choiceLabel)
    }
    ans.selectedChoices.sort()
    ans.answer = ans.selectedChoices.join('')
  } else {
    ans.answer = choiceLabel
    ans.selectedChoices = [choiceLabel]
  }
}

function setTrueFalse(qId, value) {
  const ans = getAnswer(qId)
  ans.answer = value
}

function handleSubmit() {
  // Validate at least all questions answered
  const unanswered = answers.filter(a => {
    const q = getQuestion(a.question_id)
    if (q.type === 'short_answer' || q.type === 'essay') {
      return a.answer.trim().length < 10
    }
    return !a.answer
  })
  if (unanswered.length > 0) {
    const confirmed = confirm(`还有 ${unanswered.length} 道题未作答，确定提交吗？`)
    if (!confirmed) return
  }
  emit('submit', answers.map(a => ({
    question_id: a.question_id,
    answer: a.answer || '（未作答）',
  })))
}

const typeNames = {
  single_choice: '单选',
  multi_choice: '多选',
  true_false: '判断',
  short_answer: '简答',
  essay: '论述',
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      ✍️ 在线作答 — {{ paper.subject }}
      <span style="margin-left:auto;font-size:13px;color:var(--text-secondary)">
        已答 {{ answeredCount }} / {{ paper.questions.length }} 题
      </span>
    </div>
    <div class="card-body">
      <div
        v-for="q in paper.questions"
        :key="q.id"
        class="question-card"
      >
        <div class="question-header">
          <span class="question-num">第 {{ q.id }} 题</span>
          <span class="question-type-badge" :class="{
            'badge-single': q.type === 'single_choice',
            'badge-multi': q.type === 'multi_choice',
            'badge-tf': q.type === 'true_false',
            'badge-short': q.type === 'short_answer',
            'badge-essay': q.type === 'essay',
          }">
            {{ typeNames[q.type] }}
          </span>
          <span class="question-score">{{ q.score }} 分</span>
        </div>
        <div class="question-content">{{ q.content }}</div>

        <!-- Single Choice -->
        <div v-if="q.type === 'single_choice' && q.choices" class="choices-list">
          <div
            v-for="c in q.choices"
            :key="c.label"
            class="choice-item"
            :class="{ selected: getAnswer(q.id).answer === c.label }"
            @click="selectChoice(q.id, c.label, false)"
          >
            <span class="choice-label">{{ c.label }}.</span>
            <span>{{ c.content }}</span>
          </div>
        </div>

        <!-- Multi Choice -->
        <div v-if="q.type === 'multi_choice' && q.choices" class="choices-list">
          <div
            v-for="c in q.choices"
            :key="c.label"
            class="choice-item"
            :class="{ selected: getAnswer(q.id).selectedChoices.includes(c.label) }"
            @click="selectChoice(q.id, c.label, true)"
          >
            <span class="choice-label">{{ c.label }}.</span>
            <span>{{ c.content }}</span>
          </div>
          <div v-if="getAnswer(q.id).selectedChoices.length" class="text-secondary" style="font-size:13px;margin-top:4px">
            已选: {{ getAnswer(q.id).selectedChoices.join(', ') }}
          </div>
        </div>

        <!-- True/False -->
        <div v-if="q.type === 'true_false'" style="display:flex;gap:12px">
          <button
            class="btn"
            :class="getAnswer(q.id).answer === '正确' ? 'btn-primary' : 'btn-outline'"
            @click="setTrueFalse(q.id, '正确')"
          >
            ✓ 正确
          </button>
          <button
            class="btn"
            :class="getAnswer(q.id).answer === '错误' ? 'btn-primary' : 'btn-outline'"
            @click="setTrueFalse(q.id, '错误')"
          >
            ✗ 错误
          </button>
        </div>

        <!-- Short Answer -->
        <div v-if="q.type === 'short_answer'">
          <textarea
            class="form-textarea"
            :value="getAnswer(q.id).answer"
            @input="e => getAnswer(q.id).answer = e.target.value"
            placeholder="请输入你的回答（50-150字）..."
            rows="4"
          ></textarea>
        </div>

        <!-- Essay -->
        <div v-if="q.type === 'essay'">
          <textarea
            class="form-textarea"
            :value="getAnswer(q.id).answer"
            @input="e => getAnswer(q.id).answer = e.target.value"
            placeholder="请输入你的论述（200-400字）..."
            rows="6"
          ></textarea>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex-between mt-4">
        <button class="btn btn-outline" @click="$emit('back')">返回查看试卷</button>
        <button class="btn btn-success btn-lg" @click="handleSubmit">
          提交答卷
        </button>
      </div>
    </div>
  </div>
</template>
