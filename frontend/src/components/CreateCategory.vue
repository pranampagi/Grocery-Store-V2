<template>
  <div class="container">
    <div class="content-section" style="width: 50%; margin-left: 25%;">
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Create Category</legend>
        <div class="form-group mb-3">
          <label for="name" class="mb-2">Name</label>
          <input type="text" v-model="category.name" class="form-control" id="name" placeholder="Enter name">
        </div>
        <div class="form-group mb-3">
          <label for="description" class="mb-2">Description</label>
          <input type="text" v-model="category.description" class="form-control" id="description" placeholder="Enter description">
        </div>
        <div class="form-group mb-3">
          <button type="submit" class="btn btn-outline-info" @click="createCategory">Create</button>
        </div>
        <div class="alert alert-danger" v-if="error">
          {{ error }}
        </div>
      </fieldset>
    </div>
  </div>
</template>



<script>
  export default {
    name: 'CreateCategory',

    data() {
      return {
        token: localStorage.getItem('token'),
        category: {
          name: '',
          description: ''
        },
        error: ''
      }
    },

    methods: {
      async createCategory() {
        const response = await fetch('http://localhost:5000/api/categories', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          },
          body: JSON.stringify(this.category)
        })
        .catch(error => console.log(error))
        const data = await response.json()
        if (response.ok) {
          this.$router.push({ name: 'showcategories' })
        } else {
          this.error = data.message
        }
      }
    }
  }
</script>