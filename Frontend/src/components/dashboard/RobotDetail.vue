<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 backdrop-blur-xs transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6"
            >
              <div>
                <div class="flex items-center justify-between border-b pb-4">
                  <div class="flex items-center">
                    <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-indigo-100">
                      <img
                        v-if="robot.imageUrl"
                        :src="robot.imageUrl"
                        :alt="robot.name"
                        class="h-10 w-10 rounded-full object-cover"
                      />
                      <IdentificationIcon v-else class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                    </div>
                    <div class="mt-3 ml-3 text-center sm:text-left">
                      <DialogTitle as="h3" class="text-base font-semibold leading-6 text-gray-900">
                        {{ robot.name }}
                      </DialogTitle>
                      <div class="text-xs text-gray-500" :title="robot.id">ID: {{ robot.id }}</div>
                    </div>
                  </div>

                  <div :class="[statusClasses[robot.status?.status || 'unknow'], 'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset']">
                    {{ getStatusTranslation(robot.status?.status || 'unknow') }}
                  </div>
                </div>

                <div class="mt-4">
                  <div class="mt-2 flex justify-between border-b py-2">
                    <div class="text-sm font-medium text-gray-500">{{ $t('robot.detail.onlineStatus') }}</div>
                    <div class="text-sm text-gray-900 flex items-center">
                      <span class="inline-block h-2 w-2 rounded-full mr-2"
                        :class="robot.status?.isOnline ? 'bg-green-400' : 'bg-red-400'" />
                        {{ robot.status?.isOnline ? $t('robot.detail.online') : $t('robot.detail.offline') }}
                    </div>
                  </div>

                  <div class="mt-2 flex justify-between border-b py-2">
                    <div class="text-sm font-medium text-gray-500">{{ $t('robot.detail.power') }}</div>
                    <div class="text-sm text-gray-900">
                      <div class="w-24 bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                        <div
                          class="h-2.5 rounded-full"
                          :class="batteryColorClass"
                          :style="`width: ${batteryPercentage}%`"
                        ></div>
                      </div>
                      <div class="text-xs mt-1 text-right">
                        <span v-if="robot.status?.isCharging" class="text-xs text-gray-500">{{ $t('home.inCharge') }}</span>
                        {{ batteryPercentage }}%
                      </div>
                    </div>
                  </div>

                  <div class="mt-2 flex justify-between border-b py-2">
                    <div class="text-sm font-medium text-gray-500">{{ $t('robot.detail.chargingStatus') }}</div>
                    <div class="text-sm text-gray-900">
                      <div class="text-xs mt-1 text-right">{{ chargingStatusText }}</div>
                    </div>
                  </div>

                  <div class="mt-2 flex justify-between border-b py-2">
                    <div class="text-sm font-medium text-gray-500">{{ $t('home.warehouseID') }}</div>
                    <div class="text-sm text-gray-900">{{ robot.cabinId || $t('common.unknown') }}</div>
                  </div>

                  <div class="mt-2 flex justify-between border-b py-2">
                    <div class="text-sm font-medium text-gray-500">{{ $t('robot.detail.location') }}</div>
                    <div class="text-sm text-gray-900">{{ robot.status?.location || $t('robot.detail.unknownLocation') }}</div>
                  </div>

                  <div class="mt-2 flex justify-between border-b py-2">
                    <div class="text-sm font-medium text-gray-500">{{ $t('robot.detail.lastMessage') }}</div>
                    <div class="text-sm text-gray-900 max-w-xs truncate" :title="robot.status?.message">
                      {{ robot.status?.message || $t('robot.detail.noMessage') }}
                    </div>
                  </div>

                  <div class="mt-2 flex justify-between py-2">
                    <div class="text-sm font-medium text-gray-500">{{ $t('robot.detail.lastActivity') }}</div>
                    <div class="text-sm text-gray-900">{{ formatDate(robot.lastActivity) }}</div>
                  </div>
                </div>
              </div>

              <div class="mt-5 sm:mt-6 flex justify-between">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  @click="control"
                >
                  {{ $t('robot.detail.controlRobot') }}
                </button>
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  @click="closeModal"
                >
                  {{ $t('robot.detail.close') }}
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { computed } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { IdentificationIcon } from '@heroicons/vue/24/outline'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  isOpen: Boolean,
  robot: {
    type: Object,
    default: () => ({
      id: '',
      name: '',
      imageUrl: '',
      status: {
        isOnline: false,
        power: 0,
        isCharging: false,
        status: '未知',
        message: '',
        location: ''
      },
      lastActivity: new Date()
    })
  }
})

const emit = defineEmits(['update:isOpen', 'controlRobot'])

const statusClasses = {
  '空闲': 'text-green-700 bg-green-50 ring-green-600/20',
  '执行任务中': 'text-yellow-600 bg-yellow-50 ring-yellow-500/30',
  '未知': 'text-gray-600 bg-gray-50 ring-gray-500/10',
  '错误': 'text-red-700 bg-red-50 ring-red-600/10'
}

const batteryPercentage = computed(() => {
  const power = props.robot.status?.power || 0
  return typeof power === 'number' ? power : parseInt(power) || 0
})

const chargingStatusText = computed(() => {
  return props.robot.status.isCharging ? t('robot.detail.charging') : t('robot.detail.notCharging')
})

const batteryColorClass = computed(() => {
  if (batteryPercentage.value > 50) return 'bg-green-600'
  if (batteryPercentage.value > 20) return 'bg-yellow-300'
  return 'bg-red-600'
})

function closeModal() {
  emit('update:isOpen', false)
}

function control() {
  emit('controlRobot', props.robot)
  closeModal()
}

function getStatusTranslation(status) {
  return t(`robot.status.${status === '空闲' ? 'idle' : 
                            status === '执行任务中' ? 'busy' : 
                            status === '错误' ? 'error' : 'unknown'}`)
}

function formatDate(date) {
  if (!date) return t('robot.detail.unknownDate')

  try {
    const dateObj = new Date(date)
    return new Intl.DateTimeFormat('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }).format(dateObj)
  } catch (e) {
    return t('robot.detail.invalidDate')
  }
}

</script>