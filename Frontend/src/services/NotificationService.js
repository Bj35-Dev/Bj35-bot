 // * @copyright Copyright (c) 2020-2025 The ESAP Project.
 // * @author AptS:1547
 // * @Link https://esaps.net/
 // * @version 0.1.0
 // * @license
 // * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
import { ref, reactive } from 'vue'

const state = reactive({
  message: '',
  type: 'info',
  show: false
})

let hideTimeout = null

const notify = (message, type = 'info') => {

  if (hideTimeout !== null) {
    clearTimeout(hideTimeout)
    hideTimeout = null
  }

  state.message = message
  state.type = type
  state.show = true

  hideTimeout = setTimeout(() => {
    state.show = false
    hideTimeout = null
  }, 3000)
}

const close = () => {
  if (hideTimeout !== null) {
    clearTimeout(hideTimeout)
    hideTimeout = null
  }

  state.show = false
}

export default {
  state,
  notify,
  close
}