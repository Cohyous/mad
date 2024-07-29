<script setup>
import { RouterLink } from 'vue-router';
</script>
<template>
  <div class="container-fluid mt-5 p-5">
    <h1 class="text-center">Welcome to eLibrary</h1>
    <p class="text-center">Read Books online from the comfort of your home.</p>
    <div class="d-flex justify-content-center">
    <RouterLink class="btn btn-primary justify-content-center" to="/login" >Shop Now </RouterLink>
    </div> 
  </div> 
</template>