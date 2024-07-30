<template>
  <div class="container">
    <h1 class="mt-4 mb-3">Most Rated Books</h1>
    <div class="row">
      <div v-for="book in mostRated" :key="book.id" class="col-md-4 mb-4">
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

    <h1 class="mt-4 mb-3">Best Sellers</h1>
    <div class="row">
      <div v-for="book in bestSellers" :key="book.id" class="col-md-4 mb-4">
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

    <h1 class="mt-4 mb-3">Newly Added</h1>
    <div class="row">
      <div v-for="book in newlyAdded" :key="book.id" class="col-md-4 mb-4">
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

<style scoped>
.card-img-top {
  height: 300px;
  object-fit: cover;
}
</style>