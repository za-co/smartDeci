<template>
  <div class="login-container">
    <div class="login-box">
      <h2>养殖场智能决策系统</h2>
      <input v-model="form.username" placeholder="用户名" />
      <input v-model="form.password" type="password" placeholder="密码" />
      <button @click="handleLogin" :disabled="loading">
        {{ loading ? '登录中...' : '立即登录' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const loading = ref(false);
const form = ref({ username: '', password: '' });

const handleLogin = async () => {
  // 1. 修正 loading 赋值
  loading.value = true; 
  try {
    // 2. 确保 URL 完全匹配（注意末尾斜杠）
    const res = await axios.post('api/login/', form.value);
    // const res = await axios.post('http://localhost:8000/api/login/', form.value);
    
    // 3. Django 默认不返回 res.data.code，直接判断 res.status 或数据内容
    if (res.status === 200) {
      localStorage.setItem('isLogin', 'true');
      localStorage.setItem('username', res.data.username);
      alert('登录成功！');
      router.push('/home');
    }
  } catch (err) {
    // 4. 细化错误提示
    if (err.response && err.response.status === 401) {
      alert('用户名或密码错误');
    } else if (err.response && err.response.status === 404) {
      alert('接口路径错误 (404)，请检查 Django 路由配置');
    } else {
      alert('网络错误或服务器未启动');
    }
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container { height: 100vh; display: flex; align-items: center; justify-content: center; background: #2c3e50; }
.login-box { background: white; padding: 40px; border-radius: 12px; width: 350px; text-align: center; }
input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
button { width: 100%; padding: 12px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>