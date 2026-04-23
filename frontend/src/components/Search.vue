<template>
  <div class="container py-5 animate-fade-in">
    <div class="row justify-content-center mb-5">
      <div class="col-md-8 text-center">
        <h1 class="display-5 fw-bold mb-4">Find Products</h1>
        <div class="glass-card p-2 d-flex">
          <input type="text" class="form-control form-control-premium border-0 bg-transparent py-3 ps-4" 
                 placeholder="Search by name, category, price or date..." v-model="query" @keyup.enter="searchProduct">
          <button class="btn btn-premium btn-primary-premium px-4" type="button" @click="searchProduct">
            <i class="bi bi-search me-2"></i> Search
          </button>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger glass-card border-danger text-danger mb-4">
      {{ error }}
    </div>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4" v-if="products.length > 0">
      <div class="col" v-for="product in products" :key="product.id">
        <div class="glass-card h-100 p-3 d-flex flex-column">
          <div class="product-info mb-3">
            <div class="text-secondary small text-uppercase tracking-wider smaller mb-1">{{ product.category.name }}</div>
            <h4 class="h5 fw-bold mb-2">{{ product.name }}</h4>
            <div class="text-primary fw-bold h4 mb-2">&#8377;{{ product.price }}</div>
            <div class="text-secondary small">Stock: {{ product.quantity || 0 }}</div>
          </div>

          <div class="mt-auto pt-3 border-top border-secondary border-opacity-25">
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
              <span class="badge bg-danger p-2 w-100 opacity-75">Out of Stock</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="result" class="glass-card p-5 text-center mt-4">
      <h3 class="text-secondary opacity-50">No products match your search.</h3>
    </div>
  </div>
</template>


<script>
  export default {
    name: 'Search',

    data() {
      return {
        query: '',
        result: false,
        products: [],
        cart: []
      }
    },

    methods: {
      async searchProduct() {
        const response = await fetch(`http://localhost:5000/api/search/${this.query}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          }
        })
          .catch(error => console.log(error));
        const data = await response.json();
        if (response.ok) {
          this.products = data;
          this.result = true;
        }
        else {
          this.error = data.message;
        }
      },

      async addToCart(quantity, product_id, product_name) {
        if (!localStorage.getItem('token')) {
          alert("Please login to add items to your cart!");
          this.$router.push({ name: 'login' });
          return;
        }
        const response = await fetch('http://localhost:5000/api/cart-item', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          },
          body: JSON.stringify({
            quantity,
            product_id
          })
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.cart = data
          if (quantity === 1) alert(`Added ${quantity} item of product ${product_name} to cart`)
          else alert(`Added ${quantity} items of product ${product_name} to cart`)
        } else {
          console.log(data.message)
          this.error = data.message
        }
      }
    }
  }
</script>