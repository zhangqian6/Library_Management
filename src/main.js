import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
// 注册所有图标为全局组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)){
    app.component(key, component)
}
app.mount('#app')
