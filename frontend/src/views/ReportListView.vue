<template>
  <div class="report-list-container">
    <div class="page-header">
      <h2>执行报告列表</h2>
      <div class="header-actions">
        <el-select v-model="projectId" placeholder="选择项目" @change="handleProjectChange" style="width: 200px; margin-right: 10px;">
          <el-option 
            v-for="project in projects" 
            :key="project.id" 
            :label="project.name" 
            :value="project.id"
          ></el-option>
        </el-select>
        <el-button @click="loadReports">刷新</el-button>
      </div>
    </div>
    
    <el-table :data="reports" style="width: 100%">
      <el-table-column prop="created_at" label="执行时间" width="180"></el-table-column>
      <el-table-column prop="case_name" label="用例名" min-width="200" flex="1"></el-table-column>
      <el-table-column prop="env_name" label="环境" width="120"></el-table-column>
      <el-table-column prop="executor_name" label="执行人" width="120"></el-table-column>
      <el-table-column prop="status" label="结果" width="80">
        <template #default="scope">
          <span :class="scope.row.status">{{ scope.row.status }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="pass_rate" label="通过率" width="80">
        <template #default="scope">
          <span>{{ scope.row.pass_rate }}%</span>
        </template>
      </el-table-column>
      <el-table-column prop="duration" label="耗时" width="80"></el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="scope">
          <el-button size="small" @click="handleViewDetail(scope.row.task_id)">查看详情</el-button>
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
const reports = ref([])
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const loadProjects = async () => {
  try {
    const response = await axios.get('http://localhost:5001/api/projects')
    if (response.data.code === 200) {
      projects.value = response.data.data.projects
      // 如果没有项目ID，使用第一个项目
      if (!projectId.value && projects.value.length > 0) {
        projectId.value = projects.value[0].id
        loadReports()
      } else if (projectId.value) {
        // 如果有项目ID，直接加载报告
        loadReports()
      }
    }
  } catch (error) {
    console.error('获取项目列表失败:', error)
  }
}

const handleProjectChange = (id) => {
  projectId.value = id
  loadReports()
}

const loadReports = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/api/projects/${projectId.value}/reports`, {
      params: {
        page: pagination.value.page,
        page_size: pagination.value.pageSize
      }
    })
    if (response.data.code === 200) {
      reports.value = response.data.data.reports.map(report => {
        // 计算通过率
        const pass_rate = report.total_steps > 0 ? Math.round((report.pass_count / report.total_steps) * 100) : 0
        return {
          ...report,
          pass_rate
        }
      })
      pagination.value.total = response.data.data.pagination.total
    }
  } catch (error) {
    console.error('获取报告列表失败:', error)
    ElMessage.error('获取报告列表失败')
  }
}

const handleViewDetail = (taskId) => {
  router.push(`/tasks/${taskId}`)
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  pagination.value.page = 1
  loadReports()
}

const handleCurrentChange = (current) => {
  pagination.value.page = current
  loadReports()
}

onMounted(async () => {
  await loadProjects()
})
</script>

<style scoped>
.report-list-container {
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

.page-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.success {
  color: #67c23a;
}

.failed {
  color: #f56c6c;
}

.running {
  color: #409eff;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>