<template>
  <el-container class="h-full">
    <!-- 头部标题栏 -->
    <el-header class="bg-gray-100 flex items-center">
      <el-icon @click="isCollapsed = !isCollapsed" size="22" :class="{'rotate-180': isCollapsed}" class="duration-300">
        <ArrowRightBold />
      </el-icon>
      <div class="heiti text-center font-semibold text-3xl place-self-center w-full">商品比价网站</div>
    </el-header>

    <el-container>
      <!-- 左侧侧边栏 -->
      <el-aside class="transition-all" height="100%" width="9.5rem" v-if="!isCollapsed || !needCollapse">
        <el-menu default-active="1" :collapse="isCollapsed" router class="h-full">
          <el-menu-item class="h-16" index="/">
            <el-icon size="25" class="!mr-4">
              <Search />
            </el-icon>
            <template #title>
              <span class="mr-1 text-base">搜索</span>
            </template>
          </el-menu-item>
          <el-menu-item class="h-16" index="/home/profile">
            <el-icon size="25" class="!mr-4">
              <User />
            </el-icon>
            <template #title>
              <span class="mr-1 text-base">追踪</span>
            </template>
          </el-menu-item>
          <el-sub-menu>
            <template #title>
              <el-icon size="25" class="!mr-4">
                <Setting />
              </el-icon>
              <span class="mr-1 text-base">设置</span>
            </template>
            <el-menu-item @click="handle_logout">
              <span class="mr-1 text-base">退出登录</span>
            </el-menu-item>
            <el-menu-item @click="handle_unregister">
              <span class="mr-1 text-base">注销账号</span>
            </el-menu-item>
            <el-menu-item @click="setCookieVisible = true">
              <span class="mr-1 text-base">设置Cookie</span>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <!-- 右侧内容区域 -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>

  <!-- 设置Cookie对话框 -->
  <el-dialog v-model="setCookieVisible" title="设置Cookie" width="30%" align-center>
    <el-input v-model="cookie" height="20em" :autosize="{ minRows: 6, maxRows: 18 }" type="textarea"
      placeholder="请输入Cookie" />
    <div class="flex justify-between mt-4 px-1">
      <el-segmented v-model="platform" :options="platforms" />
      <div>
        <el-button type="error" @click="setCookieVisible = false">取消</el-button>
        <el-button type="primary" @click="handle_set_cookie">确定</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      isCollapsed: true,
      setCookieVisible: false,
      cookie: "",
      platform: "淘宝",
      platforms: ["淘宝", "京东"],
    };
  },
  methods: {
    async handle_logout() {
      try {
        const response = await axios.delete("/logout");
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
        const response = await axios.delete("/unregister");
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
    async handle_set_cookie() {
      try {
        const response = await axios.put("/cookie", {
          platform: this.platform,
          cookie: JSON.parse(this.cookie),
        });
        if (response.data.success) {
          ElMessage.success("设置成功！");
          this.setCookieVisible = false;
        } else {
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        if (error instanceof SyntaxError) {
          ElMessage.error("Cookie 无法解析为 JSON 格式");
        } else {
          ElMessage.error(error.message);
        }
      }
    },
  },
  computed: {
    user() {
      return JSON.parse(localStorage.getItem("user"));
    },
    needCollapse() {
      return window.innerWidth < window.innerHeight;
    },
  },
};
</script>

<style>
.rotate-180 {
  transform: rotate(180deg);
  transition: transform 0.3s ease-in-out;
}
:root {
  --el-menu-item-height: 64px !important;
}
</style>