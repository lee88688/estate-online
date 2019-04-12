import axios from 'axios'

axios.interceptors.response.use(function (config) {
  return config
})
