<template>
  <button :class="computedClass" @click="handleClick">
    <slot></slot>
  </button>
</template>

<script>
export default {
  props: {
    buttonClass: {
      type: String,
      default: 'button-cyan', // Default class for unclicked state
    },
    activeClass: {
      type: String,
      default: 'button-green', // Class to apply when the button is clicked
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
      return this.buttonClass;
    },
  },
  methods: {
    handleClick(event) {
      this.buttonClass = 'button-green' // Toggle the clicked state
     // this.$emit('click', event);   // Emit the click event to the parent
    },
  },
};
</script>

<style scoped>
/* Add styles for button-cyan, button-green, or others here */
</style>
