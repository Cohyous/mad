<template>
  <div class="container mt-5">
    <div v-if="book" class="card">
      <div class="card-body">
        <h5 class="card-title">{{ book.name }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">Author: {{ book.author }}</h6>
        <p class="card-text"><strong>Description:</strong> {{ book.description }}</p>
        <p class="card-text"><strong>ISBN:</strong> {{ book.isbn_no }}</p>
        <p class="card-text"><strong>Price:</strong> ${{ book.price }}</p>
        <p class="card-text"><strong>Date Published:</strong> {{ formatDate(book.date_published) }}</p>
        <p class="card-text"><strong>Average Rating:</strong> {{ book.avg_rating }} ({{ book.total_ratings }} ratings)</p>

        <!-- Conditional buttons based on user eligibility and book status -->
        <div v-if="isUser">
          <button v-if="!userEligibility.borrowed_books.includes(book.id)" class="btn btn-secondary" @click="borrowBook">Borrow</button>
          <button v-if="userEligibility.owned_books.includes(book.id)" class="btn btn-success" @click="downloadBook">Download</button>
          <button v-else class="btn btn-primary" @click="purchaseBook">Purchase</button>
        </div>
        <div v-else-if="isLibrarian">
          <button class="btn btn-warning" @click="editBook">Edit Book</button>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-warning" role="alert">
      Book details not found.
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

export default {
  setup() {
    const book = ref(null);
    const isUser = ref(false);
    const isLibrarian = ref(false);
    const userEligibility = ref({
      owned_books: [],
      borrowed_books: [],
      requested_books: []
    });
    const route = useRoute();
    const bookId = route.params.id;

    const fetchBookDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/v1/search_books?filter=id&value=${bookId}`);
        if (response.data.length > 0) {
          book.value = response.data[0];
        } else {
          book.value = null;
        }
      } catch (error) {
        console.error('Error fetching book details:', error);
        book.value = null;
      }
    };

    const fetchUserEligibility = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/v1/user_eligibility');
        if (response.data.message === 'You are a librarian') {
          isLibrarian.value = true;
        } else {
          isUser.value = true;
          userEligibility.value = response.data;
        }
      } catch (error) {
        console.error('Error fetching user eligibility:', error);
      }
    };

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString();
    };

    const purchaseBook = () => {
      // Implement purchase logic
      console.log('Purchase button clicked');
    };

    const borrowBook = () => {
      // Implement borrow logic
      console.log('Borrow button clicked');
    };

    const downloadBook = () => {
      // Implement download logic
      console.log('Download button clicked');
    };

    const editBook = () => {
      // Implement edit logic
      console.log('Edit button clicked');
    };

    onMounted(() => {
      fetchBookDetails();
      fetchUserEligibility();
    });

    return {
      book,
      formatDate,
      isUser,
      isLibrarian,
      userEligibility,
      purchaseBook,
      borrowBook,
      downloadBook,
      editBook,
    };
  },
};
</script>

<style scoped>
.card {
  max-width: 600px;
  margin: auto;
}
</style>

  