<template>
  <div id="outer_div">
    <div id="inner_div">
      <NavBar  />
      <div class="container-fluid">
        <div class="container mt-3">
           <div class="form-group">
             <input 
              type="text" 
              v-model="search" 
              class="form-control" 
              placeholder="Search for books">
          </div>  
          <div v-for="section in filteredSections" :key="section.id" class="mt-3">
            <h4><i>{{ section.name }}</i></h4>
            <div class="row">
              <div v-for="book in section.books" :key="book.id" class="col-md-3 mb-3">
                <div class="card book-card" style="width: 100%;">        
                  <img src="data:image/jpeg;base64,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" class="card-img-top" alt="image">
                  <div class="card-body">
                    <h5 class="card-title">{{ book.name }}</h5>
                    <p class="card-text">Author: {{ book.author_name }} </p>  
                    <button @click="requestBook(book.id)" class="btn btn-primary btn-block">
                      Request Book
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  components: {
    NavBar
  },
  data() {
    return {
      sections: [],
      search: ''
    }
  },
  async created() {
    this.getdata()
  },
  computed: {
    filteredSections() {
      if (!this.search) {
        return this.sections;
      }
      const searchTerm = this.search.toLowerCase();
      return this.sections.map(section => {
        const filteredBooks = section.books.filter(book => 
          book.name.toLowerCase().includes(searchTerm)
        );
        return { ...section, books: filteredBooks };
      }).filter(section => section.books.length > 0);
    }
  },
  methods: {
    async getdata() {
      try {
        const response = await fetch('http://localhost:5000/getallbookinfo', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.sections = data;
          console.log(this.section);
          console.log("data fetched");
        } else {
          console.log("data not fetched");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async requestBook(bookId) {
      try {
        const response = await fetch(`http://localhost:5000/request/${bookId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({
            book_id: bookId
          })
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Error requesting book:", error);
      }
    }
  }
};
</script>

<style scoped>
/* *{
    margin: 0px;
} */
/* #outer_div, #inner_div{
    border: 2px solid black;
} */
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
.card-container {
  padding: 15px
}
</style>
