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
    reset: 'Reset',
    moveUp: 'Move Up',
    moveDown: 'Move Down'
  },
  
  // 导航菜单
  nav: {
    home: 'Home',
    tasks: 'Tasks',
    publish: 'Publish Task',
    team: 'Our Team',
    settings: 'Settings',
    profile: 'Profile'
  },
  
  // 首页
  home: {
    welcome: 'Welcome to BJ35-Bot Management System',
    usage: 'Click to view the latest robot tasks and status',
    electricity: 'Electricity',
    inCharge: 'In Charge',
    taskStatus: 'Task Status',
    location: 'Location',
    warehouseID: 'Warehouse ID',
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
      noNodesYet: 'No task nodes added yet, click "Add Node" button to start creating the task flow',
      move: 'Move',
      back: 'Return to Charge',
      send: 'Send Message',
      configureParams: 'Configure parameters'
    },
    notification: {
      publishSuccess: 'Task published successfully',
      publishFailed: 'Failed to publish task',
      noRobot: 'Please select a robot first',
      invalidParams: 'Invalid task parameters',
      messageSent: 'Message sent to {user}',
      messageFailure: 'Failed to send message: {error}',
      specifyUserMessage: 'Send command requires specifying user and message',
      taskPublished: 'Task has been published!',
      taskExecuted: 'Task executed successfully',
      allTasksComplete: 'All tasks completed'
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
    },
    detail: {
      onlineStatus: 'Online Status',
      online: 'Online',
      offline: 'Offline',
      power: 'Power',
      chargingStatus: 'Charging Status',
      charging: 'Charging',
      notCharging: 'Not Charging',
      cabinId: 'Cabin ID',
      location: 'Location',
      unknownLocation: 'Unknown Location',
      lastMessage: 'Last Message',
      noMessage: 'No Message',
      lastActivity: 'Last Activity',
      unknownDate: 'Unknown',
      invalidDate: 'Invalid Date',
      controlRobot: 'Control Robot',
      close: 'Close'
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
  },
  
  // 任务看板
  taskBoard: {
    title: 'Task Board',
    description: 'Click to view details',
    loading: 'Loading...',
    rowsPerPage: 'Rows per page',
    taskNo: 'Task NO',
    createdAt: 'Created At',
    status: 'Status',
    target: 'Target',
    pagination: {
      showing: 'Showing',
      to: 'to',
      of: 'of',
      results: 'results',
      previous: 'Previous',
      next: 'Next'
    },
    modal: {
      title: 'Task Details',
      taskNo: 'Task NO',
      taskId: 'Task ID',
      outTaskId: 'Out Task ID',
      createdAt: 'Created At',
      updatedAt: 'Updated At',
      status: 'Status',
      taskType: 'Task Type',
      target: 'Target'
    },
    renderingComponent: 'Rendering component...'
  },
  
  // 个人资料
  profile: {
    general: 'General',
    security: 'Security',
    notifications: 'Notifications',
    teamMembers: 'Team members',
    logout: 'Logout',
    title: 'Profile',
    personalInfo: {
      name: 'Name',
      emailAddress: 'Email address',
      mobile: 'Mobile',
      department: 'Department',
      wecom: 'Wecom'
    },
    languageAndDates: {
      title: 'Language and dates',
      description: 'Choose what language and date format to use throughout your account.',
      language: 'Language',
      dateFormat: 'Date format',
      automaticTimezone: 'Automatic timezone'
    },
    avatar: {
      uploadTitle: 'Upload and Crop Avatar',
      cancel: 'Cancel',
      save: 'Save',
      success: 'Avatar updated successfully!',
      failed: 'Failed to update avatar. Please try again.',
      noCropped: 'No cropped image available.',
      noCropper: 'Cropper instance is not available.'
    },
    actions: {
      update: 'Update',
      save: 'Save',
      uploadAvatar: 'Upload Avatar'
    },
    messages: {
      invalidEmail: 'Invalid email address.',
      verificationSent: 'A verification email has been sent to {email}.',
      updateSuccess: 'Profile updated successfully!',
      updateFailed: 'Failed to update profile. Reason: {message}',
      updateError: 'Error updating profile. Please try again.',
      languageUpdated: 'Language updated to {language}'
    }
  },

  // 通用组件
  components: {
    messageInfo: {
      close: 'Close'
    },
    loadingSpinner: {
      loading: 'Loading...'
    }
  },

  // 404错误页面
  notFound: {
    pageNotFound: 'Page not found',
    waitingForContent: 'Waiting for you to fill in the blank here',
    backToHome: 'Back to home'
  },
  
  // 登录页面
  login: {
    title: 'Sign in to your account',
    rememberMe: 'Remember me',
    loginWithAccount: 'Sign in with username',
    loginWithWecom: 'Sign in with Enterprise WeChat',
    validatingCredentials: 'Validating credentials...',
    wecomLoginSuccess: 'Enterprise WeChat login successful',
    invalidCredentials: 'Invalid or expired credentials',
    validationFailed: 'Validation failed: ',
    loginFailed: 'Login failed: ',
    loggingIn: 'Signing in...',
    loginSuccess: 'Login successful',
    checkCredentials: 'Login failed, please check your username and password',
    systemError: 'System error: '
  }
}
