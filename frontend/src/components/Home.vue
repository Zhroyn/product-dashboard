<template>
  <div class="flex flex-col">
    <div class="heiti text-4xl text-center mb-16">Welcome to the Home Page</div>
    <div class="flex justify-center space-x-10">
      <el-button size="large" type="primary" @click="handle_logout">退出登录</el-button>
      <el-button size="large" type="primary" @click="handle_unregister">注销账户</el-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  methods: {
    async handle_logout() {
      try {
        const response = await axios.delete("/logout", { withCredentials: true });
        if (response.data.success) {
          ElMessage.success("退出成功！");
        } else {
          ElMessage.error("用户未登录");
        }
        localStorage.removeItem("user");
        this.$router.push("/login");
      } catch (error) {
        ElMessage.error(error.message);
      }
    },
    async handle_unregister() {
      try {
        const response = await axios.delete("/unregister", { withCredentials: true });
        if (response.data.success) {
          ElMessage.success("注销成功！");
        } else {
          ElMessage.error(response.data.message);
        }
        localStorage.removeItem("user");
        this.$router.push("/login");
      } catch (error) {
        ElMessage.error(error.message);
      }
    },
  },
};
</script>