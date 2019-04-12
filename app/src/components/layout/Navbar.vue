<template>
  <div class="navbar">
    <div class="left">
      <hamburger :is-active="isCollapse" @toggle="$emit('update:is-collapse', $event)"></hamburger>
      <span>{{ title }}</span>
    </div>
    <div class="right">
    </div>
  </div>
</template>

<script>
import Hamburger from '@/components/Hamburger'

export default {
  name: 'Navbar',
  props: {
    isCollapse: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    title () {
      return this.$route.meta.title
    }
  },
  components: { Hamburger }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);

  .left {
    display: flex;
    justify-content: flex-start;
    align-items: center;
  }
}
</style>
