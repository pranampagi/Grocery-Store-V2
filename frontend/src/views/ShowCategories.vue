<template>
  <div class="container py-5 animate-fade-in">
    <div class="mb-5">
      <h1 class="display-5 fw-bold mb-0">{{ role === 'Admin' ? 'Admin Dashboard' : 'Manager Dashboard' }}</h1>
      <p class="text-secondary">Welcome back, {{ role === 'Admin' ? 'Administrator' : 'Store Manager' }}!</p>
    </div>

    <div class="glass-card p-4">
      <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-secondary border-opacity-25">
        <h2 class="h4 fw-bold mb-0 text-uppercase tracking-wider">Product Categories</h2>
        <div v-if="role === 'Admin' || role === 'Storemanager'">
          <router-link :to="{ name: 'createcategory' }" class="btn btn-premium btn-primary-premium btn-sm">
            <i class="bi bi-plus-lg me-1"></i> Add Category
          </router-link>
        </div>
      </div>

      <div class="alert alert-danger glass-card border-danger text-danger mb-4" v-if="error">
        {{ error }}
      </div>

      <div class="table-responsive">
        <table class="table table-borderless align-middle text-white">
          <thead class="text-secondary small text-uppercase tracking-wider border-bottom border-secondary border-opacity-10">
            <tr>
              <th class="ps-0">ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Creator</th>
              <th class="text-center">Status</th>
              <th class="text-end pe-0">Actions</th>
            </tr>
          </thead>
          <tbody v-if="categories.length">
            <tr v-for="category in categories" :key="category.id" class="border-bottom border-secondary border-opacity-10">
              <td class="ps-0 py-3 text-secondary">#{{ category.id }}</td>
              <td><span class="fw-bold">{{ category.name }}</span></td>
              <td><span class="text-secondary small d-inline-block text-truncate" style="max-width: 200px;">{{ category.description }}</span></td>
              <td>{{ category.creator }}</td>
              <td class="text-center">
                <div v-if="category.delete" class="mb-2">
                  <span class="badge rounded-pill bg-danger bg-opacity-25 text-danger px-3 smaller">Deletion Requested</span>
                </div>
                <span v-if="category.active" class="badge rounded-pill bg-success bg-opacity-25 text-success px-3">Active</span>
                <span v-else-if="role === 'Storemanager'" class="badge rounded-pill bg-warning bg-opacity-25 text-warning px-3">Pending</span>
                <button v-else-if="role === 'Admin'" class="btn btn-sm btn-success rounded-pill px-3" @click="activateCategory(category.id)">Activate</button>
              </td>
              <td class="text-end pe-0">
                <div class="d-flex justify-content-end gap-2">
                  <router-link :to="{ name: 'editcategory', params: { id: category.id } }" class="btn btn-sm btn-outline-info border-info border-opacity-50 px-3">
                    <i class="bi bi-pencil-square me-1"></i> Edit
                  </router-link>
                  
                  <!-- Storemanager delete request button -->
                  <button v-if="role === 'Storemanager'" class="btn btn-sm btn-outline-danger border-danger border-opacity-50 px-3" @click="deleteCategory(category.id)">
                    <i class="bi bi-trash-fill me-1"></i> Delete
                  </button>

                  <!-- Admin Accept/Reject buttons -->
                  <div v-else-if="role === 'Admin' && category.delete" class="d-flex gap-2">
                    <button class="btn btn-sm btn-success rounded-pill px-3 fw-bold" @click="deleteCategory(category.id)">
                      <i class="bi bi-check-lg me-1"></i> Accept
                    </button>
                    <button class="btn btn-sm btn-danger rounded-pill px-3 fw-bold" @click="rejectCategory(category.id)">
                      <i class="bi bi-x-lg me-1"></i> Reject
                    </button>
                  </div>
                  <button v-else-if="role === 'Admin'" class="btn btn-sm btn-outline-danger border-danger border-opacity-50 px-3" @click="deleteCategory(category.id)">
                    <i class="bi bi-trash-fill me-1"></i> Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="6" class="text-center py-5 text-secondary">No categories found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import API_BASE from '@/api';
  export default {
    name: 'ShowCategories',

    data() {
      return {
        token: localStorage.getItem('token'),
        role: localStorage.getItem('role'),
        categories: [],
        error: ''
      }
    },

    methods: {
      async getCategories(){
        const response = await fetch(`${API_BASE}/api/categories`, {
          method: "GET",
          headers: {
            'Authentication-Token': this.token
          }
        }).catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.categories = data
        } else {
          this.error = data.message
        }
      },

      async activateCategory(id) {
        const response = await fetch(`${API_BASE}/activate/category/${id}`, {
          method: "PUT",
          headers: {
            'Authentication-Token': this.token
          }
        }).catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          alert('Category activated')
          this.getCategories()
        } else {
          this.error = data.message
        }
      },

      
      async deleteCategory(id) {
        const response = await fetch(`${API_BASE}/api/category/${id}`, {
          method: "DELETE",
          headers: {
            'Authentication-Token': this.token
          }
        }).catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.getCategories()
          if (this.role === 'Storemanager') {
            alert('Request to delete category sent to admin')
          } else {
            alert('Category deleted successfully')
          }
        } else {
          this.error = data.message
        }
      },

      async rejectCategory(id) {
        const response = await fetch(`${API_BASE}/reject/category/${id}`, {
          method: "PUT",
          headers: {
            'Authentication-Token': this.token
          }
        }).catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          alert('Deletion request rejected')
          this.getCategories()
        } else {
          this.error = data.message
        }
      }


    },

    async mounted () {
      this.getCategories()
    }
  }
</script>