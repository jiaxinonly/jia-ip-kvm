import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from "@/views/LoginPage.vue";
import KVMPage from "@/views/KVMPage.vue";

const routes = [
    {
        path: '/',
        name: 'index',
        component: LoginPage
    },
    {
        path: '/kvm',
        name: 'kvm',
        component: KVMPage
    }
]

const router = createRouter({
    routes: routes,
    history: createWebHistory()
})

export default router