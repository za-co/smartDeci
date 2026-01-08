<template>
  <div class="profile-page">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else class="container">
      <aside class="profile-card">
        <div class="avatar-section">
          <div class="avatar-placeholder">{{ userInfo.username[0] }}</div>
          <h2>{{ userInfo.username }}</h2>
          <span class="badge">{{ userInfo.role }}</span>
        </div>
        <div class="info-list">
          <!-- <div class="info-item"><label>邮箱</label><span>{{ userInfo.email }}</span></div> -->
          <div class="info-item"><label>加入于</label><span>{{ userInfo.date_joined }}</span></div>
          <div class="info-item"><label>上次登录</label><span>{{ formatTime(userInfo.last_login) }}</span></div>
        </div>
        <button class="btn-logout" @click="handleLogout">返回面板</button>
      </aside>

      <main class="main-content">
        <section class="stats-grid">
          <div class="stat-card">
            <p>负责设备总数</p>
            <div class="value">{{ userInfo.stats?.total_sensors || 0 }} 台</div>
          </div>
          <div class="stat-card alert">
            <p>当前异常告警</p>
            <div class="value">{{ userInfo.stats?.active_alerts || 0 }} 条</div>
          </div>
        </section>

        <section class="settings-card">
          <h3>账号设置</h3>
          <div class="setting-item">
            <span>消息通知推送</span>
            <input type="checkbox" v-model="notifications">
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const notifications = ref(true)
const userInfo = ref({
  username: '',
  role: '',
  email: '',
  date_joined: '',
  last_login: '',
  stats: { total_sensors: 0, active_alerts: 0 } // 预设结构
})

const fetchUserInfo = async () => {
  // 从登录时存入的 localStorage 获取用户名
  const savedUsername = localStorage.getItem('username')
  if (!savedUsername) {
    alert('请先登录')
    window.location.href = '/login'
    return
  }

  try {
    // 增加 params 传递用户名，确保后端能查到数据
    const res = await axios.get('http://localhost:8000/api/user/info/', {
      params: { username: savedUsername }
    })
    userInfo.value = res.data
  } catch (err) {
    console.error("加载失败:", err)
    alert('获取信息失败，请检查后端服务')
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
//   localStorage.clear()
  window.location.href = '/home'
}

// 时间处理函数：手动增加 8 小时
const formatTime = (timeStr) => {
  if (!timeStr) return '无数据'
  try {
    // 1. 解析原始时间
    const date = new Date(timeStr)
    
    // 2. 手动增加 8 小时的毫秒数
    const offsetDate = new Date(date.getTime() + 8 * 60 * 60 * 1000)
    
    // 3. 使用手动拼接，避免 toISOString() 强制转回 UTC
    const Y = offsetDate.getFullYear()
    const M = String(offsetDate.getMonth() + 1).padStart(2, '0')
    const D = String(offsetDate.getDate()).padStart(2, '0')
    const h = String(offsetDate.getHours()).padStart(2, '0')
    const m = String(offsetDate.getMinutes()).padStart(2, '0')
    const s = String(offsetDate.getSeconds()).padStart(2, '0')
    
    return `${Y}-${M}-${D} ${h}:${m}:${s}`
  } catch (e) {
    console.error("时间格式化错误:", e)
    return timeStr
  }
}
onMounted(fetchUserInfo)
</script>

<style scoped>
/* 使用你之前的 CSS 即可，确保 .loading 有样式 */
.loading { text-align: center; padding: 50px; font-size: 20px; color: #666; }
.profile-page { background: #f4f7f6; min-height: 100vh; padding: 30px; }
.container { display: flex; gap: 20px; max-width: 1000px; margin: auto; }
.profile-card { width: 300px; background: white; padding: 20px; border-radius: 10px; text-align: center; height: fit-content; }
.avatar-placeholder { width: 70px; height: 70px; background: #4caf50; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: auto; color: white; font-size: 30px; }
.main-content { flex: 1; }
.stats-grid { display: flex; gap: 20px; margin-bottom: 20px; }
.stat-card { flex: 1; background: white; padding: 20px; border-radius: 10px; }
.alert { border-left: 5px solid #ff4d4f; }
.value { font-size: 24px; font-weight: bold; margin-top: 10px; }
.settings-card { background: white; padding: 20px; border-radius: 10px; }
.setting-item { display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid #eee; }
.btn-logout { width: 100%; margin-top: 20px; padding: 10px; background: #ff4d4f; color: white; border: none; border-radius: 5px; cursor: pointer; }

.btn-logout { 
  width: 100%; 
  margin-top: 20px; 
  padding: 10px; 
  background: #1890ff; /* 蓝色更符合“返回”语义 */
  color: white; 
  border: none; 
  border-radius: 5px; 
  cursor: pointer; 
}

/* 1. 角色标签优化：牧场操作员 */
.badge {
  display: inline-block;
  margin-top: 8px;
  padding: 4px 12px;
  background-color: #e6f7ff; /* 浅蓝色背景 */
  color: #1890ff;            /* 深蓝色文字 */
  border: 1px solid #91d5ff;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

/* 2. 信息列表布局优化 */
.info-list {
  margin-top: 25px;
  text-align: left; /* 改为左对齐更易读 */
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

/* 3. “加入于/上次登录”等标签字体 */
.info-item label {
  color: #8c8c8c; /* 灰度文字，降低视觉优先级 */
  font-size: 14px;
}

/* 4. 具体的时间数值字体 */
.info-item span {
  color: #262626; /* 深黑色文字，强调内容 */
  font-weight: 500;
  font-family: 'Monaco', 'Courier New', monospace; /* 使用等宽字体让时间排版更整齐 */
}

/* 5. 鼠标悬停在卡片上的微小动效 */
.profile-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* 容器背景动画 */
.profile-page {
  min-height: 100vh;
  padding: 30px;
  /* 独立的背景：科技感的紫青渐变 */
  background: linear-gradient(-45deg, #232526, #414345, #1e3c72, #2a5298);
  background-size: 400% 400%;
  animation: profilePulse 8s ease infinite;
}

@keyframes profilePulse {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* 个人信息卡片：磨砂质感 */
.profile-card, .stat-card, .settings-card {
  background: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
}

/* 所有的文本颜色适配 */
h2, h3, p, label, span, .value {
  color: #ffffff !important;
}

/* 角色标签样式修正 */
.badge {
  background-color: rgba(24, 144, 255, 0.2) !important;
  color: #40a9ff !important;
  border: 1px solid rgba(64, 169, 255, 0.5);
}

/* 输入框和信息列表线条 */
.info-item { border-bottom: 1px solid rgba(255, 255, 255, 0.15); }
.info-item label { color: rgba(255, 255, 255, 0.6) !important; }

.profile-page {
  /* ... 原有代码 ... */
  min-height: 100vh;
  /* 同步增加顶部内边距 */
  padding-top: 100px !important; 
  box-sizing: border-box;
}

.container {
  /* 确保主体内容在垂直方向上有更好的比例 */
  align-items: flex-start; 
}

</style>