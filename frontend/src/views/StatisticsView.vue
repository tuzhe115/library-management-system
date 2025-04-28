<template>
  <div class="statistics-background">
    <div class="statistics-page">
      <div class="statistics-container">
        <div class="button-bar">
          <el-button
            type="primary"
            icon="ArrowLeft"
            @click="goToDashboard"
            style="margin-bottom: 20px"
          >
            Back to Overview
          </el-button>
        </div>
        <div class="user-statistics">
          <h2 class="chart-title">User Statistics</h2>
          <el-card>
            <div id="user-line-chart" class="chart"></div>
          </el-card>
          <el-card>
            <div id="user-role-pie-chart" class="chart"></div>
          </el-card>
          <el-card>
            <div id="user-borrow-bar-chart" class="chart"></div>
          </el-card>
          <el-card>
            <div class="section-title">User Address</div>
            <div id="small-map" class="map-thumbnail" @click="openDialog"></div>
          </el-card>
        </div>

        <div class="book-statistics">
          <h2 class="chart-title">Book Statistics</h2>
          <el-card>
            <div id="book-line-chart" class="chart"></div>
          </el-card>
          <el-card>
            <div id="book-category-pie-chart" class="chart"></div>
          </el-card>
          <el-card>
            <div class="borrowed-header">
              <el-select
                v-model="selectedBorrowedMonth"
                placeholder="Select Month"
                @change="updateBorrowedCategoryChart"
                style="width: 100px"
              >
                <el-option
                  v-for="month in borrowedMonths"
                  :key="month"
                  :label="month"
                  :value="month"
                />
              </el-select>
            </div>
            <div id="book-monthly-borrow-pie-chart" class="chart"></div>
          </el-card>
          <el-card>
            <div id="book-top-bar-chart" class="chart"></div>
          </el-card>
        </div>
      </div>
      <el-dialog v-model="dialogVisible" title="User Map" width="80%" top="5vh">
        <div id="full-map" class="map-full"></div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import axios from "../utils/axios.js";

export default {
  name: "StatisticsView",
  data() {
    return {
      smallMap: null,
      fullMap: null,
      users: [],
      dialogVisible: false,
      markers: [],
      borrowedCategoryData: [],
      borrowedMonths: [],
      selectedBorrowedMonth: "",
    };
  },
  methods: {
    goToDashboard() {
      this.$router.push("/dashboard");
    },
    async fetchUsers() {
      try {
        const res = await axios.get("http://localhost:8000/api/users/");
        this.users = res.data.results || res.data;
        this.renderSmallMap();
      } catch (error) {
        console.error("Failed to fetch users:", error);
      }
    },
    async loadUserGrowthData() {
      try {
        const res = await axios.get(
          "http://localhost:8000/api/statistics/user_growth_statistics/"
        );
        const data = res.data;
        const chart = echarts.getInstanceByDom(
          document.getElementById("user-line-chart")
        );
        chart.setOption({
          title: { text: "Monthly New and Active Users" },
          tooltip: { trigger: "axis" },
          legend: {
            data: ["New Users", "Active Users"],
            right: "10%",
          },
          xAxis: {
            type: "category",
            data: data.months,
          },
          yAxis: {
            type: "value",
          },
          series: [
            {
              name: "New Users",
              type: "line",
              data: data.total_users,
            },
            {
              name: "Active Users",
              type: "line",
              data: data.active_users,
            },
          ],
        });
      } catch (error) {
        console.error("Failed to load user growth data:", error);
      }
    },
    async loadUserRoleDistribution() {
      try {
        const res = await axios.get(
          "http://localhost:8000/api/statistics/user_role_distribution/"
        );
        const data = res.data;
        const chart = echarts.getInstanceByDom(
          document.getElementById("user-role-pie-chart")
        );
        chart.setOption({
          title: { text: "User Role Distribution", left: "center" },
          tooltip: { trigger: "item" },
          legend: {
            orient: "vertical",
            left: "left",
          },
          series: [
            {
              name: "Role",
              type: "pie",
              radius: "50%",
              data: data,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: "rgba(0, 0, 0, 0.5)",
                },
              },
            },
          ],
        });
      } catch (error) {
        console.error("Failed to load user role distribution:", error);
      }
    },
    async loadUserBorrowData() {
      try {
        const res = await axios.get(
          "http://localhost:8000/api/statistics/user_borrow_statistics/"
        );
        const data = res.data;
        const chart = echarts.getInstanceByDom(
          document.getElementById("user-borrow-bar-chart")
        );
        chart.setOption({
          title: { text: "Monthly Average Borrows by Role" },
          tooltip: { trigger: "axis" },
          grid: {
            top: "30%",
            bottom: "1%",
            left: "10%",
            right: "10%",
            containLabel: true,
          },
          legend: {
            data: [
              "Total",
              "Undergraduate",
              "Postgraduate",
              "Doctor",
              "Professor",
            ],
            right: "10%",
            top: "10%",
          },
          xAxis: {
            type: "category",
            data: data.months,
          },
          yAxis: {
            type: "value",
          },
          series: [
            {
              name: "Total",
              type: "bar",
              data: data.total_borrows,
            },
            {
              name: "Undergraduate",
              type: "bar",
              data: data.undergraduate,
            },
            {
              name: "Postgraduate",
              type: "bar",
              data: data.postgraduate,
            },
            {
              name: "Doctor",
              type: "bar",
              data: data.doctor,
            },
            {
              name: "Professor",
              type: "bar",
              data: data.professor,
            },
          ],
        });
      } catch (error) {
        console.error("Failed to load user borrow statistics:", error);
      }
    },
    async loadBookGrowthData() {
      try {
        const res = await axios.get(
          "http://localhost:8000/api/statistics/book_growth_statistics/"
        );
        const data = res.data;
        console.log("Book growth data:", data);
        const chart = echarts.getInstanceByDom(
          document.getElementById("book-line-chart")
        );
        chart.setOption({
          title: { text: "Book Total and Monthly Loans" },
          tooltip: { trigger: "axis" },
          legend: {
            data: ["Total Books", "Monthly Loans"],
            right: "10%",
          },
          xAxis: {
            type: "category",
            data: data.months,
          },
          yAxis: {
            type: "value",
          },
          series: [
            {
              name: "Total Books",
              type: "line",
              data: data.months.map(() => data.total_books),
            },
            {
              name: "Monthly Loans",
              type: "line",
              data: data.borrowed_books,
            },
          ],
        });
      } catch (error) {
        console.error("Failed to load book growth data:", error);
      }
    },
    async loadBookCategoryDistribution() {
      try {
        const res = await axios.get(
          "http://localhost:8000/api/statistics/book_category_distribution/"
        );
        const data = res.data;
        const chart = echarts.getInstanceByDom(
          document.getElementById("book-category-pie-chart")
        );
        chart.setOption({
          title: {
            text: "Book Category Distribution",
            left: "center",
          },
          tooltip: {
            trigger: "item",
          },
          legend: {
            orient: "vertical",
            left: "left",
          },
          series: [
            {
              name: "Categories",
              type: "pie",
              radius: "50%",
              left: "20%",
              data: data,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: "rgba(0, 0, 0, 0.5)",
                },
              },
            },
          ],
        });
      } catch (error) {
        console.error("Failed to load book category distribution:", error);
      }
    },
    async loadBorrowedCategoryDistribution() {
      try {
        const res = await axios.get(
          "http://localhost:8000/api/statistics/monthly_borrowed_category_distribution/"
        );
        const data = res.data;
        if (!data.length) return;

        this.borrowedCategoryData = data;
        this.borrowedMonths = data.map((item) => item.month);
        this.selectedBorrowedMonth =
          this.borrowedMonths[this.borrowedMonths.length - 1];

        this.updateBorrowedCategoryChart();
      } catch (error) {
        console.error("Failed to load borrowed category distribution:", error);
      }
    },
    updateBorrowedCategoryChart() {
      const monthData = this.borrowedCategoryData.find(
        (item) => item.month === this.selectedBorrowedMonth
      );
      if (!monthData) return;

      const chart = echarts.getInstanceByDom(
        document.getElementById("book-monthly-borrow-pie-chart")
      );
      chart.setOption({
        title: {
          text: `Borrowed Categories (${monthData.month})`,
          left: "center",
          top: "0px",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          bottom: "0px",
          type: "scroll",
        },
        series: [
          {
            type: "pie",
            radius: "50%",
            top: "0px",
            data: monthData.categories,
          },
        ],
      });
    },
    async loadTopCategoriesAndBooks() {
      try {
        const res = await axios.get(
          "http://localhost:8000/api/statistics/top_categories_and_books/"
        );
        const rawData = res.data;
        const months = Object.keys(rawData).sort();
        const xAxisData = [];
        const seriesData = [];
        const color = [
          "#5470C6",
          "#91CC75",
          "#FAC858",
          "#EE6666",
          "#73C0DE",
          "#3BA272",
        ];

        months.forEach((month) => {
          for (let i = 0; i < 6; i++) {
            xAxisData.push(month);
          }

          const categories = rawData[month].categories;
          const books = rawData[month].books;
          let colorIndex = 0;

          categories.forEach((cat) => {
            seriesData.push({
              value: cat.count,
              name: `Category Top ${colorIndex + 1}: ${cat.name}`,
              itemStyle: { color: color[colorIndex % color.length] },
            });
            colorIndex++;
          });

          books.forEach((book) => {
            seriesData.push({
              value: book.count,
              name: `Book Top ${colorIndex - 2}: ${book.name}`,
              itemStyle: { color: color[colorIndex % color.length] },
            });
            colorIndex++;
          });
        });

        const chart = echarts.init(
          document.getElementById("book-top-bar-chart")
        );
        chart.setOption({
          title: {
            text: "Top 3 Categories and Top 3 Books Per Month",
            left: "center",
          },
          tooltip: {
            trigger: "item",
            formatter: function (params) {
              return `${params.name}<br/>Borrow Count: ${params.value}`;
            },
          },
          grid: { left: "5%", right: "5%", bottom: "15%", containLabel: true },
          xAxis: {
            type: "category",
            data: xAxisData,
            axisLabel: {
              interval: 5,
              rotate: 0,
            },
          },
          yAxis: { type: "value" },
          series: [
            {
              name: "Borrow Count",
              type: "bar",
              data: seriesData,
              itemStyle: {
                borderRadius: 4,
              },
            },
          ],
        });
      } catch (error) {
        console.error("Failed to load top categories and books:", error);
      }
    },
    initSmallMap() {
      this.smallMap = L.map("small-map", { zoomControl: false }).setView(
        [51.5, -0.1],
        3
      );
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(this.smallMap);
    },
    initFullMap() {
      this.fullMap = L.map("full-map").setView([51.5, -0.1], 5);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(this.fullMap);

      this.users.forEach((user) => {
        if (user.latitude && user.longitude) {
          L.marker([user.latitude, user.longitude])
            .addTo(this.fullMap)
            .bindPopup(`<strong>${user.name}</strong><br>${user.address}`);
        }
      });
    },
    renderSmallMap() {
      this.users.forEach((user) => {
        if (user.latitude && user.longitude) {
          L.marker([user.latitude, user.longitude]).addTo(this.smallMap);
        }
      });
    },
    openDialog() {
      this.dialogVisible = true;
      this.$nextTick(() => {
        if (!this.fullMap) {
          this.initFullMap();
        } else {
          this.fullMap.invalidateSize();
        }
      });
    },

    initCharts() {
      this.initUserLineChart();
      this.initUserRolePieChart();
      this.initUserBorrowBarChart();
      this.initBookLineChart();
      this.initBookCategoryPieChart();
      this.initBookBorrowedCategoryPieChart();
      this.initBookTopBarChart();
    },
    initUserLineChart() {
      const chart = echarts.init(document.getElementById("user-line-chart"));
      chart.setOption({
        title: { text: "Monthly Total and Active Users" },
        tooltip: {},
        xAxis: { type: "category", data: [] },
        yAxis: { type: "value" },
        series: [],
      });
    },
    initUserRolePieChart() {
      const chart = echarts.init(
        document.getElementById("user-role-pie-chart")
      );
      chart.setOption({
        title: { text: "User Role Distribution", left: "center" },
        tooltip: { trigger: "item" },
        series: [{ type: "pie", radius: "50%", data: [] }],
      });
    },
    initUserBorrowBarChart() {
      const chart = echarts.init(
        document.getElementById("user-borrow-bar-chart")
      );
      chart.setOption({
        title: { text: "Average Borrow per Month by Role" },
        tooltip: {},
        xAxis: { type: "category", data: [] },
        yAxis: { type: "value" },
        series: [],
      });
    },
    initBookLineChart() {
      const chart = echarts.init(document.getElementById("book-line-chart"));
      chart.setOption({
        title: { text: "Book Total and Monthly Loans" },
        tooltip: {},
        xAxis: { type: "category", data: [] },
        yAxis: { type: "value" },
        series: [],
      });
    },
    initBookCategoryPieChart() {
      const chart = echarts.init(
        document.getElementById("book-category-pie-chart")
      );
      chart.setOption({
        title: { text: "Book Category Distribution", left: "center" },
        tooltip: { trigger: "item" },
        series: [{ type: "pie", radius: "50%", data: [] }],
      });
    },
    initBookBorrowedCategoryPieChart() {
      const chart = echarts.init(
        document.getElementById("book-monthly-borrow-pie-chart")
      );
      chart.setOption({
        title: {
          text: "Borrowed Categories (Monthly)",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "bottom",
        },
        series: [
          {
            type: "pie",
            radius: "50%",
            data: [],
          },
        ],
      });
    },
    initBookTopBarChart() {
      const chart = echarts.init(document.getElementById("book-top-bar-chart"));
      chart.setOption({
        title: { text: "Top Borrowed Categories" },
        tooltip: {},
        xAxis: { type: "category", data: [] },
        yAxis: { type: "value" },
        series: [],
      });
    },
  },
  mounted() {
    this.initCharts();
    this.initSmallMap();
    this.fetchUsers();
    this.loadUserGrowthData();
    this.loadUserRoleDistribution();
    this.loadUserBorrowData();
    this.loadBookGrowthData();
    this.loadBookCategoryDistribution();
    this.loadBorrowedCategoryDistribution();
    this.loadTopCategoriesAndBooks();
  },
};
</script>

<style scoped>
.statistics-page {
  padding: 40px;
}

.statistics-container {
  display: flex;
  gap: 20px;
}

.user-statistics,
.book-statistics {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart {
  width: 100%;
  height: 300px;
}

.map-thumbnail {
  height: 200px;
  width: 100%;
  border: 2px solid #ccc;
  cursor: pointer;
}

.map-full {
  height: 70vh;
  width: 100%;
}

.borrowed-header {
  display: flex;
  justify-content: flex-start;
}

.el-card {
  height: 350px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.section-title {
  font-size: 19px;
  font-weight: bold;
  margin-top: 0px;
  margin-bottom: 10px;
}

.statistics-background {
  background-image: url("/images/Journal.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  padding: 40px 0;
}

.chart-title {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: bold;
  display: inline-block;
}
</style>
