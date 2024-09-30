<template>
    <div id="outer_div">
      <div id="inner_div">
        <NavBar/>   
        <div id="trans-table">
          <h2 class="headings">Books of Section {{ section.name }}</h2>
          <div v-if="books.length > 0">
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">Book Id</th>
                  <th scope="col">Book Name</th>
                  <th scope="col">Author's Name</th>
                  <th scope="col">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="book in books" :key="book.id">
                  <td>{{ book.id }}</td>
                  <td>{{ book.name }}</td>
                  <td>{{ book.author_name }}</td>
                  <td>
                    <router-link v-if="this.is_librarian" :to="{ name: 'updateBook', params: { id: book.id } }" class="btn btn-primary"style="margin-right: 0.5cm;">Update</router-link>
                    <button v-if="this.is_librarian" @click="deleteBook(book.id)" class="btn btn-danger" >Delete</button>
                  </td>
                </tr>
              </tbody>    
            </table>
          </div>
          <div v-else>
            <p>No books found.</p>
          </div><br>
          <router-link :to="{ name: 'addBook', params: { sectionId: section.id } }" class="btn btn-primary" >
            <i class="fas fa-plus"></i> Add
          </router-link>
          <div style="text-align: right; margin-top: 150px;">
            <router-link to="/sections" class="btn btn-primary">
              Back
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>



  
  <script>
import NavBar from '@/components/NavBar.vue';
import userMixin from '@/mixins/userMixin';

export default {
  name: 'SectionBooks',
  components: {
    NavBar
  },
  mixins: [userMixin],
  data() {
    return {
      section: {},
      books: []
    };
  },
  created() {
    this.fetchSectionAndBooks();
  },
  methods: {
    async fetchSectionAndBooks() {
      const sectionId = this.$route.params.id;
      try {
        const sectionResponse = await fetch(`http://127.0.0.1:5000/section/${sectionId}`);
        const sectionData = await sectionResponse.json();
        this.section = sectionData;

        const booksResponse = await fetch(`http://127.0.0.1:5000/section/${sectionId}/book`);
        const booksData = await booksResponse.json();
        this.books = booksData;
      } catch (error) {
        console.log(error);
      }
    },
    async deleteBook(id) {
            try{
                const response = await fetch(`http://localhost:5000/book/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    console.log(data.message);
                    alert(data.message);
                    this.fetchSectionAndBooks();
                } else {
                    console.log(data.error);
                    alert(data.error);
                }
            }catch(error){
                console.error(error);s
            }
        },
  }
}
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
  