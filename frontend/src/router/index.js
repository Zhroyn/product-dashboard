import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import Home from '@/components/Home.vue'
import { ElMessage } from "element-plus";
import axios from 'axios'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  try{
    axios.get('/verify').then(response => {
      if (!response.data.success) {
        localStorage.removeItem('user')
      }
    })
  } catch (error) {
    ElMessage.error(error.message)
  }
  
  const isAuthenticated = localStorage.getItem('user')
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.name === 'login' && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router