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
  <header class="fixed inset-x-0 top-0 z-50 flex h-16 border-b border-gray-900/10">
    <div class="mx-auto flex w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <div class="flex flex-1 items-center gap-x-6">
        <button type="button" class="-m-3 p-3 md:hidden" @click="mobileMenuOpen = true">
          <span class="sr-only">Open main menu</span>
          <Bars3Icon class="size-5 text-gray-900" aria-hidden="true" />
        </button>
      </div>
      <!-- 在桌面环境下，增加了 overflow-x-auto 和 whitespace-nowrap -->
      <nav class="hidden md:flex md:overflow-x-auto md:whitespace-nowrap md:gap-x-11 md:text-sm/6 md:font-semibold">
        <a
          v-for="(item, itemIdx) in navigation"
          :key="itemIdx"
          :href="item.href"
          class="text-gray-700 hover:text-indigo-600"
          @click.prevent="item.action ? item.action() : null"
        >
          <component
            v-if="item.icon"
            :is="item.icon"
            class="size-6 mr-1"
            aria-hidden="false"
          />
          {{ $t(`profile.${item.name.toLowerCase()}`) }}
        </a>
      </nav>
      <div class="flex flex-1 items-center justify-end gap-x-8">
        <!-- 这里可以添加额外的右侧元素 -->
      </div>
    </div>
    <Dialog class="lg:hidden" @close="mobileMenuOpen = false" :open="mobileMenuOpen">
      <div class="fixed inset-0 z-50" />
      <DialogPanel class="fixed inset-y-0 left-0 z-50 w-full overflow-y-auto bg-white px-4 pb-6 sm:max-w-sm sm:px-6 sm:ring-1 sm:ring-gray-900/10">
        <div class="-ml-0.5 flex h-16 items-center gap-x-6">
          <button type="button" class="-m-2.5 p-2.5 text-gray-700" @click="mobileMenuOpen = false">
            <span class="sr-only">{{ $t('common.close') }}</span>
            <XMarkIcon class="size-6" aria-hidden="true" />
          </button>
          <div class="-ml-0.5">
            <a href="#" class="-m-1.5 block p-1.5">
              <span class="sr-only">Your Company</span>
              <img class="h-8 w-auto" src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=600" alt="" />
            </a>
          </div>
        </div>
        <div class="mt-2 space-y-2">
          <a
            v-for="item in navigation"
            :key="item.name"
            :href="item.href"
            class="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50"
            @click.prevent="item.action ? item.action() : null"
          >
            <component
              v-if="item.icon"
              :is="item.icon"
              :class="[item.current ? 'text-indigo-600' : 'text-gray-400', 'size-6 shrink-0 mr-1']"
              aria-hidden="true"
            />
            {{ $t(`profile.${item.name.toLowerCase()}`) }}
          </a>
        </div>
      </DialogPanel>
    </Dialog>
  </header>

  <div class="max-w-7xl lg:px-16 pt-16">
    <h1 class="sr-only">{{ $t('settings.profile') }}</h1>
    <main class="px-4 py-16 sm:px-0 lg:px-0 lg:py-20">
      <div v-if="!showChangePassword">
        <div class="flex justify-end mb-8">
          <div class="relative inline-block">
            <img :src="profile.avatar" alt="Avatar" class="w-64 h-66 rounded-full object-cover" />
            <button
              class="absolute bottom-4 right-4 bg-white p-2 rounded-full shadow hover:bg-gray-100"
              @click="openCropper"
            >
              <PencilIcon class="w-5 h-5 text-gray-700" />
            </button>
          </div>
        </div>
        <div class="mx-auto max-w-2xl space-y-16 sm:space-y-20">
          <div>
            <h2 class="text-base font-semibold text-gray-900">{{ $t('profile.title') }}</h2>
            <dl class="mt-6 divide-y divide-gray-100 border-t border-gray-200 text-sm">
              <div v-for="(value, key) in profileData" :key="key" class="py-6 sm:flex">
                <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">{{ $t(`profile.personalInfo.${key.toLowerCase().replace(/\s+/g, '')}`) }}</dt>
                <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                  <div class="text-gray-900 flex items-center">
                    <template v-if="editingField === key">
                      <input
                        type="text"
                        v-model="editingValue"
                        @keyup.enter="saveField(key)"
                        class="border border-gray-300 rounded p-1"
                      />
                      <span v-if="key === 'Wecom'" class="ml-2 text-gray-400">@北京三十五中</span>
                    </template>
                    <template v-else>
                      {{ value }}
                      <span v-if="key === 'Wecom'" class="ml-2 text-gray-400">@北京三十五中</span>
                    </template>
                  </div>
                  <div class="flex items-center gap-x-2">
                    <button
                      type="button"
                      class="font-semibold text-indigo-600 hover:text-indigo-500"
                      @click="editingField === key ? saveField(key) : updateField(key)"
                    >
                      {{ editingField === key ? $t('profile.actions.save') : $t('profile.actions.update') }}
                    </button>
                  </div>
                </dd>
              </div>
            </dl>
          </div>
          <div>
            <h2 class="text-base font-semibold text-gray-900">{{ $t('profile.languageAndDates.title') }}</h2>
            <p class="mt-1 text-sm text-gray-500">{{ $t('profile.languageAndDates.description') }}</p>
            <dl class="mt-6 divide-y divide-gray-100 border-t border-gray-200 text-sm">
              <div class="py-6 sm:flex">
                <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">{{ $t('profile.languageAndDates.language') }}</dt>
                <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                  <div class="text-gray-900">
                    <template v-if="editingLanguage">
                      <select v-model="currentLanguage" class="border border-gray-300 rounded p-1">
                        <option v-for="option in languageOptions" :key="option" :value="option">{{ option }}</option>
                      </select>
                    </template>
                    <template v-else>
                      {{ currentLanguage }}
                    </template>
                  </div>
                  <button type="button" @click="toggleLanguageEdit" class="font-semibold text-indigo-600 hover:text-indigo-500">
                    {{ editingLanguage ? $t('profile.actions.save') : $t('profile.actions.update') }}
                  </button>
                </dd>
              </div>
              <div class="py-6 sm:flex">
                <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">{{ $t('profile.languageAndDates.dateFormat') }}</dt>
                <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                  <div class="text-gray-900">DD-MM-YYYY</div>
                  <button type="button" class="font-semibold text-indigo-600 hover:text-indigo-500">{{ $t('profile.actions.update') }}</button>
                </dd>
              </div>
              <SwitchGroup as="div" class="flex pt-6">
                <SwitchLabel as="dt" class="flex-none pr-6 font-medium text-gray-900 sm:w-64" passive>
                  {{ $t('profile.languageAndDates.automaticTimezone') }}
                </SwitchLabel>
                <dd class="flex flex-auto items-center justify-end">
                  <Switch
                    v-model="automaticTimezoneEnabled"
                    :class="[automaticTimezoneEnabled ? 'bg-indigo-600' : 'bg-gray-200', 'flex w-8 cursor-pointer rounded-full p-1 ring-1 ring-gray-900/5 transition-colors duration-200 ease-in-out ring-inset focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600']"
                  >
                    <span
                      aria-hidden="true"
                      :class="[automaticTimezoneEnabled ? 'translate-x-3.5' : 'translate-x-0', 'size-4 transform rounded-full bg-white ring-1 shadow-xs ring-gray-900/5 transition duration-200 ease-in-out']"
                    />
                  </Switch>
                </dd>
              </SwitchGroup>
            </dl>
          </div>
        </div>
      </div>
      <ChangePassword v-if="showChangePassword" @close="showChangePassword = false" />
    </main>
  </div>

  <Dialog :open="cropperOpen" @close="closeCropper">
    <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h2 class="text-lg font-semibold mb-2">{{ $t('profile.avatar.uploadTitle') }}</h2>
        <input type="file" accept="image/*" @change="onFileChange" class="mb-4" />
        <div v-if="imageSrc" class="mb-4">
          <vue-cropper
            ref="cropper"
            :src="imageSrc"
            :aspect-ratio="1"
            :view-mode="1"
            class="cropper-container"
          />
        </div>
        <div class="flex justify-end gap-2">
          <button class="px-4 py-2 bg-gray-200 rounded" @click="closeCropper">{{ $t('profile.avatar.cancel') }}</button>
          <button class="px-4 py-2 bg-indigo-600 text-white rounded" @click="saveCroppedAvatar">{{ $t('profile.avatar.save') }}</button>
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Dialog, DialogPanel, Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import { Bars3Icon, BellIcon, XMarkIcon, PencilIcon } from '@heroicons/vue/20/solid'
import { UserCircleIcon, FingerPrintIcon, UsersIcon, XCircleIcon } from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AuthService from '@/services/AuthService.js'
import VueCropper from 'vue-cropperjs';
import 'vue-cropperjs/dist/vue-cropper.css';

import ApiServices from "@/services/ApiServices.js";
import ChangePassword from '@/components/dashboard/profile/change_password.vue'

const router = useRouter()
const { t } = useI18n()
const showChangePassword = ref(false)

function logout() {
  AuthService.logout()
  router.push('/login')
}

function goToSecurity() {
  showChangePassword.value = true
}

const navigation = [
  { name: 'General', href: '#', icon: UserCircleIcon, current: true },
  { name: 'Security', href: '#', icon: FingerPrintIcon, current: false, action: goToSecurity },
  { name: 'Notifications', href: '#', icon: BellIcon, current: false },
  { name: 'Logout', href: '#', icon: XCircleIcon, action: logout },
]

const mobileMenuOpen = ref(false)
const automaticTimezoneEnabled = ref(true)

const profile = ref({
    name: "None",
    Email: "None",
    role: "None",
    mobile: "None",
    Wecom: "",
    avatar: ""
})

const profileData = computed(() => ({
  "Name": profile.value.name || "None",
  "Email address": profile.value.Email || "None",
  "Mobile": profile.value.mobile || "None",
  "Department": profile.value.role || "None",
  "Wecom": profile.value.Wecom ? `${profile.value.Wecom.split('@')[0]}` : "None"
}))

const editingField = ref(null)
const editingValue = ref('')

function updateField(key) {
  editingField.value = key
  if (key === "Wecom") {
    editingValue.value = profile.value.Wecom.split('@')[0] || ""
  } else {
    editingValue.value = profileData.value[key]
  }
}

async function saveField(key) {
  if (key === "Email address") {
    if (!validateEmail(editingValue.value)) {
      alert(t('profile.messages.invalidEmail'))
      return
    }
    alert(t('profile.messages.verificationSent', { email: editingValue.value }))
  }

  try {
    // 将已编辑的值保存到本地 profile 对象中
    profile.value[key.replace(/\s+/g, '')] = editingValue.value;
    // 调用 updateUserProfile 方法并传入编辑后的字段和值
    const updateResponse = await ApiServices.updateUserProfile({
      "name_old": profile.value.name,
      [key.replace(/\s+/g, '').toLowerCase()]: editingValue.value
    })
    if (updateResponse.success) {
      alert(t('profile.messages.updateSuccess'));
      await getUserInfo();
      if (key.replace(/\s+/g, '').toLowerCase() === "name") {
        AuthService.logout()
        await router.push('/login')
      }

    } else {
      alert(t('profile.messages.updateFailed', { message: updateResponse.message }));
    }
  } catch (error) {
    console.error('Error updating profile:', error);
    alert(t('profile.messages.updateError'));
  } finally {
    editingField.value = null;
    editingValue.value = '';
  }
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

function updateAvatar() {
  openCropper()
}

const cropperOpen = ref(false)
const imageSrc = ref(null)
const cropper = ref(null)

function openCropper() {
  cropperOpen.value = true
}

function closeCropper() {
  cropperOpen.value = false;
  imageSrc.value = null;
}

function onFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imageSrc.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}

async function saveCroppedAvatar() {
  if (cropper.value) {
    const croppedCanvas = cropper.value.getCroppedCanvas({ width: 256, height: 256 });
    if (croppedCanvas) {
      try {
        const croppedImageData = croppedCanvas.toDataURL('image/png');
        const avatarUpdateResponse = await ApiServices.updateUserAvatar(croppedImageData)
        if (avatarUpdateResponse.success) {
          profile.value.avatar = croppedImageData;
          alert(t('profile.avatar.success'));
        } else {
          alert(t('profile.avatar.failed'))
        }
        closeCropper();
      } catch (error) {
        console.error('Error saving cropped avatar:', error);
        alert(t('profile.avatar.failed'));
      }
    } else {
      alert(t('profile.avatar.noCropped'));
    }
  } else {
    alert(t('profile.avatar.noCropper'));
  }
}

const languageOptions = ["English", "中文(简体)", "中文(繁体)"]
const currentLanguage = ref("English")
const editingLanguage = ref(false)

function toggleLanguageEdit() {
  if (editingLanguage.value) {
    alert(t('profile.messages.languageUpdated', { language: currentLanguage.value }))
    ApiServices.updateUserLanguage(currentLanguage.value)
  }
  editingLanguage.value = !editingLanguage.value
}

const getUserInfo = async () => {
  try {
    const data = await ApiServices.getUserInfo();
    profile.value = {
      name: data.name || "None",
      Email: data.email || "None",
      role: data.department || "None",
      mobile: data.mobile || "None",
      Wecom: data.wecom || "",
      avatar: data.avatar || "",
    };
  } catch (error) {
    console.error('获取任务数据失败:', error);
  }
}

onMounted(() => {
  getUserInfo();
});
</script>

<style>
.cropper-container {
  max-width: 100%;
  max-height: 300px;
}
</style>
