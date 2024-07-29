<script setup>
import { RouterLink} from 'vue-router';
import { auth } from '@/stores/auth';
const auth_store = auth();
</script>
<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <h3 class="navbar-brand">eBooks</h3>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item"  v-if="auth_store.isAuthenticated && auth_store.role === 'user'">
              <RouterLink class="nav-link" to="/login">Borrowed Books</RouterLink>
          </li>
          <li class="nav-item"  v-if="auth_store.isAuthenticated && auth_store.role === 'user'">
              <RouterLink class="nav-link" to="/login">Owned Books</RouterLink>
          </li>
          <li class="nav-item"  v-if="auth_store.isAuthenticated && auth_store.role === 'librarian'">
              <RouterLink class="nav-link" to="/login">Borrowed Books</RouterLink>
          </li>
          <li class="nav-item"  v-if="auth_store.isAuthenticated && auth_store.role === 'librarian'">
              <RouterLink class="nav-link" to="/login">Borrowed Books</RouterLink>
          </li>  
        </ul>
        <form class="d-flex" role="search">
          <button type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#userfilter">
            <img src="./icons/Filter.png" width="35" height="35" alt="Filter" />

          </button>
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
          <div class="modal fade" id="userfilter" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Filter</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div>
                      <div class="modal-body">
                        <div>
                          
                        
                          <div class="form-check form-check-inline" >
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio4" value="books_Name" checked>
                            <label class="form-check-label" for="inlineRadio4">Book Name</label>
                          </div>
                          <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio5" value="books_BookID" >
                            <label class="form-check-label" for="inlineRadio5">BookID</label>
                          </div>
                          <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio6" value="books_Author">
                            <label class="form-check-label" for="inlineRadio6">Author</label>
                          </div>
                          <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio7" value="books_ISBNno">
                            <label class="form-check-label" for="inlineRadio7">ISBNno</label>
                          </div>
                          <div class="form-check form-check-inline">
                              <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio8" value="books_Section">
                              <label class="form-check-label" for="inlineRadio8">Section</label>
                          </div>
                          <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio9" value="books_DatePublished">
                                <label class="form-check-label" for="inlineRadio9">Date Published</label>
                          </div>
                          <div class="form-check form-check-inline">
                                  <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio10" value="books_Price">
                                  <label class="form-check-label" for="inlineRadio10">Price</label>
                          </div>
  
                        </div>
                      </div>
                          
                      
                            
                            
                            
                    </div>

                </div>
                </div>
              </div>    
                
        </form>
        <ul class="nav justify-content-end">
              <li class="nav-item" v-if="!auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/login">Login</RouterLink>
                </li>
                <li class="nav-item" v-if="!auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/register">Register</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
                </li>
                <li class="nav-item disabled" v-if="auth_store.isAuthenticated">
                    <a class="nav-link">{{auth_store.username}}</a>
                </li>

            </ul>

      </div>
    </div>
  </nav>
</template>