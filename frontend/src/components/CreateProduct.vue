<template>
  <div class="container py-5 animate-fade-in">
    <div class="glass-card p-5 mx-auto" style="max-width: 600px;">
      <div class="mb-4 pb-3 border-bottom border-secondary border-opacity-25 text-center">
        <h2 class="fw-bold text-white mb-0">Create Product</h2>
        <p class="text-secondary small mt-2">Add a new item to your inventory</p>
      </div>

      <div class="form-group mb-3">
        <label for="name" class="mb-2 text-secondary small text-uppercase fw-bold">Name</label>
        <input type="text" v-model="product.name" class="form-control form-control-premium" id="name" placeholder="e.g. Fresh Apples">
      </div>

      <div class="form-group mb-3">
        <label for="price" class="mb-2 text-secondary small text-uppercase fw-bold">Price (&#8377;)</label>
        <input type="number" v-model="product.price" class="form-control form-control-premium" id="price" placeholder="0.00" min="0" step="0.01">
      </div>

      <div class="form-group mb-3">
        <label for="category" class="mb-2 text-secondary small text-uppercase fw-bold">Category</label>
        <select v-model="product.category_id" class="form-control form-control-premium" id="category_id">
          <option :value="null" disabled>Select a category</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="quantity" class="mb-2 text-secondary small text-uppercase fw-bold">Quantity</label>
        <input type="number" v-model="product.quantity" class="form-control form-control-premium" id="quantity" placeholder="0" min="0">
      </div>

      <div class="form-group mb-4">
        <label for="manufacture_date" class="mb-2 text-secondary small text-uppercase fw-bold">Manufacture Date</label>
        <input type="date" v-model="product.manufacture_date" class="form-control form-control-premium" id="manufacture_date">
      </div>

      <div class="form-group mt-5">
        <button type="submit" class="btn btn-premium btn-primary-premium w-100 py-3" @click="createProduct">
          <i class="bi bi-plus-lg me-2"></i> Create Product
        </button>
      </div>

      <div v-if="error" class="alert alert-danger mt-4 small border-0 bg-danger bg-opacity-10 text-danger">
        <i class="bi bi-exclamation-triangle me-2"></i> {{ typeof error === 'object' ? Object.values(error)[0] : error }}
      </div>
    </div>
  </div>
</template>


<script>
import API_BASE from '@/api';
  export default {
    name: 'CreateProduct',

    data() {
      return {
        token: localStorage.getItem('token'),
        product: {
          name: '',
          price: null,
          category_id: null,
          quantity: null,
          manufacture_date: null
        },
        categories: [],
        error: ''
      }
    },

    methods: {
      async createProduct() {
        const response = await fetch(`${API_BASE}/api/products`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          },
          body: JSON.stringify(this.product)
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.$router.push({ name: 'showproducts' })
        } else {
          this.error = data.message
        }
      },

      async getCategories() {
        const response = await fetch(`${API_BASE}/api/categories`, {
          method: 'GET',
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          }
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.categories = data
        } else {
          this.error = data.message
        }
      }
    },

    mounted() {
      this.getCategories()
    }
  }
</script>