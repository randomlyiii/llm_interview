<script setup>
import { computed } from 'vue'

const props = defineProps({
  grade: { type: Object, required: true },
  paper: { type: Object, required: true },
})
const emit = defineEmits(['view-key', 'reset'])

function getQuestion(id) {
  return props.paper.questions.find(q => q.id === id)
}

function getResult(id) {
  return props.grade.results.find(r => r.question_id === id)
}

function scoreClass(result) {
  if (!result) return ''
  const ratio = result.score / result.max_score
  if (ratio >= 1) return 'correct'
  if (ratio > 0) return 'partial'
  return 'wrong'
}

function scoreIcon(result) {
  if (!result) return ''
  const ratio = result.score / result.max_score
  if (ratio >= 1) return '✓'
  if (ratio > 0) return '△'
  return '✗'
}

const scorePercent = computed(() => {
  if (!props.grade) return 0
  return Math.round((props.grade.total_score / props.grade.max_score) * 100)
})

const correctCount = computed(() =>
  props.grade.results.filter(r => r.is_correct).length
)
const totalObjective = computed(() =>
  props.grade.results.filter(r => r.is_correct !== null).length
)
</script>

<template>
  <div class="card">
    <div class="card-header">
      📊 批改结果 — {{ paper.subject }}
    </div>
    <div class="card-body">
      <!-- Score Summary -->
      <div class="summary-card">
        <div class="summary-score">{{ grade.total_score }} / {{ grade.max_score }}</div>
        <div class="text-center text-secondary" style="font-size:15px;margin-top:4px">
          得分率 {{ scorePercent }}%
          <span v-if="totalObjective > 0">
            | 客观题正确 {{ correctCount }}/{{ totalObjective }}
          </span>
        </div>
      </div>

      <!-- Overall Summary -->
      <div v-if="grade.summary" class="status-bar success mb-3">
        <span style="font-size:13px;white-space:pre-wrap">{{ grade.summary }}</span>
      </div>

      <!-- Per-Question Results -->
      <div
        v-for="r in grade.results"
        :key="r.question_id"
        class="grade-item"
      >
        <div class="grade-score" :class="scoreClass(r)">
          <div>{{ scoreIcon(r) }}</div>
          <div>{{ r.score }}/{{ r.max_score }}</div>
        </div>
        <div style="flex:1">
          <div style="font-weight:600;margin-bottom:4px">
            第 {{ r.question_id }} 题
            <span class="text-secondary" style="font-weight:400;font-size:13px">
              {{ getQuestion(r.question_id)?.topic }}
            </span>
          </div>
          <div style="font-size:14px;line-height:1.6;white-space:pre-wrap">
            {{ r.comment }}
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex-between mt-4">
        <button class="btn btn-outline" @click="$emit('reset')">重新选题</button>
        <button class="btn btn-primary btn-lg" @click="$emit('view-key')">
          查看标准答案
        </button>
      </div>
    </div>
  </div>
</template>
