 // * @copyright Copyright (c) 2020-2025 The ESAP Project.
 // * @author AptS:1547
 // * @Link https://esaps.net/
 // * @version 0.1.0
 // * @license
 // * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
import { createI18n } from 'vue-i18n'
import en from './locales/en.js'
import zhcn from './locales/zhcn.js'
import ja from './locales/ja.js'
import zhtw from './locales/zhtw.js'

// 从浏览器获取首选语言
const getBrowserLocale = () => {
  const navigatorLocale = navigator.language || navigator.userLanguage || 'en'
  const trimmedLocale = navigatorLocale.trim().split('-')[0]
  const localeWithRegion = navigatorLocale.trim().split('-')[1] || ''

  if (trimmedLocale === 'zh') {
    if (localeWithRegion === 'CN') {
      return 'zhcn'
    } else if (localeWithRegion === 'TW') {
      return 'zhtw'
    } else {
      // 如果無法確定，默認為簡體中文
      return 'zhcn'
    }
  } else {
    return ['en', 'zhcn', 'zhtw', 'ja'].includes(navigatorLocale) ? navigatorLocale : 'en'
  }
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
    zhcn,
    ja,
    zhtw
  }
})

// 提供一个切换语言的方法
export const setLocale = (locale) => {
  i18n.global.locale.value = locale
  localStorage.setItem('locale', locale)
  document.querySelector('html').setAttribute('lang', locale)
}

export default i18n
