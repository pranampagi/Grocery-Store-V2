<template>
   <div class="container">
    <div class="content-section" style="width: 50%; margin-left: 25%;">
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Join As a Manager</legend>
        <div class="form-group mb-3">
          <label for="name" class="mb-2">Name</label>
          <input type="text" v-model="credentials.name" class="form-control" id="name" placeholder="Enter name">
        </div>
        <div class="form-group mb-3">
          <label for="username" class="mb-2">Username</label>
          <input type="text" v-model="credentials.username" class="form-control" id="username" placeholder="Enter username">
        </div>
        <div class="form-group mb-3">
          <label for="email" class="mb-2">Email address</label>
          <input type="email" v-model="credentials.email" class="form-control" id="email" placeholder="Enter email">
        </div>
        <div class="form-group mb-3">
          <label for="password" class="mb-2">Password</label>
          <input type="password" v-model="credentials.password" class="form-control" id="password" placeholder="Password">
        </div>
        <div class="form-group mb-3">
          <label for="confirm_password" class="mb-2">Confirm Password</label>
          <input type="password" v-model="credentials.confirm_password" class="form-control" id="confirm_password" placeholder="Confirm Password">
        </div>
        <div class="form-group mb-3">
          <button type="submit" class="btn btn-outline-primary" @click="register">Register</button>
        </div> 
        <div class="alert alert-danger" v-if="error">
          {{ error }}
        </div>
      </fieldset>
    </div>
  </div>
</template>


<script>
  export default {
    name: 'RegisterStoreManager',

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
        const response = await fetch('http://localhost:5000/manager-register', {
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