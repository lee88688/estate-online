<template>
  <div class="sidebar">
    <el-scrollbar :wrap-style="{'overflow-x': 'hidden'}">
      <el-menu :collapse="isCollapse"
               background-color="#304156"
               text-color="#bfcbd9"
               active-text-color="#409EFF"
               :router="true"
               mode="vertical"
               :collapse-transition="true"
               style="height: 100%;">
        <el-menu-item v-for="menu in menus" :index="menu.path" :key="menu.path">
          <i :class="menu.meta.icon"></i>
          <span slot="title">{{ menu.meta.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>

export default {
  name: 'Sidebar',
  data () {
    return {}
  },
  props: {
    isCollapse: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    menus () {
      const router = this.$router.options.routes
      let index = null
      for (let route of router) {
        if (route.name === 'index') {
          index = route
        }
      }
      return index.children
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar {
  height: 100%;
  background-color: #304156;
  border-right: solid 1px #e6e6e6;

  .el-scrollbar {
    /*height: 100%;*/
  }

  .el-menu {
    border-right: none;
  }
}
</style>
