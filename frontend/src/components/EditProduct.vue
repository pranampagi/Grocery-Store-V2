<template>
  <div class="container py-5 animate-fade-in">
    <div class="glass-card p-5 mx-auto" style="max-width: 600px;">
      <div class="mb-4 pb-3 border-bottom border-secondary border-opacity-25 text-center">
        <h2 class="fw-bold text-white mb-0">Edit Product</h2>
        <p class="text-secondary small mt-2">Modify product details and stock</p>
      </div>

      <div class="form-group mb-3">
        <label for="name" class="mb-2 text-secondary small text-uppercase fw-bold">Name</label>
        <input type="text" v-model="product.name" class="form-control form-control-premium" id="name" placeholder="Enter name">
      </div>

      <div class="form-group mb-3">
        <label for="price" class="mb-2 text-secondary small text-uppercase fw-bold">Price (&#8377;)</label>
        <input type="number" v-model="product.price" class="form-control form-control-premium" id="price" placeholder="Enter price">
      </div>

      <div class="form-group mb-3">
        <label for="category" class="mb-2 text-secondary small text-uppercase fw-bold">Category</label>
        <select v-model="product.category_id" class="form-control form-control-premium" id="category_id">
          <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="quantity" class="mb-2 text-secondary small text-uppercase fw-bold">Quantity</label>
        <input type="number" v-model="product.quantity" class="form-control form-control-premium" id="quantity" placeholder="Enter quantity">
      </div>

      <div class="form-group mb-4">
        <label for="manufacture_date" class="mb-2 text-secondary small text-uppercase fw-bold">Manufacture Date</label>
        <input type="date" v-model="product.manufacture_date" class="form-control form-control-premium" id="manufacture_date">
      </div>

      <div class="form-group mt-5">
        <button type="submit" class="btn btn-premium btn-primary-premium w-100 py-3" @click="editProduct">
          <i class="bi bi-save me-2"></i> Update Product
        </button>
      </div>

      <div v-if="error" class="alert alert-danger mt-4 small border-0 bg-danger bg-opacity-10 text-danger">
        <i class="bi bi-exclamation-triangle me-2"></i> {{ typeof error === 'object' ? Object.values(error)[0] : error }}
      </div>
    </div>
  </div>
</template>


<script>
  export default {
    name: 'EditProduct',

    props: {
      id: {
        type: [Number, String],
        required: true}
    },

    data() {
      return {
        product: {
          id: null,
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
      async editProduct() {
        const response = await fetch(`http://localhost:5000/api/product/${this.product.id}`, {
          method: 'PUT',
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
        const response = await fetch('http://localhost:5000/api/categories', {
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

    beforeRouteEnter(to, from, next) {
      fetch(`http://localhost:5000/api/product/${to.params.id}`, {
        method: "GET",
        headers: {
          'Authentication-Token': localStorage.getItem('token')
        }
      })
      .then(response => response.json())
      .then(data => {
        next(vm => {
          vm.product = data
        })
      })
      .catch(error => console.log(error))
    },

    beforeRouteUpdate(to, from, next) {
      fetch(`http://localhost:5000/api/product/${to.params.id}`, {
        method: "GET",
        headers: {
          'Authentication-Token': localStorage.getItem('token')
        }
      })
      .then(response => response.json())
      .then(data => {
        this.product = data
        next()
      })
    },

    mounted() {
      this.getCategories()
    }

  }
</script>