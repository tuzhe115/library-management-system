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
        Add Loan
      </el-button>
    </div>

    <el-dialog v-model="addDialogVisible" title="Add New Loan" width="600px">
      <el-form :model="newLoan" label-width="140px">
        <el-form-item label="Book">
          <el-select
            v-model="newLoan.book"
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
            v-model="newLoan.user"
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
        <el-button type="primary" @click="submitNewLoan">Submit</el-button>
      </template>
    </el-dialog>

    <h1 class="page-title">Loan Management</h1>
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
        @keyup.enter.native="fetchLoans"
        clearable
      />
      <el-button type="primary" icon="Search" @click="fetchLoans"
        >Search</el-button
      >
    </div>
    <el-table :data="loans" stripe style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="book_title" label="Book" />
      <el-table-column prop="user_name" label="User" />
      <el-table-column prop="borrow_time" label="Borrow Time" />
      <el-table-column prop="due_time" label="Due Time" />
      <el-table-column prop="return_time" label="Return Time" />
      <el-table-column prop="loan_status" label="Loan Status" />
      <el-table-column label="Actions">
        <template #default="scope">
          <el-button
            size="small"
            type="primary"
            @click="goToDetail(scope.row.id)"
            >Details</el-button
          >
          <el-button
            v-if="!scope.row.return_time"
            size="small"
            type="success"
            @click="returnLoan(scope.row)"
          >
            Return
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(scope.row.id)"
            >Delete</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "../utils/axios.js";
import dayjs from "dayjs";

export default {
  name: "LoanView",
  data() {
    return {
      loans: [],
      users: [],
      books: [],
      userLoading: false,
      bookLoading: false,
      loading: false,
      addDialogVisible: false,
      newLoan: {
        book: "",
        user: "",
        loan_status: "",
      },
      searchField: "book_title",
      searchKeyword: "",
      searchOptions: [
        { label: "Book", value: "book_title" },
        { label: "User", value: "user_name" },
        { label: "Loan Status", value: "loan_status" },
      ],
    };
  },
  mounted() {
    this.fetchLoans();
  },
  methods: {
    goToDashboard() {
      this.$router.push("/dashboard");
    },
    goToDetail(loanId) {
      this.$router.push(`/loan/${loanId}`);
    },
    async fetchLoans() {
      this.loading = true;
      try {
        const params = {};
        if (this.searchKeyword && this.searchField) {
          params.keyword = this.searchKeyword;
          params.field = this.searchField;
        }
        const response = await axios.get("http://localhost:8000/api/loans/", {
          params,
        });
        this.loans = response.data.results || response.data;
      } catch (err) {
        console.error("Failed to fetch loans:", err);
      } finally {
        this.loading = false;
      }
    },
    async returnLoan(loan) {
      try {
        const return_time = dayjs().format("DD-MM-YYYY HH:mm:ss");
        await axios.patch(`http://localhost:8000/api/loans/${loan.id}/`, {
          book: loan.book,
          user: loan.user,
          return_time,
          loan_status: "returned",
        });
        this.$message.success("Loan returned successfully");
        this.fetchLoans();
      } catch (err) {
        console.error("Failed to return loan:", err);
      }
    },
    openAddDialog() {
      this.addDialogVisible = true;
    },
    async submitNewLoan() {
      try {
        this.newLoan.loan_status = "Active";
        await axios.post("http://localhost:8000/api/loans/", this.newLoan);
        this.addDialogVisible = false;
        this.$message.success("Loan added successfully");
        this.fetchLoans();
        this.resetForm();
      } catch (err) {
        const errorData = err?.response?.data;
        let message = "Failed to add loan";
        if (errorData && typeof errorData === "object") {
          message = Object.values(errorData).flat().join(", ");
        }
        this.$message.error(message);
        console.error("Failed to add loan:", err.response?.data || err);
      }
    },
    resetForm() {
      this.newLoan = {
        book: "",
        user: "",
        loan_status: "",
      };
    },
    async handleDelete(id) {
      try {
        await axios.delete(`http://localhost:8000/api/loans/${id}/`);
        this.$message.success("Loan deleted successfully!");
        this.fetchLoans();
      } catch (err) {
        console.error("Failed to delete loan:", err);
        this.$message.error("Failed to delete loan");
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
