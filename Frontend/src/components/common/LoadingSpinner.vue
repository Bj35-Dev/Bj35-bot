<!--
 * @fileoverview LoadingSpinner.vue - 通用加载中组件
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
    <div class="text-center py-4">
      <div 
        class="inline-block animate-spin rounded-full border-4 border-t-blue-500 border-r-transparent border-b-blue-500 border-l-transparent" 
        :class="[
          `h-${size} w-${size}`,
          borderColorClass
        ]"
      ></div>
      <p v-if="displayMessage" class="mt-2 text-gray-600">{{ displayMessage }}</p>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  import { useI18n } from 'vue-i18n';
  
  const { t } = useI18n();
  
  const props = defineProps({
    size: {
      type: [String, Number],
      default: 8
    },
    color: {
      type: String,
      default: 'blue'
    },
    message: {
      type: String,
      default: ''
    }
  });
  
  const displayMessage = computed(() => {
    return t('components.loadingSpinner.loading') || props.message;
  });
  
  const borderColorClass = computed(() => {
    const colorMap = {
      blue: 'border-t-blue-500 border-r-transparent border-b-blue-500 border-l-transparent',
      green: 'border-t-green-500 border-r-transparent border-b-green-500 border-l-transparent',
      red: 'border-t-red-500 border-r-transparent border-b-red-500 border-l-transparent',
      yellow: 'border-t-yellow-500 border-r-transparent border-b-yellow-500 border-l-transparent',
      purple: 'border-t-purple-500 border-r-transparent border-b-purple-500 border-l-transparent',
      indigo: 'border-t-indigo-500 border-r-transparent border-b-indigo-500 border-l-transparent',
      gray: 'border-t-gray-500 border-r-transparent border-b-gray-500 border-l-transparent',
    };
    
    return colorMap[props.color] || colorMap.blue;
  });
</script>