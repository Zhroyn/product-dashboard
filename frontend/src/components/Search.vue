<template>
  <!-- 没有商品时的提示 -->
  <template v-if="products.length === 0">
    <div class="w-full h-full flex place-content-center">
      <div class="place-self-center p-12 mb-24">
        <div class="output-font font-extrabold text-5xl 
          text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-pink-500 my-8">
          Welcome to Product Dashboard!
        </div>
        <div class="output-font font-bold text-3xl text-center my-8">
          Let's start by searching for a product.
        </div>
      </div>
    </div>
  </template>

  <!-- 商品卡片列表 -->
  <template v-else>
    <div class="flex flex-wrap justify-center items-start">
      <Product v-for="product in products" :key="product.id" :product="product" />
    </div>
  </template>

  <!-- 搜索框 -->
  <div class="place-content-center min-h-36 search-box flex-none">
    <el-affix position="bottom" :offset="60" class="w-2/3 place-self-center max-w-[720px]">
      <div class="flex place-content-between items-center w-full">
        <el-input v-model="keyword" size="large" placeholder="Waiting for input" class="min-h-12 input-box"
          @keyup.enter="$emit('search', keyword)">
        </el-input>
        <el-button type="primary" color="#626aef" circle class="ml-6 min-h-12 min-w-12 flex place-content-center"
          @click="$emit('search', keyword)">
          <IconSearch />
        </el-button>
      </div>
    </el-affix>
  </div>
</template>

<script>
import { Search } from "@element-plus/icons-vue";

export default {
  components: { Search },
  data() {
    return {
      keyword: "",
    };
  },
  props: ["products"],
  emits: ["search"],
};
</script>

<style scoped>
::v-deep .el-input__inner {
  font-size: 16px;
  padding-left: 6px;
  font-family: "Outfit", "Noto Sans SC";
}
.el-input {
  --el-input-border-radius: 9999px !important;
  --el-input-border-color: #aaa;
  --el-input-hover-border-color: #777;
  --el-input-focus-border-color: #626aef;
}
</style>