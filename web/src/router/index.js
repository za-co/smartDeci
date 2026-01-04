import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/login.vue';
import Home from '../views/home.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { 
    path: '/home', 
    name: 'Home', 
    component: Home,
    // 简单模拟守卫：未登录跳回登录页
    beforeEnter: (to, from, next) => {
      const isLogin = localStorage.getItem('isLogin');
      isLogin ? next() : next('/login');
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
