import axios from 'axios';
import { ElMessage } from 'element-plus';

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE}`,
  timeout: 10000
});

// 请求拦截：注入 token
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  err => {
    ElMessage.error('请求发送失败，请检查网络连接');
    return Promise.reject(err);
  }
);

// 响应拦截：统一错误处理
instance.interceptors.response.use(
  res => res.data,
  err => {
    // 统一处理 HTTP 状态码
    if (err.response) {
      const status = err.response.status;
      const message = err.response.data?.detail || err.response.statusText;

      switch (status) {
        case 401:
          // 清除 token 并重定向到登录页
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          location.href = '/login';
          break;
        case 403:
          ElMessage.error('权限不足，请联系管理员');
          break;
        case 404:
          ElMessage.error(`资源未找到: ${err.response.config.url}`);
          break;
        case 500:
          ElMessage.error('服务器内部错误，请稍后再试');
          break;
        default:
          ElMessage.error(`${status}: ${message}`);
      }
    } else if (err.request) {
      // 请求发送失败（如网络问题）
      ElMessage.error('请求发送失败，请检查网络连接');
    } else {
      // 配置错误
      ElMessage.error(`请求配置错误: ${err.message}`);
    }

    return Promise.reject(err);
  }
);

export default instance;