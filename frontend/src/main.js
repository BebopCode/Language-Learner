import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router';// Import the Google OAuth plugin
import vue3GoogleLogin from 'vue3-google-login';
const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const app = createApp(App);

app.use(router);
app.use(vue3GoogleLogin,{
    clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID,
})
app.mount('#app');
