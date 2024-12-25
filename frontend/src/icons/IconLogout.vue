<template>
  <svg t="1735137070692" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
    p-id="5940" :width="size" :height="size">
    <path fill="currentColor"
      d="M128 213.333333c0-46.933333 38.4-85.333333 85.333333-85.333333h341.333334v85.333333H213.333333v597.333334h341.333334v85.333333H213.333333c-46.933333 0-85.333333-38.4-85.333333-85.333333V213.333333z m604.842667 256L624.64 361.130667l60.330667-60.330667 211.2 211.2-211.2 211.2-60.330667-60.330667L732.842667 554.666667H451.84v-85.333334h281.002667z"
      p-id="5941"></path>
  </svg>
</template>

<script>
export default {
  props: {
    size: {
      type: Number,
      default: 24,
    }
  },
  name: "IconLogout",
};
</script>