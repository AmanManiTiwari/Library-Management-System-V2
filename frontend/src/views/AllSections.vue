<template>
    <div id="outer_div">
        <div id="inner_div">
            <NavBar class="navbar navbar-expand-lg navbar-light bg-light" />
            <div class="container mt-5">
        <div class="center"><h1>All Sections</h1>
        <div v-if="sections.length > 0">
        <table class="table table-success table-striped">
            <thead>
                <tr>
                    <th>Section ID</th>
                    <th>Section Name</th>
                    <th> Number of Books </th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="section in sections" :key="section.id">
                    <td>{{ section.id }}</td>
                    <td>{{ section.name }}</td>
                    <td> {{ section.book_count }}</td>
                    <td >
                        <router-link v-if="this.is_librarian" :to="{ name: 'viewSection', params: { id: section.id } }" class="btn btn-primary"style="margin-right: 0.25cm;">View</router-link>
                        <router-link v-if="this.is_librarian" :to="{ name: 'updateSection', params: { id: section.id } }" class="btn btn-primary"style="margin-right: 0.25cm;">Update</router-link>
                        <button v-if="this.is_librarian" @click="deleteSection(section.id)" class="btn btn-danger">Delete</button>
                    </td>
                </tr>
            </tbody>  
            </table>
            </div>
            <div v-else>
                <p>No sections found.</p>
            </div><br>
            <router-link  v-if="this.is_librarian" :to="{ name: 'createSection' }" class="btn btn-primary">Create a new Section</router-link>
    </div>   </div> 
            
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import userMixin from '@/mixins/userMixin';
export default {
    components: {
        NavBar
    },
    mixins: [userMixin],
    data() {
        return {
            sections: [],
        }
    },
    async created() {
        await this.getAllSections();
    },
    methods: {
        async getAllSections() {
            try {
                const response = await fetch('http://localhost:5000/sections', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();
                this.sections = data;
            } catch (error) {
                console.error(error);
            }
        },
        async deleteSection(id) {
            try{
                const response = await fetch(`http://localhost:5000/section/delete/${id}`, {
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
                    this.getAllSections();
                } else {
                    console.log(data.error);
                    alert(data.error);
                }
            }catch(error){
                console.error(error);s
            }
        },
        viewSection(id){
        console.log('VIEWING Section', id);
        this.$router.push('/section/:id/book')
        },

    }
}
</script>

<style scoped>
/* .center {
  margin: auto;
  width: 50%;
  border: 3px solid green;
  padding: 10px;
} */

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