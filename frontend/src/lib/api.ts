import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL?.trim()

if (!baseURL) {
  console.warn('VITE_API_BASE_URL is not set. Falling back to relative API requests.')
}

export const api = axios.create({
  baseURL: baseURL || undefined,
})

export default api
