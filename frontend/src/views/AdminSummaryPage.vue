<template>
    <div id="outer_div">
      <div id="inner_div">
        <NavBar />
        <h1>Library Statistics</h1>
        <div id="trans-table">
          <div v-if="stats">
            <div class="col-md-12">
              <div class="row mt-4">
                <div class="col-md-6">
                  <h5>Summary</h5>
                  <img :src="'http://localhost:5000/stats?timestamp=' + new Date().getTime()" alt="**" class="img-fluid">
                </div>
                <div class="col-md-6">
                  <h5>Books Issued from different Sections</h5>
                  <img :src="'http://localhost:5000/issue-section-pie-chart?timestamp=' + new Date().getTime()" alt="bar graph" class="img-fluid">
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p>Loading...</p>
          </div>
        </div>
        <!-- <a href="http://localhost:5000/download-issue-csv" class="btn btn-primary mt-4">Download CSV</a> -->
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
        stats: null
      };
    },
    created() {
      this.fetchStats();
    },
    methods: {
      async fetchStats() {
        try {
          const response = await fetch('http://localhost:5000/book-issued-history-report');
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          this.stats = data;
        } catch (error) {
          console.error('Error fetching stats:', error);
        }
      }
    },
    watch: {
      $route(to, from) {
        if (to.name === 'adminStats') {
          this.fetchStats();
        }
      }
    }
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
    height: 603px;
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




  