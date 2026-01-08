<template>
  <div class="common-params-container">
    <div class="page-header">
      <h2>公共参数管理</h2>
      <el-button type="primary" @click="handleCreateParam">+ 新建公共参数组</el-button>
    </div>
    
    <el-table :data="globalParams" style="width: 100%" :cell-style="{ padding: '12px 8px' }">
      <el-table-column prop="name" label="名称" width="180"></el-table-column>
      <el-table-column prop="headers" label="Headers 预览" min-width="300" flex="1">
        <template #default="scope">
          <pre class="headers-preview">{{ typeof scope.row.headers === 'object' ? JSON.stringify(scope.row.headers, null, 2) : scope.row.headers }}</pre>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" width="150"></el-table-column>
      <el-table-column prop="creator_name" label="创建人" width="120"></el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="handleEditParam(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDeleteParam(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页组件 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="globalPagination.page"
        v-model:page-size="globalPagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="globalPagination.total"
        @size-change="handleGlobalSizeChange"
        @current-change="handleGlobalCurrentChange"
      />
    </div>
    
    <!-- 新建/编辑公共参数对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="paramForm" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="paramForm.name" placeholder="请输入参数组名称"></el-input>
        </el-form-item>
        <el-form-item label="Headers">
          <el-input 
            v-model="paramForm.headers" 
            type="textarea" 
            placeholder="请输入 Headers JSON"
            rows="6"
          ></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="paramForm.description" type="textarea" placeholder="请输入描述"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveParam">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const activeTab = ref('global')
const globalParams = ref([])
const projectParams = ref([])
const globalPagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})
const projectPagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})
const dialogVisible = ref(false)
const dialogTitle = ref('新建公共参数组')
const paramForm = ref({
  id: null,
  name: '',
  headers: '{}',
  description: '',
  scope: 'global'
})

const loadCommonParams = async () => {
  try {
    const response = await axios.get('http://localhost:5001/api/common-params', {
      params: {
        page: 1,
        page_size: 100 // 加载足够多的参数以支持标签页切换
      }
    })
    if (response.data.code === 200) {
      const params = response.data.data.common_params
      globalParams.value = params.filter(p => p.project_id === null)
      projectParams.value = params.filter(p => p.project_id !== null)
      globalPagination.value.total = globalParams.value.length
      projectPagination.value.total = projectParams.value.length
    }
  } catch (error) {
    console.error('获取公共参数失败:', error)
    ElMessage.error('获取公共参数失败')
  }
}

const handleCreateParam = () => {
  paramForm.value = {
    id: null,
    name: '',
    headers: '{}',
    description: '',
    scope: 'global'
  }
  dialogTitle.value = '新建公共参数组'
  dialogVisible.value = true
}

const handleEditParam = (row) => {
  paramForm.value = {
    id: row.id,
    name: row.name,
    headers: typeof row.headers === 'object' ? JSON.stringify(row.headers, null, 2) : row.headers,
    description: row.description,
    scope: row.project_id === null ? 'global' : 'project'
  }
  dialogTitle.value = '编辑公共参数组'
  dialogVisible.value = true
}

const handleSaveParam = async () => {
  try {
    let response
    const data = {
      project_id: paramForm.value.scope === 'global' ? null : 1, // 假设当前项目ID为1
      name: paramForm.value.name,
      headers: typeof paramForm.value.headers === 'string' ? JSON.parse(paramForm.value.headers) : paramForm.value.headers,
      description: paramForm.value.description
    }
    
    if (paramForm.value.id) {
      response = await axios.put(`http://localhost:5001/api/common-params/${paramForm.value.id}`, data)
    } else {
      response = await axios.post('http://localhost:5001/api/common-params', data)
    }
    
    if (response.data.code === 200) {
      ElMessage.success(paramForm.value.id ? '编辑成功' : '创建成功')
      dialogVisible.value = false
      loadCommonParams()
    }
  } catch (error) {
    console.error('保存公共参数失败:', error)
    ElMessage.error('保存公共参数失败')
  }
}

const handleDeleteParam = async (id) => {
  try {
    const response = await axios.delete(`http://localhost:5001/api/common-params/${id}`)
    if (response.data.code === 200) {
      ElMessage.success('删除成功')
      loadCommonParams()
    }
  } catch (error) {
    console.error('删除公共参数失败:', error)
    ElMessage.error('删除公共参数失败')
  }
}

const handleGlobalSizeChange = (size) => {
  globalPagination.value.pageSize = size
  globalPagination.value.page = 1
}

const handleGlobalCurrentChange = (current) => {
  globalPagination.value.page = current
}

const handleProjectSizeChange = (size) => {
  projectPagination.value.pageSize = size
  projectPagination.value.page = 1
}

const handleProjectCurrentChange = (current) => {
  projectPagination.value.page = current
}

onMounted(() => {
  loadCommonParams()
})
</script>

<style scoped>
.common-params-container {
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

.page-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.headers-preview {
  font-size: 12px;
  line-height: 1.4;
  margin: 0;
  color: #666;
  white-space: pre-wrap;
  word-wrap: break-word;
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