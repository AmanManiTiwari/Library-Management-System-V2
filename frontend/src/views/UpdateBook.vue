<template>
    <div id="outer_div">
        <div id="inner_div">
            <NavBar/>
            <div id="trans-area" style="height: 450px; margin-top: 50px;">
                <h2 class="headings">Update Book</h2>
                <form class="row g-3 p-2"@submit.prevent="updateBook">
                    
                    <div class="mb-3">
                        <label for="name" class="form-label">Book Name:</label>
                        <input type="text" v-model="name" value="{{book.name}}" class="form-control" id="name" required>

                    </div>
                    <div class="mb-3">
                        <label for="author_name" class="form-label">Author Name:</label>
                        <input type="text" v-model="author_name" value="{{book.author_name}}" class="form-control" id="author_name" required>

                    </div>
                    <div class="form-group">
                            <label for="content" class="form-label">Content:</label>
                            <textarea v-model="content" 
                                      id="content" 
                                      class="form-control"
                                      required></textarea>
                        </div><br><br>
                        <div class="form-group">
                            <label for="sectionId" class="form-label">Section ID:</label>
                            <input type="number" 
                                   v-model="sectionId" 
                                   id="sectionId" 
                                   class="form-control"
                                   required>
                        </div>
                    <br><br><br><br>
                    <div id="create-btn">
                        <button type="submit" class="btn btn-success">
                            Update Book Details
                        </button>
                    </div>
                </form>
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
                name: '',
                author_name: '',
                content: '',
                sectionId: null
            }
        },
        mounted() {
            const bookId = this.$route.params.id;
            this.fetchBookDetails(bookId);
        },
        methods: {
            async fetchBookDetails(bookId) {
                try {
                    const response = await fetch(`http://localhost:5000/book/${bookId}`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        }
                    });
                    const data = await response.json();
                    console.log("data", data);
                    if (response.ok) {
                        this.name = data.name;
                        this.author_name = data.author_name;
                        this.content = data.content;
                        this.sectionId = data.section_id;
                    } else {
                        console.log(data.error);
                        alert(data.error);
                    }
                } catch (error) {
                    console.error(error);
                }
            },
            async updateBook() {
                const bookId = this.$route.params.id;
                try {
                    const response = await fetch(`http://localhost:5000/book/update/${bookId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        },
                        body: JSON.stringify({
                            name: this.name,
                            author_name: this.author_name,
                            content: this.content,
                            section_id: this.sectionId
                        })
                    });
                    const data = await response.json();
                    if (response.ok) {
                        console.log(data.message);
                        alert(data.message);
                        this.$router.push(`/section/${this.sectionId}/book`);
                    } else {
                        console.log(data.error);
                        alert(data.error);
                    }
                } catch (error) {
                    console.error(error);
                }
            }
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
    height: 603px;
    padding: 10px;
}
#form_div{
    border: 1px solid grey;
    width: 370px;
    height: 350px;
    margin: auto;
    margin-top: 100px;
    padding: 5px;
    border-radius: 5px;
}
.headings{
    margin: 3px;
    padding-left: 5px;
}
#trans-table{
    height: 600px;
}
.headings{
    margin: 3px;
    padding-left: 5px;
    text-align: center;
}
#trans-area{
    border: 2px solid black;
    height: 315px;
    width: 500px;
    margin: auto;
    margin-top: 151px;
    border-radius: 10px;
}


#create-btn{
    text-align: right;
}

#t-details{
    padding: 25px 0px;
    text-align: center;
}
.amt{
    width:275px;
    margin:auto;
}
#create-btn{
    text-align: center;
}
</style>