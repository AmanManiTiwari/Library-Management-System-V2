<template>
    <div id="outer_div">
      <div id="inner_div">
        <NavBar />
        <h2 class="headings">Book Requested</h2>
        <!-- <div id="trans-table"> -->
          <table class="table table-success table-striped">
            <thead>
              <tr>
                <th scope="col">Request Id</th>
                <th scope="col">User Id</th>
                <th scope="col">Book Id</th>
                <th scope="col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requests" :key="request.id">
                <td>{{ request.id }}</td>
                <td>{{ request.user_id }}</td>
                <td>{{ request.book_id }}</td>
                <td>
                <button @click="rejectRequest(request.id)" class="btn btn-danger" style="margin-right: 0.5cm;">
                  Reject
                </button>
                <button @click="acceptRequest(request.id)" class="btn btn-success">
                  Accept
                </button>
              </td>
              </tr>
            </tbody>
          </table>
        <!-- </div> -->
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
        requests: []
      };
    },
    created() {
      this.fetchRequests();
    },
    methods: {
      fetchRequests() {
        fetch('http://localhost:5000/bookrequested')
          .then(response => response.json())
          .then(data => {
            this.requests = data;
          })
          .catch(error => {
            console.error("There was an error fetching the requests:", error);
          });
      },
      async rejectRequest(id) {
            try{
                const response = await fetch(`http://localhost:5000/reject/${id}`, {
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
                    this.fetchRequests();
                } else {
                    console.log(data.error);
                    alert(data.error);
                }
            }catch(error){
                console.error(error);s
            }
        },
        async acceptRequest(id) {
            try{
                const response = await fetch(`http://localhost:5000/accept/${id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    console.log(data.message);
                    alert(data.message);
                    this.fetchRequests();
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
  * {
    margin: 0px;
  }
  #outer_div, #inner_div {
    border: 2px solid black;
  }
  #inner_div {
    width: 80%;
    margin: auto;
    height: 636px;
    padding: 10px;
  }
  .headings {
    margin: 3px;
    padding-left: 5px;
  }
  #trans-table {
    border: 2px solid black;
    height: 530px;
    width: 500px;
    margin: auto;
    margin-top: 80px;
    border-radius: 10px;
  }
  </style>
 