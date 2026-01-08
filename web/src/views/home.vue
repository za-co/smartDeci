<template>
  <div class="home-container">
    <header class="dashboard-header">
      <div class="title-area">
        <h1>养殖场智能决策大屏</h1>
        <p class="subtitle">{{ currentTime }} 系统运行正常</p>
      </div>
      <div class="summary-cards">
        <div class="card glass score">
          <span class="label">全场健康评分</span>
          <span class="value">{{ farmReport.summary?.health_score }}</span>
        </div>
        <div class="card glass alert" :class="{ 'has-alerts': farmReport.summary?.alert_sensors > 0 }">
          <span class="label">异常预警设备</span>
          <span class="value">{{ farmReport.summary?.alert_sensors }}</span>
        </div>
        <div class="card glass total">
          <span class="label">在线设备总数</span>
          <span class="value">{{ farmReport.summary?.total_sensors }}</span>
        </div>
      </div>
    </header>

    <div class="main-layout">
      <section class="panel list-panel">
        <div class="panel-header">
          <h3>环境评估实时报告</h3>
          <div class="header-actions">
            <button class="btn-add" @click="showAddModal = true">+ 模拟录入</button>
            <span class="hint">点击行查看历史趋势</span>
          </div>
        </div>

        <div v-if="showAddModal" class="modal-overlay">
          <div class="modal-content glass">
            <h3>手动模拟数据录入</h3>
            <div class="form-group">
              <label>选择传感器:</label>
              <select v-model="formData.sensor_id">
                <option v-for="s in farmReport.detail" :key="s.id" :value="s.id">{{ s.name }} ({{ s.location }})</option>
              </select>
            </div>
            <div class="form-group">
              <label>监测数值:</label>
              <input type="number" v-model="formData.value" step="0.1" placeholder="请输入数值">
            </div>
            <div class="modal-btns">
              <button class="btn-cancel" @click="showAddModal = false">取消</button>
              <button class="btn-confirm" @click="submitData" :disabled="submitting">
                {{ submitting ? '提交中...' : '确认上传' }}
              </button>
            </div>
          </div>
        </div>
        
        <div class="table-wrapper">
          <table class="status-table">
            <thead>
              <tr>
                <th>位置</th>
                <th>数值</th>
                <th>状态</th>
                <th>建议</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in farmReport.detail" 
                  :key="item.id" 
                  @click="renderChart(item)"
                  :class="{ 'active-row': activeSensorId === item.id }">
                <td>
                  <div class="loc-name">{{ item.location }}</div>
                  <div class="sensor-name">{{ item.name }}</div>
                </td>
                <td class="num-text">
                  <span class="val">{{ item.recent_readings?.[item.recent_readings.length-1]?.value || '--' }}</span>
                  <span class="unit">{{ item.unit }}</span>
                </td>
                <td>
                  <span class="badge" :class="item.current_status?.level">
                    {{ item.current_status?.assessment }}
                  </span>
                </td>
                <td class="suggestion">{{ item.current_status?.suggestion }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="panel chart-panel">
        <div class="panel-header">
          <h3>{{ selectedSensorName }} - 趋势分析</h3>
        </div>
        <div id="chart" class="chart-container"></div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import service from '../api/request'; // 使用统一的请求工具
import * as echarts from 'echarts';

const farmReport = ref({ summary: {}, detail: [] });
const activeSensorId = ref(null);
const selectedSensorName = ref('请选择传感器');
const currentTime = ref(new Date().toLocaleString());
let myChart = null;

// 格式化当前时间
setInterval(() => {
  currentTime.value = new Date().toLocaleString();
}, 1000);

const fetchData = async () => {
  try {
    const res = await service.get('sensors/smart_farm_report/');
    farmReport.value = res.data;
    if (res.data.detail.length > 0) {
      renderChart(res.data.detail[0]); // 默认加载第一个
    }
  } catch (err) {
    console.error("加载数据失败", err);
  }
};

const renderChart = async (sensor) => {
  activeSensorId.value = sensor.id;
  selectedSensorName.value = sensor.name;
  
  try {
    const res = await service.get(`sensors/${sensor.id}/high_frequency_analysis/`);
    const chartData = res.data.info.recent_readings;

    const option = {
      grid: { top: '15%', left: '5%', right: '5%', bottom: '10%', containLabel: true },
      tooltip: { trigger: 'axis', backgroundColor: 'rgba(0,0,0,0.7)', textColor: '#fff' },
      xAxis: { 
        type: 'category', 
        data: chartData.map(d => new Date(d.timestamp).toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit'})),
        axisLine: { lineStyle: { color: '#ddd' } }
      },
      yAxis: { 
        type: 'value', 
        name: sensor.unit,
        splitLine: { lineStyle: { type: 'dashed' } }
      },
      series: [{
        name: sensor.name,
        data: chartData.map(d => d.value),
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(52, 152, 219, 0.5)' },
            { offset: 1, color: 'rgba(52, 152, 219, 0)' }
          ])
        },
        itemStyle: { color: '#3498db', borderWidth: 2 }
      }]
    };
    
    if (!myChart) myChart = echarts.init(document.getElementById('chart'));
    myChart.setOption(option);
  } catch (err) {
    console.error("图表数据加载失败", err);
  }
};

onMounted(fetchData);

// 响应式图表
window.addEventListener('resize', () => myChart?.resize());
onUnmounted(() => window.removeEventListener('resize', () => myChart?.resize()));

// --- 新增状态变量 ---
const showAddModal = ref(false);
const submitting = ref(false);
const formData = ref({
  sensor_id: null,
  value: null
});

// --- 新增提交方法 ---
const submitData = async () => {
  if (!formData.value.sensor_id || formData.value.value === null) {
    alert("请填写完整信息");
    return;
  }

  submitting.value = true;
  try {
    // 构造后端需要的 payload 结构
    const payload = {
      sensor_id: formData.value.sensor_id,
      readings: [
        {
          value: parseFloat(formData.value.value),
          timestamp: new Date().toISOString() // 自动生成当前时间戳
        }
      ]
    };

    // 调用后端 @action(detail=False, methods=['post']) 定义的 upload_batch_data
    await service.post('sensors/upload_batch_data/', payload);
    
    alert("数据上传成功！");
    showAddModal.value = false;
    formData.value.value = null; // 重置
    fetchData(); // 刷新大屏数据
  } catch (err) {
    console.error("提交失败", err);
    alert("提交失败：" + (err.response?.data?.error || "服务器错误"));
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.home-container { min-height: 100vh; background: #f0f2f5; padding: 25px; font-family: 'Segoe UI', sans-serif; }

/* Header 样式 */
.dashboard-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px; }
.title-area h1 { margin: 0; color: #2c3e50; font-size: 24px; }
.subtitle { color: #7f8c8d; margin-top: 5px; font-size: 14px; }

.summary-cards { display: flex; gap: 15px; }
.card { padding: 15px 30px; border-radius: 12px; display: flex; flex-direction: column; min-width: 120px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.score { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }
.alert { background: white; border: 2px solid #eee; }
.alert.has-alerts { border-color: #e74c3c; color: #e74c3c; }
.total { background: linear-gradient(135deg, #34495e, #2c3e50); color: white; }
.card .label { font-size: 12px; opacity: 0.9; }
.card .value { font-size: 28px; font-weight: bold; }

/* 布局 */
.main-layout { display: grid; grid-template-columns: 1fr 1.2fr; gap: 20px; height: calc(100vh - 180px); }
.panel { background: white; border-radius: 16px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }
.panel-header { padding: 15px 20px; border-bottom: 1px solid #f5f5f5; display: flex; justify-content: space-between; align-items: center; }
.panel-header h3 { margin: 0; font-size: 16px; color: #34495e; }
.hint { font-size: 12px; color: #bdc3c7; }

/* 表格 */
.table-wrapper { flex: 1; overflow-y: auto; }
.status-table { width: 100%; border-collapse: collapse; }
.status-table tr { cursor: pointer; transition: 0.2s; }
.status-table tr:hover { background: #f8faff; }
.status-table tr.active-row { background: #edf6ff; border-left: 4px solid #3498db; }
th { background: #fafafa; position: sticky; top: 0; padding: 12px 20px; font-size: 13px; color: #95a5a6; }
td { padding: 15px 20px; border-bottom: 1px solid #f9f9f9; }

.loc-name { font-weight: bold; color: #2c3e50; }
.sensor-name { font-size: 12px; color: #95a5a6; }
.num-text .val { font-size: 18px; font-weight: bold; color: #3498db; }
.num-text .unit { font-size: 12px; margin-left: 4px; }

/* 状态标签 */
.badge { padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; text-transform: uppercase; color: white; }
.red { background: #e74c3c; }
.orange { background: #f39c12; }
.green { background: #2ecc71; }
.blue { background: #3498db; }

/* 图表容器 */
.chart-container { flex: 1; padding: 20px; }

/* 按钮样式 */
.btn-add { background: #3498db; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; margin-right: 10px; }
.btn-add:hover { background: #2980b9; }

/* 弹窗遮罩 */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal-content { background: white; padding: 30px; border-radius: 16px; width: 400px; box-shadow: 0 20px 50px rgba(0,0,0,0.2); }
.form-group { margin-bottom: 20px; display: flex; flex-direction: column; }
.form-group label { font-size: 14px; margin-bottom: 8px; color: #7f8c8d; }
.form-group input, .form-group select { padding: 10px; border: 1px solid #ddd; border-radius: 8px; outline: none; }

.modal-btns { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-cancel { background: #eee; border: none; padding: 8px 20px; border-radius: 6px; cursor: pointer; }
.btn-confirm { background: #2ecc71; color: white; border: none; padding: 8px 20px; border-radius: 6px; cursor: pointer; }
.btn-confirm:disabled { background: #bdc3c7; }

/* 适配后的状态标签 */
.badge {
  display: inline-flex;    /* 使用 flex 布局让文字居中更稳 */
  align-items: center;
  justify-content: center;
  white-space: nowrap;     /* 强制文字在一行，绝不换行 */
  padding: 4px 12px;       /* 增加左右内边距，更美观 */
  border-radius: 20px;
  font-size: 11px;
  font-weight: bold;
  text-transform: uppercase;
  color: white;
  flex-shrink: 0;          /* 防止在挤压时变形 */
  min-width: fit-content;  /* 确保宽度适应文字内容 */
}

/* 容器背景动画 */
.home-container {
  min-height: 100vh;
  padding: 25px;
  font-family: 'Segoe UI', sans-serif;
  /* 独立的背景动画：深蓝到深绿的缓慢交替 */
  background: linear-gradient(125deg, #1a2a6c, #2a4858, #1d3321);
  background-size: 300% 300%;
  animation: homeMove 12s ease infinite;
  position: relative;
}

@keyframes homeMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* 关键：让所有面板变成半透明毛玻璃 */
.panel {
  background: rgba(255, 255, 255, 0.1) !important; /* 极低不透明度 */
  backdrop-filter: blur(15px); /* 毛玻璃模糊 */
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff; /* 确保暗背景下文字可读 */
}

/* 调整标题和表头颜色，适应暗色背景 */
.title-area h1, .panel-header h3 { color: #ffffff; }
.subtitle, .hint { color: rgba(255,255,255,0.7); }

/* 表格行样式适配 */
.status-table tr:hover { background: rgba(255, 255, 255, 0.1); }
.status-table tr.active-row { background: rgba(52, 152, 219, 0.2); border-left: 4px solid #3498db; }
th { background: rgba(0, 0, 0, 0.2); color: #fff; }
td { border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #fff; }
.loc-name { color: #fff; }

.home-container {
  /* ... 原有代码 ... */
  min-height: 100vh;
  /* 增加顶部内边距：导航栏高度约64px + 20px 呼吸间距 */
  padding-top: 84px !important; 
  box-sizing: border-box; /* 确保 padding 不会撑大容器 */
}

/* 如果你的 dashboard-header 也有 margin，可以适当微调 */
.dashboard-header {
  margin-top: 10px; 
}

</style>