<template>
  <router-view />
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
:root {
  --el-font-family: "Outfit", "Noto Sans SC";
}
body {
  margin: 0;
  padding: 0;
}
.el-form-item__label {
  font-size: 16px;
  font-weight: 500;
}
.el-loading-spinner .el-loading-text, .el-dialog__title {
  font-size: 20px !important;
}
.el-dialog {
  padding: 24px;
}
.el-dialog__title {
  margin-left: 4px;
  font-weight: 600;
}
.el-menu-item {
  border-radius: 10px;
  margin: 5px 10px;
  height: 45px !important;
}
.el-button {
  font-size: 16px;
  font-weight: 500;
}
.el-segmented {
  --el-segmented-item-selected-bg-color: #626aef;
}
</style>