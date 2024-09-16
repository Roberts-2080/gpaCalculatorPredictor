import axios from 'axios'

// 创建 axios 实例并配置基础 URL
const instance = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 5000  // 设置请求超时时间（可选）
})

export default instance