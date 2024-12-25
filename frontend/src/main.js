import './assets/css/main.css'
import './assets/css/tailwindcss.css'

import router from './router'

import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:5000'
axios.defaults.withCredentials = true;

import { createApp } from 'vue'
import App from './App.vue'
import Product from './components/Product.vue'
import IconHome from './icons/IconHome.vue'
import IconChart from './icons/IconChart.vue'
import IconSearch from './icons/IconSearch.vue'
import IconCookie from './icons/IconCookie.vue'
import IconLogout from './icons/IconLogout.vue'
import IconUnregister from './icons/IconUnregister.vue'

const app = createApp(App)
app.component('Product', Product)
app.component('IconHome', IconHome)
app.component('IconChart', IconChart)
app.component('IconSearch', IconSearch)
app.component('IconCookie', IconCookie)
app.component('IconLogout', IconLogout)
app.component('IconUnregister', IconUnregister)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(router)
app.use(ElementPlus)
app.mount('#app')