import { createWebHistory, createRouter } from "vue-router";
import Learner from "../views/Learner.vue";
import Home from "../views/Home.vue";


const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path:"/learner",
    name:"Learner",
    component:Learner,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;