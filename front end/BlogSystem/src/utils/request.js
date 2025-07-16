import axios from 'axios'
import { ElMessage } from 'element-plus'

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE}`,
  timeout: 10000
})

// 请求拦截：注入 token
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  err => Promise.reject(err)
)

// 响应拦截：统一 401 处理
instance.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response && err.response.status === 401) {
      console.log(err.response)
      console.log(localStorage.getItem('access_token'))
      // 可以尝试 refresh token 或者直接跳转
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      location.href = '/login'
    } else {
      ElMessage.error(err.response?.data?.detail || '网络错误')
    }
    return Promise.reject(err)
  }
)

export default instance