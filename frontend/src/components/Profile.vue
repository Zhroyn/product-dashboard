<template>
  <div class="p-2">
    <!-- 用户信息 -->
    <div class="text-center text-5xl font-semibold my-24">
      Statistic
    </div>
    <el-row class="p-2 my-10">
      <el-col :span="8">
        <el-statistic class="text-center" title="Username" :formatter="getUsername" />
      </el-col>
      <el-col :span="8">
        <el-statistic class="text-center" title="Email" :formatter="getEmail" />
      </el-col>
      <el-col :span="8">
        <el-statistic class="text-center" title="Total Traces" :value="user.price_alerts.length" />
      </el-col>
    </el-row>

    <!-- 价格历史表 -->
    <div id="chart" class="h-[400px] text-center"></div>

    <!-- 价格提示列表 -->
    <div class="px-8 mt-8" v-if="user.price_alerts.length > 0">
      <!-- 表头 -->
      <el-row :gutter="20" class="justify-center border-b py-2">
        <el-col :span="spans[0]" class="font-semibold text-lg text-gray-600">商品标题</el-col>
        <el-col :span="spans[1]" class="font-semibold text-lg text-gray-600 text-center">平台</el-col>
        <el-col :span="spans[2]" class="font-semibold text-lg text-gray-600">最新价格</el-col>
        <el-col :span="spans[3]" class="font-semibold text-lg text-gray-600">目标价格</el-col>
        <el-col :span="spans[4]" class="font-semibold text-lg text-gray-600">店铺</el-col>
        <el-col :span="spans[5]" class="font-semibold text-lg text-gray-600">创建时间</el-col>
        <el-col :span="spans[6]" class="font-semibold text-lg text-gray-600 text-center">操作</el-col>
      </el-row>

      <!-- 表格内容 -->
      <el-row :gutter="20" v-for="(alert, index) in user.price_alerts" :key="index"
        class="py-2 justify-center items-center flex-nowrap border-b hover:bg-gray-50 duration-500">
        <el-col :span="spans[0]">
          <div class="line-clamp-3">
            {{ alert.product.title }}
          </div>
        </el-col>
        <el-col :span="spans[1]" class="text-center">{{ alert.product.platform }}</el-col>
        <el-col :span="spans[2]">¥{{ alert.product.price }}</el-col>
        <el-col :span="spans[3]">¥{{ alert.target_price }}</el-col>
        <el-col :span="spans[4]">{{ alert.product.shop_name }}</el-col>
        <el-col :span="spans[5]">{{ new Date(alert.created_at).toLocaleString() }}</el-col>
        <el-col :span="spans[6]" class="space-x-4 text-center">
          <el-tooltip content="查看价格历史" placement="top" effect="light">
            <el-icon size="16" @click="handleViewHistory(index)" class="hover:text-indigo-600">
              <View />
            </el-icon>
          </el-tooltip>
          <el-tooltip content="删除价格提示" placement="top" effect="light">
            <el-icon size="16" @click="handleDelete(index)" class="hover:text-indigo-600">
              <Delete />
            </el-icon>
          </el-tooltip>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from "echarts";
import { markRaw } from "vue";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      user: { price_alerts: [] },
      spans: [8, 2, 2, 2, 4, 3, 3],
      chartVisible: false,
      chart: null,
      timestamp: [],
      price: [],
    };
  },
  methods: {
    getUsername(value) {
      return this.user.username;
    },
    getEmail(value) {
      return this.user.email;
    },
    async fetchUserData() {
      try {
        const response = await axios.get("/api/user");
        if (response.data.success) {
          this.user = response.data.user;
          localStorage.setItem("user", JSON.stringify(response.data.user));
          this.handleViewHistory(0);
        } else {
          this.user = JSON.parse(localStorage.getItem("user"));
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        ElMessage.error(error.message);
        return;
      }
    },
    async handleDelete(index) {
      try {
        const response = await axios.delete("/api/alert", {
          data: this.user.price_alerts[index].product,
        });
        if (response.data.success) {
          this.user.price_alerts.splice(index, 1);
          localStorage.setItem("user", JSON.stringify(this.user));
          ElMessage.success(response.data.message);
        } else {
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        ElMessage.error(error.message);
        return;
      }
    },
    handleViewHistory(index) {
      if (index < 0 || index >= this.user.price_alerts.length) {
        return;
      }
      if (!this.chart) {
        const chartId = document.getElementById("chart");
        this.chart = markRaw(echarts.init(chartId));
      }

      const product = this.user.price_alerts[index].product;
      const option = {
        title: {
          text: product.title,
          bottom: 10,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 300,
            fontStyle: 'oblique',
          },
        },
        tooltip: {
          trigger: "axis",
          formatter: function (params) {
            const timestamp = params[0].name;
            const formattedTime = new Date(timestamp).toLocaleString();
            const price = params[0].data;
            return `${formattedTime}<br/>¥${price}`;
          },
        },
        xAxis: {
          name: "Time",
          data: product.price_histories.timestamps,
          axisLabel: {
            formatter: (value) => {
              return new Date(value).toLocaleString();
            },
          },
        },
        yAxis: {
          type: "value",
          name: "Price",
        },
        series: [
          {
            name: "Price History",
            type: "line",
            data: product.price_histories.prices,
          },
        ],
      };

      this.chart.setOption(option);
      this.chartVisible = true;
    },
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.fetchUserData();
    });
  },
};
</script>

<style>
.el-button {
  font-size: 14px !important;
  font-weight: 500;
}
</style>