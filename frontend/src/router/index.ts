import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import MainLayout from '../layout/MainLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import History from '../views/History.vue'
import Login from '../views/Login.vue'
import Settings from '../views/Settings.vue'
import Prompts from '../views/Prompts.vue'
import PromptsCreate from '../views/PromptsCreate.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'dashboard',
        component: Dashboard
      },
      {
        path: 'history',
        name: 'history',
        component: History
      },
      {
        path: 'settings',
        name: 'settings',
        component: Settings
      },
      {
        path: 'prompts',
        name: 'prompts',
        component: Prompts
      },
      {
        path: 'prompts/new',
        name: 'prompts-create',
        component: PromptsCreate
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
