<template>
  <div class="detail-background">
    <div class="page-container">
      <el-card v-if="book">
        <el-button
          type="primary"
          icon="ArrowLeft"
          class="back-button"
          @click="goBack"
          >Back</el-button
        >
        <p><strong>Title:</strong> {{ book.title }}</p>
        <p><strong>Author:</strong> {{ book.author }}</p>
        <p><strong>ISBN:</strong> {{ book.ISBN }}</p>
        <p><strong>Publisher:</strong> {{ book.publisher }}</p>
        <p><strong>Published Year:</strong> {{ book.published_year }}</p>
        <p><strong>Price:</strong> {{ book.price }}</p>
        <p><strong>Total Copies:</strong> {{ book.total_copies }}</p>
        <p><strong>Available Copies:</strong> {{ book.available_copies }}</p>
        <p><strong>Category:</strong> {{ book.category_names?.join(", ") }}</p>

        <el-button type="success" class="edit-button" @click="openEditDialog"
          >Edit</el-button
        >
      </el-card>

      <el-dialog v-model="editDialogVisible" title="Edit Book" width="600px">
        <el-form :model="book" label-width="140px">
          <el-form-item label="Title"
            ><el-input v-model="book.title"
          /></el-form-item>
          <el-form-item label="Author"
            ><el-input v-model="book.author"
          /></el-form-item>
          <el-form-item label="ISBN"
            ><el-input v-model="book.ISBN"
          /></el-form-item>
          <el-form-item label="Publisher"
            ><el-input v-model="book.publisher"
          /></el-form-item>
          <el-form-item label="Published Year"
            ><el-input v-model="book.published_year"
          /></el-form-item>
          <el-form-item label="Price"
            ><el-input v-model="book.price"
          /></el-form-item>
          <el-form-item label="Total Copies"
            ><el-input v-model="book.total_copies"
          /></el-form-item>
          <el-form-item label="Available Copies"
            ><el-input v-model="book.available_copies"
          /></el-form-item>
          <el-form-item label="Categories">
            <el-select
              v-model="book.category"
              multiple
              filterable
              placeholder="Select categories"
            >
              <el-option
                v-for="cat in categories"
                :key="cat.id"
                :label="cat.category_name"
                :value="cat.id"
              />
            </el-select>
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
import { useRoute, useRouter } from "vue-router";
import axios from "../utils/axios.js";

export default {
  name: "BookDetailView",
  data() {
    return {
      book: {},
      categories: [],
      editDialogVisible: false,
    };
  },
  mounted() {
    this.fetchBook();
  },
  methods: {
    async fetchBook() {
      const id = this.$route.params.id;
      try {
        const res = await axios.get(`http://localhost:8000/api/books/${id}/`);
        this.book = res.data;
      } catch (err) {
        console.error("Failed to fetch book:", err);
      }
    },
    async fetchCategories() {
      try {
        const res = await axios.get("http://localhost:8000/api/categories/");
        this.categories = res.data.results || res.data;
      } catch (err) {
        console.error("Failed to fetch categories:", err);
      }
    },
    openEditDialog() {
      this.editDialogVisible = true;
      this.fetchCategories();
    },
    async submitUpdate() {
      try {
        await axios.put(
          `http://localhost:8000/api/books/${this.book.id}/`,
          this.book
        );
        this.editDialogVisible = false;
        this.fetchBook();
      } catch (err) {
        console.error("Update failed:", err);
      }
    },
    goBack() {
      this.$router.push("/books");
    },
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
