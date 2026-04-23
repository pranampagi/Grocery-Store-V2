<template>
  <div class="container">
    <h1 v-if="role === 'Admin'">Admin Dashboard</h1>
    <h1 v-else>Manager Dashboard</h1>
    <h4 class="lead" v-if="role ==='Admin'">Welcome to the admin dashboard, Admin!</h4>
    <h4 class="lead" v-else>Welcome to the Store Manager dashboard, Manager!</h4>
    <hr>

    <h2>Store Managers</h2>
    <table class="table table-striped mb-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Role</th>
          <th>Activate</th>
        </tr>
      </thead>
      <tbody v-for="user in users" :key="user.id">
        <tr v-if="user.roles[0].name === 'Storemanager'">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.roles[0].name }}</td>
          <td v-if="!user.active && user.roles[0].name === 'Storemanager'">
            <button class="btn btn-success" @click="activateStoremanager(user.id)">Activate</button>
          </td>
          <td v-else>
            <button class="btn btn-outline-success" disabled>Activated</button>
          </td>
        </tr>
      </tbody>
    </table>


    <h2>Customers</h2>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Role</th>
        </tr>
      </thead>
      <tbody v-for="user in users" :key="user.id">
        <tr v-if="user.roles[0].name === 'Customer'">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.roles[0].name }}</td>
        </tr>
      </tbody>
    </table>
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