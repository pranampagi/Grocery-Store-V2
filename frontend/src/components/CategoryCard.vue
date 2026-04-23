<template>
  
</template>

<script>
  export default {
    name: 'CategoryCard',

    data() {
      return {
        category: []
      }
    },

    async mounted () {
      const response = await fetch('http://localhost:5000/api/categories', {
        method: "GET",
        headers: {
          'Content-Type': 'application/json'
        }
      }).catch(error => console.log(error))
      const data = await response.json()
      if (response.ok) {
        this.category = data
      }
    }
  }
</script>
