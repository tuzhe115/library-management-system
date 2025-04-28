import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { ArrowLeft } from '@element-plus/icons-vue'
import { Search } from '@element-plus/icons-vue'


const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.component('ArrowLeft', ArrowLeft)
app.component('Search', Search)
app.mount('#app')
