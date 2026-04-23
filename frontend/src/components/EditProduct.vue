<template>
  <div class="container">
    <div class="content-section" style="width: 50%; margin-left: 25%;">
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Edit Product</legend>
        <div class="form-group mb-3">
          <label for="name" class="mb-2">Name</label>
          <input type="text" v-model="product.name" class="form-control" id="name" placeholder="Enter name">
        </div>
        <div class="form-group mb-3">
          <label for="price" class="mb-2">Price</label>
          <input type="number" v-model="product.price" class="form-control" id="price" placeholder="Enter price">
        </div>
        <div class="form-group mb-3">
          <label for="category" class="mb-2">Category</label>
          <select v-model="product.category_id" class="form-control" id="category_id">
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </select>
        </div>
        <div class="form-group mb-3">
          <label for="quantity" class="mb-2">Quantity</label>
          <input type="number" v-model="product.quantity" class="form-control" id="quantity" placeholder="Enter quantity">
        </div>
        <div class="form-group mb-3">
          <label for="manufacture_date" class="mb-2">Manufacture Date</label>
          <input type="date" v-model="product.manufacture_date" class="form-control" id="manufacture_date" placeholder="Enter manufacture date">
        </div>
        <div class="form-group mb-3">
          <button type="submit" class="btn btn-outline-info" @click="editProduct">Update</button>
        </div>
        <div class="alert alert-danger" v-if="error">
          {{ Object.values(error)[0] }}
        </div>
      </fieldset>
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