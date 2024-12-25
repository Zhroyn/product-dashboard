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
        <div class="badge platform">{{ product.platform }}</div>
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
        <div v-for="info in getItems(product.extra_info)" :key="info.key">
          <span v-if="!info.key.includes('desc')" class="badge" :class="info.key">
            {{ info.value }}
          </span>
        </div>
      </div>

      <!-- 店铺名称 -->
      <div class="flex px-1 mt-1">
        <a :href="product.shop_url" :title="product.shop_name" target="_blank" rel="noopener noreferrer"
          class="text-sm text-gray-500 line-clamp-1">
          {{ product.shop_name }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
import axios from "axios";

export default {
  props: ["product"],
  methods: {
    getItems(object) {
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
.platform {
  background-color: #f04747;
  border-color: #f04747;
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