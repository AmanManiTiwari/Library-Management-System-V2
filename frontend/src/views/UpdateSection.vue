<template>
    <div id="outer_div">
        <div id="inner_div">
            <NavBar/>
            <div class="container-sm">
                <div id="trans-area">
                    <h2 class="headings">Update Section</h2>
                    <form class="row g-3 p-2" @submit.prevent="updateSection">
                        <div class="form-group">
                            <label for="sectionName" class="form-label">Section Name:</label>
                            <input type="text" 
                            v-model="name" 
                            id="sectionName" 
                            class="form-control"
                            required>
                        </div>
                       <br><br><br><br>
                        <button type="submit" class="btn btn-success">
                            Update
                        </button>
                    </form>
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
                name: ''
            }
        },
        mounted() {
            const sectionId = this.$route.params.id;
            this.fetchSectionDetails(sectionId);
        },
        methods: {
            async fetchSectionDetails(sectionId) {
                try {
                    const response = await fetch(`http://localhost:5000/section/${sectionId}`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        }
                    });
                    const data = await response.json();
                    console.log("data",data)
                    if (response.ok) {
                        this.name = data.name;
            
                    } else {
                        console.log(data.error);
                        alert(data.error);
                    }
                } catch (error) {
                    console.error(error);
                }
            },
            async updateSection() {
                const sectionId = this.$route.params.id;
                try {
                    const response = await fetch(`http://localhost:5000/section/update/${sectionId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        },
                        body: JSON.stringify({
                            name: this.name
                        })
                    });
                    const data = await response.json();
                    if (response.ok) {
                        console.log(data.message);
                        alert(data.message);
                        this.$router.push('/sections');
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
    height:600px;
}
.headings{
    margin: 3px;
    padding-left: 5px;
    text-align: center;
}
#trans-area{
    border: 2px solid black;
    height: 215px;
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