<script setup>
const props = defineProps({
  answerKey: { type: Object, required: true },
  paper: { type: Object, required: true },
  grade: { type: Object, default: null },
})
const emit = defineEmits(['back', 'reset'])

function getQuestion(id) {
  return props.paper.questions.find(q => q.id === id)
}

function getKeyItem(id) {
  return props.answerKey.items.find(i => i.question_id === id)
}

function getGradeResult(id) {
  if (!props.grade) return null
  return props.grade.results.find(r => r.question_id === id)
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
      📖 标准答案与解析 — {{ paper.subject }}
    </div>
    <div class="card-body">
      <div
        v-for="item in answerKey.items"
        :key="item.question_id"
        class="question-card"
      >
        <div class="question-header">
          <span class="question-num">第 {{ item.question_id }} 题</span>
          <span class="question-type-badge" :class="{
            'badge-single': getQuestion(item.question_id)?.type === 'single_choice',
            'badge-multi': getQuestion(item.question_id)?.type === 'multi_choice',
            'badge-tf': getQuestion(item.question_id)?.type === 'true_false',
            'badge-short': getQuestion(item.question_id)?.type === 'short_answer',
            'badge-essay': getQuestion(item.question_id)?.type === 'essay',
          }">
            {{ typeNames[getQuestion(item.question_id)?.type] }}
          </span>
          <span class="text-secondary" style="font-size:12px">
            {{ getQuestion(item.question_id)?.topic }}
          </span>

          <!-- Show grade if available -->
          <span
            v-if="getGradeResult(item.question_id)"
            style="margin-left:auto;font-size:13px"
            :style="{
              color: getGradeResult(item.question_id).score === getGradeResult(item.question_id).max_score
                ? 'var(--success)' : getGradeResult(item.question_id).score > 0
                ? 'var(--warning)' : 'var(--danger)'
            }"
          >
            你的得分: {{ getGradeResult(item.question_id).score }}/{{ getGradeResult(item.question_id).max_score }}
          </span>
        </div>

        <div class="question-content">
          {{ getQuestion(item.question_id)?.content }}
        </div>

        <!-- Choices for reference -->
        <div v-if="getQuestion(item.question_id)?.choices?.length" style="margin-bottom:8px;font-size:13px;color:var(--text-secondary)">
          <div v-for="c in getQuestion(item.question_id).choices" :key="c.label">
            {{ c.label }}. {{ c.content }}
          </div>
        </div>

        <!-- Correct Answer -->
        <div class="answer-correct">
          <strong>正确答案：</strong>{{ item.correct_answer }}
        </div>

        <!-- Explanation -->
        <div class="answer-explanation">
          <strong>解析：</strong>{{ item.explanation }}
        </div>

        <!-- Key Points -->
        <div v-if="item.key_points && item.key_points.length" class="key-points">
          <strong style="font-size:13px">采分点：</strong>
          <span
            v-for="(kp, idx) in item.key_points"
            :key="idx"
            class="key-point-tag"
          >
            {{ kp }}
          </span>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex-between mt-4">
        <button class="btn btn-outline" @click="$emit('back')">返回批改结果</button>
        <button class="btn btn-primary btn-lg" @click="$emit('reset')">重新选题</button>
      </div>
    </div>
  </div>
</template>
