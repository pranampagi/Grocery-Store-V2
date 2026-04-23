import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Cart from '@/views/Cart.vue'
import Users from '@/views/Users.vue'


import Register from '@/views/Register.vue'
import Login from '@/views/Login.vue'
import RegisterStoreManager from '@/views/RegisterStoreManager.vue'
import Search from '@/components/Search.vue'

import CreateCategory from '@/components/CreateCategory.vue'
import EditCategory from '@/components/EditCategory.vue'
import ShowCategories from '@/views/ShowCategories.vue'

import CreateProduct from '@/components/CreateProduct.vue'
import EditProduct from '@/components/EditProduct.vue'
import ShowProducts from '@/views/ShowProducts.vue'

import Orders from '@/views/Orders.vue'



const routes = [
  { path: '/', name: 'home', component: Home },

  { path: '/register', name: 'register', component: Register },
  { path: '/login', name: 'login', component: Login },
  { path: '/registerstoremanager', name: 'registerstoremanager', component: RegisterStoreManager },

  { path: '/createcategory', name: 'createcategory', component: CreateCategory },
  { path: '/editcategory/:id',  name: 'editcategory', component: EditCategory, props: true },
  { path: '/showcategories', name: 'showcategories', component: ShowCategories },

  { path: '/createproduct', name: 'createproduct', component: CreateProduct },
  { path: '/editproduct/:id',  name: 'editproduct', component: EditProduct, props: true },
  { path: '/showproducts', name: 'showproducts', component: ShowProducts },

  { path: '/orders', name: 'orders', component: Orders },
  { path: '/cart', name: 'cart', component: Cart  },
  { path: '/search', name: 'search', component: Search },
  { path: '/users', name: 'users', component: Users }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
