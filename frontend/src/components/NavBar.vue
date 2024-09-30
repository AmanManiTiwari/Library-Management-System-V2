<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light" >
    <div class="container-fluid">
  <router-link class="navbar-brand" to="/">The Book Hub</router-link>
  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavDropdown">
    <ul v-if="this.isloggedin" class="navbar-nav">
      <li class="nav-item">
          <router-link v-if="!is_librarian" class="nav-link" to="/home">Home</router-link>
      </li>
      <li class="nav-item">
          <router-link v-if="is_librarian" class="nav-link" to="/sections">Home</router-link>
      </li>
      <li class="nav-item">
          <router-link v-if="is_librarian" class="nav-link" to="/bookrequested">Book Requested</router-link>
      </li>
      <li class="nav-item">
          <router-link v-if="is_librarian" class="nav-link" to="/bookstatus">Book Status</router-link>
      </li>
      <li class="nav-item">
          <router-link v-if="is_librarian" class="nav-link" to="/summary">Summary</router-link>
      </li>
      <li class="nav-item" v-if="is_librarian">
            <a class="nav-link" @click="exportEbooks">Export CSV</a>
      </li>
      <li class="nav-item">
          <router-link v-if="!is_librarian" class="nav-link" to="/issued">Book Issued</router-link>
      </li>
      <li class="nav-item">
          <a class="nav-link" @click="logout">Logout</a>
      </li> 
      
      </ul>
      <ul v-else class="navbar-nav">
      <li class="nav-item">
          <router-link class="nav-link" to="/">Login</router-link>
      </li>
      <li class="nav-item">
          <router-link class="nav-link" to="/userregister">Register</router-link>
      </li>
    </ul>
  </div>
</div>
            </nav>
</template>


<!-- <script>
import UserMixin from '../mixins/userMixin'
export default {
  name: 'NavBar',
  mixins: [UserMixin],
}
</script> -->
<script>
import UserMixin from '../mixins/userMixin';

export default {
  name: 'NavBar',
  mixins: [UserMixin],
  methods: {
    async exportEbooks() {
      try {
        const response = await fetch('http://localhost:5000/export_csv_report?librarian_id=1&email=admin@gmail.com', {
          method: 'GET'
        });
        const result = await response.json();
        console.log(result);
        if (response.ok) {
          alert('Export task started. You will receive an email once it is completed.');
        } else {
          alert('Failed to start export task.');
        }
      } catch (error) {
        console.error('Error exporting ebooks:', error);
        alert('Error exporting ebooks.');
      }
    }
  }
};
</script>
<style scoped   >
</style>