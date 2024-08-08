<script setup>
import { ref, onMounted } from "vue";
import { useRouter, RouterLink } from "vue-router";
import Cookies from 'js-cookie'; // Import js-cookie

const router = useRouter();
const isLoggedIn = ref(false);
const username = ref("");

const handleLogout = () => {
  // Remove user details from localStorage
  localStorage.removeItem("user_details");

  // Clear cookie
  Cookies.remove('auth_token');

  // Update the state
  isLoggedIn.value = false;
  username.value = "";

  // Redirect to login page
  router.push("/login");
};

onMounted(() => {
  const userDetails = localStorage.getItem("user_details");
  if (userDetails) {
    const user = JSON.parse(userDetails);
    username.value = user.username;
    isLoggedIn.value = true;
  }
});
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">EBooks</RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <form class="d-flex ms-auto" role="search">
          <input
            class="form-control me-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <button class="btn btn-outline-light" type="submit">Search</button>
        </form>
        <ul class="navbar-nav ms-3" v-if="isLoggedIn">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/collections">Collections</RouterLink>
          </li>
          <li class="nav-item">
            <span class="nav-link">{{ username }}</span>
          </li>
          <li class="nav-item">
            <button
              class="btn btn-outline-light nav-link"
              @click="handleLogout"
            >
              Logout
            </button>
          </li>

        </ul>
        <ul class="navbar-nav ms-3" v-else>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/register">Register</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/login">Login</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar-nav .nav-item .nav-link {
  cursor: pointer;
}
</style>