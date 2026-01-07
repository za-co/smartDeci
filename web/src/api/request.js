// web/src/api/request.js
import axios from 'axios';

const service = axios.create({
  baseURL: 'http://localhost:8000/api/', // 部署时改为你的云服务器IP
    // baseURL: '/api',
  timeout: 5000
});

// 你可以在这里添加拦截器，比如自动注入 Token
service.interceptors.request.use(config => {
  // const token = localStorage.getItem('token');
  // if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default service;