import {createRouter, createWebHistory} from 'vue-router';
import LoginPage from "@/views/LoginPage.vue";
import KVMPage from "@/views/KVMPage.vue";
import { ElMessage } from 'element-plus';

const routes = [
    {
        path: '/',
        name: 'index',
        component: LoginPage
    },
    {
        path: '/kvm',
        name: 'kvm',
        component: KVMPage,
        meta: {requiresAuth: true}
    }
]

const router = createRouter({
    routes: routes,
    history: createWebHistory()
})

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const userLogin = localStorage.getItem('userLogin');
    console.log(to)
    console.log(requiresAuth, userLogin)
    if (requiresAuth && !userLogin) {
        ElMessage.error("请先登录！")
        next('/');
    } else {
        next();
    }
});

export default router