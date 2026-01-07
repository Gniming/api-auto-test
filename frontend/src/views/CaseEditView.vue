<template>
  <div class="case-edit-container">
    <div class="case-header">
      <el-button @click="handleBack">← 返回</el-button>
      <div class="case-info">
        <el-input v-model="caseInfo.name" placeholder="用例名称" class="case-name-input"></el-input>
        <el-input v-model="caseInfo.description" type="textarea" placeholder="用例描述" class="case-description-input"></el-input>
      </div>
      <el-button type="primary" @click="handleSaveCase" class="save-button">保存</el-button>
    </div>
    
    <div class="case-content">
      <div class="steps-list">
        <h3>步骤列表</h3>
        <el-button type="primary" @click="handleAddStep" class="add-step-button">+ 添加步骤</el-button>
        <div class="step-items">
          <div 
            v-for="(step, index) in steps" 
            :key="step.id || index"
            class="step-item"
            :class="{ active: activeStepIndex === index }"
            @click="handleSelectStep(index)"
          >
            <div class="step-header">
              <span class="step-index">{{ index + 1 }}</span>
              <span class="step-name">{{ step.name }}</span>
              <span class="step-method">{{ step.method }}</span>
              <span class="step-path">{{ step.path }}</span>
              <div class="step-actions">
                <el-button size="small" @click.stop="handleEditStep(index)">编辑</el-button>
                <el-button size="small" type="danger" @click.stop="handleDeleteStep(index)">删除</el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="step-detail" v-if="activeStep">
        <h3>步骤详情</h3>
        <el-form :model="activeStep" label-width="100px">
          <el-form-item label="步骤名称">
            <el-input v-model="activeStep.name" placeholder="步骤名称"></el-input>
          </el-form-item>
          <el-form-item label="请求方法">
            <el-select v-model="activeStep.method" placeholder="请求方法">
              <el-option label="GET" value="GET"></el-option>
              <el-option label="POST" value="POST"></el-option>
              <el-option label="PUT" value="PUT"></el-option>
              <el-option label="DELETE" value="DELETE"></el-option>
              <el-option label="PATCH" value="PATCH"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="请求路径">
            <el-input v-model="activeStep.path" placeholder="请求路径"></el-input>
          </el-form-item>
          
          <el-tabs v-model="activeTab">
            <el-tab-pane label="Params" name="params">
              <el-button type="primary" size="small" @click="handleAddParam">+ 添加参数</el-button>
              <el-table :data="activeStep.request.paramsList" style="width: 100%; margin-top: 10px;">
                <el-table-column prop="key" label="参数名" width="150">
                  <template #default="scope">
                    <el-input v-model="scope.row.key" placeholder="参数名"></el-input>
                  </template>
                </el-table-column>
                <el-table-column prop="value" label="参数值">
                  <template #default="scope">
                    <el-input v-model="scope.row.value" placeholder="参数值"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="100">
                  <template #default="scope">
                    <el-button size="small" type="danger" @click="handleDeleteParam(scope.$index)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="Headers" name="headers">
              <el-button type="primary" size="small" @click="handleAddHeader">+ 添加头部</el-button>
              <el-table :data="activeStep.request.headersList" style="width: 100%; margin-top: 10px;">
                <el-table-column prop="key" label="头部名" width="150">
                  <template #default="scope">
                    <el-input v-model="scope.row.key" placeholder="头部名"></el-input>
                  </template>
                </el-table-column>
                <el-table-column prop="value" label="头部值">
                  <template #default="scope">
                    <el-input v-model="scope.row.value" placeholder="头部值"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="100">
                  <template #default="scope">
                    <el-button size="small" type="danger" @click="handleDeleteHeader(scope.$index)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="Body" name="body">
              <el-input 
                v-model="activeStep.request.data" 
                type="textarea" 
                placeholder="Body JSON"
                rows="6"
              ></el-input>
            </el-tab-pane>
          </el-tabs>
          
          <el-form-item label="变量提取">
            <el-button type="primary" size="small" @click="handleAddExtract">+ 添加提取规则</el-button>
            <el-table :data="activeStep.extracts" style="width: 100%; margin-top: 10px;">
                  <el-table-column prop="var_name" label="变量名" width="150">
                    <template #default="scope">
                      <el-input v-model="scope.row.var_name" placeholder="变量名"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column prop="expression" label="表达式">
                    <template #default="scope">
                      <el-input v-model="scope.row.expression" placeholder="表达式"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="100">
                    <template #default="scope">
                      <el-button size="small" type="danger" @click="handleDeleteExtract(scope.$index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
          </el-form-item>
          
          <el-form-item label="断言规则">
            <el-button type="primary" size="small" @click="handleAddAssert">+ 添加断言</el-button>
            <el-table :data="activeStep.asserts" style="width: 100%; margin-top: 10px;">
                  <el-table-column prop="assert_type" label="类型" width="150">
                    <template #default="scope">
                      <el-select v-model="scope.row.assert_type" placeholder="断言类型">
                        <el-option label="status_code" value="status_code"></el-option>
                        <el-option label="contain" value="contain"></el-option>
                        <el-option label="not_contain" value="not_contain"></el-option>
                        <el-option label="json_equal" value="json_equal"></el-option>
                        <el-option label="json_schema" value="json_schema"></el-option>
                        <el-option label="regex" value="regex"></el-option>
                        <el-option label="length" value="length"></el-option>
                        <el-option label="database" value="database"></el-option>
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="expect_value" label="预期值">
                    <template #default="scope">
                      <el-input v-model="scope.row.expect_value" placeholder="预期值"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column prop="actual_source" label="来源">
                    <template #default="scope">
                      <el-input 
                        v-model="scope.row.actual_source" 
                        placeholder="来源 (如: response_body 或 JSONPath 表达式 $.code)"
                      ></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="100">
                    <template #default="scope">
                      <el-button size="small" type="danger" @click="handleDeleteAssert(scope.$index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
          </el-form-item>
        </el-form>
        
        <div class="step-actions-bottom">
          <el-button type="primary" @click="handleTestStep">测试当前步骤</el-button>
          <el-button @click="handleRunFromStep">从此步骤开始测试</el-button>
          <el-button type="success" @click="handleRunFullCase">执行完整用例</el-button>
        </div>
        
        <!-- 执行配置对话框 -->
        <el-dialog v-model="execDialogVisible" :title="execDialogTitle" width="600px">
          <el-form label-width="100px">
            <el-form-item label="选择环境">
              <el-select v-model="execConfig.envId" placeholder="请选择环境" style="width: 100%">
                <el-option 
                  v-for="env in environments" 
                  :key="env.id" 
                  :label="env.name + ' - ' + env.base_url" 
                  :value="env.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="选择公共参数">
              <el-checkbox-group v-model="execConfig.commonParamsIds">
                <el-checkbox 
                  v-for="param in commonParams" 
                  :key="param.id" 
                  :label="param.id"
                  style="display: block; margin-bottom: 10px;"
                >
                  {{ param.name }} ({{ param.project_id ? '项目级' : '全局' }})
                </el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="execDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="handleExecConfirm">确定</el-button>
            </span>
          </template>
        </el-dialog>
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
const caseId = ref(route.params.id)
const caseInfo = ref({
  name: '',
  description: ''
})
const steps = ref([])
const activeStepIndex = ref(-1)
const activeTab = ref('headers')
const environments = ref([])
const commonParams = ref([])
const execDialogVisible = ref(false)
const execDialogTitle = ref('执行配置')
const execConfig = ref({
  envId: null,
  commonParamsIds: [],
  execType: '', // 'step', 'fromStep', 'full'
  stepId: null
})
const activeStep = computed(() => {
  if (activeStepIndex.value >= 0 && activeStepIndex.value < steps.value.length) {
    return steps.value[activeStepIndex.value]
  }
  return null
})

const loadCaseInfo = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/api/cases/${caseId.value}/edit`)
    if (response.data.code === 200) {
      caseInfo.value = response.data.data.case
      steps.value = response.data.data.steps.map(step => {
        // 确保请求数据格式正确
        if (!step.request) {
          step.request = {
            headersList: [],
            paramsList: [],
            data: '{}',
            timeout: 30
          }
        } else {
          // 处理 headers
          if (typeof step.request.headers === 'object') {
            // 将headers对象转换为headersList数组
            const headersObj = step.request.headers
            step.request.headersList = Object.entries(headersObj).map(([key, value]) => ({
              key,
              value: String(value)
            }))
          } else {
            // 如果是字符串，尝试解析为对象
            try {
              const headersObj = JSON.parse(step.request.headers)
              step.request.headersList = Object.entries(headersObj).map(([key, value]) => ({
                key,
                value: String(value)
              }))
            } catch {
              step.request.headersList = []
            }
          }
          
          // 处理 params
          if (typeof step.request.params === 'object') {
            // 将params对象转换为paramsList数组
            const paramsObj = step.request.params
            step.request.paramsList = Object.entries(paramsObj).map(([key, value]) => ({
              key,
              value: String(value)
            }))
          } else {
            // 如果是字符串，尝试解析为对象
            try {
              const paramsObj = JSON.parse(step.request.params)
              step.request.paramsList = Object.entries(paramsObj).map(([key, value]) => ({
                key,
                value: String(value)
              }))
            } catch {
              step.request.paramsList = []
            }
          }
          
          // 处理 data
          if (typeof step.request.data === 'object') {
            step.request.data = JSON.stringify(step.request.data, null, 2)
          }
        }
        // 确保提取和断言数组存在
        if (!step.extracts) {
          step.extracts = []
        }
        if (!step.asserts) {
          step.asserts = []
        }
        return step
      })
      if (steps.value.length > 0) {
          activeStepIndex.value = 0
        }
      }
    } catch (error) {
      console.error('获取用例信息失败:', error)
      ElMessage.error('获取用例信息失败')
    }
  }
  
  // 初始化时加载环境和公共参数
  onMounted(async () => {
    await loadCaseInfo()
    await loadEnvironmentsAndParams()
  })

const handleBack = () => {
  router.push('/projects/1/cases')
}

const handleSaveCase = async () => {
  try {
    // 准备保存数据
    const saveData = {
      case_name: caseInfo.value.name,
      case_description: caseInfo.value.description,
      steps: steps.value.map(step => {
        // 将字符串转换回对象
        try {
          // 将headersList转换为headers对象
          const headers = {}
          if (step.request.headersList) {
            step.request.headersList.forEach(item => {
              if (item.key) {
                headers[item.key] = item.value
              }
            })
          }
          
          // 将paramsList转换为params对象
          const params = {}
          if (step.request.paramsList) {
            step.request.paramsList.forEach(item => {
              if (item.key) {
                params[item.key] = item.value
              }
            })
          }
          
          return {
            id: step.id,
            name: step.name,
            method: step.method,
            path: step.path,
            sort: step.sort,
            enabled: step.enabled,
            request: {
              headers: headers,
              params: params,
              data: JSON.parse(step.request.data),
              timeout: step.request.timeout || 30
            },
            extracts: step.extracts || [],
            asserts: step.asserts || []
          }
        } catch (e) {
          ElMessage.error('JSON 格式错误，请检查')
          return step
        }
      })
    }
    
    const response = await axios.put(`http://localhost:5001/api/cases/${caseId.value}/steps/batch`, saveData)
    if (response.data.code === 200) {
      ElMessage.success('保存成功')
    }
  } catch (error) {
    console.error('保存用例失败:', error)
    ElMessage.error('保存用例失败')
  }
}

const handleAddStep = () => {
  const newStep = {
    id: null,
    name: '新步骤',
    method: 'GET',
    path: '',
    request: {
      headersList: [],
      paramsList: [],
      data: '{}',
      timeout: 30
    },
    extracts: [],
    asserts: []
  }
  steps.value.push(newStep)
  activeStepIndex.value = steps.value.length - 1
}

const handleSelectStep = (index) => {
  activeStepIndex.value = index
}

const handleDeleteStep = (index) => {
  steps.value.splice(index, 1)
  if (activeStepIndex.value >= index) {
    activeStepIndex.value = Math.max(0, activeStepIndex.value - 1)
  }
}

const handleEditStep = (index) => {
  // 编辑步骤逻辑，这里直接选中步骤即可
  activeStepIndex.value = index
}

const handleAddExtract = () => {
  if (activeStep.value) {
    activeStep.value.extracts.push({
      var_name: '',
      expression: ''
    })
  }
}

const handleDeleteExtract = (index) => {
  if (activeStep.value) {
    activeStep.value.extracts.splice(index, 1)
  }
}

const handleAddHeader = () => {
  if (activeStep.value) {
    if (!activeStep.value.request.headersList) {
      activeStep.value.request.headersList = []
    }
    activeStep.value.request.headersList.push({
      key: '',
      value: ''
    })
  }
}

const handleDeleteHeader = (index) => {
  if (activeStep.value && activeStep.value.request.headersList) {
    activeStep.value.request.headersList.splice(index, 1)
  }
}

const handleAddParam = () => {
  if (activeStep.value) {
    if (!activeStep.value.request.paramsList) {
      activeStep.value.request.paramsList = []
    }
    activeStep.value.request.paramsList.push({
      key: '',
      value: ''
    })
  }
}

const handleDeleteParam = (index) => {
  if (activeStep.value && activeStep.value.request.paramsList) {
    activeStep.value.request.paramsList.splice(index, 1)
  }
}

const handleAddAssert = () => {
  if (activeStep.value) {
    activeStep.value.asserts.push({
      assert_type: 'status_code',
      expect_value: '200',
      actual_source: 'response_status'
    })
  }
}

const handleDeleteAssert = (index) => {
  if (activeStep.value) {
    activeStep.value.asserts.splice(index, 1)
  }
}

const loadEnvironmentsAndParams = async () => {
  try {
    // 加载环境列表
    const envResponse = await axios.get('http://localhost:5001/api/envs')
    if (envResponse.data.code === 200) {
      environments.value = envResponse.data.data.envs
    }
    
    // 加载公共参数列表
    const paramsResponse = await axios.get('http://localhost:5001/api/common-params')
    if (paramsResponse.data.code === 200) {
      commonParams.value = paramsResponse.data.data.common_params
    }
  } catch (error) {
    console.error('加载环境和参数失败:', error)
  }
}

const handleTestStep = async () => {
  if (!activeStep.value) {
    ElMessage.warning('请先选择步骤')
    return
  }
  
  if (!activeStep.value.id) {
    ElMessage.warning('请先保存步骤')
    return
  }
  
  await loadEnvironmentsAndParams()
  
  if (environments.value.length === 0) {
    ElMessage.warning('请先创建环境')
    return
  }
  
  // 打开执行配置对话框
  execConfig.value = {
    envId: environments.value[0].id,
    commonParamsIds: [],
    execType: 'step',
    stepId: activeStep.value.id
  }
  execDialogTitle.value = '测试当前步骤'
  execDialogVisible.value = true
}

const handleRunFromStep = async () => {
  ElMessage.info('功能待实现')
}

const handleRunFullCase = async () => {
  await loadEnvironmentsAndParams()
  
  if (environments.value.length === 0) {
    ElMessage.warning('请先创建环境')
    return
  }
  
  // 打开执行配置对话框
  execConfig.value = {
    envId: environments.value[0].id,
    commonParamsIds: [],
    execType: 'full',
    stepId: null
  }
  execDialogTitle.value = '执行完整用例'
  execDialogVisible.value = true
}

const handleExecConfirm = async () => {
  try {
    if (!execConfig.value.envId) {
      ElMessage.warning('请选择环境')
      return
    }
    
    switch (execConfig.value.execType) {
      case 'step':
        // 测试单个步骤
        const debugResponse = await axios.post('http://localhost:5001/api/debug/run', {
          env_id: execConfig.value.envId,
          step_ids: [execConfig.value.stepId],
          common_params_ids: execConfig.value.commonParamsIds
        })
        if (debugResponse.data.code === 200) {
          ElMessage.success('测试成功')
          router.push(`/tasks/${debugResponse.data.data.task_id}`)
        }
        break
        
      case 'full':
        // 执行完整用例
        const fullResponse = await axios.post(`http://localhost:5001/api/cases/${caseId.value}/run`, {
          env_id: execConfig.value.envId,
          common_params_ids: execConfig.value.commonParamsIds
        })
        if (fullResponse.data.code === 200) {
          ElMessage.success('执行成功')
          router.push(`/tasks/${fullResponse.data.data.task_id}`)
        }
        break
    }
    
    execDialogVisible.value = false
  } catch (error) {
    console.error('执行失败:', error)
    ElMessage.error('执行失败')
  }
}

onMounted(() => {
  loadCaseInfo()
})
</script>

<style scoped>
.case-edit-container {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.case-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.case-info {
  flex: 1;
  margin: 0 20px;
}

.case-name-input {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.case-description-input {
  min-height: 60px;
}

.save-button {
  white-space: nowrap;
}

.case-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.steps-list {
  width: 300px;
  border-right: 1px solid #e0e0e0;
  padding-right: 20px;
  overflow-y: auto;
}

.steps-list h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.add-step-button {
  margin-bottom: 20px;
}

.step-items {
  margin-top: 10px;
}

.step-item {
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.step-item:hover {
  border-color: #409eff;
}

.step-item.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.step-index {
  display: inline-block;
  width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  background-color: #409eff;
  color: white;
  border-radius: 50%;
  margin-right: 10px;
}

.step-name {
  font-weight: bold;
  margin-right: 10px;
}

.step-method {
  display: inline-block;
  padding: 2px 8px;
  background-color: #f0f9ff;
  color: #409eff;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 10px;
}

.step-path {
  font-size: 12px;
  color: #666;
}

.step-actions {
  margin-top: 10px;
  text-align: right;
}

.step-detail {
  flex: 1;
  padding-left: 20px;
  overflow-y: auto;
}

.step-detail h3 {
  margin-top: 0;
  margin-bottom: 20px;
}

.step-actions-bottom {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 10px;
}

@media (max-width: 1200px) {
  .case-content {
    flex-direction: column;
  }
  
  .steps-list {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
    padding-right: 0;
    padding-bottom: 20px;
    margin-bottom: 20px;
  }
  
  .step-detail {
    padding-left: 0;
  }
}
</style>