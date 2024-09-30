<template>
  <div>
    <h2>Task Manager</h2>
    <form @submit.prevent="addTask">
      <input v-model="task.title" placeholder="Task Title" required>
      <input type="datetime-local" v-model="task.deadline" required>
      <textarea v-model="task.description" placeholder="Description"></textarea>
      <button type="submit">Add Task</button>
    </form>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }} - {{ task.deadline }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      task: {
        title: '',
        description: '',
        deadline: ''
      },
      tasks: []
    };
  },
  methods: {
    addTask() {
      // Post task to Flask API
      fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.task)
      }).then(response => response.json()).then(data => {
        this.tasks.push({...this.task, id: data.id});
        this.task = {title: '', description: '', deadline: ''}; // Reset form
      });
    }
  },
  mounted() {
    // Fetch tasks from the backend API
    fetch('/api/tasks').then(res => res.json()).then(data => this.tasks = data);
  }
};
</script>
