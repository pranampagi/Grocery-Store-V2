<template>
  <div class="container py-5 animate-fade-in text-white">
    <div class="mb-5">
      <h1 class="display-5 fw-bold mb-0 text-white">{{ role === 'Admin' ? 'Admin Dashboard' : 'Manager Dashboard' }}</h1>
      <p class="text-secondary lead">{{ role === 'Admin' ? 'Welcome to the admin dashboard, Admin!' : 'Welcome to the Store Manager dashboard, Manager!' }}</p>
    </div>

    <div class="glass-card p-4 mb-5">
      <div class="mb-4 pb-3 border-bottom border-secondary border-opacity-25">
        <h2 class="h4 fw-bold mb-0 text-uppercase tracking-wider text-white">Store Managers</h2>
      </div>
      
      <div class="table-responsive">
        <table class="table table-borderless align-middle text-white bg-transparent">
          <thead class="text-secondary small text-uppercase tracking-wider border-bottom border-secondary border-opacity-10">
            <tr>
              <th class="ps-0">ID</th>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
              <th class="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in storeManagers" :key="user.id" class="border-bottom border-secondary border-opacity-10">
              <td class="ps-0 py-3 text-secondary">#{{ user.id }}</td>
              <td><span class="fw-bold">{{ user.name }}</span></td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td class="text-center">
                <button v-if="!user.active" class="btn btn-sm btn-success rounded-pill px-4" @click="activateStoremanager(user.id)">
                  Activate
                </button>
                <span v-else class="badge rounded-pill bg-success bg-opacity-25 text-success px-4">Active</span>
              </td>
            </tr>
            <tr v-if="storeManagers.length === 0">
              <td colspan="5" class="text-center py-4 text-secondary">No store managers found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>


    <div class="glass-card p-4">
      <div class="mb-4 pb-3 border-bottom border-secondary border-opacity-25">
         <h2 class="h4 fw-bold mb-0 text-uppercase tracking-wider text-white">Customers</h2>
      </div>
      
      <div class="table-responsive">
        <table class="table table-borderless align-middle text-white bg-transparent">
          <thead class="text-secondary small text-uppercase tracking-wider border-bottom border-secondary border-opacity-10">
            <tr>
              <th class="ps-0">ID</th>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in customers" :key="user.id" class="border-bottom border-secondary border-opacity-10">
              <td class="ps-0 py-3 text-secondary">#{{ user.id }}</td>
              <td><span class="fw-bold">{{ user.name }}</span></td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
            </tr>
            <tr v-if="customers.length === 0">
              <td colspan="4" class="text-center py-4 text-secondary">No customers found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Users',

    data() {
      return {
        token: localStorage.getItem('token'),
        role: localStorage.getItem('role'),
        users: []
      }
    },

    computed: {
      storeManagers() {
        return this.users.filter(u => u.roles && u.roles[0] && u.roles[0].name === 'Storemanager');
      },
      customers() {
        return this.users.filter(u => u.roles && u.roles[0] && u.roles[0].name === 'Customer');
      }
    },

    methods: {
      async getUsers() {
        fetch('http://localhost:5000/api/users', {
          method: "GET",
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          }
        }).then(response => response.json())
          .then(data => {
            this.users = data
          })
          .catch(error => console.log(error))
      },


      async activateStoremanager(id) {
        const response = await fetch(`http://localhost:5000/activate/storemanager/${id}`, {
          method: 'PUT',
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          }
        }).catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          alert("Storemanager activated")
          this.getUsers()
        } else {
          console.log(data.message)
        }
      },
    },

    async mounted() {
      this.getUsers()
    },
    

    // async updated() {
    //   this.getUsers()
    // }
  }
</script>