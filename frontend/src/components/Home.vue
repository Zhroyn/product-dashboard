<template>
  <div class="flex flex-col">
    <div class="heiti text-4xl text-center mb-16">Welcome to the Home Page</div>
    <div class="flex justify-center space-x-10">
      <el-button size="large" type="primary" @click="handle_logout">退出登录</el-button>
      <el-button size="large" type="primary" @click="handle_unregister">注销账户</el-button>
      <el-button size="large" type="primary" @click="handle_user_info">用户信息</el-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  methods: {
    handle_logout() {
      axios.post("/logout").then((response) => {
        if (response.status === 200) {
          ElMessage.success("退出登录！");
          this.$router.push("/login");
        } else {
          ElMessage.error(response.data.message);
        }
      });
    },
    handle_unregister() {
      axios.delete("/unregister").then((response) => {
        if (response.status === 200) {
          ElMessage.success("注销成功！");
          this.$router.push("/login");
        } else {
          ElMessage.error(response.data.message);
        }
      });
    },
    handle_user_info() {
      axios.get("/user").then((response) => {
        if (response.status === 200) {
          ElMessage.success("获取用户信息成功！");
          console.log(response.data);
        } else {
          ElMessage.error(response.data.message);
        }
      });
    },
  },
};
</script>