<template>
  <div class="case-list-container">
    <div class="page-header">
      <h2>用例列表</h2>
      <div class="header-actions">
        <el-select v-model="projectId" placeholder="选择项目" @change="handleProjectChange" style="width: 200px; margin-right: 10px;">
          <el-option 
            v-for="project in projects" 
            :key="project.id" 
            :label="project.name" 
            :value="project.id"
          ></el-option>
        </el-select>
        <el-button type="primary" @click="handleCreateCase">+ 新建用例</el-button>
        <el-button @click="loadCases" class="reload-button">刷新</el-button>
      </div>
    </div>
    <el-table :data="cases" style="width: 100%">
      <el-table-column prop="name" label="用例名" width="200"></el-table-column>
      <el-table-column prop="description" label="描述"></el-table-column>
      <el-table-column prop="creator_name" label="创建人" width="100"></el-table-column>
      <el-table-column prop="last_executed" label="最后执行时间" width="180"></el-table-column>
      <el-table-column label="操作" width="300">
        <template #default="scope">
          <div class="action-buttons">
          <el-button size="small" @click="handleEditCase(scope.row.id)">编辑</el-button>
          <el-button size="small" type="primary" @click="handleRunCase(scope.row.id)">执行</el-button>
          <el-button size="small" type="danger" @click="handleDeleteCase(scope.row.id)">删除</el-button>
          <el-button size="small" @click="handleCopyCase(scope.row.id)">复制</el-button>
        </div>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页组件 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 新建/编辑用例对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="caseForm" label-width="80px">
        <el-form-item label="用例名">
          <el-input v-model="caseForm.name" placeholder="请输入用例名"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="caseForm.description" type="textarea" placeholder="请输入用例描述"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveCase">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const projectId = ref(route.params.id)
const projects = ref([])
const cases = ref([])
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})
const dialogVisible = ref(false)
const dialogTitle = ref('新建用例')
const caseForm = ref({
  id: null,
  name: '',
  description: ''
})
const environments = ref([])
const commonParams = ref([])
const execDialogVisible = ref(false)
const execDialogTitle = ref('执行配置')
const execConfig = ref({
  envId: null,
  commonParamsIds: [],
  caseId: null
})
const loadProjects = async () => {
  try {
    const response = await axios.get('http://localhost:5001/api/projects')
    if (response.data.code === 200) {
      projects.value = response.data.data.projects
      // 如果没有项目ID，使用第一个项目
      if (!projectId.value && projects.value.length > 0) {
        projectId.value = projects.value[0].id
        loadCases()
      } else if (projectId.value && projects.value.length > 0) {
        // 确保项目ID有效
        const projectExists = projects.value.some(p => p.id == projectId.value)
        if (!projectExists) {
          projectId.value = projects.value[0].id
          loadCases()
        }
      }
    }
  } catch (error) {
    console.error('获取项目列表失败:', error)
  }
}

const handleProjectChange = (id) => {
  projectId.value = id
  loadCases()
}

const loadCases = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/api/projects/${projectId.value}/cases`, {
      params: {
        page: pagination.value.page,
        page_size: pagination.value.pageSize
      }
    })
    if (response.data.code === 200) {
      cases.value = response.data.data.cases.map(caseItem => ({
        ...caseItem,
        creator_name: caseItem.creator_id || '-',
        last_executed: caseItem.last_executed || '-'
      }))
      pagination.value.total = response.data.data.pagination.total
    }
  } catch (error) {
    console.error('获取用例列表失败:', error)
    ElMessage.error('获取用例列表失败')
  }
}
const handleCreateCase = () => {
  caseForm.value = {
    id: null,
    name: '',
    description: ''
  }
  dialogTitle.value = '新建用例'
  dialogVisible.value = true
}

const handleEditCase = (id) => {
  router.push(`/cases/${id}/edit`)
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

const handleRunCase = async (id) => {
  await loadEnvironmentsAndParams()
  
  if (environments.value.length === 0) {
    ElMessage.warning('请先创建环境')
    return
  }
  
  // 打开执行配置对话框
  execConfig.value = {
    envId: environments.value[0].id,
    commonParamsIds: [],
    caseId: id
  }
  execDialogTitle.value = '执行用例'
  execDialogVisible.value = true
}

const handleExecConfirm = async () => {
  try {
    if (!execConfig.value.envId) {
      ElMessage.warning('请选择环境')
      return
    }
    
    const response = await axios.post(`http://localhost:5001/api/cases/${execConfig.value.caseId}/run`, {
      env_id: execConfig.value.envId,
      common_params_ids: execConfig.value.commonParamsIds
    })
    
    if (response.data.code === 200) {
      ElMessage.success('执行成功')
      router.push(`/tasks/${response.data.data.task_id}`)
    }
    
    execDialogVisible.value = false
  } catch (error) {
    console.error('执行失败:', error)
    ElMessage.error('执行失败')
  }
}
const handleSaveCase = async () => {
  try {
    let response
    if (caseForm.value.id) {
      response = await axios.put(`http://localhost:5001/api/cases/${caseForm.value.id}`, {
        name: caseForm.value.name,
        description: caseForm.value.description
      })
    } else {
      response = await axios.post(`http://localhost:5001/api/projects/${projectId.value}/cases`, {
        name: caseForm.value.name,
        description: caseForm.value.description
      })
    }
    if (response.data.code === 200) {
      ElMessage.success(caseForm.value.id ? '编辑成功' : '创建成功')
      dialogVisible.value = false
      loadCases()
    }
  } catch (error) {
    console.error('保存用例失败:', error)
    ElMessage.error('保存用例失败')
  }
}

const handleDeleteCase = async (id) => {
  try {
    const response = await axios.delete(`http://localhost:5001/api/cases/${id}`)
    if (response.data.code === 200) {
      ElMessage.success('删除成功')
      loadCases()
    }
  } catch (error) {
    console.error('删除用例失败:', error)
    ElMessage.error('删除用例失败')
  }
}
const handleCopyCase = (id) => {
  ElMessage.info('复制功能待实现')
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  pagination.value.page = 1
  loadCases()
}

const handleCurrentChange = (current) => {
  pagination.value.page = current
  loadCases()
}

onMounted(async () => {
  await loadProjects()
})</script>

<style scoped>
.case-list-container {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
}

.reload-button {
  margin-left: 10px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
  align-items: center;
  flex-wrap: wrap;
}

.page-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.dialog-footer {
  text-align: right;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>