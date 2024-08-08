<template>
    <div class="container">
      <h1 class="mt-4 mb-3">My Books</h1>
  
      <h2 class="mt-4 mb-3">Purchased Books</h2>
      <div class="row">
        <div v-for="book in ownedBooks" :key="book.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <img :src="getImageUrl(book.id)" class="card-img-top" :alt="book.name">
            <div class="card-body">
              <h5 class="card-title">{{ book.name }}</h5>
              <p class="card-text">{{ book.author }}</p>
              <p class="card-text"><small class="text-muted">Price: ${{ book.price }}</small></p>
            </div>
            <div class="card-footer">
              <router-link :to="'/books/' + book.id" class="btn btn-primary">View Details</router-link>
            </div>
          </div>
        </div>
      </div>
  
      <h2 class="mt-4 mb-3">Borrowed Books</h2>
      <div class="row">
        <div v-for="book in borrowedBooks" :key="book.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <img :src="getImageUrl(book.id)" class="card-img-top" :alt="book.name">
            <div class="card-body">
              <h5 class="card-title">{{ book.name }}</h5>
              <p class="card-text">{{ book.author }}</p>
              <p class="card-text"><small class="text-muted">Price: ${{ book.price }}</small></p>
            </div>
            <div class="card-footer">
              <router-link :to="'/books/' + book.id" class="btn btn-primary">View Details</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const ownedBooks = ref([]);
  const borrowedBooks = ref([]);
  
  const backendUrl = 'http://127.0.0.1:5000/api/v1'; // Update with your actual backend URL
  
  const getImageUrl = (bookId) => {
    return `${backendUrl}/static/thumbnails/${bookId}.jpg`;
  };
  
  const fetchOwnedBooks = async () => {
    try {
      const response = await axios.get(`${backendUrl}/owned_books`,
          {
            headers: {
              "Authentication-Token": localStorage.getItem("token"),
            },
          });
      ownedBooks.value = response.data;
    } catch (error) {
      console.error('Error fetching owned books:', error);
    }
  };
  
  const fetchBorrowedBooks = async () => {
    try {
      const response = await axios.get(`${backendUrl}/borrowed_books`,
          {
            headers: {
              "Authentication-Token": localStorage.getItem("token"),
            },
          });
      borrowedBooks.value = response.data;
    } catch (error) {
      console.error('Error fetching borrowed books:', error);
    }
  };
  
  onMounted(() => {
    fetchOwnedBooks();
    fetchBorrowedBooks();
  });
  </script>
  
  <style scoped>
  .card-img-top {
    height: 300px;
    object-fit: cover;
  }
  </style>