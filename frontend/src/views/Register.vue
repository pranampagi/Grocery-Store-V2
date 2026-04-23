<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="glass-card p-5 animate-fade-in">
          <div class="text-center mb-5">
            <h2 class="display-6 fw-bold">Create Account</h2>
            <p class="text-secondary">Join our fresh grocery community</p>
          </div>

          <div class="form-group mb-4">
            <label for="name" class="form-label small fw-bold text-secondary text-uppercase tracking-wider">Full Name</label>
            <input type="text" v-model="credentials.name" class="form-control form-control-premium" id="name" placeholder="John Doe">
          </div>

          <div class="form-group mb-4">
            <label for="username" class="form-label small fw-bold text-secondary text-uppercase tracking-wider">Username</label>
            <input type="text" v-model="credentials.username" class="form-control form-control-premium" id="username" placeholder="johndoe123">
          </div>

          <div class="form-group mb-4">
            <label for="email" class="form-label small fw-bold text-secondary text-uppercase tracking-wider">Email address</label>
            <input type="email" v-model="credentials.email" class="form-control form-control-premium" id="email" placeholder="name@example.com">
          </div>

          <div class="form-group mb-4">
            <label for="password" class="form-label small fw-bold text-secondary text-uppercase tracking-wider">Password</label>
            <input type="password" v-model="credentials.password" class="form-control form-control-premium" id="password" placeholder="••••••••">
          </div>

          <div class="form-group mb-5">
            <label for="confirm_password" class="form-label small fw-bold text-secondary text-uppercase tracking-wider">Confirm Password</label>
            <input type="password" v-model="credentials.confirm_password" class="form-control form-control-premium" id="confirm_password" placeholder="••••••••">
          </div>

          <button type="submit" class="btn btn-premium btn-primary-premium w-100 py-3 mb-4" @click="register">
            Register Account
          </button>

          <div class="text-center">
            <span class="text-secondary small">Already have an account? </span>
            <router-link :to="{ name: 'login'}" class="text-primary small fw-bold text-decoration-none">Login Here</router-link>
          </div>

          <div class="alert alert-danger glass-card border-danger text-danger mt-4" v-if="error">
            {{ error }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
  export default {
    name: 'Register',

    data() {
      return {
        credentials: {
          name: '',
          username: '',
          email: '',
          password: '',
          confirm_password: ''
        },
        error: ''
      }
    },

    methods: {
      async register() {
        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.credentials)
        })
        const data = await response.json()
        if (response.ok) {
          this.$router.push({ name: 'login' })
        } else {
          this.error = data.message
        }
      }
    }
  }
</script>