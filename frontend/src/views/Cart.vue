<template>
  <div class="container py-5 animate-fade-in">
    <div class="d-flex justify-content-between align-items-end mb-5">
      <div>
        <h1 class="display-5 fw-bold mb-0">Your Cart</h1>
        <p class="text-secondary mb-0">Manage your selected items and checkout</p>
      </div>
      <div v-if="Object.keys(cart).length" class="text-end">
        <div class="text-secondary small text-uppercase tracking-wider mb-1">Estimated Total</div>
        <div class="h2 fw-bold text-primary mb-0">&#8377;{{ total }}</div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger glass-card border-danger text-danger mb-4 d-flex justify-content-between align-items-center">
      <span><strong>Error!</strong> {{ error }}</span>
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>

    <div v-if="!Object.keys(cart).length" class="glass-card p-5 text-center my-5">
      <div class="display-1 text-secondary mb-4 opacity-25">
        <i class="bi bi-cart-x"></i>
      </div>
      <h2 class="fw-bold mb-3">Your cart is empty</h2>
      <p class="text-secondary mb-4">Looks like you haven't added anything to your cart yet.</p>
      <router-link :to="{ name: 'home' }" class="btn btn-premium btn-primary-premium px-5">
        Start Shopping
      </router-link>
    </div>

    <div v-else>
      <div v-for="(items, category) in cart" :key="category" class="category-group mb-5">
        <div class="d-flex align-items-center mb-4">
          <div class="h4 fw-bold mb-0 me-3 text-secondary text-uppercase tracking-wider">{{ category }}</div>
          <div class="flex-grow-1 border-bottom border-secondary opacity-25"></div>
        </div>

        <div class="row g-4">
          <div class="col-12" v-for="item in items" :key="item.id">
            <div class="glass-card p-4">
              <div class="row align-items-center">
                <div class="col-md-5">
                  <h4 class="h5 fw-bold mb-1">{{ item.name }}</h4>
                  <div class="text-secondary small">Price per unit: &#8377;{{ item.price }}</div>
                </div>
                
                <div class="col-md-3">
                  <div class="d-flex align-items-center justify-content-center bg-black bg-opacity-25 rounded-pill p-1" style="width: fit-content;">
                    <button class="btn btn-sm btn-link text-white text-decoration-none px-3" 
                            @click="updateCart(item.quantity - 1, item.id, item.product_id)">-</button>
                    <span class="px-3 fw-bold">{{ item.quantity }}</span>
                    <button class="btn btn-sm btn-link text-white text-decoration-none px-3" 
                            @click="updateCart(item.quantity + 1, item.id, item.product_id)">+</button>
                  </div>
                </div>

                <div class="col-md-2 text-center text-md-end">
                  <div class="text-secondary small text-uppercase tracking-wider smaller mb-1">Subtotal</div>
                  <div class="fw-bold h5 mb-0">&#8377;{{ Math.round(item.price * item.quantity * 100) / 100 }}</div>
                </div>

                <div class="col-md-2 text-end">
                  <button class="btn btn-sm btn-outline-danger border-0" @click="deleteCartItem(item.id)">
                    <i class="bi bi-trash me-1"></i> Remove
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="glass-card p-4 mt-5 d-flex flex-column flex-md-row justify-content-between align-items-center">
        <div class="mb-3 mb-md-0">
          <router-link :to="{ name: 'home' }" class="text-secondary text-decoration-none small fw-bold">
            <i class="bi bi-arrow-left me-1"></i> Continue Shopping
          </router-link>
        </div>
        <div class="d-flex align-items-center gap-4">
          <div class="text-end">
            <div class="text-secondary small text-uppercase tracking-wider mb-0">Final Total</div>
            <div class="h3 fw-bold text-primary mb-0">&#8377;{{ total }}</div>
          </div>
          <button class="btn btn-premium btn-primary-premium px-5 py-3" @click="checkout">
            Checkout Now
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Cart',

    data() {
      return {
        cart: [],
        total: 0,
        error: ''
      }
    },

    methods: {
      async getCart() {
        const response = await fetch('http://localhost:5000/api/cart', {
          method: 'GET',
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          },
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.cart = data
          this.cart = this.cart.cart_items.reduce((result, item) => {
            const { category, ...productDetails } = item;

            if (!result[category]) {
              result[category] = [];
            }
            result[category].push(productDetails);
            return result;
          }, {});

          this.updateQuantity()
          this.total = Object.values(this.cart).flat().reduce((total, item) => total + item.price * item.quantity, 0);
          this.total = Math.round(this.total * 100) / 100
        } else {
          console.log(data.message)
          this.error = data.message
        }
      },

      async updateCart(quantity, cart_item_id, product_id) {
        // Set quantity to 1 if it is less than 1
        if (quantity < 1) quantity = 1

        const response = await fetch(`http://localhost:5000/api/cart-item/${cart_item_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          },
          body: JSON.stringify({
            product_id,
            quantity
          })
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.cart = data
          await this.getCart()
        } else {
          console.log(data.message)
          this.error = data.message
        }
      },

      async deleteCartItem(cart_item_id) {
        const response = await fetch(`http://localhost:5000/api/cart-item/${cart_item_id}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          }
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.cart = data
          alert('Item removed from cart')
          await this.getCart()
        } else {
          console.log(data.message)
          this.error = data.message
        }
      },


      async checkout() {
        const response = await fetch('http://localhost:5000/api/order', {
          method: 'POST',
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          }
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.cart = data
          alert('Order placed successfully')
          this.$router.push({ name: 'orders' })
        } else {
          console.log(data.message)
          this.error = data.message
        }
      },



      async updateQuantity() {
        const response = await fetch('http://localhost:5000/quantity', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          },
          body: JSON.stringify(this.cart)
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.cart = data
          this.$router.push({ name: 'cart' })
        } else {
          console.log(data.message)
          this.error = data.message
        }

      }
    },




    async mounted () {
      await this.getCart()
    },

    // async created () {
    //   await this.updateQuantity()
    // }
  }
</script>