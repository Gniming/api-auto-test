<template>
  <div class="project-list-container">
    <div class="page-header">
      <h2>项目管理</h2>
      <el-button type="primary" @click="handleCreateProject">+ 新建项目</el-button>
    </div>
    <el-table :data="projects" style="width: 100%">
      <el-table-column prop="name" label="项目名" width="200"></el-table-column>
      <el-table-column prop="description" label="描述"></el-table-column>
      <el-table-column prop="creator_name" label="创建人" width="120"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="handleEditProject(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDeleteProject(scope.row.id)">删除</el-button>
          <el-button size="small" @click="handleEnterProject(scope.row.id)">进入</el-button>
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

    <!-- 新建/编辑项目对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="projectForm" label-width="80px">
        <el-form-item label="项目名">
          <el-input v-model="projectForm.name" placeholder="请输入项目名"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="projectForm.description" type="textarea" placeholder="请输入项目描述"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveProject">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()

const projects = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新建项目')
const projectForm = ref({
  id: null,
  name: '',
  description: ''
})

// 分页相关状态
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const loadProjects = async () => {
  try {
    const response = await axios.get('http://localhost:5001/api/projects', {
      params: {
        page: pagination.value.page,
        page_size: pagination.value.pageSize
      }
    })
    if (response.data.code === 200) {
      projects.value = response.data.data.projects
      pagination.value.total = response.data.data.pagination.total
    }
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
  }
}

// 分页相关事件处理函数
const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadProjects()
}

const handleCurrentChange = (current) => {
  pagination.value.page = current
  loadProjects()
}

const handleCreateProject = () => {
  projectForm.value = {
    id: null,
    name: '',
    description: ''
  }
  dialogTitle.value = '新建项目'
  dialogVisible.value = true
}

const handleEditProject = (row) => {
  projectForm.value = {
    id: row.id,
    name: row.name,
    description: row.description
  }
  dialogTitle.value = '编辑项目'
  dialogVisible.value = true
}

const handleSaveProject = async () => {
  try {
    let response
    if (projectForm.value.id) {
      response = await axios.put(`http://localhost:5001/api/projects/${projectForm.value.id}`, {
        name: projectForm.value.name,
        description: projectForm.value.description
      })
    } else {
      response = await axios.post('http://localhost:5001/api/projects', {
        name: projectForm.value.name,
        description: projectForm.value.description
      })
    }
    if (response.data.code === 200) {
      ElMessage.success(projectForm.value.id ? '编辑成功' : '创建成功')
      dialogVisible.value = false
      loadProjects()
    }
  } catch (error) {
    console.error('保存项目失败:', error)
    ElMessage.error('保存项目失败')
  }
}

const handleDeleteProject = async (id) => {
  try {
    const response = await axios.delete(`http://localhost:5001/api/projects/${id}`)
    if (response.data.code === 200) {
      ElMessage.success('删除成功')
      loadProjects()
    }
  } catch (error) {
    console.error('删除项目失败:', error)
    ElMessage.error('删除项目失败')
  }
}

const handleEnterProject = (id) => {
  router.push(`/projects/${id}/cases`)
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.project-list-container {
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

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  text-align: right;
}
</style>