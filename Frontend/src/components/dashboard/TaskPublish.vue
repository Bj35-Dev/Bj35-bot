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
  <div class="task-publish-container">
    <!-- 页面标题 -->
    <div class="mb-5">
      <h1 class="text-2xl font-semibold text-gray-900">{{ $t('tasks.publish') }}</h1>
      <p class="mt-1 text-sm text-gray-500">{{ $t('tasks.publishDescription') }}</p>
    </div>

    <!-- 机器人选择与状态部分 -->
    <div class="grid grid-cols-1 gap-6 mb-8 lg:grid-cols-3">
      <!-- 机器人选择 -->
      <div class="p-5 bg-white rounded-lg shadow">
        <h2 class="mb-4 text-lg font-medium text-gray-900">{{ $t('tasks.form.selectRobot') }}</h2>

        <div v-if="loading" class="flex items-center justify-center py-4">
          <div class="w-5 h-5 border-2 border-t-transparent border-gray-500 rounded-full animate-spin"></div>
          <span class="ml-2 text-gray-500">{{ $t('robot.loading') }}</span>
        </div>

        <div v-else-if="!robots.length" class="py-4 text-center text-gray-500">
          {{ $t('robot.noAvailableRobots') }}
        </div>

        <div v-else class="space-y-2">
          <div
            v-for="robot in robots"
            :key="robot.id"
            :class="['flex items-center p-3 rounded-md cursor-pointer border hover:bg-gray-50',
              selectedRobot?.id === robot.id ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200']"
            @click="selectRobot(robot)"
          >
            <div class="flex-shrink-0 p-2 rounded-full" :class="robot.status.isOnline ? 'bg-green-50' : 'bg-red-50'">
              <div class="w-3 h-3 rounded-full" :class="robot.status.isOnline ? 'bg-green-500' : 'bg-red-500'"></div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-900">{{ robot.name }}</p>
              <p class="text-xs text-gray-500">ID: {{ robot.id.substring(0, 8) }}...</p>
            </div>
            <div class="ml-auto text-xs px-2 py-1 rounded" :class="getStatusClass(robot.status.status)">
              {{ getStatusTranslation(robot.status?.status || 'unknow') }}
            </div>
          </div>
        </div>
      </div>

      <!-- 机器人状态 -->
      <div class="p-5 bg-white rounded-lg shadow lg:col-span-2">
        <h2 class="mb-4 text-lg font-medium text-gray-900">{{ $t('robot.statusTitle') }}</h2>

        <div v-if="!selectedRobot" class="py-8 text-center text-gray-500">
          {{ $t('robot.pleaseSelectRobot') }}
        </div>

        <div v-else class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="p-3 bg-gray-50 rounded-md">
              <p class="text-xs text-gray-500">{{ $t('robot.info.location') }}</p>
              <p class="mt-1 text-sm font-medium">{{ selectedRobot.status.location || $t('common.unknown') }}</p>
            </div>
            <div class="p-3 bg-gray-50 rounded-md">
              <p class="text-xs text-gray-500">{{ $t('robot.info.battery') }}</p>
              <div class="mt-1 flex items-center">
                <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    class="h-full rounded-full"
                    :class="getBatteryColorClass(selectedRobot.status.power)"
                    :style="{width: `${selectedRobot.status.power}%`}">
                  </div>
                </div>
                <span class="ml-2 text-sm font-medium">{{ selectedRobot.status.power }}%</span>
              </div>
            </div>
          </div>

          <div class="flex items-center">
            <span class="px-2 py-1 text-xs rounded"
                  :class="getStatusClass(selectedRobot.status.status)">
              {{ getStatusTranslation(selectedRobot.status?.status || 'unknow') }}
            </span>
            <span class="ml-2 text-sm text-gray-500">{{ selectedRobot.status.message }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务创建部分 -->
    <div class="p-5 bg-white rounded-lg shadow mb-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-medium text-gray-900">{{ $t('tasks.form.taskFlow') }}</h2>
        <div>
          <button
            class="px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            @click="addTaskNode"
          >
            {{ $t('tasks.form.addNode') }}
          </button>
        </div>
      </div>

      <!-- 任务流构建区域 -->
      <div class="mt-6 mb-4">
        <div v-if="!taskNodes.length" class="py-8 text-center text-gray-500 border-2 border-dashed border-gray-200 rounded-lg">
          {{ $t('tasks.form.noNodesYet') }}
        </div>

        <TransitionGroup
          name="task-list"
          tag="div"
          class="space-y-3"
        >
          <div
            v-for="(node, index) in taskNodes"
            :key="node.id"
            class="flex items-start p-4 bg-gray-50 rounded-lg border border-gray-200"
          >
            <!-- 任务节点序号 -->
            <div class="flex-shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 font-medium">
              {{ index + 1 }}
            </div>

            <!-- 任务节点内容 -->
            <div class="ml-4 flex-grow">
              <div class="flex items-center mb-2">
                <select
                  v-model="node.type"
                  @change="updateNodeParams(node)"
                  class="block w-36 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="move">{{ $t('tasks.form.move') }}</option>
                  <option value="back">{{ $t('tasks.form.back') }}</option>
                  <option value="send">{{ $t('tasks.form.send') }}</option>
                </select>

                <button
                  @click="removeTaskNode(index)"
                  class="ml-3 text-red-600 hover:text-red-800"
                >
                  <span class="sr-only">{{ $t('common.delete') }}</span>
                  <TrashIcon class="size-6" aria-hidden="true" />
                </button>

                <div class="ml-auto flex items-center">
                  <button
                    v-if="index > 0"
                    @click="moveNodeUp(index)"
                    class="text-gray-500 hover:text-gray-700"
                  >
                    <span class="sr-only">{{ $t('common.moveUp') }}</span>
                    <ArrowUpIcon class="size-6" aria-hidden="true" />
                  </button>
                  <button
                    v-if="index < taskNodes.length - 1"
                    @click="moveNodeDown(index)"
                    class="ml-2 text-gray-500 hover:text-gray-700"
                  >
                    <span class="sr-only">{{ $t('common.moveDown') }}</span>
                    <ArrowDownIcon class="size-6" aria-hidden="true" />
                  </button>
                </div>
              </div>

              <!-- 根据任务类型显示不同的参数 -->
              <div class="mt-2">
                <!-- move 命令：两个带搜索的下拉框(target, user) 和 一个输入框(message) -->
                <div v-if="node.type === 'move'" class="grid grid-cols-3 gap-3">
                  <div>
                    <label class="block text-xs text-gray-500">{{ $t('tasks.form.target') }}</label>
                    <input
                      v-model="node.params.target"
                      :list="`move-target-options-${node.id}`"
                      type="text"
                      :placeholder="$t('tasks.form.searchTarget')"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <datalist :id="`move-target-options-${node.id}`">
                      <option
                        v-for="(optionData, index) in targetOptions"
                        :key="index"
                        :value="optionData.value"
                      >
                        {{ optionData.label }}
                      </option>
                    </datalist>

                  </div>
                  <div>
                    <label class="block text-xs text-gray-500">{{ $t('tasks.form.user') }}</label>
                    <input
                      v-model="node.params.user"
                      :list="`move-user-options-${node.id}`"
                      type="text"
                      :placeholder="$t('tasks.form.searchUser')"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <datalist :id="`move-user-options-${node.id}`">
                      <option
                        v-for="option in userOptions"
                        :key="option.value"
                        :value="option.value"
                      >
                        {{ option.label }}
                      </option>
                    </datalist>
                  </div>
                  <div>
                    <label class="block text-xs text-gray-500">{{ $t('tasks.form.message') }}</label>
                    <input
                      v-model="node.params.message"
                      type="text"
                      :placeholder="$t('tasks.form.enterMessage')"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                </div>

                <!-- back 命令：下拉框选择充电桩 -->
                <div v-else-if="node.type === 'back'" class="grid grid-cols-1 gap-3">
                  <div>
                    <label class="block text-xs text-gray-500">{{ $t('tasks.form.chargePoint') }}</label>
                    <select
                      v-model="node.params.charge_point"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    >
                      <option value="" disabled>{{ $t('tasks.form.selectChargePoint') }}</option>
                      <option value="3F">3F</option>
                      <option value="1F">1F</option>
                    </select>
                  </div>
                </div>

                <!-- send 命令：带搜索下拉框(user) 和 输入框(message) -->
                <div v-else-if="node.type === 'send'" class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs text-gray-500">{{ $t('tasks.form.user') }}</label>
                    <input
                      v-model="node.params.user"
                      :list="`send-user-options-${node.id}`"
                      type="text"
                      :placeholder="$t('tasks.form.searchUser')"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <datalist :id="`send-user-options-${node.id}`">
                      <option
                        v-for="option in userOptions"
                        :key="option.value"
                        :value="option.value"
                      >
                        {{ option.label }}
                      </option>
                    </datalist>
                  </div>
                  <div>
                    <label class="block text-xs text-gray-500">{{ $t('tasks.form.message') }}</label>
                    <input
                      v-model="node.params.message"
                      type="text"
                      :placeholder="$t('tasks.form.enterMessage')"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                </div>

                <!-- 如果需要扩展其他任务类型，可在此添加 -->
                <div v-else class="mt-2">
                  <p class="text-sm text-gray-600">{{ $t('tasks.form.configureParams') }}</p>
                </div>
              </div>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <!-- 提交按钮 -->
      <div class="flex justify-end space-x-3 mt-6">
        <button
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          @click="resetTaskNodes"
        >
          {{ $t('common.reset') }}
        </button>
        <button
          class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          @click="publishTask"
        >
          {{ $t('tasks.form.publish') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { TransitionGroup } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import { useI18n } from 'vue-i18n'
import UserService from '@/services/UserService'
import DeviceService from '@/services/DeviceService'
import TaskService from '@/services/TaskService'
import NotificationService from '@/services/NotificationService'

import {
  ArrowUpIcon,
  ArrowDownIcon,
  TrashIcon
} from '@heroicons/vue/20/solid'

const { t } = useI18n()

// 定义组件的 props
const props = defineProps({
  isOpen: Boolean,
  robot: {
    type: Object,
    default: () => ({})
  }
})

// 状态样式映射
const statusClasses = {
  '空闲': 'bg-green-50 text-text-700',
  '执行任务中': 'bg-yellow-50 text-yellow-600',
  '未知': 'bg-gray-50 text-gray-600',
  '错误': 'bg-red-50 text-red-700'
}

// 状态数据
const robots = ref([])
const loading = ref(true)
const selectedRobot = ref(null)

// 任务节点
const taskNodes = ref([])

// 教室列表
const targetOptions = ref([])

const fetchTargets = async () => {
  try {
    const data = await TaskService.getTargetlist()
    // 假设 data 是数组格式
    targetOptions.value = data
    // 可选：打印结果确认赋值
    console.log(targetOptions.value)
  } catch (error) {
    console.error('获取任务数据失败:', error)
  } finally {
    loading.value = false
  }
}

const userOptions = ref([
  { value: '用户1', label: '用户1' },
  { value: '用户2', label: '用户2' },
  { value: '用户3', label: '用户3' }
])

// 获取状态样式类
function getStatusClass(status) {
  return statusClasses[status] || statusClasses['未知']
}

function getStatusTranslation(status) {
  return t(`robot.status.${status === '空闲' ? 'idle' : 
                            status === '执行任务中' ? 'busy' : 
                            status === '错误' ? 'error' : 'unknown'}`)
}

// 获取电量颜色
function getBatteryColorClass(power) {
  if (power > 50) return 'bg-green-600'
  if (power > 20) return 'bg-yellow-600'
  return 'bg-red-600'
}

// 选择机器人
function selectRobot(robot) {
  selectedRobot.value = robot
}

// 添加任务节点，默认类型为 move，新格式的参数结构
function addTaskNode() {
  console.log(selectedRobot.value)
  if (!selectedRobot.value) {
    showNotification('tasks.notification.noRobot', 'warning')
    return
  }
  taskNodes.value.push({
    id: uuidv4(),
    type: 'move',
    params: {
      target: '',
      user: '',
      message: ''
    }
  })
}

// 移除任务节点
function removeTaskNode(index) {
  taskNodes.value.splice(index, 1)
}

// 节点上移
function moveNodeUp(index) {
  if (index > 0) {
    const temp = taskNodes.value[index]
    taskNodes.value[index] = taskNodes.value[index - 1]
    taskNodes.value[index - 1] = temp
  }
}

// 节点下移
function moveNodeDown(index) {
  if (index < taskNodes.value.length - 1) {
    const temp = taskNodes.value[index]
    taskNodes.value[index] = taskNodes.value[index + 1]
    taskNodes.value[index + 1] = temp
  }
}

// 重置任务节点
function resetTaskNodes() {
  taskNodes.value = []
}

// 根据任务节点类型切换，重置对应的参数数据
function updateNodeParams(node) {
  switch (node.type) {
    case 'move':
      node.params = { target: '', user: '', message: '' }
      break
    case 'back':
      node.params = { charge_point: '' }
      break
    case 'send':
      node.params = { user: '', message: '' }
      break
    default:
      node.params = {}
  }
}

// 判断是否可以发布任务
const canPublish = computed(() => {
  return selectedRobot.value &&
         selectedRobot.value.status.isOnline &&
         taskNodes.value.length > 0
})

// 发布任务
async function publishTask() {
  if (!canPublish.value) {
    NotificationService.notify(t('tasks.notification.invalidParams'), 'error')
    return
  }

  try {
    // 处理所有任务节点
    for (const node of taskNodes.value) {
      if (node.type === 'send') {
        // 发送消息节点
        if (!node.params.user || !node.params.message) {
          NotificationService.notify(t('tasks.notification.specifyUserMessage'), 'warning')
          continue
        }

        try {
          await UserService.sendMessage(node.params.message, node.params.user)
          NotificationService.notify(t('tasks.notification.messageSent', {user: node.params.user}), 'success')
        } catch (error) {
          NotificationService.notify(t('tasks.notification.messageFailure', {error: error.message}), 'error')
        }
      }
    }

    // 将移动任务节点转换为位置列表
    const locations = taskNodes.value
      .filter(node => ['move', 'back'].includes(node.type))
      .map(node => {
        if (node.type === 'move') {
          return node.params.target
        } else if (node.type === 'back') {
          return node.params.charge_point
        }
        return null
      })
      .filter(Boolean)

    // 如果有移动任务，调用RUN API
    if (locations.length > 0) {
      NotificationService.notify(t('tasks.notification.taskPublished'), 'info');
      const response = await DeviceService.runRobotTask(selectedRobot.value.id, locations);

      NotificationService.notify(t('tasks.notification.taskExecuted'), 'success')
      return response;
    }

    NotificationService.notify(t('tasks.notification.allTasksComplete'), 'info')
    return []
  } catch (error) {
    console.error('发布任务失败:', error)
    NotificationService.notify(t('tasks.notification.publishFailed', { error: error.message || t('common.unknown') }), 'error')
  }
}

// 获取所有设备
async function fetchRobots() {
  try {
    loading.value = true

    // 调用DeviceService获取机器人列表
    const response = await DeviceService.getRobotList();

    if (response.code === 0) {
      // 格式化数据以匹配前端结构
      robots.value = response.data.map(robot => ({
        id: robot.deviceId,
        name: robot.name,
        imageUrl: robot.imageUrl || '',
        status: {
          isOnline: robot.status.isOnline,
          power: robot.status.power,
          message: robot.status.message,
          status: robot.status.status,
          location: robot.status.location
        }
      }))
    } else {
      NotificationService.notify(`获取机器人列表失败: ${response.message}`, 'error')
      robots.value = []
    }
  } catch (error) {
    console.error('获取机器人列表失败:', error)
    NotificationService.notify(`获取机器人列表失败: ${error.message || '未知错误'}`, 'error')
  } finally {
    loading.value = false
  }
}

// 提示方法
function showNotification(message, type) {
  NotificationService.notify(t(message), type)
}

// 组件挂载时获取机器人列表
onMounted(() => {
  fetchRobots()
  fetchTargets()
})

// 监听传递的机器人信息并设置为选中的机器人
watch(
  () => props.robot,
  (newRobot) => {
    console.log('[Watch] props.robot changed:', newRobot)
    if (newRobot && newRobot.cabinId) {
      // 封装绑定逻辑
      const bindRobot = () => {
        console.log('[bindRobot] robots array:', robots.value)
        const matchedRobot = robots.value.find(r => r.id === newRobot.id)
        if (matchedRobot) {
          console.log('[bindRobot] Matched robot found:', matchedRobot)
        } else {
          console.log('[bindRobot] No matching robot found, using newRobot:', newRobot)
        }
        selectedRobot.value = matchedRobot || newRobot
        if (taskNodes.value.length === 0) {
          console.log('[bindRobot] taskNodes empty, adding default task node')
          addTaskNode()
        }
      }

      // 定义等待 robots 数组加载的函数，每隔 500 毫秒检查一次
      const waitForRobots = () => {
        console.log('[waitForRobots] robots.length:', robots.value.length)
        if (robots.value.length > 0) {
          console.log('[waitForRobots] robots list loaded, proceeding to bind')
          bindRobot()
        } else {
          console.log('[waitForRobots] robots not loaded yet, retrying in 500ms...')
          setTimeout(waitForRobots, 500)
        }
      }

      if (robots.value.length === 0) {
        console.log('[Watch] robots array is empty at the moment, starting waitForRobots()')
        waitForRobots()
      } else {
        console.log('[Watch] robots array already loaded')
        bindRobot()
      }
    }
  },
  { immediate: true }
)

</script>


<style scoped>
.task-list-move,
.task-list-enter-active,
.task-list-leave-active {
  transition: all 0.5s ease;
}

.task-list-enter-from,
.task-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.task-list-leave-active {
  position: absolute;
}
</style>