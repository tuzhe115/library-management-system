<template>
  <div class="detail-background">
    <div class="page-container">
      <el-card v-if="user">
        <el-button
          type="primary"
          icon="ArrowLeft"
          class="back-button"
          @click="goBack"
          >Back</el-button
        >
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Account:</strong> {{ user.account }}</p>
        <p><strong>Password:</strong> {{ user.password }}</p>
        <p><strong>Phone:</strong> {{ user.phone }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Role:</strong> {{ user.role }}</p>
        <p><strong>Address:</strong> {{ user.address }}</p>
        <p><strong>Borrow Duration:</strong> {{ user.borrow_duration }}</p>
        <p><strong>Borrow Number:</strong> {{ user.borrow_num }}</p>
        <p>
          <strong>Reservation Duration:</strong> {{ user.reservation_duration }}
        </p>
        <p><strong>Registration Time:</strong> {{ user.registration_time }}</p>
        <el-button type="success" class="edit-button" @click="openEditDialog"
          >Edit</el-button
        >
      </el-card>

      <el-dialog v-model="editDialogVisible" title="Edit User" width="600px">
        <el-form :model="user" label-width="180px">
          <el-form-item label="Name">
            <el-input v-model="user.name" />
          </el-form-item>
          <el-form-item label="Account">
            <el-input v-model="user.account" />
          </el-form-item>
          <el-form-item label="Password">
            <el-input v-model="user.password" />
          </el-form-item>
          <el-form-item label="Phone">
            <el-input v-model="user.phone" />
          </el-form-item>
          <el-form-item label="Email">
            <el-input v-model="user.email" />
          </el-form-item>
          <el-form-item label="Role">
            <el-select
              v-model="user.role"
              placeholder="Select Role"
              @change="updateRoleValues"
            >
              <el-option label="Undergraduate" value="Undergraduate" />
              <el-option label="Postgraduate" value="Postgraduate" />
              <el-option label="Doctor" value="Doctor" />
              <el-option label="Professor" value="Professor" />
            </el-select>
          </el-form-item>
          <el-form-item label="Address">
            <el-input v-model="user.address" />
          </el-form-item>
          <el-form-item label="Borrow Duration">
            <el-input v-model="user.borrow_duration" disabled />
          </el-form-item>
          <el-form-item label="Reservation Duration">
            <el-input v-model="user.reservation_duration" disabled />
          </el-form-item>
          <el-form-item label="Borrow Number">
            <el-input v-model="user.borrow_num" disabled />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="submitUpdate">Save</el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from "../utils/axios.js";

export default {
  name: "UserDetailView",
  data() {
    return {
      user: {},
      editDialogVisible: false,
    };
  },
  methods: {
    goBack() {
      this.$router.push("/user");
    },
    async fetchUser() {
      const id = this.$route.params.id;
      try {
        const res = await axios.get(`http://localhost:8000/api/users/${id}/`);
        this.user = res.data;
      } catch (err) {
        console.error("Failed to fetch user:", err);
      }
    },
    openEditDialog() {
      this.editDialogVisible = true;
    },
    updateRoleValues() {
      const config = {
        Undergraduate: {
          borrow_duration: 14,
          reservation_duration: 14,
          borrow_num: 10,
        },
        Postgraduate: {
          borrow_duration: 21,
          reservation_duration: 21,
          borrow_num: 15,
        },
        Doctor: {
          borrow_duration: 30,
          reservation_duration: 30,
          borrow_num: 15,
        },
        Professor: {
          borrow_duration: 30,
          reservation_duration: 30,
          borrow_num: 20,
        },
      };
      const selected = config[this.user.role];
      if (selected) {
        this.user.borrow_duration = selected.borrow_duration;
        this.user.reservation_duration = selected.reservation_duration;
        this.user.borrow_num = selected.borrow_num;
      }
    },
    async submitUpdate() {
      try {
        await axios.put(
          `http://localhost:8000/api/users/${this.user.id}/`,
          this.user
        );
        this.editDialogVisible = false;
        this.fetchUser();
      } catch (err) {
        console.error("Update failed:", err);
      }
    },
  },
  mounted() {
    this.fetchUser();
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
