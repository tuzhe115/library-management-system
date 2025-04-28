import axios from 'axios'

const instance = axios.create()

// Add token to every request automatically
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default instance
