import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Device from '@/components/Device'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Index',
            component: Index
        },
        {
            path: '/page/:page',
            name: 'IndexPaging',
            component: Index
        },
        {
            path: '/device/:devId',
            name: 'Device',
            component: Device
        }
    ]
})
