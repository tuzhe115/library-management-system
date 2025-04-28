import { createRouter, createWebHistory } from "vue-router";
import BookListView from "../views/BookListView.vue";
import LoginView from "../views/LoginView.vue";
import DashBoardView from "../views/DashBoardView.vue";
import LoanView from "../views/LoanView.vue";
import ReservationView from "../views/ReservationView.vue";
import UserView from "../views/UserView.vue";
import BookDetailView from "../views/BookDetailView.vue";
import LoanDetailView from "../views/LoanDetailView.vue";
import ReservationDetailView from "../views/ReservationDetailView.vue";
import UserDetailView from "../views/UserDetailView.vue";
import StatisticsView from "../views/StatisticsView.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/dashboard", component: DashBoardView },
  { path: "/login", component: LoginView },
  { path: "/books", component: BookListView },
  { path: "/loan", component: LoanView },
  { path: "/reservation", component: ReservationView },
  { path: "/user", component: UserView },
  { path: "/books/:id", component: BookDetailView },
  { path: "/loan/:id", component: LoanDetailView },
  { path: "/reservation/:id", component: ReservationDetailView },
  { path: "/user/:id", component: UserDetailView },
  { path: "/statistics", component: StatisticsView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
