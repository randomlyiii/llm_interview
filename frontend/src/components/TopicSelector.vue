<script setup>
import { ref } from 'vue'

const emit = defineEmits(['generate'])

const presetTopics = [
  { key: 'java', label: 'Java', desc: 'JVM、内存模型、垃圾回收、类加载' },
  { key: 'c++', label: 'C++', desc: '多线程与多进程、内存管理、RAII' },
  { key: 'python', label: 'Python', desc: 'GIL、asyncio、装饰器、生成器' },
  { key: 'mysql', label: 'MySQL', desc: '索引、事务、锁、SQL 优化' },
  { key: 'linux', label: 'Linux', desc: 'CPU调度、内核、Docker、常用指令' },
  { key: 'llm', label: 'LLM', desc: 'MCP协议、RAG、Prompt Engineering' },
]

const selectedTopic = ref('java')
const customTopic = ref('')
const useCustom = ref(false)

function selectTopic(key) {
  selectedTopic.value = key
  useCustom.value = false
}

function enableCustom() {
  useCustom.value = true
  selectedTopic.value = ''
}

function handleGenerate() {
  const topic = useCustom.value ? customTopic.value.trim() : selectedTopic.value
  if (!topic) {
    alert('Please select or enter a topic')
    return
  }
  emit('generate', topic)
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      Select Topic
    </div>
    <div class="card-body">
      <div class="form-label">Preset Topics</div>
      <div class="tag-grid mb-3">
        <button
          v-for="t in presetTopics"
          :key="t.key"
          class="tag"
          :class="{ active: selectedTopic === t.key && !useCustom }"
          @click="selectTopic(t.key)"
        >
          <strong>{{ t.label }}</strong>
          <br />
          <small class="text-secondary">{{ t.desc }}</small>
        </button>
      </div>

      <div class="form-group mt-3">
        <div class="form-label">
          Or enter a custom topic
          <small class="text-secondary">(e.g. "Redis: data structures and clustering")</small>
        </div>
        <input
          class="form-input"
          type="text"
          v-model="customTopic"
          placeholder="e.g. Go: goroutines and channels"
          @focus="enableCustom"
          @input="enableCustom"
          :style="{ borderColor: useCustom ? 'var(--primary)' : 'var(--border)' }"
        />
      </div>

      <div class="text-center mt-4">
        <button class="btn btn-primary btn-lg" @click="handleGenerate">
          Generate Exam
        </button>
        <p class="text-secondary" style="margin-top:8px;font-size:13px">
          20 questions: 10+ single choice, multi choice, T/F, short answer, essay
        </p>
      </div>
    </div>
  </div>
</template>
