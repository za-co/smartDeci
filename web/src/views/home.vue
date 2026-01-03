<template>
  <div class="container">
    <h1>养殖场运行状态智能评估</h1>

    <div class="card">
      <p>温度：{{ data.temperature }} ℃</p>
      <p>湿度：{{ data.humidity }} %</p>
      <p>氨气：{{ data.ammonia }} ppm</p>
      <p>
        运行状态：
        <span :class="data.status">{{ data.status }}</span>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      data: {}
    }
  },
  mounted() {
    // axios.get("http://127.0.0.1:8000/api/status/")
    axios.get("http://47.95.11.134:8000/api/status/")
      .then(res => {
        this.data = res.data
      })
  }
} 
</script>

<style>
.container {
  width: 400px;
  margin: auto;
  font-family: Arial;
}
.card {
  border: 1px solid #ccc;
  padding: 20px;
}
.正常 {
  color: green;
}
.异常 {
  color: red;
}
</style>
