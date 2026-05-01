<template>
  
</template>

<script>
import API_BASE from '@/api';
  export default {
    name: 'CategoryCard',

    data() {
      return {
        category: []
      }
    },

    async mounted () {
      const response = await fetch(`${API_BASE}/api/categories`, {
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
