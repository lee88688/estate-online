<template>
  <el-card>
    <el-form :inline="true">
      <el-form-item label="区县：">
        <el-select></el-select>
      </el-form-item>
      <el-form-item label="面积范围：">
        <el-input></el-input>
      </el-form-item>
      <el-form-item label="项目名称：">
        <el-input></el-input>
      </el-form-item>
      <el-form-item label="开发企业：">
        <el-input></el-input>
      </el-form-item>
      <el-form-item label="项目地址：">
        <el-input></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary">查询</el-button>
      </el-form-item>
    </el-form>
    <el-pagination :page-size="10" layout="prev, pager, next, jumper" class="pagination"></el-pagination>
  </el-card>
</template>

<script>
export default {
  name: 'EstateData'
}
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
}
</style>
