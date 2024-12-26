<template>
  <el-container class="h-full">
    <!-- 左侧侧边栏 -->
    <el-aside height="100%" :class="isCollapsed ? 'total-collapse' : 'un-colllapse'">
      <el-menu default-active="1" :collapse="isCollapsed" :collapse-transition="false" router
        class="flex flex-col h-full overflow-clip">
        <!-- 顶部标题 -->
        <p class="outfit-font font-bold text-[26px] text-center my-6">
          Product Dashboard
        </p>

        <!-- 侧边栏上半部分 -->
        <el-menu-item index="/">
          <IconHome :size="22" />
          <span class="menu-item">Home</span>
        </el-menu-item>
        <el-menu-item index="/home/profile">
          <IconChart :size="22" />
          <span class="menu-item">Statistic</span>
        </el-menu-item>

        <div class="flex-grow"></div>

        <!-- 侧边栏下半部分 -->
        <el-menu-item @click="setCookieVisible = true">
          <IconCookie :size="22" />
          <span class="menu-item">Cookie</span>
        </el-menu-item>
        <el-menu-item @click="handleLogout">
          <IconLogout :size="22" />
          <span class="menu-item">Logout</span>
        </el-menu-item>
        <el-menu-item @click="handleUnregister">
          <IconUnregister :size="22" />
          <span class="menu-item">Unregister</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 右侧内容区域 -->
    <el-main class="flex flex-col" v-loading="isLoading" element-loading-text="Search ...">
      <el-icon @click="isCollapsed = !isCollapsed" size="24" :class="{'rotate-180': isCollapsed}"
        class="duration-300 m-3">
        <ArrowRightBold />
      </el-icon>
      <router-view :products="products" @search="handleSearch" />
    </el-main>
  </el-container>

  <!-- 设置Cookie对话框 -->
  <el-dialog v-model="setCookieVisible" title="设置Cookie" width="30%" align-center>
    <el-input v-model="cookie" height="20em" :autosize="{ minRows: 6, maxRows: 18 }" type="textarea"
      placeholder="请输入Cookie" />
    <div class="flex flex-wrap justify-between mt-4">
      <el-segmented color="#626aef" v-model="platform" :options="platforms" class="w-1/3 max-w-56" />
      <el-button color="#626aef" type="primary" plain @click="handleSetCookie" class="w-1/3 max-w-48 min-w-12">确定
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";
import IconChart from "@/icons/IconChart.vue";

export default {
  components: { IconChart },
  data() {
    return {
      isLoading: false,
      isCollapsed: false,
      setCookieVisible: false,
      products: [],
      cookie: "", // 输入的 Cookie
      platform: "淘宝", // Cookie 对应的平台
      platforms: ["淘宝", "京东"], // Cookie 支持的平台
    };
  },
  methods: {
    handleLoading(isLoading) {
      this.isLoading = isLoading;
    },
    async handleLogout() {
      try {
        const response = await axios.delete("/logout");
        if (response.data.success) {
          ElMessage.success(response.data.message);
        } else {
          ElMessage.error(response.data.message);
        }
        localStorage.removeItem("user");
        this.$router.push("/login");
      } catch (error) {
        ElMessage.error(error.message);
      }
    },
    async handleUnregister() {
      try {
        const response = await axios.delete("/unregister");
        if (response.data.success) {
          ElMessage.success(response.data.message);
        } else {
          ElMessage.error(response.data.message);
        }
        localStorage.removeItem("user");
        this.$router.push("/login");
      } catch (error) {
        ElMessage.error(error.message);
      }
    },
    async handleSetCookie() {
      try {
        const response = await axios.put("/cookie", {
          platform: this.platform,
          cookie: JSON.parse(this.cookie),
        });
        if (response.data.success) {
          ElMessage.success(response.data.message);
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
    async handleSearch(keyword) {
      if (!keyword) {
        ElMessage.warning("输入不能为空");
        return;
      }
      // 从数据库中搜索商品
      this.isLoading = true;
      this.products = [];
      try {
        const response = await axios.get(`/search?keyword=${keyword}`);
        if (response.data.success) {
          this.products = response.data.products;
          ElMessage.success(response.data.message);
          this.isLoading = false;
        } else {
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        this.isLoading = false;
        ElMessage.error(error.message);
        return;
      }
      this.isLoading = false;

      // 使用爬虫爬取最新数据
      let new_products = [];
      try {
        const response = await axios.put(`/search?keyword=${keyword}`);
        if (response.data.success) {
          new_products = response.data.products;
          ElMessage.success(response.data.message);
        } else {
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        ElMessage.error(error.message);
      }

      // 若商品中已存在，则更新；否则添加
      for (let new_product of new_products) {
        let index = this.products.findIndex(
          (product) => product.id === new_product.id
        );
        if (index !== -1) {
          this.products[index] = new_product;
        } else {
          this.products.push(new_product);
        }
      }
    },
  },
  computed: {
    user() {
      return JSON.parse(localStorage.getItem("user"));
    },
    totalCollapse() {
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
.menu-item {
  margin-left: 12px;
  font-size: 16px;
  font-weight: 500;
}
.total-collapse {
  --el-aside-width: 0px;
  --el-menu-icon-width: 0px;
  --el-menu-base-level-padding: 0px;
}
.un-colllapse {
  --el-aside-width: 280px;
}
</style>