<template>
  <div class="container mt-4">
    <h2>Movies</h2>

    <div class="row">
      <div class="col-md-6 mb-4" v-for="movie in movies" :key="movie.id">
        <div class="card h-100">
          <div class="row g-0">
            <div class="col-md-4">
              <img
                :src="movie.poster"
                class="img-fluid rounded-start h-100 object-fit-cover"
                :alt="movie.title"
              />
            </div>

            <div class="col-md-8">
              <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text">{{ movie.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="movies.length === 0">
      <p>No movies added yet.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

function fetchMovies() {
  fetch("/api/v1/movies")
    .then((response) => response.json())
    .then((data) => {
      movies.value = data.movies;
    })
    .catch((error) => {
      console.log(error);
    });
}

onMounted(() => {
  fetchMovies();
});
</script>