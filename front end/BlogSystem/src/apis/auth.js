import request from '@/utils/request'

export const login = ({ username, password }) =>
  request.post('/login/', { username, password })

export const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  location.href = '/login'
}