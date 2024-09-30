<template>
  <div class="flex items-center space-x-2" @click="handleClick"> <!-- space-x-2 adds some spacing between buttons -->

    <button :class="computedClass" >
      <slot></slot> <!-- Content on the left -->
      {{  buttonData }}
    </button>
    <button class="button-inside" @click="getMeaning($event)">?</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  props: {
    buttonClass: {
      type: String,
      default: 'button-cyan', // Default class for unclicked state
    },
    activeClass: {
      type: String,
      default: 'button-green', // Class to apply when the button is clicked
    },
    reset: { // This prop will be passed from the parent to trigger the reset
      type: Boolean,
      default: false
    },
    buttonData: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      clicked: false, // State to track if the button is clicked
    };
  },
  computed: {
    computedClass() {
      // Returns the appropriate class based on the clicked state
      return this.clicked ? this.activeClass : this.buttonClass;
    },
  },
  watch: {
    // Watch the 'reset' prop for changes and reset the button state if triggered
    reset(newValue) {
      if (newValue) {
        this.clicked = false; // Reset the clicked state to false
      }
    }
  },
  methods: {
    handleClick(event) {
      this.clicked = !this.clicked; // Toggle the clicked state
      //this.$emit('click', event);   // Emit the click event to the parent
    },
    getMeaning(event) {
      const token = sessionStorage.getItem('token'); // Retrieve token from local storage

      axios.post(`${import.meta.env.VITE_API_URL}/word_meaning/`, {
        word: this.buttonData // Send the array of strings
      }, {
        headers: {
          'Authorization': `Bearer ${token}` // Send token in the header
        }
      })
        .then(response => {
          console.log("Words updated successfully:", response.data);
          this.$emit('updateParent', response.data);
        })
        .catch(error => {
          console.error("Error updating words:", error);
        });
        event.stopPropagation();
      //console.log(response)
    }
  },
};
</script>

<style scoped>
/* Add styles for button-cyan, button-green, or others here */
</style>
