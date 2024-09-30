<template>
  <div id="outer_div">
    <div id="inner_div">
      <NavBar />
      <div id="trans-area" style="height: 470px; margin-top: 70px;">
        <h2 class="headings">Feedback</h2>
        <form class="row g-3 p-2" @submit.prevent="submitFeedback">
          <div class="mb-3">
            <label for="user_id" class="form-label">User Id:</label>
            <input
              type="text"
              v-model="user_id"
              class="form-control"
              id="user_id"
              readonly
            />
          </div>
          <div class="mb-3">
            <label for="book_id" class="form-label">Book Id:</label>
            <input
              type="text"
              v-model="book_id"
              class="form-control"
              id="book_id"
              readonly
            />
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">Your Opinion:</label>
            <textarea
              class="form-control"
              v-model="content"
              id="content"
              rows="3"
            ></textarea>
          </div>
          <div id="create-btn">
            <button type="submit" class="btn btn-primary mb-3">Submit</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import userMixin from "@/mixins/userMixin";

export default {
  components: {
    NavBar,
  },
  mixins: [userMixin],
  data() {
    return {
      user_id: "",
      book_id: this.$route.params.id,
      content: "",
    };
  },
  watch: {
    user(newUser) {
      if (newUser) {
        this.user_id = newUser.id;
      }
    }
  },
  created() {
    if (this.user) {
      this.user_id = this.user.id;
    }
  },
  methods: {
    async submitFeedback() {
      if (!this.user_id || !this.book_id || !this.content) {
        alert("Please fill out all details");
        return;
      }
      try {
        const response = await fetch("http://localhost:5000/submitFeedback", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            user_id: this.user_id,
            book_id: this.book_id,
            content: this.content,
          }),
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push(`/issued`);
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error(error);
        alert("An error occurred while submitting feedback");
      }
    },
  },
};
</script>

<style scoped>
* {
  margin: 0px;
}
#inner_div {
  width: 80%;
  margin: auto;
  height: 636px;
  padding: 10px;
}
#form_div {
  border: 1px solid grey;
  width: 370px;
  height: 350px;
  margin: auto;
  margin-top: 100px;
  padding: 5px;
  border-radius: 5px;
}
.headings {
  margin: 3px;
  padding-left: 5px;
  text-align: center;
}
#trans-area {
  border: 2px solid black;
  height: 315px;
  width: 500px;
  margin: auto;
  margin-top: 151px;
  border-radius: 10px;
}
#create-btn {
  text-align: right;
}
#t-details {
  padding: 25px 0px;
  text-align: center;
}
.amt {
  width: 275px;
  margin: auto;
}
#create-btn {
  text-align: center;
}
</style>
