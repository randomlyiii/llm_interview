import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000, // 2 minutes for LLM calls
})

/**
 * 生成面试模拟试卷
 * @param {string} subject - 考察领域
 * @param {number} questionCount - 题目总数
 * @param {number} singleChoiceMin - 最少选择题数
 */
export async function generateExam(subject, questionCount = 20, singleChoiceMin = 10) {
  const { data } = await api.post('/generate', {
    subject,
    question_count: questionCount,
    single_choice_min: singleChoiceMin,
  })
  return data
}

/**
 * 获取已生成的试卷
 * @param {string} examId
 */
export async function getExam(examId) {
  const { data } = await api.get(`/exam/${examId}`)
  return data
}

/**
 * 提交答卷进行批改
 * @param {string} examId
 * @param {Array} answers - [{question_id, answer}, ...]
 */
export async function gradeExam(examId, answers) {
  const { data } = await api.post(`/grade/${examId}`, {
    exam_id: examId,
    answers,
  })
  return data
}

/**
 * 获取标准答案与解析
 * @param {string} examId
 */
export async function getAnswerKey(examId) {
  const { data } = await api.get(`/answer-key/${examId}`)
  return data
}

/**
 * 健康检查
 */
export async function healthCheck() {
  const { data } = await api.get('/health')
  return data
}
