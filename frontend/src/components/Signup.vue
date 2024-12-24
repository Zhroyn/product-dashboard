<template>
  <div class="h-screen flex justify-center items-center">
    <el-card class="w-[40em] h-[25em] py-10 px-16 rounded-3xl shadow-lg">
      <h2 class="text-2xl font-semibold text-center mb-8">注册</h2>
      <el-form :model="form" :rules="rules" label-width="auto" ref="SignupForm" label-position="left">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="请输入密码">
            <template #suffix>
              <div @click="showPassword = !showPassword" class="flex">
                <el-icon v-if="showPassword" size="20">
                  <View />
                </el-icon>
                <el-icon v-else size="20">
                  <Hide />
                </el-icon>
              </div>
            </template>
          </el-input>
        </el-form-item>
        <div class="flex justify-center space-x-16 mt-6">
          <el-button size="large" type="primary" @click="handle_login">登录</el-button>
          <el-button size="large" type="primary" @click="handle_signup">注册</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      showPassword: false,
      form: {
        username: "",
        email: "",
        password: "",
      },
      rules: {
        username: [
          { type: "string" },
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 6,
            max: 100,
            message: "长度需要在 6 到 100 个字符",
            trigger: "blur",
          },
        ],
        email: [
          { type: "email", message: "请输入正确的邮箱地址", trigger: "blur" },
          { required: true, message: "请输入邮箱", trigger: "blur" },
          {
            min: 6,
            max: 100,
            message: "长度需要在 6 到 100 个字符",
            trigger: "blur",
          },
        ],
        password: [
          { type: "string" },
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 20,
            message: "长度需要在 6 到 20 个字符",
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    async handle_login() {
      this.$router.push("/login");
    },
    async handle_signup() {
      // 校验注册表单
      try {
        await this.$refs.SignupForm.validate();
      } catch (error) {
        ElMessage.error("请检查输入是否正确");
        return;
      }

      // 发送注册请求
      try {
        const response = await axios.post("/signup", this.form);
        if (response.data.success) {
          ElMessage.success("注册成功！");
          this.$router.push("/login");
        } else {
          const message = response.data.message;
          if (typeof message === "string") {
            ElMessage.error(message);
          } else {
            for (const key in message) {
              message[key].forEach((msg) => {
                ElMessage.error(msg);
              });
            }
          }
        }
      } catch (error) {
        ElMessage.error(error.message);
      }
    },
  },
};
</script>
