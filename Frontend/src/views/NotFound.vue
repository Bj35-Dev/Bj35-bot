<!--
 * @fileoverview NotFound.vue - 404页面
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
    <div>
        <main class="mx-auto flex w-full max-w-7xl flex-auto flex-col justify-center px-6 py-24 sm:py-64 lg:px-8">
            <div class="text-center">
            <p class="text-base font-semibold text-indigo-600">404</p>
            <h1 class="mt-4 text-5xl font-semibold tracking-tight text-balance text-gray-900 sm:text-7xl">{{ $t('notFound.pageNotFound') }}</h1>
            <p class="mt-6 text-lg font-medium text-pretty text-gray-500 sm:text-xl/8">{{ $t('notFound.waitingForContent') }}</p>
            <div class="mt-10 flex items-center justify-center gap-x-6">
                <a href="/" class="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">{{ $t('notFound.backToHome') }}</a>
            </div>
            </div>
        </main>
    </div>
  </template>

  <script setup>
  import { useI18n } from 'vue-i18n';
  
  const { t } = useI18n();
  </script>