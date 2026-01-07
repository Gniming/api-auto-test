import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    isLoggedIn: !!localStorage.getItem('user')
  }),
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('http://localhost:5001/api/login', {
          username,
          password
        })
        if (response.data.code === 200) {
          this.user = response.data.data.user
          this.isLoggedIn = true
          // 持久化到本地存储
          localStorage.setItem('user', JSON.stringify(response.data.data.user))
          return true
        }
        return false
      } catch (error) {
        console.error('登录失败:', error)
        return false
      }
    },
    async logout() {
      try {
        await axios.post('http://localhost:5001/api/logout')
        this.user = null
        this.isLoggedIn = false
        // 清除本地存储
        localStorage.removeItem('user')
        return true
      } catch (error) {
        console.error('注销失败:', error)
        return false
      }
    }
  }
})