<template>
  <div id="app">
    <nav v-if="showNavbar" class="navbar">
      <div class="nav-brand">养殖场智能决策系统</div>
      <div class="nav-menu">
        <span class="welcome">欢迎, {{ username }}</span>
        <button @click="goToProfile" class="nav-btn">个人中心</button>
        <button @click="handleLogout" class="nav-btn logout">退出登录</button>
      </div>
    </nav>

    <router-view />
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';


const router = useRouter();
const route = useRoute();
const username = ref('');

// 动态判断是否显示导航栏
// 逻辑：当前路由不是 /login 且 localStorage 中有登录状态
const showNavbar = computed(() => {
  return route.path !== '/login' && localStorage.getItem('isLogin') === 'true';
});

// 监听路由变化，实时获取最新的用户名（防止登录后刷新才显示）
watch(() => route.path, () => {
  username.value = localStorage.getItem('username') || '';
});

// 导航到个人页面
const goToProfile = () => {
  router.push('/profile'); 
};

// 退出登录逻辑
const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    localStorage.removeItem('isLogin');
    localStorage.removeItem('username');
    alert('已退出登录');
    router.push('/login');
  }
};
</script>

<style>
/* 全局基础样式 */
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', sans-serif;
  background-color: #f5f7fa;
  color: #2c3e50;
}

#app {
  -webkit-font-smoothing: antialiased;
}

/* 导航栏样式 */
/* .navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #ffffff;
  height: 60px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
} */

.nav-brand {
  font-size: 1.2rem;
  font-weight: bold;
  color: #3498db;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 15px;
}

.welcome {
  font-size: 0.9rem;
  color: #606266;
}

.nav-btn {
  padding: 8px 16px;
  border: 1px solid #dcdfe6;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-btn:hover {
  color: #409eff;
  border-color: #409eff;
}

.nav-btn.logout {
  background-color: #f56c6c;
  color: white;
  border: none;
}

.nav-btn.logout:hover {
  background-color: #f78989;
}

/* 导航栏样式优化 */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  
  /* --- 关键修改：透明度与毛玻璃 --- */
  background-color: rgba(255, 255, 255, 0.5); /* 白色，0.7透明度 */
  backdrop-filter: blur(10px);               /* 毛玻璃模糊效果 */
  -webkit-backdrop-filter: blur(10px);        /* 兼容 Safari */
  
  height: 60px;
  /* 阴影调淡一点，配合透明感 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05); 
  border-bottom: 1px solid rgba(255, 255, 255, 0.3); /* 增加一条细微的高光边框 */
  
  position: sticky;
  top: 0;
  z-index: 1000;
}


.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  height: 64px;
  
  /* --- 关键修改：悬浮布局 --- */
  position: fixed;   /* 变成固定定位，不再占位 */
  top: 0;
  left: 0;
  right: 0;          /* 铺满宽度 */
  z-index: 1000;     /* 确保在最上层 */

  /* 背景保持暗色毛玻璃 */
  background-color: rgba(0, 0, 0, 0.15); 
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  
  /* 移除外边距确保贴顶 */
  margin: 0;
}
</style>