<template>
  <div class="p-2">

    <!-- 用户信息 -->
    <div class="text-center text-5xl font-semibold my-16">
      Statistic
    </div>
    <el-row class="p-2 my-16 mb-16">
      <el-col :span="8">
        <el-statistic class="text-center" title="Username" :value="user.username" />
      </el-col>
      <el-col :span="8">
        <el-statistic class="text-center" title="Email" :value="user.email" />
      </el-col>
      <el-col :span="8">
        <el-statistic class="text-center" title="Total Traces" :value="user.price_alerts.length" />
      </el-col>
    </el-row>

    <!-- 表头 -->
    <el-row :gutter="20" class="p-2 justify-center border-b">
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
      class="p-2 justify-center items-center flex-nowrap border-b hover:bg-gray-50 duration-500">
      <el-col :span="spans[0]">
        <div class="line-clamp-3">
          {{ alert.title }}
        </div>
      </el-col>
      <el-col :span="spans[1]" class="text-center">{{ alert.platform }}</el-col>
      <el-col :span="spans[2]">¥{{ alert.price }}</el-col>
      <el-col :span="spans[3]">¥{{ alert.target_price }}</el-col>
      <el-col :span="spans[4]">{{ alert.shop_name }}</el-col>
      <el-col :span="spans[5]">{{ new Date(alert.created_at).toLocaleString() }}</el-col>
      <el-col :span="spans[6]" class="space-x-4 text-center">
        <el-tooltip content="查看历史价格" placement="top" effect="light">
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
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      user: { price_alerts: [] },
      spans: [8, 2, 2, 2, 4, 3, 3],
    };
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.fetchUserData();
    });
  },
  methods: {
    async fetchUserData() {
      console.log(this.user);
      try {
        const response = await axios.get("/user");
        if (response.data.success) {
          this.user = response.data.user;
          localStorage.setItem("user", JSON.stringify(response.data.user));
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
        const response = await axios.delete("/alert", {
          data: this.user.price_alerts[index],
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
  },
};
</script>

<style>
.el-button {
  font-size: 14px !important;
  font-weight: 500;
}
</style>