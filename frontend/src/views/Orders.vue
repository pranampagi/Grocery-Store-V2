<template>
  <div class="container py-5 animate-fade-in">
    <div class="mb-5">
      <h1 class="display-5 fw-bold mb-0">Order History</h1>
      <p class="text-secondary">Track and view your previous purchases</p>
    </div>

    <div v-if="!orders.length" class="glass-card p-5 text-center my-5">
      <div class="display-1 text-secondary mb-4 opacity-25">
        <i class="bi bi-bag-check"></i>
      </div>
      <h2 class="fw-bold mb-3">No orders found</h2>
      <p class="text-secondary mb-4">You haven't placed any orders yet. Start filling your cart!</p>
      <router-link :to="{ name: 'home' }" class="btn btn-premium btn-primary-premium px-5">
        Go Shopping
      </router-link>
    </div>

    <div v-else>
      <div v-for="order in orders" :key="order.id" class="glass-card p-4 mb-5">
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4 pb-3 border-bottom border-secondary border-opacity-25">
          <div>
            <span class="text-secondary small text-uppercase tracking-wider">Order ID:</span>
            <span class="fw-bold ms-2">#{{ order.id }}</span>
          </div>
          <div>
            <span class="text-secondary small text-uppercase tracking-wider">Placed On:</span>
            <span class="fw-bold ms-2 text-primary">{{ formatDate(order.date) }}</span>
          </div>
        </div>

        <div class="table-responsive">
          <table class="table table-borderless align-middle text-white">
            <thead class="text-secondary small text-uppercase tracking-wider border-bottom border-secondary border-opacity-10">
              <tr>
                <th class="ps-0">Product Details</th>
                <th class="text-center">Quantity</th>
                <th class="text-end">Unit Price</th>
                <th class="text-end pe-0">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in order.order_items" :key="item.id" class="border-bottom border-secondary border-opacity-10">
                <td class="ps-0 py-3">
                  <div class="fw-bold">{{ item.name }}</div>
                </td>
                <td class="text-center">{{ item.quantity }}</td>
                <td class="text-end">&#8377;{{ item.price }}</td>
                <td class="text-end pe-0 fw-bold">&#8377;{{ item.price * item.quantity }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="d-flex justify-content-end mt-3">
          <div class="text-end">
            <div class="text-secondary small text-uppercase tracking-wider mb-1">Order Total</div>
            <div class="h3 fw-bold text-primary mb-0">&#8377;{{ order.total_price }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
  export default {
    name: 'Orders',

    data() {
      return {
        token: localStorage.getItem('token'),
        role: localStorage.getItem('role'),
        orders: [],
        error: ''
      }
    },

    methods: {
      formatDate(dateStr) {
        if (!dateStr) return 'N/A';
        return new Date(dateStr).toLocaleString('en-IN', {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      },
      async getOrders() {
        const response = await fetch('http://localhost:5000/api/order', {
          method: 'GET',
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          },
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.orders = data

          this.orders.forEach(order => {
            const totalOrderPrice = order.order_items.reduce((total, item) => total + item.price * item.quantity, 0);
            order.total_price = totalOrderPrice;
          });
        } else {
          console.log(data.message)
          this.error = data.message
        }
      }
    },

    created() {
      this.getOrders()
    }
  }
</script>