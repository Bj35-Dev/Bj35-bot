export default {
  // 公共部分
  common: {
    login: '登入',
    logout: '退出登入',
    username: '使用者名稱',
    password: '密碼',
    confirm: '確認',
    cancel: '取消',
    save: '儲存',
    delete: '刪除',
    edit: '編輯',
    search: '搜尋',
    loading: '載入中...',
    success: '成功',
    error: '錯誤',
    warning: '警告',
    info: '資訊',
    switchLanguage: '切換語言',
    openSidebar: '開啟側邊欄',
    close: '關閉',
    viewNotifications: '檢視通知',
    openUserMenu: '開啟使用者選單',
    unknown: '未知',
    renderingComponent: '正在渲染元件...',
    reset: '重置',
    moveUp: '上移',
    moveDown: '下移'
  },

  // 導航選單
  nav: {
    home: '首頁',
    tasks: '任務',
    publish: '發布任務',
    team: '團隊介紹',
    settings: '設定',
    profile: '個人資料'
  },

  // 首頁
  home: {
    welcome: '歡迎使用BJ35-Bot管理系統',
    usage: '點擊查看最新的機器人任務和狀態',
    electricity: '電量',
    inCharge: '充電中',
    taskStatus: '任務狀態',
    location: '位置',
    warehouseID: '倉庫ID',
  },

  // 任務相關
  tasks: {
    create: '建立任務',
    publish: '發布任務',
    list: '任務清單',
    details: '任務詳情',
    status: {
      all: '全部',
      pending: '待處理',
      inProgress: '進行中',
      completed: '已完成',
      failed: '失敗'
    },
    form: {
      selectRobot: '選擇機器人',
      taskFlow: '建立任務流程',
      addNode: '新增任務節點',
      nodeType: '節點類型',
      target: '目標',
      user: '使用者',
      message: '消息',
      chargePoint: '充電站',
      searchTarget: '搜尋目標',
      searchUser: '搜尋使用者',
      enterMessage: '輸入消息',
      selectChargePoint: '選擇充電站',
      reset: '重置',
      publish: '發布',
      noNodesYet: '尚未新增任務節點，點擊"新增任務節點"按鈕開始建立任務流程',
      move: '移動',
      back: '返回充電',
      send: '傳送消息',
      configureParams: '配置參數'
    },
    notification: {
      publishSuccess: '任務發布成功',
      publishFailed: '任務發布失敗',
      noRobot: '請先選擇一個機器人',
      invalidParams: '無效的任務參數',
      messageSent: '消息已傳送給 {user}',
      messageFailure: '傳送消息失敗: {error}',
      specifyUserMessage: '傳送消息需要指定使用者和消息內容',
      taskPublished: '任務已發布！',
      taskExecuted: '任務已執行成功',
      allTasksComplete: '所有任務已處理完成'
    },
    publishDescription: '建立機器人任務序列並發送執行'
  },

  // 機器人相關
  robot: {
    status: {
      online: '線上',
      offline: '離線',
      idle: '空閒',
      busy: '忙碌',
      error: '錯誤',
      unknown: '未知'
    },
    info: {
      location: '目前位置',
      battery: '電池電量',
      status: '狀態'
    },
    loading: '載入機器人清單...',
    noAvailableRobots: '沒有可用的機器人',
    pleaseSelectRobot: '請先選擇一個機器人',
    statusTitle: '機器人狀態',
    detail: {
      onlineStatus: '線上狀態',
      online: '線上',
      offline: '離線',
      power: '電量',
      chargingStatus: '充電狀態',
      charging: '正在充電',
      notCharging: '未充電',
      cabinId: '倉庫ID',
      location: '位置',
      unknownLocation: '未知位置',
      lastMessage: '最近消息',
      noMessage: '無消息',
      lastActivity: '最近活動',
      unknownDate: '未知',
      invalidDate: '無效日期',
      controlRobot: '控制機器人',
      close: '關閉'
    }
  },

  // 團隊頁面
  team: {
    title: '關於我們',
    description: '我們是一個創新和解決問題的團隊，將設計感和功能精密度融為一體。從布魯克林靈感的美学到極簡細節，我們注重工藝而不拘泥於形式。',
    techStack: '技術棧',
    joinUs: '加入我們',
    joinDescription: '我們一直在尋找優秀的開發者加入團隊',
    contactUs: '聯繫我們',
    projectStats: '項目統計',
    completedProjects: '完成項目',
    codeLines: '程式碼行數',
    teamExperience: '團隊經驗',
    support: '技術支援'
  },

  // 設定和個人資料
  settings: {
    profile: '個人資料設定',
    account: '帳號',
    appearance: '外觀',
    language: '語言',
    theme: {
      title: '主題',
      light: '淺色',
      dark: '深色',
      system: '跟隨系統'
    },
    notifications: '通知',
    security: '安全',
    changePassword: '修改密碼',
    oldPassword: '舊密碼',
    newPassword: '新密碼',
    confirmPassword: '確認新密碼'
  },

  // 任務看板
  taskBoard: {
    title: '任務看板',
    description: '點擊查看詳細資訊',
    loading: '載入中',
    rowsPerPage: '每頁顯示',
    taskNo: '任務編號',
    createdAt: '建立時間',
    status: '狀態',
    target: '目標',
    pagination: {
      showing: '顯示',
      to: '至',
      of: '共',
      results: '筆記錄',
      previous: '上一頁',
      next: '下一頁'
    },
    modal: {
      title: '任務詳情',
      taskNo: '任務編號',
      taskId: '任務 ID',
      outTaskId: '外部任務 ID',
      createdAt: '建立時間',
      updatedAt: '更新時間',
      status: '狀態',
      taskType: '任務類型',
      target: '目標'
    },
    renderingComponent: '正在渲染元件...'
  },

  // 個人資料
  profile: {
    general: '通用',
    security: '安全',
    notifications: '通知',
    teamMembers: '團隊成員',
    logout: '退出登入',
    title: '個人資料',
    personalInfo: {
      name: '姓名',
      emailaddress: '電子郵件地址',
      mobile: '手機',
      department: '部門',
      wecom: '企業微信'
    },
    languageAndDates: {
      title: '語言和日期',
      description: '選擇您帳號中使用的語言和日期格式。',
      language: '語言',
      dateFormat: '日期格式',
      automaticTimezone: '自動時區'
    },
    avatar: {
      uploadTitle: '上傳並裁剪頭像',
      cancel: '取消',
      save: '儲存',
      success: '頭像更新成功！',
      failed: '頭像更新失敗，請重試。',
      noCropped: '沒有可用的裁剪圖像。',
      noCropper: '裁剪工具不可用。'
    },
    actions: {
      update: '更新',
      save: '儲存',
      uploadAvatar: '上傳頭像'
    },
    messages: {
      invalidEmail: '電子郵件地址無效。',
      verificationSent: '驗證電子郵件已發送至 {email}。',
      updateSuccess: '個人資料更新成功！',
      updateFailed: '個人資料更新失敗。原因：{message}',
      updateError: '更新個人資料時出錯，請重試。',
      languageUpdated: '語言已更新為 {language}'
    }
  },

  // 404錯誤頁面
  notFound: {
    pageNotFound: '頁面找不到',
    waitingForContent: '正在等您填充這裡的空白',
    backToHome: '回到首頁'
  },

  // 登入頁面
  login: {
    title: '登入您的帳號',
    rememberMe: '記住我',
    loginWithAccount: '帳號密碼登入',
    loginWithWecom: '企業微信登入',
    validatingCredentials: '驗證登入憑證...',
    wecomLoginSuccess: '企業微信登入成功',
    invalidCredentials: '登入憑證無效或已過期',
    validationFailed: '驗證失敗：',
    loginFailed: '登入失敗：',
    loggingIn: '登入中……',
    loginSuccess: '登入成功',
    checkCredentials: '登入失敗，請檢查您的使用者名稱和密碼',
    systemError: '系統錯誤：'
  },

  // 通用元件
  components: {
    messageInfo: {
      close: '關閉'
    },
    loadingSpinner: {
      loading: '載入中...'
    }
  }
}
