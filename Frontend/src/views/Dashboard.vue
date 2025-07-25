<!--
 * @fileoverview Dashboard.vue - 任务看板页面
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
  <div>
    <!-- 移动版侧边栏 -->
    <TransitionRoot as="template" :show="sidebarOpen">
      <Dialog class="relative z-50 lg:hidden" @close="sidebarOpen = false">
        <TransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-gray-900/80" />
        </TransitionChild>

        <div class="fixed inset-0 flex">
          <TransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="-translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="-translate-x-full">
            <DialogPanel class="relative mr-16 flex w-full max-w-xs flex-1">
              <TransitionChild as="template" enter="ease-in-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-300" leave-from="opacity-100" leave-to="opacity-0">
                <div class="absolute top-0 left-full flex w-16 justify-center pt-5">
                  <button type="button" class="-m-2.5 p-2.5" @click="sidebarOpen = false">
                    <span class="sr-only">{{ $t('common.close') }}</span>
                    <XMarkIcon class="size-6 text-white" aria-hidden="true" />
                  </button>
                </div>
              </TransitionChild>
              <!-- Sidebar component -->
              <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-indigo-600 px-6 pb-4">
                <div class="flex h-16 shrink-0 items-center">
                  <img class="h-8 w-auto" src="/src/assets/favicon.svg" alt="BJ35-Bot-Management"/>
                </div>
                <nav class="flex flex-1 flex-col">
                  <ul role="list" class="flex flex-1 flex-col gap-y-7">
                    <li>
                      <ul role="list" class="-mx-2 space-y-1">
                        <li v-for="item in navigation" :key="item.name">
                          <a
                            href="#"
                            :class="[item.current ? 'bg-indigo-700 text-white' : 'text-indigo-200 hover:bg-indigo-700 hover:text-white', 'group flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold']"
                            @click.prevent="setActiveView(item); sidebarOpen = false"
                          >
                            <component :is="item.icon" :class="[item.current ? 'text-white' : 'text-indigo-200 group-hover:text-white', 'size-6 shrink-0']" aria-hidden="true" />
                            {{ $t(item.nameKey) }}
                          </a>
                        </li>
                      </ul>
                    </li>
                  </ul>
                </nav>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- 桌面版侧边栏 - 带平滑过渡效果 -->
    <div
      class="fixed inset-y-0 z-50 flex flex-col transition-all duration-300 ease-in-out overflow-hidden"
      :class="[ isLargeScreen ? 'translate-x-0 w-72' : '-translate-x-full w-0', 'lg:translate-x-0 lg:w-72' ]"
    >
      <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-indigo-600 px-6 pb-4">
        <div class="flex h-16 shrink-0 items-center">
          <img class="h-8 w-auto" src="/src/assets/favicon.svg" alt="BJ35-Bot-Management" />
        </div>
        <nav class="flex flex-1 flex-col">
          <ul role="list" class="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" class="-mx-2 space-y-1">
                <li v-for="item in navigation" :key="item.name">
                  <a
                    href="#"
                    :class="[item.current ? 'bg-indigo-700 text-white' : 'text-indigo-200 hover:bg-indigo-700 hover:text-white', 'group flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold']"
                    @click.prevent="setActiveView(item)"
                  >
                    <component :is="item.icon" :class="[item.current ? 'text-white' : 'text-indigo-200 group-hover:text-white', 'size-6 shrink-0']" aria-hidden="true" />
                    {{ $t(item.nameKey) }}
                  </a>
                </li>
              </ul>
            </li>
            <li class="mt-auto">
              <a
                  href="#"
                  class="group -mx-2 flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold text-indigo-200 hover:bg-indigo-700 hover:text-white"
                  @click.prevent="setActiveView({ componentName: 'Profile' })"
              >
                <Cog6ToothIcon class="size-6 shrink-0 text-indigo-200 group-hover:text-white" aria-hidden="true" />
                {{ $t('nav.settings') }}
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- 主内容区域 - 带平滑过渡效果 -->
    <div
      class="transition-all duration-300 ease-in-out"
      :class="[ isLargeScreen ? 'pl-72' : 'pl-0', 'lg:pl-72' ]"
    >
      <div class="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-xs sm:gap-x-6 sm:px-6 lg:px-8">
        <button type="button" class="-m-2.5 p-2.5 text-gray-700 lg:hidden" @click="sidebarOpen = true">
          <span class="sr-only">{{ $t('common.openSidebar') }}</span>
          <Bars3Icon class="size-6" aria-hidden="true" />
        </button>

        <!-- Separator -->
        <div class="h-6 w-px bg-gray-900/10 lg:hidden" aria-hidden="true" />

        <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
          <div class="grid flex-1 grid-cols-1 items-center">
            <!-- <h1 class="text-lg/6 font-semibold text-gray-900">Dashboard</h1> -->
          </div>
          <div class="flex items-center gap-x-4 lg:gap-x-6">
            <LanguageSwitcher />
            <button type="button" class="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500">
              <span class="sr-only">{{ $t('common.viewNotifications') }}</span>
              <BellIcon class="size-6" aria-hidden="true" />
            </button>

            <!-- Separator -->
            <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />

            <!-- Profile dropdown -->
            <Menu as="div" class="relative">
              <MenuButton class="-m-1.5 flex items-center p-1.5">
                <span class="sr-only">{{ $t('common.openUserMenu') }}</span>
                <img class="size-8 rounded-full bg-gray-50" :src="useravatar" alt="" />
                <span class="hidden lg:flex lg:items-center">
                  <span class="ml-4 text-sm/6 font-semibold text-gray-900" aria-hidden="true"> {{ username }} </span>
                  <ChevronDownIcon class="ml-2 size-5 text-gray-400" aria-hidden="true" />
                </span>
              </MenuButton>
              <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                <MenuItems class="absolute right-0 z-10 mt-2.5 w-32 origin-top-right rounded-md bg-white py-2 ring-1 shadow-lg ring-gray-900/5 focus:outline-hidden">
                  <MenuItem v-for="item in userNavigation" :key="item.name" v-slot="{ active }">
                    <a
                      href="#"
                      :class="[active ? 'bg-gray-50 outline-hidden' : '', 'block px-3 py-1 text-sm/6 text-gray-900']"
                      @click="item.action ? item.action() : setActiveView(item)"
                    >
                      {{ $t(item.nameKey) }}
                    </a>
                  </MenuItem>

                </MenuItems>
              </transition>
            </Menu>


          </div>
        </div>
      </div>

      <main class="py-10">
        <div class="px-4 sm:px-6 lg:px-8">
          <LoadingSpinner v-if="loading" :message="$t('common.loading')" />
          <Suspense v-else>
            <template #default>
              <component
                :is="currentComponent"
                :robot="selectedRobotForControl"
                @control-robot="switchToTaskPublish"
              />
            </template>
            <template #fallback>
              <LoadingSpinner :message="$t('common.renderingComponent')" color="indigo" />
            </template>
          </Suspense>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted, onBeforeUnmount, defineAsyncComponent } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AuthService from '@/services/AuthService'
import ApiServices from '@/services/ApiServices'
import LanguageSwitcher from '@/components/common/LanguageSwitcher.vue'

import {
  Dialog,
  DialogPanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import {
  Bars3Icon,
  BellIcon,
  ChartBarSquareIcon,
  Cog6ToothIcon,
  DocumentArrowUpIcon,
  HomeIcon,
  XMarkIcon,
} from '@heroicons/vue/24/outline'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const router = useRouter()
const { t } = useI18n()
const sidebarOpen = ref(false)
const isLargeScreen = ref(window.innerWidth >= 1024)
const loading = ref(true)

const username = ref("")
const useravatar = ref("")

const currentComponent = shallowRef(null)
const selectedRobotForControl = ref(null)

function logout() {
  AuthService.logout()
  router.push('/login')
}

const navigation = [
  { name: '主页', nameKey: 'nav.home', href: '#', icon: HomeIcon, current: true, componentName: 'Overview'  },
  { name: '发布任务', nameKey: 'nav.publish', href: '#', icon: DocumentArrowUpIcon, current: false, componentName: 'TaskPublish'  },
  { name: '任务看板', nameKey: 'nav.tasks', href: '#', icon: ChartBarSquareIcon, current: false, componentName: 'TaskBoard'  },
  { name: '开发团队', nameKey: 'nav.team', href: '#', icon: ChartBarSquareIcon, current: false, componentName: 'Team'  },
  { name: '管理页面', nameKey: 'nav.admin', href: '#', icon: ChartBarSquareIcon, current: false, componentName: 'admin'  },
]
const userNavigation = [
  { name: '个人资料', nameKey: 'nav.profile', href: '#', componentName: 'Profile' },
  { name: '退出登录', nameKey: 'common.logout', href: '#', action: logout },
]

const componentMap = {
  Overview: () => import('../components/dashboard/Overview.vue'),
  TaskPublish: () => import('../components/dashboard/TaskPublish.vue'),
  TaskBoard: () => import('../components/dashboard/TaskBoard.vue'),
  Profile: () => import('../components/dashboard/Profile.vue'),
  Team: () => import('../components/dashboard/team.vue')
}
const activeView = ref(navigation[0])

async function setActiveView(item, robotData = null) {
  loading.value = true

  try {
    // 更新导航项的当前状态
    navigation.forEach(nav => {
      nav.current = nav === item || nav.componentName === item.componentName
    })

    // 设置活动视图
    activeView.value = item

    // 存储选中的机器人（如果有）
    if (robotData) {
      selectedRobotForControl.value = robotData
    } else {
      selectedRobotForControl.value = null
    }

    // 异步加载新组件
    const AsyncComponent = defineAsyncComponent(componentMap[item.componentName])
    currentComponent.value = AsyncComponent
  } catch (error) {
    console.error(`加载组件 ${item.componentName} 失败:`, error)
  } finally {
    loading.value = false
  }
}

// 提供切换到任务发布界面的方法
function switchToTaskPublish(robotData) {
  const taskPublishItem = navigation.find(item => item.componentName === 'TaskPublish')
  if (taskPublishItem) {
    setActiveView(taskPublishItem, robotData)
  }
}


// 监听窗口大小变化
function handleResize() {
  isLargeScreen.value = window.innerWidth >= 1024
  // 如果切换到大屏幕，关闭移动侧边栏
  if (isLargeScreen.value) {
    sidebarOpen.value = false
  }
}

// 在组件挂载时添加事件监听器
onMounted(async () => {
  username.value = AuthService.getUsername()
  
  // 这里可以保持使用统一的 ApiServices 接口
  useravatar.value = await ApiServices.getUserAvatar()
  
  window.addEventListener('resize', handleResize)
  await setActiveView(navigation[0])
})

// 在组件卸载前移除事件监听器
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})
</script>
