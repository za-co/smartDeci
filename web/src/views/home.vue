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
          <span class="hint">点击行查看历史趋势</span>
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
</style>