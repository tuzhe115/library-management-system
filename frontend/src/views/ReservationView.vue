<template>
  <div class="page-container">
    <div class="button-bar">
      <el-button
        type="primary"
        icon="ArrowLeft"
        @click="goToDashboard"
        style="margin-bottom: 20px"
      >
        Back to Overview
      </el-button>
      <el-button
        type="success"
        size="default"
        @click="openAddDialog"
        style="margin-bottom: 20px; float: right"
      >
        Add Reservation
      </el-button>
    </div>

    <el-dialog
      v-model="addDialogVisible"
      title="Add New Reservation"
      width="600px"
    >
      <el-form :model="newReservation" label-width="140px">
        <el-form-item label="Book">
          <el-select
            v-model="newReservation.book"
            placeholder="Search Book"
            filterable
            remote
            reserve-keyword
            :remote-method="searchBooks"
            :loading="bookLoading"
          >
            <el-option
              v-for="b in books"
              :key="b.id"
              :label="b.title"
              :value="b.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="User">
          <el-select
            v-model="newReservation.user"
            placeholder="Search User"
            filterable
            remote
            reserve-keyword
            :remote-method="searchUsers"
            :loading="userLoading"
          >
            <el-option
              v-for="u in users"
              :key="u.id"
              :label="u.name"
              :value="u.id"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="addDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitNewReservation"
          >Submit</el-button
        >
      </template>
    </el-dialog>

    <h1 class="page-title">Reservation Management</h1>
    <div class="search-bar">
      <el-select
        v-model="searchField"
        placeholder="Select Field"
        style="width: 180px"
      >
        <el-option
          v-for="opt in searchOptions"
          :key="opt.value"
          :label="opt.label"
          :value="opt.value"
        />
      </el-select>
      <el-input
        v-model="searchKeyword"
        placeholder="Enter keyword"
        style="width: 240px"
        @keyup.enter.native="fetchReservations"
        clearable
      />
      <el-button type="primary" icon="Search" @click="fetchReservations"
        >Search</el-button
      >
    </div>
    <el-table
      :data="reservations"
      stripe
      style="width: 100%"
      v-loading="loading"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="book_title" label="Book" />
      <el-table-column prop="user_name" label="User" />
      <el-table-column prop="reservation_time" label="Reservation Time" />
      <el-table-column prop="r_due_time" label="Reservation Due Time" />
      <el-table-column prop="reservation_status" label="Reservation Status" />
      <el-table-column label="Actions">
        <template #default="scope">
          <el-button
            size="small"
            type="primary"
            @click="goToDetail(scope.row.id)"
            >Details</el-button
          >
          <el-button
            v-if="
              scope.row.reservation_status !== 'cancelled' &&
              scope.row.reservation_status !== 'expired'
            "
            size="small"
            type="warning"
            @click="cancelReservation(scope.row)"
          >
            Cancel
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(scope.row.id)"
          >
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "../utils/axios.js";
import dayjs from "dayjs";

export default {
  name: "ReservationView",
  data() {
    return {
      reservations: [],
      users: [],
      books: [],
      loading: false,
      userLoading: false,
      bookLoading: false,
      addDialogVisible: false,
      newReservation: {
        book: "",
        user: "",
        reservation_status: "",
      },
      searchField: "book_title",
      searchKeyword: "",
      searchOptions: [
        { label: "Book", value: "book_title" },
        { label: "User", value: "user_name" },
        { label: "Reservation Status", value: "reservation_status" },
      ],
    };
  },
  mounted() {
    this.fetchReservations();
  },
  methods: {
    goToDashboard() {
      this.$router.push("/dashboard");
    },
    goToDetail(reservationId) {
      this.$router.push(`/reservation/${reservationId}`);
    },
    async fetchReservations() {
      this.loading = true;
      try {
        const params = {};
        if (this.searchKeyword && this.searchField) {
          params.keyword = this.searchKeyword;
          params.field = this.searchField;
        }
        const response = await axios.get(
          "http://localhost:8000/api/reservations/",
          {
            params,
          }
        );
        this.reservations = response.data.results || response.data;
      } catch (err) {
        console.error("Failed to fetch reservations:", err);
      } finally {
        this.loading = false;
      }
    },

    openAddDialog() {
      this.addDialogVisible = true;
    },
    async submitNewReservation() {
      try {
        this.newReservation.reservation_status = "Active";
        await axios.post(
          "http://localhost:8000/api/reservations/",
          this.newReservation
        );
        this.addDialogVisible = false;
        this.$message.success("Reservations added successfully");
        this.fetchReservations();
        this.resetForm();
      } catch (err) {
        const errorData = err?.response?.data;
        let message = "Failed to add reservation";
        if (errorData && typeof errorData === "object") {
          message = Object.values(errorData).flat().join(", ");
        }
        this.$message.error(message);
        console.error("Failed to add reservation:", err.response?.data || err);
      }
    },
    async cancelReservation(reservation) {
      try {
        await axios.patch(
          `http://localhost:8000/api/reservations/${reservation.id}/`,
          {
            book: reservation.book,
            user: reservation.user,
            reservation_status: "cancelled",
          }
        );
        this.$message.success("Reservations cancelled successfully");
        this.fetchReservations();
      } catch (err) {
        console.error("Cancel failed", err);
      }
    },
    resetForm() {
      this.newReservation = {
        book: "",
        user: "",
        reservation_status: "",
      };
    },
    async handleDelete(id) {
      try {
        await axios.delete(`http://localhost:8000/api/reservations/${id}/`);
        this.$message.success("Reservation deleted successfully!");
        this.fetchReservations();
      } catch (err) {
        console.error("Failed to delete reservation:", err);
        this.$message.error("Failed to delete reservation");
      }
    },
    async searchUsers(query) {
      if (!query) return;
      this.userLoading = true;
      try {
        const res = await axios.get("http://localhost:8000/api/users/", {
          params: { search: query },
        });
        this.users = res.data.results || res.data;
      } finally {
        this.userLoading = false;
      }
    },

    async searchBooks(query) {
      if (!query) return;
      this.bookLoading = true;
      try {
        const res = await axios.get("http://localhost:8000/api/books/", {
          params: { search: query },
        });
        this.books = res.data.results || res.data;
      } finally {
        this.bookLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.page-container {
  padding: 40px;
}
.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.el-button {
  margin-left: 5px;
}
</style>
