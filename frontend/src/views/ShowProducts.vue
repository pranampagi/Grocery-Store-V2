<template>
  <div class="container py-5 animate-fade-in">
    <div class="mb-5">
      <h1 class="display-5 fw-bold mb-0">{{ role === 'Admin' ? 'Admin Dashboard' : 'Manager Dashboard' }}</h1>
      <p class="text-secondary">Manage your inventory and stock levels</p>
    </div>

    <div class="glass-card p-4">
      <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-secondary border-opacity-25">
        <h2 class="h4 fw-bold mb-0 text-uppercase tracking-wider">Product Inventory</h2>
        <div class="d-flex gap-2 align-items-center">
          <div v-if="isWaiting" class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
          <button class="btn btn-premium btn-secondary-premium btn-sm" @click="downloadProducts" v-if="products.length && role === 'Storemanager'">
            <i class="bi bi-download me-1"></i> Export CSV
          </button>
          <router-link :to="{ name: 'createproduct' }" class="btn btn-premium btn-primary-premium btn-sm" v-if="role === 'Storemanager'">
            <i class="bi bi-plus-lg me-1"></i> Add Product
          </router-link>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger glass-card border-danger text-danger mb-4 d-flex justify-content-between align-items-center">
        <span><strong>Error!</strong> {{ error }}</span>
        <button type="button" class="btn-close" @click="error = ''"></button>
      </div>

      <div class="table-responsive">
        <table class="table table-borderless align-middle text-white">
          <thead class="text-secondary small text-uppercase tracking-wider border-bottom border-secondary border-opacity-10">
            <tr>
              <th class="ps-0">ID</th>
              <th>Name</th>
              <th>Category</th>
              <th class="text-end">Price</th>
              <th class="text-center">Stock</th>
              <th>Manufacture</th>
              <th class="text-end pe-0">Actions</th>
            </tr>
          </thead>
          <tbody v-if="products.length">
            <tr v-for="product in products" :key="product.id" class="border-bottom border-secondary border-opacity-10">
              <td class="ps-0 py-3 text-secondary">#{{ product.id }}</td>
              <td><span class="fw-bold">{{ product.name }}</span></td>
              <td><span class="badge bg-secondary bg-opacity-25 text-white fw-normal">{{ product.category.name }}</span></td>
              <td class="text-end">&#8377;{{ product.price }}</td>
              <td class="text-center">
                <span :class="['badge rounded-pill px-3', product.quantity > 10 ? 'bg-success bg-opacity-25 text-success' : 'bg-danger bg-opacity-25 text-danger']">
                  {{ product.quantity }}
                </span>
              </td>
              <td>
                <div v-if="product.delete" class="mb-1">
                  <span class="badge rounded-pill bg-danger bg-opacity-25 text-danger px-3 smaller">Deletion Requested</span>
                </div>
                {{ formatDate(product.manufacture_date) }}
              </td>
              <td class="text-end pe-0">
                <div class="d-flex justify-content-end gap-2">
                  <router-link v-if="role === 'Storemanager'" :to="{ name: 'editproduct', params: { id: product.id } }" class="btn btn-sm btn-outline-light border-secondary border-opacity-50">
                    <i class="bi bi-pencil"></i>
                  </router-link>
                  <button v-if="role === 'Storemanager' || product.delete" 
                          class="btn btn-sm btn-outline-danger border-secondary border-opacity-50" 
                          @click="deleteProduct(product.id)"
                          :title="product.delete ? 'Confirm Deletion' : 'Request Deletion'">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="7" class="text-center py-5 text-secondary">No products found in inventory.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>


<script>
import router from '@/router'

  export default {
    name: 'ShowProducts',
    data() {
        return {
            token: localStorage.getItem('token'),
            role: localStorage.getItem('role'),
            products: [],
            isWaiting: false,
            error: ''
        };
    },
    methods: {
        async getProducts() {
            const response = await fetch('http://localhost:5000/api/products', {
                method: 'GET',
                headers: {
                    'Authentication-Token': localStorage.getItem('token')
                }
            })
                .catch(error => console.log(error));
            const data = await response.json();
            if (response.ok) {
                this.products = data;
            }
            else {
                this.error = data.message;
            }
        },
        formatDate(dateStr) {
          if (!dateStr) return 'N/A';
          return new Date(dateStr).toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
          });
        },
        async deleteProduct(id) {
            const response = await fetch(`http://localhost:5000/api/product/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authentication-Token': localStorage.getItem('token')
                }
            })
                .catch(error => console.log(error));
            const data = await response.json();
            if (response.ok) {
              this.getProducts();
              if (this.role === 'Storemanager') {
                alert('Request to delete product sent to admin');
              }
              else {
                alert('Product deleted successfully');
              }
            }
            else {
                this.error = data.message;
            }
        },


        async downloadProducts() {
          this.isWaiting = true;
          const response = await fetch('http://localhost:5000/download-csv', {
            method: 'GET',
            headers: {
                'Authentication-Token': localStorage.getItem('token')
            }
          })
          .catch(error => console.log(error));
          const data = await response.json();
          if (response.ok) {
            const taskId = data.task_id;
            const intv = setInterval(async () => {
              const csv_response = await fetch(`http://localhost:5000/get-csv/${taskId}`, {
                method: 'GET',
                headers: {
                    'Authentication-Token': localStorage.getItem('token')
                }
              })
              .catch(error => console.log(error));
              if (csv_response.ok) {
                this.isWaiting = false;
                clearInterval(intv);
                window.location.href = `http://localhost:5000/get-csv/${taskId}`;
              }
            }, 1000);
          }
          else {
              this.error = data.message;
              this.isWaiting = false;
          }
        }
    },
    async mounted() {
        this.getProducts();
    },
    components: { router }
}
</script>