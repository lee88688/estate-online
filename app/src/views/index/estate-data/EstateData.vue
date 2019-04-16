<template>
  <el-card>
    <el-form :inline="true">
      <el-form-item label="区县：">
        <el-select v-model="form.region" clearable>
          <el-option v-for="r in region" :value="r.code" :label="r.name" :key="r.code"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="面积范围：">
        <el-input></el-input>
      </el-form-item>
      <el-form-item label="项目名称：">
        <el-input v-model="form.project_name" clearable></el-input>
      </el-form-item>
      <el-form-item label="开发企业：">
        <el-input v-model="form.enterprise_name" clearable></el-input>
      </el-form-item>
      <el-form-item label="项目地址：">
        <el-input v-model="form.location" clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="refresh">查询</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="tableData" border stripe>
      <el-table-column label="楼盘名称" prop="project_name"></el-table-column>
      <el-table-column label="开发商" prop="enterprise_name"></el-table-column>
      <el-table-column label="楼盘地址" prop="location"></el-table-column>
    </el-table>
    <el-pagination :page-size="pagination.pageSize"
                   :current-page.sync="pagination.pageIndex"
                   :total="pagination.total"
                   @current-change="refresh"
                   layout="prev, pager, next, jumper" class="pagination"></el-pagination>
  </el-card>
</template>

<script>
import { apiRegion, apiQuery } from '@/lib/api'
import { isSuccess } from '@/lib/request'
import { cloneObject } from '@/lib/utils'

export default {
  name: 'EstateData',
  data () {
    return {
      region: [],
      form: {
        region: '',
        project_name: '',
        enterprise_name: '',
        location: ''
      },
      tableData: null,
      pagination: {
        pageSize: 10,
        pageIndex: 1,
        total: 0
      }
    }
  },
  methods: {
    async refresh () {
      let params = cloneObject(this.form)
      params['page_size'] = this.pagination.pageSize
      params['page_index'] = this.pagination.pageIndex
      let res = await apiQuery(params)
      if (!isSuccess(res)) {
        this.$message.error('请求失败请稍后再试！')
      }
      this.tableData = res.result.data
      this.pagination.total = res.result['total_size']
    }
  },
  async created () {
    this.region = await apiRegion()
    this.refresh()
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
}
</style>
