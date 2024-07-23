import {createApp} from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import VueSocketIO from 'vue-3-socket.io'
import io from 'socket.io-client';
import router from "./router";
import vueAxios from 'vue-axios'
import axios from 'axios';

const socketio = new VueSocketIO({
    debug: false,
    connection: io('/ws/', {autoConnect: false})
});


const app = createApp(App)

app.use(ElementPlus)
app.use(socketio)
app.use(vueAxios, axios)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router);
app.mount('#app')


