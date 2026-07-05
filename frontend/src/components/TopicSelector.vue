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
    alert('请输入或选择考察范围')
    return
  }
  emit('generate', topic)
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      📋 选择考察范围
    </div>
    <div class="card-body">
      <!-- Preset Topics -->
      <div class="form-label">预设考察领域</div>
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

      <!-- Custom Topic -->
      <div class="form-group mt-3">
        <div class="form-label">
          或输入自定义考察范围
          <small class="text-secondary">（如 "Redis：数据结构与集群"）</small>
        </div>
        <input
          class="form-input"
          type="text"
          v-model="customTopic"
          placeholder="例如：Go语言：goroutine与channel"
          @focus="enableCustom"
          @input="enableCustom"
          :class="{ active: useCustom }"
          style="border-color: v-bind('useCustom ? \"var(--primary)\" : \"var(--border)\"')"
        />
      </div>

      <!-- Generate Button -->
      <div class="text-center mt-4">
        <button class="btn btn-primary btn-lg" @click="handleGenerate">
          生成试卷
        </button>
        <p class="text-secondary" style="margin-top:8px;font-size:13px">
          将生成 20 题全题型试卷（单选≥10题 + 多选 + 判断 + 简答 + 论述）
        </p>
      </div>
    </div>
  </div>
</template>
