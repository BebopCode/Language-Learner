<!-- src/views/Callback.vue -->
<template>
    <div>
      <h1>Processing Authentication...</h1>
    </div>
  </template>
  
  <script>
  export default {
    async mounted() {
      try {
        // Wait for the authentication response from Google
        const googleUser = await this.$gAuth.getAuthCode();
  
        // You can retrieve user information from googleUser
        const profile = googleUser.getBasicProfile();
        console.log('ID:', profile.getId());
        console.log('Name:', profile.getName());
        console.log('Email:', profile.getEmail());
        console.log('ID Token:', googleUser.getAuthResponse().id_token);
  
        // Now that you're authenticated, you can redirect to a different route
        this.$router.push({ name: 'Learner' });
      } catch (error) {
        console.error('Error during Google Authentication:', error);
        this.$router.push({ name: 'Learner' }); // Redirect on error
      }
    },
  };
  </script>
  