<template>
  <div class="p-4">
    <router-view />
  </div>
</template>

<script>
import BookListView from "./views/BookListView.vue";
import LoginView from "./views/LoginView.vue";
import DashBoardView from "./views/DashBoardView.vue";
import LoanView from "./views/LoanView.vue";
import ReservationView from "./views/ReservationView.vue";
import UserView from "./views/UserView.vue";
import BookDetailView from "./views/BookDetailView.vue";
import LoanDetailView from "./views/LoanDetailView.vue";
import ReservationDetailView from "./views/ReservationDetailView.vue";
import UserDetailView from "./views/UserDetailView.vue";
import StatisticsView from "./views/StatisticsView.vue";

export default {
  components: {
    DashBoardView,
    LoginView,
    BookListView,
    LoanView,
    ReservationView,
    UserView,
    BookDetailView,
    LoanDetailView,
    ReservationDetailView,
    UserDetailView,
    StatisticsView,
  },
};
</script>
