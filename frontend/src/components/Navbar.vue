<template>
  <nav class="navbar navbar-expand-md navbar-dark nav-glass mb-4 sticky-top">
    <div class="container-fluid px-lg-5">
      <router-link class="navbar-brand navbar-brand-premium mr-4" :to="{ name: 'home'}" v-if="role === 'Customer' || !is_login">Grocery Store</router-link>
      <router-link class="navbar-brand navbar-brand-premium mr-4" :to="{ name: 'showcategories'}" v-else>Grocery Store</router-link>
      
      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarScroll">
        <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll">
          <li class="nav-item">
            <router-link class="nav-link px-3" aria-current="page" :to="{ name: 'home' }" v-if="role === 'Customer' || !is_login">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link px-3" :to="{ name: 'search'}" v-if="role === 'Customer' || !is_login">Search</router-link>
          </li>
          <li class="nav-item" v-if="role === 'Admin'">
            <router-link class="nav-link px-3" :to="{ name: 'users'}">Users</router-link>
          </li>
          <li class="nav-item" v-if="role === 'Admin' || role === 'Storemanager'">
            <router-link class="nav-link px-3" :to="{ name: 'showcategories'}">Categories</router-link>
          </li>
          <li class="nav-item" v-if="role === 'Admin' || role === 'Storemanager'">
            <router-link class="nav-link px-3" :to="{ name: 'showproducts'}">Products</router-link>
          </li>
        </ul>

        <div class="d-flex align-items-center">
          <ul class="navbar-nav">
            <li class="nav-item" v-if="role === 'Admin' || role === 'Storemanager'">
              <router-link class="nav-link px-3" :to="{ name: 'createcategory'}">Add Category</router-link>
            </li>
            <li class="nav-item" v-if="role === 'Storemanager'">
              <router-link class="nav-link px-3" :to="{ name: 'createproduct'}">Add Product</router-link>
            </li>
            <li class="nav-item" v-if="role === 'Customer'">
              <router-link class="nav-link px-3 position-relative" :to="{ name: 'cart'}">
                Cart
                <span v-if="cartCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                  {{ cartCount }}
                </span>
              </router-link>
            </li>
            <li class="nav-item" v-if="role === 'Customer'">
              <router-link class="nav-link px-3" :to="{ name: 'orders'}">Orders</router-link>
            </li>
            <li class="nav-item ms-lg-3" v-if="!is_login">
              <router-link class="btn btn-premium btn-primary-premium btn-sm" :to="{ name: 'login'}">Login</router-link>
            </li>
            <li class="nav-item" v-if="is_login">
              <button class="btn btn-link nav-link px-3 text-danger border-0" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import API_BASE from '@/api';
export default {
  name: 'Navbar',
  data() {
    return {
      token: localStorage.getItem('token'),
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('token'),
      cartCount: 0,
      error: ''
    }
  },
  methods: {
    async logout() {
      try {
        const response = await fetch(`${API_BASE}/user-logout`, {
          method: 'GET',
          headers: {
            'Authentication-Token': this.token
          }
        })
        if (response.ok) {
          localStorage.removeItem('token')
          localStorage.removeItem('role')
          this.$router.push({ name: 'login' })
        }
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
  }
}
</script>

<style scoped>
.nav-link {
  transition: var(--transition);
  font-weight: 500;
  color: var(--text-secondary) !important;
}
.nav-link:hover, .router-link-active {
  color: var(--text-primary) !important;
  transform: translateY(-1px);
}
.nav-link.router-link-active {
  color: var(--primary) !important;
}
</style>