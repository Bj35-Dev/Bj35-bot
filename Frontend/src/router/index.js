 // * @copyright Copyright (c) 2020-2025 The ESAP Project.
 // * @author AptS:1547
 // * @Link https://esaps.net/
 // * @version 0.1.0
 // * @license
 // * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
import { createRouter, createWebHistory } from 'vue-router'
import AuthService from '@/services/AuthService'

const routes = [
  { path: '/', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },

  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.name !== 'Login' && !AuthService.isAuthenticated()) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && AuthService.isAuthenticated()) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router