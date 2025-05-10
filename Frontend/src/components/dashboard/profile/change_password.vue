<template>
  <div class="max-w-7xl lg:px-16 pt-16">
    <div class="px-4 py-16 sm:px-0 lg:px-0 lg:py-20">
      <div class="mx-auto max-w-2xl space-y-16 sm:space-y-20">
        <div>
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-base font-semibold text-gray-900">修改密码</h2>
            <button
              @click="goBack"
              class="text-sm text-indigo-600 hover:text-indigo-500"
            >
              返回
            </button>
          </div>

          <form @submit.prevent="handlePasswordChange" class="mt-6 space-y-6">
            <div class="border-t border-gray-100">
              <dl class="divide-y divide-gray-100">
                <div class="py-6 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium text-gray-900">当前密码</dt>
                  <dd class="mt-1 sm:col-span-2 sm:mt-0">
                    <input
                      type="password"
                      v-model="currentPassword"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                      required
                    />
                  </dd>
                </div>

                <div class="py-6 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium text-gray-900">新密码</dt>
                  <dd class="mt-1 sm:col-span-2 sm:mt-0">
                    <input
                      type="password"
                      v-model="newPassword"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                      required
                    />
                  </dd>
                </div>

                <div class="py-6 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium text-gray-900">确认新密码</dt>
                  <dd class="mt-1 sm:col-span-2 sm:mt-0">
                    <input
                      type="password"
                      v-model="confirmPassword"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                      required
                    />
                  </dd>
                </div>
              </dl>
            </div>

            <div class="flex justify-start gap-x-3">
              <button
                type="submit"
                class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                :disabled="isSubmitting"
              >
                {{ isSubmitting ? '提交中...' : '更新密码' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ApiServices from '@/services/ApiServices'
import AuthService from '@/services/AuthService'
import NotificationService from '@/services/NotificationService'

const router = useRouter()
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const isSubmitting = ref(false)

function goBack() {
  router.back()
}

async function handlePasswordChange() {
  if (newPassword.value !== confirmPassword.value) {
    NotificationService.notify('两次输入的新密码不一致', 'error')
    return
  }

  isSubmitting.value = true

  try {
    const response = await ApiServices.changeUserPassword({
      wecom_id: AuthService.getUserWecomId(),
      old_password: currentPassword.value,
      new_password: newPassword.value
    })
    console.log('密码修改成功:', response.data)
    console.log('token:', response)
    if (response.success) {
      NotificationService.notify('密码修改成功，请重新登录', 'success')
      setTimeout(() => {
        AuthService.logout()
        router.push('/login')
      }, 1500)
    } else {
      NotificationService.notify(response.message || '密码修改失败', 'error')
    }
  } catch (error) {
    console.error('密码修改失败:', error)
    NotificationService.notify(error.response?.message || '系统错误，请稍后重试', 'error')
  } finally {
    isSubmitting.value = false
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  }
}
</script>