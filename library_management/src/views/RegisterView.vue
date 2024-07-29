<script setup>
import { RouterLink } from 'vue-router';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const password = ref('');
const confirm_password = ref('');
//const address = ref('');
const role = ref('');
const router = useRouter();

const auth_store = auth();
const message_store = messageStore();

function validate_input(){
    if (password.value.length < 8){
        message_store.setmessage('Password should be atleast 8 characters')
        return false
    }
    if(password.value !== confirm_password.value){
        message_store.setmessage('Password and Confirm Password should be same')
        return false
    }
    if(username.value.length < 3){
        message_store.setmessage('Username should be atleast 3 characters and alphanumeric')
        return false
    }
    return true
}

function onSubmit(){
    if (validate_input()){
        const data = {
            username: username.value,
            email: email.value,
            password: password.value,
            confirm_password: confirm_password.value,
            //address: address.value,
            role: role.value
        }
        auth_store.register(data).then(
            (resp)=>{
                message_store.setmessage(resp.message)
                if(resp.status){
                    router.push({path: '/'})
                }
            }
        )
    }
}

</script>

<template>
    <div class="container-fluid mt-2 p-3">
    <h1 class="text-center">Register</h1>
    <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent="onSubmit">
            <div class="mb-3">
                <label for="username" class="form-label"><strong>Username</strong></label>
                <input type="text" class="form-control" id="username" aria-describedby="usernameHelp" required v-model="username">
                <div id="usernameHelp" class="form-text">Username Should be alphanumeric and should contain atleast 3 characters.</div>
            </div>
            <div class="mb-3">
              <label for="email" class="form-label"><strong>Email Address</strong></label>
              <input type="email" class="form-control" id="email" v-model="email" required >
            </div>
            <div class="row">
              <div class="mb-3 col-6">
                  <label for="exampleInputPassword1" class="form-label"><strong>Password</strong></label>
                  <input type="password" class="form-control" id="exampleInputPassword1" v-model="password" required>
              </div>
              <div class="mb-3 col-6">
                  <label for="exampleInputPassword2" class="form-label"><strong>Confirm Password</strong> </label>
                  <input type="password" class="form-control" id="exampleInputPassword2" v-model='confirm_password' required>
              </div>
            </div>
            
            <div class="mb-3">
                <label for="phone" class="form-label"><strong>Role</strong></label>
                <div class="input-group d-flex align-center">
                  <input type="radio" id="storemanager" v-model="role" value="librarian" required>&ensp;
                  <label for="storemanager"> Librarian </label>&ensp; &ensp;
                  <input type="radio" id="customer" v-model="role" value="user" required>&ensp;
                  <label for="customer">Customer</label>
                </div>
            </div>
            <div class="d-flex justify-content-center mb-3">
                <button type="submit" class="btn btn-primary">Register</button>
            </div>
            <div class="d-flex justify-content-center mt-2">
                <span>Alreay an existing user? &ensp; </span>
                <RouterLink to="/login">Login</RouterLink>
            </div>
        </form>
    </div>  
</div>
</template>