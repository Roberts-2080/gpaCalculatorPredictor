<template>
  <div class="app">
    <router-view />
    <Tabbar />
  </div>
</template>

<script setup>
import Tabbar from './components/Tabbar.vue'
</script>

<style>
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 500px;
  margin: 0 auto;
}
</style>
