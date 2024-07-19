import {createApp} from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import VueSocketIO from 'vue-3-socket.io'
import io from 'socket.io-client';
import router from "./router";

const socketio = new VueSocketIO({
    debug: false,
    connection: io('ws://127.0.0.1:5000/ws'),
    //http:自己的服务：端口
    extraHeaders: {"Access-Control-Allow-Origin": '*'},
});


const app = createApp(App)

app.use(ElementPlus)
app.use(socketio)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router);
app.mount('#app')


