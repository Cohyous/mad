<template>
    <div>
      <h1>Most Rated</h1>
      <div class="scroll-container">
        <div class="scroll-content">
          <div v-for="m in mostRated" :key="m[0].BookID">
            <router-link :to="'/view/' + m[0].BookID">
              <img :src="getImageUrl(m[0].BookID)" alt="Most Rated Book" />
            </router-link>
          </div>
        </div>
      </div>
      <br><br>
      <h1>Best Sellers</h1>
      <div class="scroll-container">
        <div class="scroll-content">
          <div v-for="b in bestSellers" :key="b[0].BookID">
            <router-link :to="'/view/' + b[0].BookID">
              <img :src="getImageUrl(b[0].BookID)" alt="Best Seller" />
            </router-link>
          </div>
        </div>
      </div>
      <br><br>
      <h1>Newly Added</h1>
      <div class="scroll-container">
        <div class="scroll-content">
          <div v-for="n in newlyAdded" :key="n.BookID">
            <router-link :to="'/view/' + n.BookID">
              <img :src="getImageUrl(n.BookID)" alt="Newly Added Book" />
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const mostRated = ref([]);
  const bestSellers = ref([]);
  const newlyAdded = ref([]);
  
  const backendUrl = 'http://127.0.0.1:5000/api/v1'; // Update with your actual backend URL
  
  const getImageUrl = (bookId) => {
    return `${backendUrl}/static/thumbnails/${bookId}.jpg`;
  };
  
  const fetchMostRated = async () => {
    try {
      const response = await axios.get(`${backendUrl}/most_rated_books`);
      mostRated.value = response.data;
    } catch (error) {
      console.error('Error fetching most rated books:', error);
    }
  };
  
  const fetchBestSellers = async () => {
    try {
      const response = await axios.get(`${backendUrl}/best_sellers`);
      bestSellers.value = response.data;
    } catch (error) {
      console.error('Error fetching best sellers:', error);
    }
  };
  
  const fetchNewlyAdded = async () => {
    try {
      const response = await axios.get(`${backendUrl}/newly_added_books`);
      newlyAdded.value = response.data;
    } catch (error) {
      console.error('Error fetching newly added books:', error);
    }
  };
  
  onMounted(() => {
    fetchMostRated();
    fetchBestSellers();
    fetchNewlyAdded();
  });
  </script>
  
  <style>
  body {
    font-family: Arial, sans-serif;
  }
  
  .scroll-container {
    width: 100%;
    overflow: auto;
    white-space: nowrap;
  }
  
  .scroll-content {
    display: inline-block;
    white-space: nowrap;
  }
  
  .scroll-content img {
    width: 300px;
    margin: 20px;
  }
  </style>
  