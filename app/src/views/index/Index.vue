<template>
  <el-container style="height: 100%;">
    <el-aside :width="isCollapse ? '64px' : '200px'">
      <sidebar :is-collapse="isCollapse"></sidebar>
    </el-aside>
    <el-container>
      <el-header height="50px" style="padding: 0;">
        <navbar :is-collapse.sync="isCollapse"></navbar>
        <div class="content-wrap">
        </div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import Navbar from '@/components/layout/Navbar'
import Sidebar from '@/components/layout/Sidebar'

export default {
  name: 'Index',
  data () {
    return {
      isCollapse: false
    }
  },
  components: { Sidebar, Navbar }
}
</script>

<style scoped>
.content-wrap {
  height: 100%;
  width: 100%;
  padding: 20px;
}
</style>
