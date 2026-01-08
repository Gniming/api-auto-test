<template>
  <el-container class="layout-container">
    <el-header class="header">
      <div class="logo">API 测试平台</div>

      <div class="user-info">
        <el-dropdown>
          <span class="user-avatar">{{ userStore.user?.nickname || '用户' }}</span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handleLogout">注销</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px" class="aside">
        <el-menu
          :default-active="activeMenu"
          class="menu"
          router
          @select="handleMenuSelect"
        >
          <el-menu-item index="/projects">
            <span>项目管理</span>
          </el-menu-item>
          <el-menu-item index="/envs">
            <span>环境管理</span>
          </el-menu-item>
          <el-menu-item index="/common-params">
            <span>公共参数</span>
          </el-menu-item>
          <el-menu-item index="/projects/1/cases">
            <span>用例管理</span>
          </el-menu-item>
          <el-menu-item index="/reports">
            <span>报告中心</span>
          </el-menu-item>
          <el-menu-item index="/builtin-functions">
            <span>内置函数</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/projects/') && path.includes('/cases')) {
    return '/projects/1/cases'
  }
  return path
})

const handleMenuSelect = (key) => {
  router.push(key)
}

const handleLogout = async () => {
  const success = await userStore.logout()
  if (success) {
    ElMessage.success('注销成功')
    router.push('/login')
  } else {
    ElMessage.error('注销失败')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.header {
  height: 60px;
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  font-size: 18px;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-avatar {
  cursor: pointer;
  padding: 0 10px;
}

.aside {
  background-color: #f0f2f5;
}

.menu {
  height: 100%;
}

.main {
  padding: 20px;
  background-color: #f9f9f9;
  overflow: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>