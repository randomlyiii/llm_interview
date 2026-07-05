<script setup>
const props = defineProps({
  paper: { type: Object, required: true },
})
const emit = defineEmits(['start-answer', 'reset'])

const typeNames = {
  single_choice: '单选',
  multi_choice: '多选',
  true_false: '判断',
  short_answer: '简答',
  essay: '论述',
}

const badgeClasses = {
  single_choice: 'badge-single',
  multi_choice: 'badge-multi',
  true_false: 'badge-tf',
  short_answer: 'badge-short',
  essay: 'badge-essay',
}

function getDifficultyText(d) {
  return d === 'easy' ? '简单' : d === 'hard' ? '困难' : '中等'
}

// 统计题型分布
function countByType(type) {
  return props.paper.questions.filter(q => q.type === type).length
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      📝 {{ paper.subject }} — 面试模拟试卷
      <span style="margin-left:auto;font-size:13px;color:var(--text-secondary)">
        {{ paper.generated_at?.slice(0, 10) }}
      </span>
    </div>
    <div class="card-body">
      <!-- Paper Meta -->
      <div class="status-bar mb-3">
        <span>📊 共 <strong>{{ paper.questions.length }}</strong> 题</span>
        <span>⭐ 满分 <strong>{{ paper.total_score }}</strong> 分</span>
        <span>⏱️ 建议 <strong>{{ paper.duration_minutes }}</strong> 分钟</span>
        <span v-if="paper.topic_detail" class="text-secondary" style="font-size:13px">
          | {{ paper.topic_detail.slice(0, 60) }}{{ paper.topic_detail.length > 60 ? '...' : '' }}
        </span>
      </div>

      <!-- Type Distribution -->
      <div class="text-secondary mb-3" style="font-size:13px;">
        题型分布：单选 {{ countByType('single_choice') }} 题 |
        多选 {{ countByType('multi_choice') }} 题 |
        判断 {{ countByType('true_false') }} 题 |
        简答 {{ countByType('short_answer') }} 题 |
        论述 {{ countByType('essay') }} 题
      </div>

      <!-- Questions -->
      <div v-for="q in paper.questions" :key="q.id" class="question-card">
        <div class="question-header">
          <span class="question-num">第 {{ q.id }} 题</span>
          <span class="question-type-badge" :class="badgeClasses[q.type]">
            {{ typeNames[q.type] }}
          </span>
          <span class="text-secondary" style="font-size:12px">{{ q.topic }}</span>
          <span
            class="text-secondary"
            style="font-size:12px"
            :style="{ color: q.difficulty === 'hard' ? 'var(--danger)' : q.difficulty === 'easy' ? 'var(--success)' : 'var(--warning)' }"
          >
            {{ getDifficultyText(q.difficulty) }}
          </span>
          <span class="question-score">{{ q.score }} 分</span>
        </div>

        <div class="question-content">{{ q.content }}</div>

        <!-- Choices -->
        <div v-if="q.choices && q.choices.length" class="choices-list">
          <div
            v-for="c in q.choices"
            :key="c.label"
            class="choice-item"
            style="cursor:default"
          >
            <span class="choice-label">{{ c.label }}.</span>
            <span>{{ c.content }}</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex-between mt-4">
        <button class="btn btn-outline" @click="$emit('reset')">返回选题</button>
        <button class="btn btn-primary btn-lg" @click="$emit('start-answer')">
          开始作答
        </button>
      </div>
    </div>
  </div>
</template>
