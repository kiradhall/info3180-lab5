<template>
  <div class="container">
    <h2>Upload Form</h2>

    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <div v-if="errors.length > 0" class="alert alert-danger">
      <ul class="mb-0">
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie" enctype="multipart/form-data">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input
          type="text"
          name="title"
          class="form-control"
        />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          name="description"
          class="form-control"
          rows="4"
        ></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Photo Upload</label>
        <input
          type="file"
          name="poster"
          class="form-control"
          accept="image/*"
        />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let errors = ref([]);
let successMessage = ref("");

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch((error) => {
      console.log(error);
    });
}

function saveMovie() {
  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);

  errors.value = [];
  successMessage.value = "";

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value
    }
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message) {
        successMessage.value = data.message;
        movieForm.reset();
      } else if (data.errors) {
        errors.value = data.errors;
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

onMounted(() => {
  getCsrfToken();
});
</script>