import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import Home from '@/components/Home.vue'
import Search from '@/components/Search.vue'
import Profile from '@/components/Profile.vue'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Search',
        component: Search
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  try {
    axios.get('/verify').then(response => {
      if (!response.data.success) {
        // localStorage.removeItem('user')
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
