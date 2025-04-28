<template>
  <div class="detail-background">
    <div class="page-container">
      <el-card v-if="loan">
        <el-button
          type="primary"
          icon="ArrowLeft"
          class="back-button"
          @click="goBack"
          style="margin-bottom: 20px"
        >
          Back to Loans
        </el-button>
        <p><strong>Loan ID:</strong> {{ loan.id }}</p>
        <p><strong>Book:</strong> {{ loan.book_title }}</p>
        <p><strong>User:</strong> {{ loan.user_name }}</p>
        <p><strong>Borrow Time:</strong> {{ loan.borrow_time }}</p>
        <p><strong>Due Time:</strong> {{ loan.due_time }}</p>
        <p><strong>Return Time:</strong> {{ loan.return_time }}</p>
        <p><strong>Status:</strong> {{ loan.loan_status }}</p>

        <el-button type="success" class="edit-button" @click="openEditDialog"
          >Edit</el-button
        >
      </el-card>

      <el-dialog title="Edit Loan" v-model="editDialogVisible">
        <el-form :model="editLoan" label-width="120px">
          <el-form-item label="Return Time">
            <el-date-picker
              v-model="editLoan.return_time"
              type="datetime"
              placeholder="Pick Return Time"
            />
          </el-form-item>
          <el-form-item label="Status">
            <el-select
              v-model="editLoan.loan_status"
              placeholder="Select Status"
            >
              <el-option label="Active" value="active" />
              <el-option label="Returned" value="returned" />
              <el-option label="Overdue" value="overdue" />
              <el-option label="Lost" value="lost" />
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
import dayjs from "dayjs";

export default {
  name: "LoanDetailView",
  data() {
    return {
      loan: null,
      editLoan: {},
      editDialogVisible: false,
    };
  },
  methods: {
    goBack() {
      this.$router.push("/loan");
    },
    async fetchLoan() {
      const id = this.$route.params.id;
      try {
        const res = await axios.get(`http://localhost:8000/api/loans/${id}/`);
        this.loan = res.data;
        this.editLoan = { ...res.data };
      } catch (err) {
        console.error("Failed to fetch loan:", err);
      }
    },
    openEditDialog() {
      this.editDialogVisible = true;
    },
    async submitEdit() {
      try {
        const edit = {
          book: this.editLoan.book,
          user: this.editLoan.user,
        };

        if (
          this.editLoan.return_time &&
          dayjs(this.editLoan.return_time).isValid()
        ) {
          edit.return_time = dayjs(this.editLoan.return_time).format(
            "DD-MM-YYYY HH:mm:ss"
          );
        }
        if (this.editLoan.loan_status) {
          edit.loan_status = this.editLoan.loan_status;
        }
        console.log("Submitting loan update:", edit);
        await axios.patch(
          `http://localhost:8000/api/loans/${this.loan.id}/`,
          edit
        );
        this.editDialogVisible = false;
        this.fetchLoan();
      } catch (err) {
        console.error("Failed to update loan:", err);
      }
    },
  },
  mounted() {
    this.fetchLoan();
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
