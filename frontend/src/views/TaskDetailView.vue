<template>
  <div class="task-detail-container">
    <div class="task-header">
      <el-button @click="handleBack">← 返回</el-button>
      <h2>执行报告详情</h2>
      <el-button type="primary" @click="handleReRun">重新执行</el-button>
    </div>
    
    <div class="task-summary">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>执行摘要</span>
          </div>
        </template>
        <div class="summary-content">
          <div class="summary-item">
            <span class="label">执行状态：</span>
            <span class="value" :class="taskInfo.status">{{ taskInfo.status }}</span>
          </div>
          <div class="summary-item">
            <span class="label">执行时间：</span>
            <span class="value">{{ taskInfo.duration }} 秒</span>
          </div>
          <div class="summary-item">
            <span class="label">环境：</span>
            <span class="value">{{ taskInfo.env_name }}</span>
          </div>
          <div class="summary-item">
            <span class="label">执行时间：</span>
            <span class="value">{{ taskInfo.created_at }}</span>
          </div>
          <div class="summary-stats">
            <div class="stat-item">
              <span class="stat-label">总步骤</span>
              <span class="stat-value">{{ taskInfo.total_steps }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">通过</span>
              <span class="stat-value success">{{ taskInfo.pass_count }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">失败</span>
              <span class="stat-value error">{{ taskInfo.fail_count }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">通过率</span>
              <span class="stat-value">{{ passRate }}%</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    
    <div class="task-steps">
      <h3>执行步骤</h3>
      <div class="step-timeline">
        <div 
          v-for="(step, index) in taskLog" 
          :key="index"
          class="step-item"
        >
          <div class="step-header">
            <div class="step-index" :class="{ success: step.passed, error: !step.passed }">
              {{ step.passed ? '✓' : '✗' }}
            </div>
            <div class="step-info">
              <h4>{{ step.step_name }}</h4>
              <div class="step-request-info">
                <span class="method">{{ step.request.method }}</span>
                <span class="url">{{ step.request.url }}</span>
              </div>
            </div>
            <div class="step-status" :class="{ success: step.passed, error: !step.passed }">
              {{ step.passed ? '通过' : '失败' }}
            </div>
          </div>
          
          <div class="step-details">
            <el-collapse>
              <el-collapse-item title="请求信息">
                <pre>{{ formatJson(step.request) }}</pre>
              </el-collapse-item>
              <el-collapse-item title="响应信息">
                <pre>{{ formatJson(step.response) }}</pre>
              </el-collapse-item>
              <el-collapse-item title="提取结果">
                <div v-if="Object.keys(step.extract_results || {}).length > 0">
                  <el-table :data="extractResultsData(step.extract_results)">
                    <el-table-column prop="key" label="变量名"></el-table-column>
                    <el-table-column prop="value" label="值"></el-table-column>
                  </el-table>
                </div>
                <div v-else>
                  <p>无提取结果</p>
                </div>
              </el-collapse-item>
              <el-collapse-item title="断言结果">
                <el-table :data="step.assert_results">
                  <el-table-column prop="type" label="类型"></el-table-column>
                  <el-table-column prop="expect" label="预期值"></el-table-column>
                  <el-table-column prop="actual" label="实际值"></el-table-column>
                  <el-table-column label="结果">
                    <template #default="scope">
                      <span :class="{ success: scope.row.passed, error: !scope.row.passed }">
                        {{ scope.row.passed ? '通过' : '失败' }}
                      </span>
                    </template>
                  </el-table-column>
                </el-table>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const taskId = ref(route.params.id)
const taskInfo = ref({
  status: '',
  duration: 0,
  env_name: '',
  created_at: '',
  total_steps: 0,
  pass_count: 0,
  fail_count: 0
})
const taskLog = ref([])

const passRate = computed(() => {
  if (taskInfo.value.total_steps === 0) return 0
  return Math.round((taskInfo.value.pass_count / taskInfo.value.total_steps) * 100)
})

const loadTaskDetail = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/api/tasks/${taskId.value}`)
    if (response.data.code === 200) {
      const data = response.data.data
      // 构建任务信息
      taskInfo.value = {
        status: data.summary.pass === data.summary.total_steps ? 'success' : 'failed',
        duration: data.summary.duration,
        env_name: '测试环境', // 这里需要从环境接口获取，暂时硬编码
        created_at: new Date().toLocaleString(), // 这里需要从任务接口获取，暂时硬编码
        total_steps: data.summary.total_steps,
        pass_count: data.summary.pass,
        fail_count: data.summary.fail
      }
      taskLog.value = data.log
    }
  } catch (error) {
    console.error('获取任务详情失败:', error)
    ElMessage.error('获取任务详情失败')
  }
}

const handleBack = () => {
  router.push('/projects/1/reports')
}

const handleReRun = () => {
  ElMessage.info('重新执行功能待实现')
}

const formatJson = (obj) => {
  try {
    return JSON.stringify(obj, null, 2)
  } catch (e) {
    return obj
  }
}

const extractResultsData = (extracts) => {
  return Object.entries(extracts || {}).map(([key, value]) => ({
    key,
    value
  }))
}

onMounted(() => {
  loadTaskDetail()
})
</script>

<style scoped>
.task-detail-container {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.task-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.task-header h2 {
  flex: 1;
  margin: 0;
  margin-left: 20px;
}

.task-summary {
  margin-bottom: 30px;
}

.summary-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.summary-item {
  display: flex;
  align-items: center;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  min-width: 80px;
}

.value {
  color: #666;
}

.value.success {
  color: #67c23a;
}

.value.failed {
  color: #f56c6c;
}

.value.running {
  color: #409eff;
}

.summary-stats {
  display: flex;
  gap: 30px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
  width: 100%;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
}

.stat-value.success {
  color: #67c23a;
}

.stat-value.error {
  color: #f56c6c;
}

.task-steps {
  margin-top: 30px;
}

.task-steps h3 {
  margin-bottom: 20px;
}

.step-timeline {
  position: relative;
  padding-left: 30px;
}

.step-timeline::before {
  content: '';
  position: absolute;
  left: 10px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #e0e0e0;
}

.step-item {
  position: relative;
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.step-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.step-index {
  position: absolute;
  left: -25px;
  top: 20px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  background-color: #e0e0e0;
  color: white;
}

.step-index.success {
  background-color: #67c23a;
}

.step-index.error {
  background-color: #f56c6c;
}

.step-info {
  flex: 1;
  margin-left: 10px;
}

.step-info h4 {
  margin: 0 0 10px 0;
}

.step-request-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.method {
  display: inline-block;
  padding: 2px 8px;
  background-color: #409eff;
  color: white;
  border-radius: 4px;
  font-size: 12px;
}

.url {
  font-family: monospace;
  color: #666;
  font-size: 14px;
}

.step-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.step-status.success {
  background-color: #f0f9ff;
  color: #67c23a;
}

.step-status.error {
  background-color: #fef0f0;
  color: #f56c6c;
}

.step-details {
  margin-top: 15px;
}

pre {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  font-family: monospace;
  font-size: 13px;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .summary-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .summary-stats {
    flex-wrap: wrap;
  }
  
  .step-request-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}
</style>