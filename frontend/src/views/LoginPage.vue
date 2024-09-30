<template>
    <div id="outer_div">
        <div id="inner_div">
            <NavBar />
            <div id="form_div" style="height: 410px;">
                <h1>Login</h1>
                <form @submit.prevent="userLogin" >
                    <div class="mb-3">
                        <label for="enter_name" class="form-label">Name</label>
                        <input type="text" v-model="name" class="form-control" id="enter_name" placeholder="abc" required>
                    </div>
                        <div class="mb-3">
                            <label for="enter_email" class="form-label">Email</label>
                            <input type="email" v-model="email" class="form-control" id="enter_email" placeholder="abc@gmail.com" required>
                        </div>
                        <div class="mb-3">
                            <label for="enter_password" class="form-label">Password</label>
                            <input type="password" v-model="password" class="form-control" id="enter_password" required>
                    </div><br>
                    <div style="text-align: center;">
                        <input type="submit" value="Login" class="btn-warning"><br>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>



<script>
    import NavBar from '@/components/NavBar.vue';
    import userMixin from '@/mixins/userMixin';
    export default{
        components: {
        NavBar
    },
    mixins: [userMixin],
        data() {
            return {
                name: '',
                email: '',
                password:'',
                librarian:false
    }
        },
        methods: {
        async userLogin() {
            try{
                const response = await fetch('http://localhost:5000/userlogin', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        
                        name: this.name,
                        email: this.email,
                        password: this.password,
                    }),
                });
                const data = await response.json();
                if(response.ok){
                    console.log(data.message);
                    localStorage.setItem('access_token', data.access_token)
                    console.log(data)
                    alert(data.message);
                    this.librarian=data.is_librarian

                    if (this.librarian) {
                        console.log("redirecting to section")
                        this.$router.push('/sections');
                    }else {
                        console.log("redirecting to home")
                        this.$router.push('/home');
                    }
                }
                else{
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
    height: 636px;
    padding: 10px;
}
#form_div{
    border: 1px solid grey;
    width: 370px;
    height: 410px;
    margin: auto;
    margin-top: 100px;
    padding: 5px;
    border-radius: 5px;
}
h1{
    text-align: center;
}
</style>
