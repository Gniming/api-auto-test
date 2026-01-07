<template>
  <div class="env-list-container">
    <div class="page-header">
      <h2>环境管理</h2>
      <el-button type="primary" @click="handleCreateEnv">+ 新建环境</el-button>
    </div>
    <el-table :data="envs" style="width: 100%">
      <el-table-column prop="name" label="环境名" width="150"></el-table-column>
      <el-table-column prop="base_url" label="Base URL"></el-table-column>
      <el-table-column prop="description" label="描述"></el-table-column>
      <el-table-column prop="creator_name" label="创建人" width="120"></el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="handleEditEnv(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDeleteEnv(scope.row.id)">删除</el-button>
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

    <!-- 新建/编辑环境对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="envForm" label-width="80px">
        <el-form-item label="环境名">
          <el-input v-model="envForm.name" placeholder="请输入环境名"></el-input>
        </el-form-item>
        <el-form-item label="Base URL">
          <el-input v-model="envForm.base_url" placeholder="请输入基础URL"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="envForm.description" type="textarea" placeholder="请输入环境描述"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveEnv">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const envs = ref([])
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})
const dialogVisible = ref(false)
const dialogTitle = ref('新建环境')
const envForm = ref({
  id: null,
  name: '',
  base_url: '',
  description: ''
})

const loadEnvs = async () => {
  try {
    const response = await axios.get('http://localhost:5001/api/envs', {
      params: {
        page: pagination.value.page,
        page_size: pagination.value.pageSize
      }
    })
    if (response.data.code === 200) {
      envs.value = response.data.data.envs
      pagination.value.total = response.data.data.pagination.total
    }
  } catch (error) {
    console.error('获取环境列表失败:', error)
    ElMessage.error('获取环境列表失败')
  }
}

const handleCreateEnv = () => {
  envForm.value = {
    id: null,
    name: '',
    base_url: '',
    description: ''
  }
  dialogTitle.value = '新建环境'
  dialogVisible.value = true
}

const handleEditEnv = (row) => {
  envForm.value = {
    id: row.id,
    name: row.name,
    base_url: row.base_url,
    description: row.description
  }
  dialogTitle.value = '编辑环境'
  dialogVisible.value = true
}

const handleSaveEnv = async () => {
  try {
    let response
    if (envForm.value.id) {
      response = await axios.put(`http://localhost:5001/api/envs/${envForm.value.id}`, {
        name: envForm.value.name,
        base_url: envForm.value.base_url,
        description: envForm.value.description
      })
    } else {
      response = await axios.post('http://localhost:5001/api/envs', {
        name: envForm.value.name,
        base_url: envForm.value.base_url,
        description: envForm.value.description
      })
    }
    if (response.data.code === 200) {
      ElMessage.success(envForm.value.id ? '编辑成功' : '创建成功')
      dialogVisible.value = false
      loadEnvs()
    }
  } catch (error) {
    console.error('保存环境失败:', error)
    ElMessage.error('保存环境失败')
  }
}

const handleDeleteEnv = async (id) => {
  try {
    const response = await axios.delete(`http://localhost:5001/api/envs/${id}`)
    if (response.data.code === 200) {
      ElMessage.success('删除成功')
      loadEnvs()
    }
  } catch (error) {
    console.error('删除环境失败:', error)
    ElMessage.error('删除环境失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  pagination.value.page = 1
  loadEnvs()
}

const handleCurrentChange = (current) => {
  pagination.value.page = current
  loadEnvs()
}

onMounted(() => {
  loadEnvs()
})
</script>

<style scoped>
.env-list-container {
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

.dialog-footer {
  text-align: right;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>