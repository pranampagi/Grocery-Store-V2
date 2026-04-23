import { createApp, watch } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css' 



createApp(App).use(router).mount('#app')

// router.beforeEach((to, from, next) => {
//   if (to.name !== 'Login' && !localStorage.getItem('auth-token') ? true : false)
//     next({ name: 'Login' })
//   else next()
// })