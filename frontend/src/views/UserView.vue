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
        Add User
      </el-button>
    </div>

    <el-dialog v-model="addDialogVisible" title="Add New User" width="600px">
      <el-form :model="newUser" label-width="140px">
        <el-form-item label="Name">
          <el-input v-model="newUser.name" />
        </el-form-item>
        <el-form-item label="Account">
          <el-input v-model="newUser.account" />
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="newUser.email" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="newUser.password" />
        </el-form-item>
        <el-form-item label="Phone">
          <el-input v-model="newUser.phone" />
        </el-form-item>
        <el-form-item label="Address">
          <el-input v-model="newUser.address" />
        </el-form-item>
        <el-form-item label="Role">
          <el-select
            v-model="newUser.role"
            placeholder="Select Role"
            @change="updateRoleValues"
          >
            <el-option label="Undergraduate" value="Undergraduate" />
            <el-option label="Postgraduate" value="Postgraduate" />
            <el-option label="Doctor" value="Doctor" />
            <el-option label="Professor" value="Professor" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="addDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitNewUser">Submit</el-button>
      </template>
    </el-dialog>

    <h1 class="page-title">User Management</h1>
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
        @keyup.enter.native="fetchUsers"
        clearable
      />

      <el-button type="primary" icon="Search" @click="fetchUsers">
        Search
      </el-button>
    </div>
    <el-table :data="users" stripe style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="account" label="Account" />
      <el-table-column prop="email" label="Email" />
      <el-table-column prop="password" label="Password" />
      <el-table-column prop="phone" label="Phone" />
      <el-table-column prop="role" label="Role" />
      <el-table-column prop="address" label="Address" />
      <el-table-column prop="borrow_duration" label="Borrow Duration" />
      <el-table-column prop="borrow_num" label="Borrow Number" />
      <el-table-column
        prop="reservation_duration"
        label="Reservation Duration"
      />
      <el-table-column prop="registration_time" label="Registration Time" />
      <el-table-column label="Actions" width="170">
        <template #default="scope">
          <el-button
            size="small"
            type="primary"
            @click="goToDetail(scope.row.id)"
            >Details</el-button
          >
          <el-button
            size="small"
            type="danger"
            @click="deleteUser(scope.row.id)"
            >Delete</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "../utils/axios.js";

export default {
  name: "UserView",
  data() {
    return {
      users: [],
      loading: false,
      addDialogVisible: false,
      newUser: {
        name: "",
        account: "",
        email: "",
        password: "",
        phone: "",
        role: "",
        address: "",
        borrow_duration: "",
        borrow_num: "",
        reservation_duration: "",
      },
      roles: [
        { label: "Undergraduate", value: "Undergraduate" },
        { label: "Postgraduate", value: "Postgraduate" },
        { label: "Doctor", value: "Doctor" },
        { label: "Professor", value: "Professor" },
      ],
      searchField: "name",
      searchKeyword: "",
      searchOptions: [
        { label: "Name", value: "name" },
        { label: "Account", value: "account" },
        { label: "Email", value: "email" },
        { label: "Phone", value: "phone" },
        { label: "Role", value: "role" },
        { label: "Address", value: "address" },
      ],
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    goToDashboard() {
      this.$router.push("/dashboard");
    },
    goToDetail(userId) {
      this.$router.push(`/user/${userId}`);
    },
    async fetchUsers() {
      this.loading = true;
      try {
        const params = {};
        if (this.searchKeyword && this.searchField) {
          params.keyword = this.searchKeyword;
          params.field = this.searchField;
        }
        const response = await axios.get("http://localhost:8000/api/users/", {
          params,
        });
        this.users = response.data.results || response.data;
      } catch (error) {
        console.error("Failed to fetch users:", error);
      } finally {
        this.loading = false;
      }
    },
    openAddDialog() {
      this.addDialogVisible = true;
    },
    updateRoleValues() {
      const roleConfig = {
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
      const selected = roleConfig[this.newUser.role];
      if (selected) {
        this.newUser.borrow_duration = selected.borrow_duration;
        this.newUser.reservation_duration = selected.reservation_duration;
        this.newUser.borrow_num = selected.borrow_num;
      }
    },
    async submitNewUser() {
      try {
        await axios.post("http://localhost:8000/api/users/", this.newUser);
        this.addDialogVisible = false;
        this.$message.success("User added successfully");
        this.fetchUsers();
        this.resetForm();
      } catch (err) {
        const errorData = err?.response?.data;
        let message = "Failed to add user";
        if (errorData && typeof errorData === "object") {
          message = Object.values(errorData).flat().join(", ");
        }
        this.$message.error(message);
        console.error("Failed to add user:", err.response?.data || err);
      }
    },
    resetForm() {
      this.newUser = {
        name: "",
        account: "",
        email: "",
        password: "",
        phone: "",
        role: "",
        address: "",
        borrow_duration: "",
        borrow_number: "",
        reservation_duration: "",
      };
    },
    async deleteUser(id) {
      try {
        await axios.delete(`http://localhost:8000/api/users/${id}/`);
        this.$message.success("User deleted successfully");
        this.fetchUsers();
      } catch (err) {
        console.error("Failed to delete user:", err);
        this.$message.error("Failed to delete user");
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
.button-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.el-button {
  margin-left: 5px;
}
</style>
