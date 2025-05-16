export default {
  // 公共部分
  common: {
    login: 'Login',
    logout: 'Logout',
    username: 'Username',
    password: 'Password',
    confirm: 'Confirm',
    cancel: 'Cancel',
    save: 'Save',
    delete: 'Delete',
    edit: 'Edit',
    search: 'Search',
    loading: 'Loading...',
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    info: 'Information',
    switchLanguage: 'Switch Language',
    openSidebar: 'Open sidebar',
    close: 'Close',
    viewNotifications: 'View notifications',
    openUserMenu: 'Open user menu',
    unknown: 'Unknown',
    renderingComponent: 'Rendering component...',
    reset: 'Reset'
  },
  
  // 导航菜单
  nav: {
    home: 'Home',
    dashboard: 'Dashboard',
    tasks: 'Tasks',
    publish: 'Publish Task',
    team: 'Our Team',
    settings: 'Settings',
    profile: 'Profile'
  },
  
  // 首页
  home: {
    welcome: 'Welcome to BJ35-Bot Management System',
    description: 'A comprehensive solution for robot task management'
  },
  
  // 仪表盘
  dashboard: {
    title: 'Dashboard',
    overview: 'Overview',
    statistics: 'Statistics',
    recentActivity: 'Recent Activity'
  },
  
  // 任务相关
  tasks: {
    create: 'Create Task',
    publish: 'Publish Task',
    list: 'Task List',
    details: 'Task Details',
    status: {
      all: 'All',
      pending: 'Pending',
      inProgress: 'In Progress',
      completed: 'Completed',
      failed: 'Failed'
    },
    form: {
      selectRobot: 'Select Robot',
      taskFlow: 'Task Flow',
      addNode: 'Add Node',
      nodeType: 'Node Type',
      target: 'Target',
      user: 'User',
      message: 'Message',
      chargePoint: 'Charge Point',
      searchTarget: 'Search Target',
      searchUser: 'Search User',
      enterMessage: 'Enter Message',
      selectChargePoint: 'Select Charge Point',
      reset: 'Reset',
      publish: 'Publish',
      noNodesYet: 'No task nodes added yet, click "Add Node" button to start creating the task flow'
    },
    notification: {
      publishSuccess: 'Task published successfully',
      publishFailed: 'Failed to publish task',
      noRobot: 'Please select a robot first',
      invalidParams: 'Invalid task parameters'
    },
    publishDescription: 'Create a robot task sequence and send it for execution'
  },
  
  // 机器人相关
  robot: {
    status: {
      online: 'Online',
      offline: 'Offline',
      idle: 'Idle',
      busy: 'Busy',
      error: 'Error'
    },
    info: {
      location: 'Current Location',
      battery: 'Battery',
      status: 'Status'
    },
    loading: 'Loading robot list...',
    noAvailableRobots: 'No available robots',
    pleaseSelectRobot: 'Please select a robot first',
    statusTitle: 'Robot Status',
    status: {
      '空闲': 'Idle',
      '执行任务中': 'Busy',
      '未知': 'Unknown',
      '错误': 'Error',
      idle: 'Idle',
      busy: 'Busy',
      error: 'Error',
      unknown: 'Unknown'
    }
  },
  
  // 团队页面
  team: {
    title: 'About Us',
    description: 'We\'re a team of innovators and problem-solvers, blending design sensibility with functional precision. From Brooklyn-inspired aesthetics to minimalist details, we value craftsmanship without pretension.',
    techStack: 'Tech Stack',
    joinUs: 'Join Us',
    joinDescription: 'We\'re always looking for talented developers to join our team',
    contactUs: 'Contact Us',
    projectStats: 'Project Statistics',
    completedProjects: 'Completed Projects',
    codeLines: 'Code Lines',
    teamExperience: 'Team Experience',
    support: 'Technical Support'
  },
  
  // 设置和个人资料
  settings: {
    profile: 'Profile Settings',
    account: 'Account',
    appearance: 'Appearance',
    language: 'Language',
    theme: {
      title: 'Theme',
      light: 'Light',
      dark: 'Dark',
      system: 'System'
    },
    notifications: 'Notifications',
    security: 'Security',
    changePassword: 'Change Password',
    oldPassword: 'Old Password',
    newPassword: 'New Password',
    confirmPassword: 'Confirm New Password'
  }
}
