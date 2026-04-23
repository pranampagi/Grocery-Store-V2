<template>
  <div id="app">
    <Navbar :key="hasChanged" />
    <div class="container-fluid mt-4 px-lg-5">
      <router-view />
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import './assets/theme.css'

export default {
  name: 'App',
  components: {
    Navbar
  },
  data() {
    return {
      hasChanged: true
    }
  },
  watch: {
    $route() {
      this.hasChanged = !this.hasChanged
    }
  }
}
</script>
