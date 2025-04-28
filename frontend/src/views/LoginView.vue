<template>
  <div class="login-container">
    <div class="login-box">
      <img
        src="https://cdn-icons-png.flaticon.com/512/29/29302.png"
        alt="Library Logo"
        class="login-logo"
      />
      <h2 class="login-title">Library Admin Login</h2>
      <p class="login-subtitle">Welcome to the University Library System</p>
      <el-form :model="form" ref="formRef" label-width="100px">
        <el-form-item label="Username">
          <el-input
            v-model="form.username"
            placeholder="Enter username"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="Password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Enter password"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            class="login-button"
            @click="handleLogin"
            :loading="loading"
            >Login</el-button
          >
        </el-form-item>
      </el-form>
      <el-alert
        v-if="error"
        type="error"
        :title="error"
        show-icon
        class="mt-2"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginView",
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      loading: false,
      error: "",
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = "";
      try {
        const response = await axios.post(
          "http://localhost:8000/api-token-auth/",
          {
            username: this.form.username,
            password: this.form.password,
          }
        );
        const token = response.data.token;
        localStorage.setItem("token", token);
        axios.defaults.headers.common["Authorization"] = `Token ${token}`;
        this.$router.push("/dashboard");
      } catch (err) {
        this.error = "Invalid username or password";
        this.form.username = "";
        this.form.password = "";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url("/images/Journal.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.login-box {
  width: 100%;
  max-width: 420px;
  background-color: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25);
  text-align: center;
}

.login-logo {
  width: 64px;
  margin-bottom: 12px;
}

.login-title {
  font-size: 26px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 6px;
}

.login-subtitle {
  font-size: 14px;
  color: #777;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  margin-top: 12px;
}
</style>
