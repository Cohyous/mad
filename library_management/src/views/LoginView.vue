<script setup>
import { RouterLink } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');

const router = useRouter();

const auth_store = auth();
const message_store = messageStore();

async function onSubmit() {
  const data = {
    email: email.value,
    password: password.value
  }
  auth_store.login(data).then(
    (resp)=>{
      message_store.setmessage(resp.message)
      if(resp.status){
        console.log(resp)
        auth_store.updateToken()
        auth_store.updateUserDetails()
        console.log("here")
        router.push({path: '/home'})
      }
    }
  )
}

</script>

<template>
    <div class="container-fluid mt-2 p-3">
      <h1 class="text-center">Login</h1>
      <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent = "onSubmit">
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">Email address</label>
            <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model = "email">
            <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Password</label>
            <input type="password" class="form-control" id="exampleInputPassword1" v-model="password">
          </div>
          <div class="d-flex justify-content-center mb-3">
            <button type="submit" class="btn btn-primary">Login</button>
          </div>
          <div class="d-flex justify-content-center mt-2">
            <span>Don't have an account? &ensp; </span>
            <RouterLink to="/register" >Register</RouterLink>
          </div>
        </form>
      </div>
    </div>
  </template>