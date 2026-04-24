<template>
  <div class="container py-5 animate-fade-in">
    <div class="glass-card p-5 mx-auto" style="max-width: 500px;">
      <div class="mb-4 pb-3 border-bottom border-secondary border-opacity-25 text-center">
        <h2 class="fw-bold text-white mb-0">Create Category</h2>
        <p class="text-secondary small mt-2">Organize your products by category</p>
      </div>

      <div class="form-group mb-3">
        <label for="name" class="mb-2 text-secondary small text-uppercase fw-bold">Category Name</label>
        <input type="text" v-model="category.name" class="form-control form-control-premium" id="name" placeholder="e.g. Beverages">
      </div>

      <div class="form-group mb-4">
        <label for="description" class="mb-2 text-secondary small text-uppercase fw-bold">Description</label>
        <textarea v-model="category.description" class="form-control form-control-premium" id="description" rows="3" placeholder="Enter category description..."></textarea>
      </div>

      <div class="form-group mt-5">
        <button type="submit" class="btn btn-premium btn-primary-premium w-100 py-3" @click="createCategory">
          <i class="bi bi-plus-lg me-2"></i> Create Category
        </button>
      </div>

      <div v-if="error" class="alert alert-danger mt-4 small border-0 bg-danger bg-opacity-10 text-danger">
        <i class="bi bi-exclamation-triangle me-2"></i> {{ error }}
      </div>
    </div>
  </div>
</template>



<script>
  export default {
    name: 'CreateCategory',

    data() {
      return {
        token: localStorage.getItem('token'),
        category: {
          name: '',
          description: ''
        },
        error: ''
      }
    },

    methods: {
      async createCategory() {
        const response = await fetch('http://localhost:5000/api/categories', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          },
          body: JSON.stringify(this.category)
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.$router.push({ name: 'showcategories' })
        } else {
          this.error = data.message
        }
      }
    }
  }
</script>