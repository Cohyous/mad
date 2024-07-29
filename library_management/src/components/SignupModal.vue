// src/components/SignupModal.vue
<template>
  <div class="modal fade" id="userSignup" tabindex="-1" aria-labelledby="signupModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="signupModalLabel">User Signup</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="signupUser">
            <div class="mb-3">
              <label for="signupUsername" class="form-label">Username</label>
              <input type="text" class="form-control" id="signupUsername" v-model="signupForm.username" required>
            </div>
            <div class="mb-3">
              <label for="signupEmail" class="form-label">Email</label>
              <input type="email" class="form-control" id="signupEmail" v-model="signupForm.email" required>
            </div>
            <div class="mb-3">
              <label for="signupPassword" class="form-label">Password</label>
              <input type="password" class="form-control" id="signupPassword" v-model="signupForm.password" required>
            </div>
            <button type="submit" class="btn btn-secondary">Signup</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      signupForm: {
        username: '',
        email: '',
        password: ''
      }
    };
  },
  methods: {
    signupUser() {
      axios.post('/signup', this.signupForm)
        .then(response => {
          alert('Signup successful');
          location.reload();
        })
        .catch(error => {
          alert('Signup failed: ' + error.response.data.message);
        });
    }
  }
};
</script>
