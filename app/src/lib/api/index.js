import {isSuccess, requestGet, requestPost} from '../request'

export async function apiQuery (params) {
  return requestPost('/api/query', params)
}

export async function apiRegion () {
  let res = await requestGet('/api/region')
  if (isSuccess(res)) {
    return res.result
  }
  return []
}
