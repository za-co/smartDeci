<template>
  <div class="login-container">
    <div class="login-box">
      <h2>{{ isLoginMode ? '养殖场智能决策系统' : '新用户注册' }}</h2>
      
      <div class="form-group">
        <input v-model="form.username" placeholder="用户名" />
        <input v-model="form.password" type="password" placeholder="密码" />
        <input 
          v-if="!isLoginMode" 
          v-model="form.confirmPassword" 
          type="password" 
          placeholder="确认密码" 
        />
      </div>

      <button @click="handleSubmit" :disabled="loading" class="main-btn">
        {{ loading ? '处理中...' : (isLoginMode ? '立即登录' : '提交注册') }}
      </button>

      <div class="switch-mode">
        <span>{{ isLoginMode ? '还没有账号？' : '已有账号？' }}</span>
        <a @click="isLoginMode = !isLoginMode">
          {{ isLoginMode ? '立即注册' : '返回登录' }}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const loading = ref(false);
const isLoginMode = ref(true); // 切换登录/注册模式

const form = ref({ 
  username: '', 
  password: '',
  confirmPassword: '' // 注册专用
});

// 统一提交入口
const handleSubmit = () => {
  if (isLoginMode.value) {
    handleLogin();
  } else {
    handleRegister();
  }
};

// 注册逻辑
const handleRegister = async () => {
  // 1. 简单的表单校验
  if (!form.value.username || !form.value.password) {
    return alert('请填写完整信息');
  }
  if (form.value.password !== form.value.confirmPassword) {
    return alert('两次输入的密码不一致');
  }

  loading.value = true;
  try {
    const res = await axios.post('http://localhost:8000/api/register/', {
      username: form.value.username,
      password: form.value.password
    });

    if (res.status === 201) {
      alert('注册成功！请登录');
      isLoginMode.value = true; // 自动跳转到登录模式
      form.value.confirmPassword = '';
    }
  } catch (err) {
    const errorMsg = err.response?.data?.error || '注册失败，请稍后重试';
    alert(errorMsg);
  } finally {
    loading.value = false;
  }
};

// 登录逻辑
const handleLogin = async () => {
  if (!form.value.username || !form.value.password) return alert('请输入用户名和密码');
  
  loading.value = true; 
  try {
    const res = await axios.post('http://localhost:8000/api/login/', {
      username: form.value.username,
      password: form.value.password
    });
    
    if (res.status === 200) {
      localStorage.setItem('isLogin', 'true');
      localStorage.setItem('username', res.data.username);
      alert('登录成功！');
      router.push('/home');
    }
  } catch (err) {
    if (err.response?.status === 401) {
      alert('用户名或密码错误');
    } else {
      alert('连接服务器失败');
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container { 
  height: 100vh; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  background: linear-gradient(135deg, #2c3e50, #4ca1af); 
}

.login-box { 
  background: white; 
  padding: 40px; 
  border-radius: 12px; 
  width: 350px; 
  text-align: center; 
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

h2 { color: #333; margin-bottom: 30px; font-size: 22px; }

.form-group { margin-bottom: 20px; }

input { 
  width: 100%; 
  padding: 12px; 
  margin: 10px 0; 
  border: 1px solid #ddd; 
  border-radius: 6px; 
  box-sizing: border-box; 
  transition: border 0.3s;
}

input:focus { border-color: #3498db; outline: none; }

.main-btn { 
  width: 100%; 
  padding: 12px; 
  background: #3498db; 
  color: white; 
  border: none; 
  border-radius: 6px; 
  cursor: pointer; 
  font-size: 16px;
  font-weight: bold;
}

.main-btn:disabled { background: #bdc3c7; cursor: not-allowed; }

.switch-mode { margin-top: 20px; font-size: 14px; color: #666; }

.switch-mode a { 
  color: #3498db; 
  cursor: pointer; 
  margin-left: 5px; 
  text-decoration: underline; 
}

/* 外层容器：动态渐变背景 */
.login-container { 
  height: 100vh; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  /* 科技感深绿到深蓝的渐变 */
  background: linear-gradient(-45deg, #1e3c72, #2a5298, #2ecc71, #27ae60);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  overflow: hidden;
  position: relative;
}

/* 动态流体动画 */
@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* 装饰性漂浮圆圈 */
.login-container::after, .login-container::before {
  content: "";
  position: absolute;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  z-index: 0;
  animation: float 20s infinite linear;
}

.login-container::before { top: -10%; left: -5%; }
.login-container::after { bottom: -10%; right: -5%; animation-duration: 25s; }

@keyframes float {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(100px, 100px) rotate(360deg); }
}

/* 登录框：毛玻璃效果 */
.login-box { 
  background: rgba(255, 255, 255, 0.85); 
  backdrop-filter: blur(15px); /* 背景模糊 */
  padding: 40px; 
  border-radius: 24px; 
  width: 380px; 
  text-align: center; 
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  z-index: 1;
  transition: transform 0.3s ease;
}

.login-box:hover {
  transform: translateY(-5px); /* 悬浮时轻微向上移动 */
}

h2 { color: #2c3e50; margin-bottom: 30px; font-size: 24px; letter-spacing: 1px; }

/* 输入框优化 */
input { 
  width: 100%; 
  padding: 14px; 
  margin: 12px 0; 
  border: 2px solid transparent; 
  border-radius: 12px; 
  background: rgba(240, 242, 245, 0.8);
  box-sizing: border-box; 
  transition: all 0.3s;
  font-size: 14px;
}

input:focus { 
  border-color: #2ecc71; 
  background: #fff;
  box-shadow: 0 0 15px rgba(46, 204, 113, 0.2);
  outline: none; 
}

/* 按钮动画 */
.main-btn { 
  width: 100%; 
  padding: 14px; 
  background: linear-gradient(to right, #2ecc71, #27ae60); 
  color: white; 
  border: none; 
  border-radius: 12px; 
  cursor: pointer; 
  font-size: 16px;
  font-weight: bold;
  margin-top: 20px;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);
}

.main-btn:hover { 
  transform: scale(1.02);
  box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4);
}

.main-btn:active { transform: scale(0.98); }

.switch-mode { margin-top: 25px; font-size: 14px; color: #7f8c8d; }

.switch-mode a { 
  color: #27ae60; 
  font-weight: bold;
  cursor: pointer; 
  margin-left: 5px; 
  text-decoration: none;
  transition: color 0.3s;
}

.switch-mode a:hover { color: #2ecc71; }

</style>