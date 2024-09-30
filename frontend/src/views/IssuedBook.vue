<template>
  <div id="outer_div">
    <div id="inner_div">
      <NavBar />
      <h2 class="headings">Issued Books</h2>
      <table class="table table-success table-striped">
        <thead>
          <tr>
            <th scope="col">Book Id</th>
            <th scope="col">Issue Id</th>
            <th scope="col">Book Name</th>
            <th scope="col">Author Name</th>
            <th scope="col">Content</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="issue in issuedBooks" :key="issue.issue_id">
            <td>{{ issue.book_id }}</td>
            <td>{{ issue.issue_id }}</td>
            <td>{{ issue.name }}</td>
            <td>{{ issue.author_name }}</td>
            <td>{{ issue.content }}</td>
            <td>
              <button @click="returnBook(issue.issue_id)" class="btn btn-warning" style="margin-right: 0.25cm;">
                Return
              </button>
              <button @click="openFeedbackform(issue.book_id)" class="btn btn-primary" style="margin-right: 0.25cm;">
                Feedback
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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
      issuedBooks: [],
    };
  },
  created() {
    this.fetchIssuedBooks();
  },
  methods: {
    async fetchIssuedBooks() {
      try {
        const response = await fetch('http://localhost:5000/issued', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Something went wrong');
        }

        const data = await response.json();
        this.issuedBooks = data.issued_books;
      } catch (error) {
        console.error('Error fetching issued books:', error);
      }
    },
    async returnBook(id) {
      try {
        const response = await fetch(`http://localhost:5000/return/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchIssuedBooks();
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error('Error returning book:', error);
      }
    },
    openFeedbackform(book_id) {
      this.$router.push({ name: 'Feedback', params: { id: book_id } });
    },
  },
};
</script>

<style scoped>
* {
  margin: 0px;
}
#outer_div, #inner_div {
  border: 2px solid black;
}
#inner_div {
  width: 80%;
  margin: auto;
  height: 603px;
  padding: 10px;
}
.headings {
  margin: 3px;
  padding-left: 5px;
}
</style>
