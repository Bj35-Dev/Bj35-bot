import { createI18n } from 'vue-i18n'
import en from './locales/en.js'
import zh from './locales/zh.js'

// 从浏览器获取首选语言
const getBrowserLocale = () => {
  const navigatorLocale = navigator.language || navigator.userLanguage || 'en'
  const trimmedLocale = navigatorLocale.trim().split('-')[0]
  return ['en', 'zh'].includes(trimmedLocale) ? trimmedLocale : 'en'
}

// 从本地存储中获取已保存的语言设置
const getStoredLocale = () => {
  return localStorage.getItem('locale') || getBrowserLocale()
}

// 创建 i18n 实例
const i18n = createI18n({
  legacy: false,
  locale: getStoredLocale(),
  fallbackLocale: 'en',
  globalInjection: true,
  messages: {
    en,
    zh
  }
})

// 提供一个切换语言的方法
export const setLocale = (locale) => {
  i18n.global.locale.value = locale
  localStorage.setItem('locale', locale)
  document.querySelector('html').setAttribute('lang', locale)
}

export default i18n
