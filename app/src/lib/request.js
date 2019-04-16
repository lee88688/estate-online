import axios from 'axios'

export async function requestGet (url, data) {
  let res = await axios.get(url, {
    params: data
  })
  return res.data
}

export async function requestPost(url, data) {
  let res = await axios.post(url, data)
  return res.data
}

export function isSuccess (res) {
  if (!res.success) {
    return false
  }
  return true
}
