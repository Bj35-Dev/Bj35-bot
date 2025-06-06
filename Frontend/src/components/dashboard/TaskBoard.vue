<!--
Copyright (c) 2025 Cg8-5712
Permission is granted to use, read, and study this code strictly for personal and non-commercial educational purposes only.
Any reproduction, modification, distribution, or use of this code — in whole or in part — in competitions, contests,
academic evaluations, commercial activities, or any form of official submissions is strictly prohibited without the
prior written consent of the author.
This software is NOT open-source. It is released under a custom license based on CC BY-NC-ND 4.0.
For licensing inquiries, contact: 5712.cg8@gmail.com.
My GitHub profile: https://github.com/cg8-5712/

版权所有 (c) 2025 Cg8-5712
仅允许出于个人学习和非商业教育目的使用、阅读和研究本代码。
未经作者书面授权，严禁将本代码（包括全部或部分）用于比赛、竞赛、学术评审、商业活动或任何形式的官方成果提交。
本软件不是开源项目，授权条款基于 CC BY-NC-ND 4.0（https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh）。
-->
<template>
  <div class="p-4">
    <!-- 标题与说明 -->
    <div class="mb-5">
      <h1 class="text-2xl font-semibold text-gray-900">{{ $t('taskBoard.title') }}</h1>
      <p class="mt-1 text-sm text-gray-500">{{ $t('taskBoard.description') }}</p>
    </div>

    <!-- 加载中状态 -->
    <div v-if="loading" class="flex justify-center items-center h-64">
<!--      <div class="text-gray-500">{{ $t('taskBoard.loading') }}</div>-->
    </div>

    <!-- 数据展示 -->
    <div v-else>
      <!-- 每页展示条数选择 -->
      <div class="mb-4 flex justify-end items-center">
        <label class="mr-2 text-sm text-gray-700">{{ $t('taskBoard.rowsPerPage') }}</label>
        <select v-model.number="pageSize" class="border border-gray-300 rounded-md p-1">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </div>

      <transition :name="transitionName" mode="out-in">
        <!-- 任务列表表格 -->
        <div class="overflow-x-auto" :key="currentPage">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{{ $t('taskBoard.taskNo') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{{ $t('taskBoard.createdAt') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{{ $t('taskBoard.status') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{{ $t('taskBoard.target') }}</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="task in pagedTasks"
                :key="task.no"
                class="cursor-pointer hover:bg-gray-100"
                @click="openTaskDetail(task)"
              >
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ task.no }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatTime(task.createdAt) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div :class="[statuses[task.status], 'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset']">{{ task.status }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ task.target }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </transition>


      <!-- 分页控件，集成了移动端和桌面端样式 -->
      <div class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 mt-4">
        <!-- 移动端视图 -->
        <div class="flex flex-1 justify-between sm:hidden">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            {{ $t('taskBoard.pagination.previous') }}
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            {{ $t('taskBoard.pagination.next') }}
          </button>
        </div>
        <!-- 桌面端视图 -->
        <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              {{ $t('taskBoard.pagination.showing') }}
              <span class="font-medium">{{ firstItem }}</span>
              {{ $t('taskBoard.pagination.to') }}
              <span class="font-medium">{{ lastItem }}</span>
              {{ $t('taskBoard.pagination.of') }}
              <span class="font-medium">{{ totalResults }}</span>
              {{ $t('taskBoard.pagination.results') }}
            </p>
          </div>
          <div>
            <nav class="isolate inline-flex -space-x-px rounded-md shadow-xs" aria-label="Pagination">
              <button
                @click="prevPage"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
              >
                <span class="sr-only">{{ $t('taskBoard.pagination.previous') }}</span>
                <ChevronLeftIcon class="h-5 w-5" aria-hidden="true" />
              </button>
              <template v-for="page in pages" :key="page">
                <template v-if="page === '...'">
                  <span class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-gray-300 ring-inset">
                    ...
                  </span>
                </template>
                <template v-else>
                  <button
                    @click="setPage(page)"
                    :aria-current="page === currentPage ? 'page' : null"
                    :class="page === currentPage ? 'relative z-10 inline-flex items-center bg-indigo-600 px-4 py-2 text-sm font-semibold text-white focus:z-20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600' : 'relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0'"
                  >
                    {{ page }}
                  </button>
                </template>
              </template>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
              >
                <span class="sr-only">{{ $t('taskBoard.pagination.next') }}</span>
                <ChevronRightIcon class="h-5 w-5" aria-hidden="true" />
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务详情弹窗 -->
    <transition name="fade">
      <div
        v-if="showModal"
        class="fixed inset-0 flex items-center justify-center backdrop-blur-xs z-15"
      >
        <div class="bg-white rounded-lg shadow-lg p-6 w-96">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-900">{{ $t('taskBoard.modal.title') }}</h2>
            <button @click="closeModal" class="text-gray-500 hover:text-gray-700">&times;</button>
          </div>
          <div class="space-y-2 text-sm text-gray-800">
            <div><span class="font-medium">{{ $t('taskBoard.modal.taskNo') }}:</span> {{ selectedTask.no }}</div>
            <div><span class="font-medium">{{ $t('taskBoard.modal.taskId') }}:</span> {{ selectedTask.taskId }}</div>
            <div><span class="font-medium">{{ $t('taskBoard.modal.outTaskId') }}:</span> {{ selectedTask.outTaskId }}</div>
            <div>
              <span class="font-medium">{{ $t('taskBoard.modal.createdAt') }}:</span>
              {{ formatTime(selectedTask.createdAt) }}
            </div>
            <div>
              <span class="font-medium">{{ $t('taskBoard.modal.updatedAt') }}:</span>
              {{ formatTime(selectedTask.updatedAt) }}
            </div>
            <div><span class="font-medium">{{ $t('taskBoard.modal.status') }}:</span> {{ selectedTask.status }}</div>
            <div><span class="font-medium">{{ $t('taskBoard.modal.taskType') }}:</span> {{ selectedTask.taskType }}</div>
            <div><span class="font-medium">{{ $t('taskBoard.modal.target') }}:</span> {{ selectedTask.target }}</div>
          </div>
        </div>
      </div>
    </transition>
    <main class="py-10">
        <div class="px-4 sm:px-6 lg:px-8">
          <LoadingSpinner v-if="loading" :message="$t('common.loading')" />
          <Suspense v-else>
            <template #default>
              <component :is="currentComponent" />
            </template>
            <template #fallback>
              <LoadingSpinner :message="$t('taskBoard.renderingComponent')" color="indigo" />
            </template>
          </Suspense>
        </div>
      </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import ApiServices from '@/services/ApiServices'
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/20/solid'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const statuses = {
  'SUCCESS': 'text-green-700 bg-green-50 ring-green-600/20 max-w-[70px]',
  'FAILED': 'text-red-700 bg-red-50 ring-red-600/10 max-w-[55px]',
  'CREATED': 'text-yellow-600 bg-yellow-50 ring-yellow-500/30 max-w-[70px]',
  'CANCELLED': 'text-gray-600 bg-gray-50 ring-gray-500/10 max-w-[85px]',
  'NOT_FETCH': 'text-red-700 bg-red-50 ring-red-600/10 max-w-[85px]'
}

// Initial data
const tasks = ref([])
const loading = ref(true)
const currentPage = ref(1)
const pageSize = ref(10)
const showModal = ref(false)
const selectedTask = ref({})

const transitionName = ref('slide-left')

// 获取模拟数据（可扩展以测试分页）
const fetchTasks = async () => {
  try {
    const Data = await ApiServices.getTasklist()
    tasks.value = Data
    console.log('获取任务数据成功:', Data)
  } catch (error) {
    console.error('获取任务数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTasks()
})



// 分页相关计算
const totalPages = computed(() => Math.ceil(tasks.value.length / pageSize.value) || 1)
const pagedTasks = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return tasks.value.slice(start, start + pageSize.value)
})
const firstItem = computed(() => (tasks.value.length === 0 ? 0 : (currentPage.value - 1) * pageSize.value + 1))
const lastItem = computed(() => Math.min(currentPage.value * pageSize.value, tasks.value.length))
const totalResults = computed(() => tasks.value.length)

// 分页页码简单算法
const pages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  if (current <= 4) {
    return [1, 2, 3, 4, 5, '...', total]
  } else if (current > total - 4) {
    return [1, '...', total - 4, total - 3, total - 2, total - 1, total]
  } else {
    return [1, '...', current - 1, current, current + 1, '...', total]
  }
})

// 翻页方法：更新动画方向
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    transitionName.value = 'slide-left'
    currentPage.value++
  }
}
const prevPage = () => {
  if (currentPage.value > 1) {
    transitionName.value = 'slide-right'
    currentPage.value--
  }
}
const setPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    // 根据页码变化方向决定动画
    transitionName.value = page > currentPage.value ? 'slide-left' : 'slide-right'
    currentPage.value = page
  }
}

// 详情弹窗控制
const openTaskDetail = (task) => {
  selectedTask.value = task
  showModal.value = true
}
const closeModal = () => {
  showModal.value = false
}
const formatTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleString()
}

watch(pageSize, () => {
  currentPage.value = 1
})
</script>

<style scoped>
/* 页面切换动画 */
.slide-left-enter-active,
.slide-left-leave-active {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.slide-left-enter-from {
  transform: translateX(100%);
  opacity: 0;
}
.slide-left-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.slide-right-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}
.slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* 弹窗淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
