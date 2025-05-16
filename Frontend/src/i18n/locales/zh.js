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
    reset: '重置'
  },
  
  // 导航菜单
  nav: {
    home: '首页',
    dashboard: '仪表盘',
    tasks: '任务',
    publish: '发布任务',
    team: '团队介绍',
    settings: '设置',
    profile: '个人资料'
  },
  
  // 首页
  home: {
    welcome: '欢迎使用BJ35-Bot管理系统',
    description: '一个全面的机器人任务管理解决方案'
  },
  
  // 仪表盘
  dashboard: {
    title: '仪表盘',
    overview: '概览',
    statistics: '统计信息',
    recentActivity: '最近活动'
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
      noNodesYet: '尚未添加任务节点，点击"添加任务节点"按钮开始创建任务流'
    },
    notification: {
      publishSuccess: '任务发布成功',
      publishFailed: '任务发布失败',
      noRobot: '请先选择一个机器人',
      invalidParams: '无效的任务参数'
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
    statusTitle: '机器人状态'
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
  }
}
