import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Home from '@/views/Home.vue';
import { auth } from '@/stores/auth';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('../views/LogoutView.vue')
    },
    {
      path: '/home',
      name: 'Home',
      component: () => import('../views/Home.vue'),
      beforeEnter: (to, from, next) => {
        const authStore = auth();
        if (authStore.isAuthenticated) {
          next();
        } else {
          next('/login');
        }
      }
    },
  ]})
  export default router