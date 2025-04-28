<template>
  <div class="detail-background">
    <div class="page-container">
      <el-card v-if="reservation">
        <el-button
          type="primary"
          icon="ArrowLeft"
          class="back-button"
          @click="goBack"
          style="margin-bottom: 20px"
        >
          Back to Reservations
        </el-button>
        <p><strong>ID:</strong> {{ reservation.id }}</p>
        <p><strong>User:</strong> {{ reservation.user_name }}</p>
        <p><strong>Book:</strong> {{ reservation.book_title }}</p>
        <p>
          <strong>Reservation Time:</strong> {{ reservation.reservation_time }}
        </p>
        <p><strong>Due Time:</strong> {{ reservation.r_due_time }}</p>
        <p><strong>Status:</strong> {{ reservation.reservation_status }}</p>

        <el-button type="success" class="edit-button" @click="openEditDialog"
          >Edit</el-button
        >
      </el-card>

      <el-dialog title="Edit Reservation" v-model="editDialogVisible">
        <el-form :model="editReservation" label-width="120px">
          <el-form-item label="Status">
            <el-select
              v-model="editReservation.reservation_status"
              placeholder="Select status"
            >
              <el-option label="active" value="active" />
              <el-option label="cancelled" value="cancelled" />
              <el-option label="expired" value="expired" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="submitEdit">Save</el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from "../utils/axios.js";

export default {
  name: "ReservationDetailView",
  data() {
    return {
      reservation: null,
      editReservation: {},
      editDialogVisible: false,
    };
  },
  methods: {
    goBack() {
      this.$router.push("/reservation");
    },
    async fetchReservation() {
      const id = this.$route.params.id;
      try {
        const res = await axios.get(
          `http://localhost:8000/api/reservations/${id}/`
        );
        this.reservation = res.data;
        this.editReservation = { ...res.data };
      } catch (err) {
        console.error("Failed to fetch reservation:", err);
      }
    },
    openEditDialog() {
      this.editDialogVisible = true;
    },
    async submitEdit() {
      try {
        const edit = {
          book: this.editReservation.book,
          user: this.editReservation.user,
          reservation_status: this.editReservation.reservation_status,
        };

        await axios.patch(
          `http://localhost:8000/api/reservations/${this.reservation.id}/`,
          edit
        );
        this.editDialogVisible = false;
        this.fetchReservation();
      } catch (err) {
        console.error("Failed to update reservation:", err);
      }
    },
  },
  mounted() {
    this.fetchReservation();
  },
};
</script>

<style scoped>
.page-container {
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.el-card {
  width: 600px;
  position: relative;
  padding-top: 20px;
}

.el-card p {
  margin: 8px 0;
  text-align: left;
}

.edit-button {
  position: absolute;
  top: 12px;
  right: 12px;
}

.back-button {
  position: absolute;
  top: 12px;
  left: 12px;
}

.detail-background {
  background-image: url("/images/Journal.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  padding: 40px 0;
}
</style>
