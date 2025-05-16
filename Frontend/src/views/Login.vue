<!--
 * @fileoverview Login.vue - 登录页面
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="w-full sm:max-w-[480px] p-6">
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <img class="mx-auto h-10 w-auto" src="@/assets/favicon.svg" alt="Login" />
        <h2 class="mt-6 text-center text-2xl/9 font-bold tracking-tight text-gray-900">{{ $t('login.title') }}</h2>
      </div>

      <div class="mt-10 sm:mx-auto sm:w-full">
        <div class="bg-white px-6 py-12 shadow-md rounded-lg sm:px-12">
          <form class="space-y-6" @submit.prevent="handleLogin">
            <div>
              <label for="username" class="block text-sm/6 font-medium text-gray-900">{{ $t('common.username') }}</label>
              <div class="mt-2">
                <input v-model="username" type="text" name="username" id="username" autocomplete="username" required="" class="border border-solid border-zinc-200 block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
              </div>
            </div>

            <div>
              <label for="password" class="block text-sm/6 font-medium text-gray-900">{{ $t('common.password') }}</label>
              <div class="mt-2">
                <input v-model="password" type="password" name="password" id="password" autocomplete="current-password" required="" class="border border-solid border-zinc-200 block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
              </div>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex gap-3">
                <div class="flex h-6 shrink-0 items-center">
                  <div class="group grid size-4 grid-cols-1">
                    <input v-model="rememberMe" id="remember-me" name="remember-me" type="checkbox" class="col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white checked:border-indigo-600 checked:bg-indigo-600 indeterminate:border-indigo-600 indeterminate:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 forced-colors:appearance-auto"/>
                    <svg class="pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white group-has-disabled:stroke-gray-950/25" viewBox="0 0 14 14" fill="none">
                      <path class="opacity-0 group-has-checked:opacity-100" d="M3 8L6 11L11 3.5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                      <path class="opacity-0 group-has-indeterminate:opacity-100" d="M3 7H11" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </div>
                </div>
                <label for="remember-me" class="block text-sm/6 text-gray-900">{{ $t('login.rememberMe') }}</label>
              </div>
            </div>

            <div class="space-y-4">
              <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">{{ $t('login.loginWithAccount') }}</button>
              <button @click="handleWeComLogin" type="button" class="flex w-full justify-center rounded-md bg-green-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-green-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-600">
                {{ $t('login.loginWithWecom') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

import AuthService from '@/services/AuthService'
import NotificationService from '@/services/NotificationService'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()

const username = ref('')
const password = ref('')
const rememberMe = ref(Boolean)

rememberMe.value = true

async function validateToken(token) {
  try {
    NotificationService.notify(t('login.validatingCredentials'), 'info')
    const isValid = await AuthService.validateToken(token)
    
    if (isValid) {
      NotificationService.notify(t('login.wecomLoginSuccess'), 'success')
      router.push({path: '/', replace: true});
    } else {
      NotificationService.notify(t('login.invalidCredentials'), 'error')
    }
  } catch (error) {
    console.error('Token validation failed:', error.message)
    NotificationService.notify(t('login.validationFailed') + error.message, 'error')
  }
}

onMounted(() => {
  const token = route.query.token
  const error = route.query.error
  if (token) {
    validateToken(token)
  } else if (error) {
    NotificationService.notify(t('login.loginFailed') + error, 'error')
  }
})

async function handleWeComLogin() {
  window.location.href = `${import.meta.env.VITE_APP_API_URL}/auth/wecom`
}

async function handleLogin() {
  try {
    NotificationService.notify(t('login.loggingIn'), 'info')
    await AuthService.login(username.value, password.value, rememberMe.value)

    if (AuthService.isAuthenticated()) {
      NotificationService.notify(t('login.loginSuccess'), 'success')
      router.push('/')
    } else {
      NotificationService.notify(t('login.checkCredentials'), 'error')
    }
  } catch (error) {
    console.error('Failed to login:', error.message)
    NotificationService.notify(t('login.systemError') + error.message, 'error')
  }
}
</script>