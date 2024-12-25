<template>
  <div class="w-64 border-2 border-gray-200 rounded-lg shadow-lg p-2 m-4">
    <div class="flex flex-col">
      <!-- 图片 -->
      <a :href="product.url" target="_blank" rel="noopener noreferrer">
        <img :src="product.image_url" :alt="product.title"
          class="w-full object-cover transform transition-transform duration-300 hover:scale-110" />
      </a>

      <!-- 商品价格和平台来源 -->
      <div class="px-2 mt-1 flex items-center">
        <p class="text-[1.7rem] font-semibold text-red-600">¥{{ product.price }}</p>
        <div class="badge" :class="getPlatform(product.platform)">{{ product.platform }}</div>
      </div>

      <!-- 商品标题 -->
      <div class="px-1 ">
        <a :href="product.url" :title="product.title" target="_blank" rel="noopener noreferrer"
          class="text-sm font-normal text-gray-800 hover:text-red-600 line-clamp-2">
          {{ product.title }}
        </a>
      </div>

      <!-- 商品额外信息 -->
      <div class="flex flex-wrap">
        <div v-for="info in getInfos(product.extra_info)" :key="info.key">
          <span v-if="!info.key.includes('desc')" class="badge" :class="info.key">
            {{ info.value }}
          </span>
        </div>
      </div>

      <div class="flex items-center justify-between px-1 mt-1">
        <!-- 店铺名称 -->
        <a :href="product.shop_url" :title="product.shop_name" target="_blank" rel="noopener noreferrer"
          class="text-sm text-gray-500 line-clamp-1">
          {{ product.shop_name }}
        </a>

        <!-- 操作按钮 -->
        <el-dropdown placement="bottom">
          <el-icon>
            <MoreFilled />
          </el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item :disabled="(haveUpate ? haveAdded : haveSetAlert)" @click="handle_set_alert">
                <el-icon>
                  <FolderAdd />
                </el-icon>
                Add Trace
              </el-dropdown-item>
              <el-dropdown-item :disabled="!(haveUpate ? haveAdded : haveSetAlert)" @click="handle_delete_alert">
                <el-icon>
                  <Delete />
                </el-icon>
                Delete Trace
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
import axios from "axios";

export default {
  props: ["product"],
  data() {
    return {
      haveUpate: false,
      haveAdded: false,
    };
  },
  methods: {
    getInfos(object) {
      let infos = [];
      for (let key in object) {
        if (typeof object[key] === "string") {
          infos.push({ key: key, value: object[key] });
        } else if (Array.isArray(object[key])) {
          for (let item of object[key]) {
            infos.push({ key: key, value: item });
          }
        }
      }
      return infos;
    },
    getPlatform(platform) {
      if (platform === "京东") {
        return "jingdong";
      } else if (platform === "淘宝") {
        return "taobao";
      }
    },
    async handle_set_alert() {
      try {
        const response = await axios.post("/alert", this.product);
        if (response.data.success) {
          localStorage.setItem("user", JSON.stringify(response.data.user));
          ElMessage.success(response.data.message);
          this.haveUpate = true;
          this.haveAdded = true;
        } else {
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        ElMessage.error(error.message);
      }
    },
    async handle_delete_alert() {
      try {
        const response = await axios.delete("/alert", { data: this.product });
        if (response.data.success) {
          localStorage.setItem("user", JSON.stringify(response.data.user));
          ElMessage.success(response.data.message);
          this.haveUpate = true;
          this.haveAdded = false;
        } else {
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        ElMessage.error(error.message);
      }
    },
  },
  computed: {
    haveSetAlert() {
      const user = JSON.parse(localStorage.getItem("user"));
      if (!user) {
        return false;
      }
      const alerts = user.price_alerts;
      for (let alert of alerts) {
        if (alert.product_id === this.product.id) {
          return true;
        }
      }
      return false;
    },
  },
};
</script>


<style>
.badge {
  font-size: 12px;
  padding: 1px 4px;
  margin-left: 0.3rem;
  border-radius: 0.25rem;
  border: 1px solid;
}
.jingdong {
  background-color: #e31c19;
  border-color: #e31c19;
  color: white;
}
.taobao {
  background-color: #ff5001;
  border-color: #ff5001;
  color: white;
}
.express_and_discount {
  border-color: #f56c6c;
  color: #f56c6c;
}
.comment_num {
  background-color: #ff9900;
  border-color: #ff9900;
  color: white;
}
.product_params {
  background-color: #718096;
  border-color: #718096;
  color: white;
}
</style>