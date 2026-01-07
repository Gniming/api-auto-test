import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import LayoutView from '../views/LayoutView.vue'
import { useUserStore } from '../stores/userStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/',
      name: 'layout',
      component: LayoutView,
      redirect: '/projects',
      meta: { requiresAuth: true },
      children: [
        {
          path: 'projects',
          name: 'projects',
          component: () => import('../views/ProjectListView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'envs',
          name: 'envs',
          component: () => import('../views/EnvListView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'common-params',
          name: 'common-params',
          component: () => import('../views/CommonParamsView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'projects/:id/cases',
          name: 'case-list',
          component: () => import('../views/CaseListView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'cases/:id/edit',
          name: 'case-edit',
          component: () => import('../views/CaseEditView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'tasks/:id',
          name: 'task-detail',
          component: () => import('../views/TaskDetailView.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: 'reports',
          name: 'reports',
          component: () => import('../views/ReportListView.vue'),
          meta: { requiresAuth: true }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    // 检查用户是否已登录
    if (userStore.isLoggedIn) {
      next()
    } else {
      // 未登录，重定向到登录页
      next({ name: 'login' })
    }
  } else {
    next()
  }
})

export default router