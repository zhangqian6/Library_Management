import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5000/api', // Flask后端API地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 登录API
export const login = async (credentials) => {
  try {
    const response = await api.post('/login', credentials)
    return response
  } catch (error) {
    console.error('登录API错误:', error)
    return {
      success: false,
      message: error.response?.data?.message || '登录失败，请重试'
    }
  }
}

// 注册API
export const register = async (userData) => {
  try {
    const response = await api.post('/register', userData)
    return response
  } catch (error) {
    console.error('注册API错误:', error)
    return {
      success: false,
      message: error.response?.data?.message || '注册失败，请重试'
    }
  }
}

// 获取用户信息API
export const getUserInfo = async () => {
  try {
    const response = await api.get('/user')
    return response
  } catch (error) {
    console.error('获取用户信息错误:', error)
    return {
      success: false,
      message: error.response?.data?.message || '获取用户信息失败'
    }
  }
}

// 登出API
export const logout = async () => {
  try {
    const response = await api.post('/logout')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    return response
  } catch (error) {
    console.error('登出错误:', error)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    return {
      success: false,
      message: error.response?.data?.message || '登出失败'
    }
  }
}

export default api 