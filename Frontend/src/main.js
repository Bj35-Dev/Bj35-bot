import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import LoadingSpinner from './components/common/LoadingSpinner.vue'
import i18n from './i18n'

const app = createApp(App)

app.component('LoadingSpinner', LoadingSpinner)

app.use(router)
app.use(i18n)

app.mount('#app')
