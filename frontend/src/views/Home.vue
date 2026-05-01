<template>
  <div class="home-container animate-fade-in">
    <div class="row mb-5 text-center">
      <div class="col">
        <h1 class="display-4 fw-bold">Fresh Groceries</h1>
        <p class="text-secondary lead">Premium quality products delivered to your doorstep</p>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger glass-card border-danger text-danger mb-4">
      <strong>Oops!</strong> {{ error }}
    </div>

    <div v-for="category in categories" :key="category.id" class="category-section mb-5">
      <div v-if="category.active">
        <div class="d-flex align-items-center mb-4">
          <h2 class="h3 mb-0 me-3">{{ category.name }}</h2>
          <span class="category-badge">{{ category.products.length }} Products</span>
        </div>

        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4" v-if="category.products.length > 0">
          <div class="col" v-for="product in category.products" :key="product.id">
            <div class="glass-card h-100 p-3 d-flex flex-column">
              <div class="product-info mb-3">
                <h4 class="h5 fw-bold mb-1">{{ product.name }}</h4>
                <div class="text-primary fw-bold h4 mb-2">&#8377;{{ product.price }}</div>
                <div class="text-secondary small mb-1">Stock: {{ product.quantity || 0 }}</div>
                <div class="text-secondary smaller">Manufactured: {{ formatDate(product.manufacture_date) }}</div>
              </div>

              <div class="mt-auto pt-3 border-top border-secondary">
                <div v-if="product.quantity > 0" class="d-flex gap-2 align-items-center">
                  <input type="number" 
                         class="form-control form-control-premium w-50" 
                         v-model.number="cart[product.id]" 
                         min="1" 
                         :max="product.quantity">
                  <button class="btn btn-premium btn-primary-premium btn-sm w-50" 
                          @click="addToCart(cart[product.id] || 1, product.id, product.name)">
                    Add
                  </button>
                </div>
                <div v-else class="text-center">
                  <span class="badge bg-danger p-2 w-100">Out of Stock</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="glass-card p-4 text-center text-secondary">
          No products available in this category.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import API_BASE from '@/api';
export default {
  name: 'Home',
  data() {
    return {
      categories: [],
      cart: {}, 
      error: ''
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      return new Date(dateStr).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      });
    },
    async getCategories() {
      try {
        const response = await fetch(`${API_BASE}/api/categories`, {
          headers: { 'Authentication-Token': localStorage.getItem('token') }
        })
        const data = await response.json()
        if (response.ok) {
          this.categories = data
        } else {
          this.error = data.message
        }
      } catch (err) {
        this.error = "Connection failed"
      }
    },
    async addToCart(quantity, product_id, product_name) {
      if (!localStorage.getItem('token')) {
        alert("Please login to add items to your cart!");
        this.$router.push({ name: 'login' });
        return;
      }
      try {
        const response = await fetch(`${API_BASE}/api/cart-item`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          },
          body: JSON.stringify({ quantity, product_id })
        })
        const data = await response.json()
        if (response.ok) {
          // Toast or subtle notification instead of alert would be better
          alert(`Success! Added ${quantity} ${product_name} to cart.`)
        } else {
          this.error = data.message
        }
      } catch (err) {
        this.error = "Failed to add to cart"
      }
    }
  },
  mounted() {
    this.getCategories()
  }
}
</script>

<style scoped>
.smaller { font-size: 0.75rem; }
.product-info { flex-grow: 1; }
</style>