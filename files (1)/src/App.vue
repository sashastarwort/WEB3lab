<template>
  <AppNavbar />
  <RouterView />
  <AppFooter />
</template>

<script setup>
import AppNavbar from './components/AppNavbar.vue'
import AppFooter from './components/AppFooter.vue'
</script>

<style>
body {
  background-color: #000;
  color: #f8f9fa;
}
.navbar-custom { backdrop-filter: blur(10px); }
.nav-link.router-link-active {
  color: #ffc107 !important;
  border-bottom: 2px solid #ffc107;
}
.card-custom { border: 1px solid rgba(255,255,255,0.1); }
</style>
