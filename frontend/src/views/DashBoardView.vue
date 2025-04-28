<template>
  <div class="dashboard-background">
    <div class="management-container">
      <h1 class="management-title">Library Management Dashboard</h1>

      <div class="management-section">
        <h2 class="section-title">Book Management</h2>
        <p class="section-description">Manage library books and catalog.</p>
        <el-button type="danger" @click="$router.push('/books')"
          >Manage Books</el-button
        >
      </div>

      <div class="management-section">
        <h2 class="section-title">Loan Management</h2>
        <p class="section-description">Track and manage book loans.</p>
        <el-button type="primary" @click="$router.push('/loan')"
          >View Loans</el-button
        >
      </div>

      <div class="management-section">
        <h2 class="section-title">Reservation Management</h2>
        <p class="section-description">View and handle book reservations.</p>
        <el-button type="success" @click="$router.push('/reservation')"
          >View Reservations</el-button
        >
      </div>

      <div class="management-section">
        <h2 class="section-title">User Management</h2>
        <p class="section-description">Manage registered users and profiles.</p>
        <el-button type="warning" @click="$router.push('/user')"
          >Manage Users</el-button
        >
      </div>

      <div class="management-section">
        <h2 class="section-title">Statistics</h2>
        <p class="section-description">Show statistics</p>
        <el-button type="info" @click="$router.push('/statistics')"
          >Show statistics</el-button
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashBoardView",
};
</script>

<style scoped>
.management-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

.management-title {
  font-size: 32px;
  font-weight: 800;
  text-align: center;
  margin-bottom: 30px;
  color: #1976d2;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 20px;
  margin-bottom: 10px;
  color: #2c3e50;
}

.section-description {
  font-size: 14px;
  margin-bottom: 15px;
  color: #555;
}

.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.dashboard-background {
  background-image: url("/images/Journal.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  padding: 40px 0;
}
</style>
