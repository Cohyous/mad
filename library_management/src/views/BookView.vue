<template>
  <div class="container mt-5">
    <div v-if="book" class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="row g-0">
            <div class="col-md-4">
              <img
                :src="`/api/book-cover/${book.id}`"
                :alt="`Cover of ${book.name}`"
                class="img-fluid rounded-start h-100 object-fit-cover"
              />
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h2 class="card-title">{{ book.name }}</h2>
                <h6 class="card-subtitle mb-2 text-muted">
                  Author: {{ book.author }}
                </h6>
                <p class="card-text mt-3">{{ book.description }}</p>
                <ul class="list-group list-group-flush mt-3">
                  <li class="list-group-item">
                    <strong>ISBN:</strong> {{ book.isbn_no }}
                  </li>
                  <li class="list-group-item">
                    <strong>Price:</strong> ${{ book.price }}
                  </li>
                  <li class="list-group-item">
                    <strong>Date Published:</strong>
                    {{ formatDate(book.date_published) }}
                  </li>
                  <li class="list-group-item">
                    <strong>Average Rating:</strong> {{ book.avg_rating }}
                    <small class="text-muted"
                      >({{ book.total_ratings }} ratings)</small
                    >
                  </li>
                </ul>
                <div class="mt-4">
                  <div v-if="isUser">
                    <!-- Check if the book is available for download -->
                    <button
                      v-if="userEligibility.owned_books.includes(book.id)"
                      class="btn btn-success me-2"
                      @click="downloadBook"
                    >
                      Download
                    </button>
                    <!-- Check if the book is not downloaded yet, and not borrowed -->
                    <button
                      v-if="
                        !userEligibility.owned_books.includes(book.id) &&
                        !userEligibility.borrowed_books.includes(book.id)
                      "
                      class="btn btn-outline-primary me-2"
                      @click="borrowBook"
                    >
                      Borrow
                    </button>
                    <button
                      v-if="!userEligibility.owned_books.includes(book.id)"
                      class="btn btn-primary me-2"
                      @click="purchaseBook"
                    >
                      Purchase
                    </button>
                  </div>
                  <div v-else-if="isLibrarian">
                    <button class="btn btn-warning" @click="editBook">
                      Edit Book
                    </button>
                  </div>
                </div>
                <div class="mt-4">
                  <h3>User Feedbacks</h3>
                  <div v-if="feedbacks.length > 0">
                    <p>Average Rating: {{ averageRating.toFixed(1) }} / 5</p>
                    <ul class="list-group">
                      <li
                        v-for="feedback in feedbacks"
                        :key="feedback.id"
                        class="list-group-item"
                      >
                        <p>Rating: {{ feedback.stars }} / 5</p>
                        <p>{{ feedback.feedback }}</p>
                      </li>
                    </ul>
                  </div>
                  <div v-else>No feedbacks yet.</div>

                  <div v-if="isUser" class="mt-3">
                    <h4>Submit Your Feedback</h4>
                    <form @submit.prevent="submitFeedback">
                      <div class="mb-3">
                        <label for="stars" class="form-label">Rating:</label>
                        <input
                          type="number"
                          id="stars"
                          v-model="newFeedback.stars"
                          min="1"
                          max="5"
                          class="form-control"
                          required
                        />
                      </div>
                      <div class="mb-3">
                        <label for="feedback" class="form-label"
                          >Your Feedback:</label
                        >
                        <textarea
                          id="feedback"
                          v-model="newFeedback.feedback"
                          class="form-control"
                          required
                        ></textarea>
                      </div>
                      <button type="submit" class="btn btn-primary">
                        Submit Feedback
                      </button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-warning" role="alert">
      Book details not found.
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";

export default {
  setup() {
    const book = ref(null);
    const isUser = ref(false);
    const isLibrarian = ref(false);
    const feedbacks = ref([]);
    const averageRating = ref(0);
    const newFeedback = ref({ stars: 5, feedback: "" });
    const userEligibility = ref({
      owned_books: [],
      borrowed_books: [],
      requested_books: [],
    });
    const route = useRoute();
    const bookId = route.params.id;

    const fetchFeedbacks = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/v1/book_feedbacks?book_id=${bookId}`,
          {
            headers: {
              "Authentication-Token": localStorage.getItem("token"),
            },
          }
        );
        feedbacks.value = response.data.feedbacks;
        averageRating.value = response.data.average_rating;
      } catch (error) {
        console.error("Error fetching feedbacks:", error);
      }
    };

    const submitFeedback = async () => {
  try {
    await axios.post(
      `http://127.0.0.1:5000/api/v1/book_feedbacks`,
      {
        book_id: bookId, // Add book_id here
        feedback: newFeedback.value,
      },
      {
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("token"),
        },
      }
    );
    alert("Feedback submitted successfully");
    newFeedback.value = { stars: 5, feedback: "" };
    fetchFeedbacks(); // Refresh feedbacks after submission
  } catch (error) {
    alert("Error submitting feedback: " + error.message);
  }
};

    const fetchBookDetails = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/v1/search_books?filter=id&value=${bookId}`
        );
        if (response.data.length > 0) {
          book.value = response.data[0];
        } else {
          book.value = null;
        }
      } catch (error) {
        console.error("Error fetching book details:", error);
        book.value = null;
      }
    };

    const fetchUserEligibility = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/v1/user_eligibility",
          {
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*",
              "Authentication-Token": localStorage.getItem("token"),
            },
          }
        );
        console.log(response.data);
        if (
          response.data.message &&
          response.data.message === "You are a librarian"
        ) {
          isLibrarian.value = true;
        } else {
          isUser.value = true;
          userEligibility.value = response.data;
        }
      } catch (error) {
        console.error("Error fetching user eligibility:", error);
      }
    };

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString();
    };

    const purchaseBook = async () => {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/v1/user_purchase",
          { book_id: book.value.id },
          {
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("token"),
            },
          }
        );

        console.log(response.data);
        window.location.reload();
      } catch (error) {
        alert("Error purchasing book:", error);
      }
    };

    const borrowBook = async () => {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/v1/user_request",
          { book_id: book.value.id },
          {
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("token"),
            },
          }
        );
        console.log(response.data);
        window.location.reload();
      } catch (error) {
        alert("Error borrowing book:", error);
      }
    };

    const downloadBook = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/v1/download_book/${book.value.id}`,
          {
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("token"),
            },
            responseType: "blob",
          }
        );
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("d  ownload", `${book.value.name}.pdf`);
        document.body.appendChild(link);
        link.click();
      } catch (error) {
        alert("Error downloading book:", error);
      }
    };

    const editBook = () => {
      // Implement edit logic
      console.log("Edit button clicked");
    };

    onMounted(() => {
      fetchBookDetails();
      fetchUserEligibility();
      fetchBookDetails();
      fetchUserEligibility();
      fetchFeedbacks();
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
      feedbacks,
      averageRating,
      newFeedback,
      submitFeedback,
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
