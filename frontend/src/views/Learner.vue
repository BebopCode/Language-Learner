<template>
  <div class="space-y-20 p-4 flex flex-col items-center">
    <div 
      v-for="(button, index) in buttons" 
      :key="index" 
      class="button-cyan" 
      @click="handleClick(button)">
      <p class="text-format">{{ button }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      buttons: []
    };
  },
  mounted() {
    axios.get('http://127.0.0.1:8000/language_api/word_data') 
      .then(response => {
        this.buttons = response.data.map(item => item.word);
      })
      .catch(error => {
        console.error("Error fetching buttons:", error);
      });
  },
  methods: {
    handleClick(buttonName) {
      alert(`${buttonName} clicked`);
    }
  }
};
</script>