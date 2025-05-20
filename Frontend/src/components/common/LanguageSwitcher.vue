<template>
  <div class="language-switcher">
    <button
      class="flex items-center text-sm focus:outline-none"
      @click="toggleDropdown"
      ref="dropdownButton"
    >
      <span class="inline-flex items-center">
        <span class="sr-only">{{ $t('common.switchLanguage') }}</span>
        <span class="flag-icon">{{ getFlagEmoji(currentLocale) }}</span>
        <span class="ml-1">{{ currentLocale.toUpperCase() }}</span>
      </span>
      <svg
        class="ml-1 h-4 w-4"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        aria-hidden="true"
      >
        <path
          fill-rule="evenodd"
          d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
          clip-rule="evenodd"
        />
      </svg>
    </button>
    
    <div
      v-if="isOpen"
      class="absolute right-0 z-10 mt-2 w-40 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
      role="menu"
      ref="dropdown"
    >
      <a
        href="#"
        class="block px-4 py-2 text-sm hover:bg-gray-100"
        @click.prevent="changeLanguage('en')"
        role="menuitem"
      >
        <span class="flag-icon">🇺🇸</span>
        <span class="ml-2">English</span>
      </a>

      <a
        href="#"
        class="block px-4 py-2 text-sm hover:bg-gray-100"
        @click.prevent="changeLanguage('zhcn')"
        role="menuitem"
      >
        <span class="flag-icon">🇨🇳</span>
        <span class="ml-2">中文</span>
      </a>

      <a
        href="#"
        class="block px-4 py-2 text-sm hover:bg-gray-100"
        @click.prevent="changeLanguage('ja')"
        role="menuitem"
      >
        <span class="flag-icon">🇯🇵</span>
        <span class="ml-2">日本語</span>
      </a>

      <a
        href="#"
        class="block px-4 py-2 text-sm hover:bg-gray-100"
        @click.prevent="changeLanguage('zhtw')"
        role="menuitem"
      >
        <span class="flag-icon">🇹🇼</span>
        <span class="ml-2">繁體中文</span>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { setLocale } from '../../i18n';

const i18n = useI18n();
const isOpen = ref(false);
const dropdown = ref(null);
const dropdownButton = ref(null);

const currentLocale = computed(() => {
  return i18n.locale.value;
});

const getFlagEmoji = (locale) => {
  switch(locale) {
    case 'en': return '🇺🇸';
    case 'zhcn': return '🇨🇳';
    case 'ja': return '🇯🇵';
    default: return '🇺🇸';
  }
};

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const changeLanguage = (locale) => {
  setLocale(locale);
  isOpen.value = false;
};

const handleClickOutside = (event) => {
  if (
    isOpen.value && 
    dropdown.value && 
    !dropdown.value.contains(event.target) && 
    !dropdownButton.value.contains(event.target)
  ) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.language-switcher {
  position: relative;
}

.flag-icon {
  display: inline-block;
  font-size: 1.2em;
  line-height: 1;
}
</style>
