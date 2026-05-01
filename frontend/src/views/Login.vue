<template>
  <div class="container d-flex align-items-center justify-content-center" style="min-height: 80vh;">
    <div class="glass-card p-5 animate-fade-in" style="width: 100%; max-width: 450px;">
      <div class="text-center mb-4">
        <h2 class="fw-bold">Welcome Back</h2>
        <p class="text-secondary">Please enter your details to sign in</p>
      </div>

      <div class="form-group mb-3">
        <label for="email" class="mb-2 text-secondary small text-uppercase fw-bold">Email address</label>
        <input type="email" 
               v-model="credentials.email" 
               class="form-control form-control-premium" 
               id="email" 
               placeholder="name@example.com">
      </div>

      <div class="form-group mb-4">
        <label for="password" class="mb-2 text-secondary small text-uppercase fw-bold">Password</label>
        <input type="password" 
               v-model="credentials.password" 
               class="form-control form-control-premium" 
               id="password" 
               placeholder="••••••••">
      </div>

      <button type="submit" 
              class="btn btn-premium btn-primary-premium w-100 mb-3 py-3" 
              @click="login">
        Sign In
      </button>

      <div v-if="error" class="alert bg-danger-subtle text-danger border-0 small text-center mb-3">
        {{ error }}
      </div>

      <div class="text-center mt-4">
        <span class="text-secondary">Don't have an account? </span>
        <router-link :to="{ name: 'register'}" class="text-primary text-decoration-none fw-bold">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import API_BASE from '@/api';
export default {
  name: 'Login',
  data() {
    return {
      credentials: {
        email: '',
        password: ''
      },
      error: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await fetch(`${API_BASE}/user-login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.credentials)
        })
        const data = await response.json()
        if (response.ok) {
          localStorage.setItem('token', data.token)
          localStorage.setItem('role', data.role)
          
          const target = data.role === 'Storemanager' ? 'showproducts' : 
                         data.role === 'Customer' ? 'home' : 'users';
          this.$router.push({ name: target })
        } else {
          this.error = data.message
        }
      } catch (err) {
        this.error = "Login failed. Please check your connection."
      }
    }
  }
}
</script>