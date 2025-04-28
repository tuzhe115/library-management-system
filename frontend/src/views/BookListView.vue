<template>
    <div class="page-container">
      <div class="button-bar">
        <el-button type="primary" icon="ArrowLeft" @click="goToDashboard" style="margin-bottom: 20px;">
          Back to Overview
        </el-button>
        <el-button type="success" size="default" @click="openAddDialog" style="margin-bottom: 20px; float: right;">
                Add Book
        </el-button>
      </div>

      <el-dialog v-model="addDialogVisible" title="Add New Book" width="600px">
        <el-form :model="newBook" label-width="140px">
          <el-form-item label="Title">
            <el-input v-model="newBook.title" />
          </el-form-item>
          <el-form-item label="Author">
            <el-input v-model="newBook.author" />
          </el-form-item>
          <el-form-item label="Category">
            <el-select v-model="newBook.category" multiple placeholder="Select categories">
              <el-option
                v-for="cat in categories"
                :key="cat.id"
                :label="cat.category_name"
                :value="cat.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="ISBN">
            <el-input v-model="newBook.ISBN" />
          </el-form-item>
          <el-form-item label="Publisher">
            <el-input v-model="newBook.publisher" />
          </el-form-item>
          <el-form-item label="Published Year">
            <el-input v-model="newBook.published_year" />
          </el-form-item>
          <el-form-item label="Price">
            <el-input v-model="newBook.price" />
          </el-form-item>
          <el-form-item label="Total Copies">
            <el-input v-model="newBook.total_copies" />
          </el-form-item>
          <el-form-item label="Available Copies">
            <el-input v-model="newBook.available_copies" />
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="addDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="submitNewBook">Submit</el-button>
        </template>
      </el-dialog>
      <h1 class="page-title">Book List</h1>
      <div class="search-bar">
        <el-select v-model="searchField" placeholder="Select Field" style="width: 180px;">
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
          style="width: 240px;"
          @keyup.enter.native="fetchBooks"
          clearable
        />

        <el-button type="primary" icon="Search" @click="fetchBooks">
          Search
        </el-button>
      
      </div>
      
      <el-table :data="books" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" />
        <el-table-column prop="title" label="Title" />
        <el-table-column prop="author" label="Author" />
        <el-table-column prop="category_names" label="Category Names">
          <template #default="scope">
            {{ scope.row.category_names.join(', ') }}
          </template>
        </el-table-column>
        <el-table-column prop="ISBN" label="ISBN" />
        <el-table-column prop="publisher" label="Publisher" />
        <el-table-column prop="published_year" label="Published Year" />
        <el-table-column prop="price" label="Price" />
        <el-table-column prop="total_copies" label="Total Copies" />
        <el-table-column prop="available_copies" label="Available Copies" />
        <el-table-column label="Actions">
          <template #default="scope">
            <el-button size="small" type="primary" @click="goToDetails(scope.row.id)">Details</el-button>
            <el-button size="small" type="danger" @click="deleteBook(scope.row.id)">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>
  
  <script>
  import axios from '../utils/axios.js'
  
  export default {
    name: 'BookListView',
    data() {
      return {
        books: [],
        loading: false,
        addDialogVisible: false,
        searchKeyword: '',
        categories: [],
        newBook: {
          title: '',
          author: '',
          category: [],
          ISBN: '',
          publisher: '',
          published_year: '',
          price: '',
          total_copies: '',
          available_copies: ''
        },
        searchField: 'title',
        searchOptions: [
          { label: 'Title', value: 'title' },
          { label: 'Author', value: 'author' },
          { label: 'Category', value: 'category' },
          { label: 'ISBN', value: 'ISBN' },
          { label: 'Publisher', value: 'publisher' },
          { label: 'Published Year', value: 'published_year' }
        ]
      }
    },
    methods: {
      goToDashboard() {
        this.$router.push('/dashboard') 
      },
      goToDetails(bookId) {
        this.$router.push(`/books/${bookId}`)
      },
      async fetchBooks() {

        this.loading = true
        try {
          const params = {}
          if (this.searchKeyword && this.searchField) {
            params.keyword = this.searchKeyword
            params.field = this.searchField
          } 
          const response = await axios.get('http://localhost:8000/api/books/', { params })
          console.log('Params sent:', params)
          this.books = response.data.results || response.data
        } catch (error) {
          console.error('Failed to fetch books:', error)
        } finally {
          this.loading = false
        }
      },
      async fetchCategories() {
        try {
          const res = await axios.get('http://localhost:8000/api/categories/')
          this.categories = res.data.results || res.data
        } catch (err) {
          console.error('Failed to fetch categories:', err)
        }
      },
      openAddDialog() {
        this.addDialogVisible = true
        this.fetchCategories()
      },
      async submitNewBook() {
        try {
          await axios.post('http://localhost:8000/api/books/', this.newBook)
          this.addDialogVisible = false
          this.fetchBooks()
          this.resetForm()
        } catch (err) {
          console.error('Failed to add book:', err.response?.data || err)
        }
      },
      resetForm() {
        this.newBook = {
          title: '',
          author: '',
          category: [],
          ISBN: '',
          publisher: '',
          published_year: '',
          price: '',
          total_copies: '',
          available_copies: ''
        }
      },
      async deleteBook(id) {
        try {
          await axios.delete(`http://localhost:8000/api/books/${id}/`)
          this.fetchBooks()
        } catch (error) {
          console.error('Failed to delete book:', error)
        }
      }
    },
    mounted() {
      this.fetchBooks()
    }
  }
  </script>
  
  <style scoped>
  .el-button {
    margin-left: 5px;
  }

  .button-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  .page-container {
    padding: 40px;
  }
  .page-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
  }

  .search-bar {
    display: flex;
    align-items: flex-end;
    gap: 12px;
    margin-bottom: 20px;
  }

  </style>
  