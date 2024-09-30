<template>
  <div>
    <div v-if="loggedIn" class="flex space-x-10 m-10">
      <div class="space-y-5 flex flex-col items-center">
        <button @click="logout" class="button-green">Logout</button>
        <h2 class="text-format">Welcome: {{ user.email }}, You know {{ wordsLearned.word_count }} words</h2>
        <CustomButton v-for="(buttonText, index) in words" :key="index" :reset="resetButton" :buttonClass="buttonClass"
          :activeClass="'button-green'" :parentData="parentData" @click="handleClick(buttonText)"
          @updateParent="updateParentData" :buttonData="buttonText">
        </CustomButton>

        <button class="button-green" @click="updateWords(selectedButtons)">Next</button>
        <button class="button-red" @click="clearButton()">Clear my learned words</button>
      </div>
      <div class="self-center w-1/2"> <!-- Align this content at the start (top) of the right side -->
        <p class="text-format">{{ parentData.meaning }}</p>
      </div>

    </div>

    <div v-else>
      <GoogleLogin :callback="callback" prompt auto-login />
    </div>
  </div>
</template>

<script>
import CustomButton from './CustomButton.vue';
import axios from 'axios';
import Login from './Login.vue';
import { GoogleLogin } from 'vue3-google-login';
import { decodeCredential, googleLogout } from 'vue3-google-login';
export default {
  components: {
    Login,
    CustomButton
  },
  data() {
    return {
      parentData: '',
      loggedIn: false,
      user: null,
      words: [],
      returnFromServer: null,
      selectedButtons: [],
      buttonClass: 'button-cyan',
      resetButton: false,
      wordsLearned: 0,
    };
  },
  methods: {
    wordsLearnedUpdate() {
      const token = sessionStorage.getItem('token'); // Retrieve token from local storage
      axios.get(`${import.meta.env.VITE_API_URL}/words_learned`, {
        headers: {
          'Authorization': `Bearer ${token}` // Send token in the header
        }
      })
        .then(response => {
          this.wordsLearned = response.data;
        })
        .catch(error => {
          console.error("Error fetching number of words learned", error);
        });
    },
    handleClick(buttonName) {
      if (this.selectedButtons.includes(buttonName)) {
        // Remove buttonName from the array if it's already selected
        this.selectedButtons = this.selectedButtons.filter(name => name !== buttonName);
        console.log('Button removed. Updated selectedButtons:', this.selectedButtons);

      } else {
        // Add buttonName to the array if it's not selected
        this.selectedButtons.push(buttonName);
        console.log('Button added. Updated selectedButtons:', this.selectedButtons);
      }

      // For debugging: see the updated array
    },
    updateParentData(newData) {
      this.parentData = newData;
    },
    logout() {
      googleLogout()
      this.loggedIn = false
    },
    async clearButton() {
      const token = sessionStorage.getItem('token'); // Retrieve token from sessionStorage
      if (!token) {
        console.error("Token not found");
        return;
      }

      try {
        const response = await axios.delete(`${import.meta.env.VITE_API_URL}/clear_user_data/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        // Handle successful response
        console.log(response.data);

        // Fetch the buttons only after the request completes
        this.fetchButtons();
        this.selectedButtons = []
        this.resetButton = true; // Trigger the reset
        this.$nextTick(() => {
          this.resetButton = false; // Reset the `resetButton` flag after it has been processed
        });
      } catch (error) {
        console.error("Error clearing user data:", error);
      }
    },
    async sendTokenToBackend(token) {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/email/`, {
          id_token: token
        }, {
          headers: {
            'Authorization': `Bearer ${token}` // Send token in Authorization header
          }
        });

        // Handle the response from the backend
        console.log("Backend response:", response.data);
        return response.data; // Return the data from the backend
      } catch (error) {
        console.error("Error sending token to backend:", error);
      }
    },
    callback(response) {
      const token = response.credential;
      console.log("logged in");
      this.loggedIn = true;
      this.user = decodeCredential(token); // Decode the token
      console.log(this.user);
      sessionStorage.setItem('token', token);
      console.log(token) // Store the token after login
      // Call the sendTokenToBackend method and await the result
      this.sendTokenToBackend(token).then(serverResponse => {
        this.returnFromServer = serverResponse; // Set the return from the backend

        // Fetch the buttons after successful login
        this.fetchButtons(); // Call the method to fetch buttons
      });
    },
    fetchButtons() {
      const token = sessionStorage.getItem('token'); // Retrieve token from local storage
      axios.get(`${import.meta.env.VITE_API_URL}/word_data`, {
        headers: {
          'Authorization': `Bearer ${token}` // Send token in the header
        }
      })
        .then(response => {
          this.words = response.data.map(item => item.word);
          this.wordsLearnedUpdate();
        })
        .catch(error => {
          console.error("Error fetching buttons:", error);
        });
      this.parentData = '';
    },
    updateWords() {
      if (this.selectedButtons.length !== 0) {

        const token = sessionStorage.getItem('token'); // Retrieve token from local storage

        axios.post(`${import.meta.env.VITE_API_URL}/word_update/`, {
          words: this.selectedButtons // Send the array of strings
        }, {
          headers: {
            'Authorization': `Bearer ${token}` // Send token in the header
          }
        })
          .then(response => {
            console.log("Words updated successfully:", response.data);
          })
          .catch(error => {
            console.error("Error updating words:", error);
          });
        this.fetchButtons()
        this.selectedButtons = []
      } else {
        this.fetchButtons();
      }

      this.selectedButtons = []
      this.resetButton = true; // Trigger the reset
      this.$nextTick(() => {
        this.resetButton = false; // Reset the `resetButton` flag after it has been processed
      });
    },


  },

};
</script>