import { createWebHistory, createRouter } from "vue-router";
import Learner from "../views/Learner.vue";
import Callback from "../views/Callback.vue";


const routes = [
  {
    path: "/",
    name: "Learner",
    component: Learner,
  },
  {
    path: "/auth/google/callback",
    name: "Callback",
    component: Callback,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;