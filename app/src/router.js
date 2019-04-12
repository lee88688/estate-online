import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/index/Index'
import EstateData from '@/views/index/estate-data/EstateData'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
      component: Index,
      children: [
        {
          path: '/estate-data',
          component: EstateData,
          meta: {
            icon: 'el-icon-tickets',
            title: '数据查询'
          }
        }
      ]
    }
  ]
})
