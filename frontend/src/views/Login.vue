<template>
    <div>
      <button @click="loginWithGoogle">Login with Google</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      loginWithGoogle() {
        this.$gAuth.signIn().then(googleUser => {
          const profile = googleUser.getBasicProfile();
          console.log('ID: ' + profile.getId());
          console.log('Name: ' + profile.getName());
          console.log('Image URL: ' + profile.getImageUrl());
          console.log('Email: ' + profile.getEmail());
  
          const idToken = googleUser.getAuthResponse().id_token;
          console.log('ID Token: ' + idToken);
  
          // Emit the token or user profile data to the parent
          this.$emit('login-success', { profile, idToken });
        }).catch(error => {
          console.log('Login failed: ', error);
          this.$emit('login-failure', error);
        });
      }
    }
  };
  </script>
  