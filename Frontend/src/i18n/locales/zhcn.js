export default {
  // 公共部分
  common: {
    login: '登录',
    logout: '退出登录',
    username: '用户名',
    password: '密码',
    confirm: '确认',
    cancel: '取消',
    save: '保存',
    delete: '删除',
    edit: '编辑',
    search: '搜索',
    loading: '加载中...',
    success: '成功',
    error: '错误',
    warning: '警告',
    info: '信息',
    switchLanguage: '切换语言',
    openSidebar: '打开侧边栏',
    close: '关闭',
    viewNotifications: '查看通知',
    openUserMenu: '打开用户菜单',
    unknown: '未知',
    renderingComponent: '正在渲染组件...',
    reset: '重置',
    moveUp: '上移',
    moveDown: '下移'
  },
  
  // 导航菜单
  nav: {
    home: '首页',
    tasks: '任务',
    publish: '发布任务',
    team: '团队介绍',
    settings: '设置',
    profile: '个人资料'
  },
  
  // 首页
  home: {
    welcome: '欢迎使用BJ35-Bot管理系统',
    usage: '点击查看最新的机器人任务和状态',
    electricity: '电量',
    inCharge: '充电中',
    taskStatus: '任务状态',
    location: '位置',
    warehouseID: '货仓ID',
  },
  
  // 任务相关
  tasks: {
    create: '创建任务',
    publish: '发布任务',
    list: '任务列表',
    details: '任务详情',
    status: {
      all: '全部',
      pending: '待处理',
      inProgress: '进行中',
      completed: '已完成',
      failed: '失败'
    },
    form: {
      selectRobot: '选择机器人',
      taskFlow: '创建任务流',
      addNode: '添加任务节点',
      nodeType: '节点类型',
      target: '目标',
      user: '用户',
      message: '消息',
      chargePoint: '充电桩',
      searchTarget: '搜索目标',
      searchUser: '搜索用户',
      enterMessage: '输入消息',
      selectChargePoint: '选择充电桩',
      reset: '重置',
      publish: '发布',
      noNodesYet: '尚未添加任务节点，点击"添加任务节点"按钮开始创建任务流',
      move: '移动',
      back: '返回充电',
      send: '发送消息',
      configureParams: '配置参数'
    },
    notification: {
      publishSuccess: '任务发布成功',
      publishFailed: '任务发布失败',
      noRobot: '请先选择一个机器人',
      invalidParams: '无效的任务参数',
      messageSent: '消息已发送给 {user}',
      messageFailure: '发送消息失败: {error}',
      specifyUserMessage: '发送消息需要指定用户和消息内容',
      taskPublished: '任务已发布！',
      taskExecuted: '任务已执行成功',
      allTasksComplete: '所有任务已处理完成'
    },
    publishDescription: '创建机器人任务序列并发送执行'
  },
  
  // 机器人相关
  robot: {
    status: {
      online: '在线',
      offline: '离线',
      idle: '空闲',
      busy: '忙碌',
      error: '错误',
      unknown: '未知'
    },
    info: {
      location: '当前位置',
      battery: '电池电量',
      status: '状态'
    },
    loading: '加载机器人列表...',
    noAvailableRobots: '没有可用的机器人',
    pleaseSelectRobot: '请先选择一个机器人',
    statusTitle: '机器人状态',
    detail: {
      onlineStatus: '在线状态',
      online: '在线',
      offline: '离线',
      power: '电量',
      chargingStatus: '充电状态',
      charging: '正在充电',
      notCharging: '未充电',
      cabinId: '货仓ID',
      location: '位置',
      unknownLocation: '未知位置',
      lastMessage: '最近消息',
      noMessage: '无消息',
      lastActivity: '最近活动',
      unknownDate: '未知',
      invalidDate: '无效日期',
      controlRobot: '控制机器人',
      close: '关闭'
    }
  },
  
  // 团队页面
  team: {
    title: '关于我们',
    description: '我们是一个创新和解决问题的团队，将设计感和功能精度融为一体。从布鲁克林灵感的美学到极简细节，我们注重工艺而不拘泥于形式。',
    techStack: '技术栈',
    joinUs: '加入我们',
    joinDescription: '我们一直在寻找优秀的开发者加入团队',
    contactUs: '联系我们',
    projectStats: '项目统计',
    completedProjects: '完成项目',
    codeLines: '代码行数',
    teamExperience: '团队经验',
    support: '技术支持'
  },
  
  // 设置和个人资料
  settings: {
    profile: '个人资料设置',
    account: '账户',
    appearance: '外观',
    language: '语言',
    theme: {
      title: '主题',
      light: '浅色',
      dark: '深色',
      system: '跟随系统'
    },
    notifications: '通知',
    security: '安全',
    changePassword: '修改密码',
    oldPassword: '旧密码',
    newPassword: '新密码',
    confirmPassword: '确认新密码'
  },
  
  // 任务看板
  taskBoard: {
    title: '任务看板',
    description: '点击查看详细信息',
    loading: '加载中...',
    rowsPerPage: '每页显示',
    taskNo: '任务 NO',
    createdAt: '创建时间',
    status: '状态',
    target: '目标',
    pagination: {
      showing: '显示',
      to: '至',
      of: '共',
      results: '条记录',
      previous: '上一页',
      next: '下一页'
    },
    modal: {
      title: '任务详情',
      taskNo: '任务 NO',
      taskId: 'Task ID',
      outTaskId: 'Out Task ID',
      createdAt: '创建时间',
      updatedAt: '更新时间',
      status: '状态',
      taskType: '任务类型',
      target: '目标'
    },
    renderingComponent: '正在渲染组件...'
  },
  
  // 个人资料
  profile: {
    general: '通用',
    security: '安全',
    notifications: '通知',
    teamMembers: '团队成员',
    logout: '退出登录',
    title: '个人资料',
    personalInfo: {
      name: '姓名',
      emailaddress: '邮箱地址',
      mobile: '手机',
      department: '部门',
      wecom: '企业微信'
    },
    languageAndDates: {
      title: '语言和日期',
      description: '选择您账户中使用的语言和日期格式。',
      language: '语言',
      dateFormat: '日期格式',
      automaticTimezone: '自动时区'
    },
    avatar: {
      uploadTitle: '上传并裁剪头像',
      cancel: '取消',
      save: '保存',
      success: '头像更新成功！',
      failed: '头像更新失败，请重试。',
      noCropped: '没有可用的裁剪图像。',
      noCropper: '裁剪工具不可用。'
    },
    actions: {
      update: '更新',
      save: '保存',
      uploadAvatar: '上传头像'
    },
    messages: {
      invalidEmail: '邮箱地址无效。',
      verificationSent: '验证邮件已发送至 {email}。',
      updateSuccess: '个人资料更新成功！',
      updateFailed: '个人资料更新失败。原因：{message}',
      updateError: '更新个人资料时出错，请重试。',
      languageUpdated: '语言已更新为 {language}'
    }
  },

  // 404错误页面
  notFound: {
    pageNotFound: '页面找不到了',
    waitingForContent: '正在等你填充这里的空白',
    backToHome: '回到首页'
  },
  
  // 登录页面
  login: {
    title: '登录您的账户',
    rememberMe: '记住我',
    loginWithAccount: '账号密码登录',
    loginWithWecom: '企业微信登录',
    validatingCredentials: '验证登录凭据...',
    wecomLoginSuccess: '企业微信登录成功',
    invalidCredentials: '登录凭据无效或已过期',
    validationFailed: '验证失败：',
    loginFailed: '登录失败：',
    loggingIn: '登录中……',
    loginSuccess: '登录成功',
    checkCredentials: '登录失败，请检查您的用户名和密码',
    systemError: '系统错误：'
  },
  
  // 通用组件
  components: {
    messageInfo: {
      close: '关闭'
    },
    loadingSpinner: {
      loading: '加载中...'
    }
  }
}
