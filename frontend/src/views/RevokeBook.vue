<template>
  <div id="outer_div">
    <div id="inner_div">
      <NavBar class="navbar navbar-expand-lg navbar-light bg-light" />
      <h2 class="headings">Book Status</h2>
      <div id="trans-table">
        <table class="table table-success table-striped">
          <thead>
            <tr>
              <th scope="col">User Id</th>
              <th scope="col">Book Id</th>
              <th scope="col">Issue Id</th>
              <th scope="col">Book Name</th>
              <th scope="col">Author Name</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="issue in issues" :key="issue.id">
              <td>{{ issue.user_id }}</td>
              <td>{{ issue.book_id }}</td>
              <td>{{ issue.id }}</td>
              <td>{{ bookDetails(issue.book_id).name }}</td>
              <td>{{ bookDetails(issue.book_id).author_name }}</td>
              <td>
                <button @click="revokeBook(issue.id)" class="btn btn-danger">
                  <i class="fas fa-trash"></i> Revoke
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      books: [],
      issues: [],
    };
  },
  methods: {
    fetchBookStatus() {
      fetch('http://localhost:5000/bookstatus', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      })
        .then(response => response.json())
        .then(data => {
          this.books = data.books;
          this.issues = data.issues;
        })
        .catch(error => {
          console.error('Error fetching book status:', error);
        });
    },
    async revokeBook(id) {
      try {
        const response = await fetch(`http://localhost:5000/revoke/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          console.log(data.message);
          alert(data.message);
          this.fetchBookStatus();
        } else {
          console.log(data.error);
          alert(data.error);
        }
      } catch (error) {
        console.error('Error revoking book:', error);
      }
    },
    bookDetails(book_id) {
      return this.books.find(book => book.id === book_id) || {};
    },
  },
  mounted() {
    this.fetchBookStatus();
  },
};
</script>


<style scoped> 
*{
    margin: 0px;
}
#outer_div, #inner_div{
    border: 2px solid black;
}
#inner_div{
    width: 80%;
    margin: auto;
    height: 636px;
    padding: 10px;
}
.headings{
    margin: 3px;
    padding-left: 5px;
}
#trans-area{
    border: 2px solid black;
    height: 530px;
    width: 500px;
    margin: auto;
    margin-top: 80px;
    border-radius: 10px;
}
</style>