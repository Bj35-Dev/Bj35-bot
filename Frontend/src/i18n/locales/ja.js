export default {
  // 公共部分
  common: {
    login: 'ログイン',
    logout: 'ログアウト',
    username: 'ユーザー名',
    password: 'パスワード',
    confirm: '確認',
    cancel: 'キャンセル',
    save: '保存',
    delete: '削除',
    edit: '編集',
    search: '検索',
    loading: '読み込み中...',
    success: '成功',
    error: 'エラー',
    warning: '警告',
    info: '情報',
    switchLanguage: '言語を切り替える',
    openSidebar: 'サイドバーを開く',
    close: '閉じる',
    viewNotifications: '通知を表示',
    openUserMenu: 'ユーザーメニューを開く',
    unknown: '不明',
    renderingComponent: 'コンポーネントをレンダリング中...',
    reset: 'リセット',
    moveUp: '上に移動',
    moveDown: '下に移動'
  },
  
  // 導航菜单
  nav: {
    home: 'ホーム',
    tasks: 'タスク',
    publish: 'タスクを発行',
    team: 'チーム紹介',
    settings: '設定',
    profile: 'プロフィール'
  },
  
  // 首页
  home: {
    welcome: 'BJ35-Bot管理システムへようこそ',
    usage: 'クリックして最新のロボットタスクとステータスを表示',
    electricity: '電力',
    inCharge: '充電中',
    taskStatus: 'タスク状態',
    location: '位置',
    warehouseID: '倉庫ID',
  },
  
  // 任务相关
  tasks: {
    create: 'タスク作成',
    publish: 'タスク発行',
    list: 'タスクリスト',
    details: 'タスク詳細',
    status: {
      all: 'すべて',
      pending: '保留中',
      inProgress: '進行中',
      completed: '完了',
      failed: '失敗'
    },
    form: {
      selectRobot: 'ロボットを選択',
      taskFlow: 'タスクフロー作成',
      addNode: 'ノードを追加',
      nodeType: 'ノードタイプ',
      target: 'ターゲット',
      user: 'ユーザー',
      message: 'メッセージ',
      chargePoint: '充電ポイント',
      searchTarget: 'ターゲットを検索',
      searchUser: 'ユーザーを検索',
      enterMessage: 'メッセージを入力',
      selectChargePoint: '充電ポイントを選択',
      reset: 'リセット',
      publish: '発行',
      noNodesYet: 'タスクノードがまだ追加されていません。「ノードを追加」ボタンをクリックしてタスクフローの作成を開始してください',
      move: '移動',
      back: '充電に戻る',
      send: 'メッセージを送信',
      configureParams: 'パラメータを設定'
    },
    notification: {
      publishSuccess: 'タスクが正常に発行されました',
      publishFailed: 'タスクの発行に失敗しました',
      noRobot: '最初にロボットを選択してください',
      invalidParams: '無効なタスクパラメータ',
      messageSent: '{user}にメッセージを送信しました',
      messageFailure: 'メッセージの送信に失敗しました: {error}',
      specifyUserMessage: '送信コマンドにはユーザーとメッセージの指定が必要です',
      taskPublished: 'タスクが発行されました！',
      taskExecuted: 'タスクが正常に実行されました',
      allTasksComplete: 'すべてのタスクが完了しました'
    },
    publishDescription: 'ロボットタスクシーケンスを作成して実行するために送信'
  },
  
  // 机器人相关
  robot: {
    status: {
      online: 'オンライン',
      offline: 'オフライン',
      idle: 'アイドル',
      busy: 'ビジー',
      error: 'エラー',
      unknown: '不明'
    },
    info: {
      location: '現在位置',
      battery: 'バッテリー',
      status: '状態'
    },
    loading: 'ロボットリストを読み込み中...',
    noAvailableRobots: '利用可能なロボットがありません',
    pleaseSelectRobot: '最初にロボットを選択してください',
    statusTitle: 'ロボット状態',
    detail: {
      onlineStatus: 'オンライン状態',
      online: 'オンライン',
      offline: 'オフライン',
      power: '電力',
      chargingStatus: '充電状態',
      charging: '充電中',
      notCharging: '充電していない',
      cabinId: 'キャビンID',
      location: '位置',
      unknownLocation: '不明な位置',
      lastMessage: '最後のメッセージ',
      noMessage: 'メッセージなし',
      lastActivity: '最後の活動',
      unknownDate: '不明',
      invalidDate: '無効な日付',
      controlRobot: 'ロボットを制御',
      close: '閉じる'
    }
  },
  
  // 团队页面
  team: {
    title: '私たちについて',
    description: '私たちは革新と問題解決のチームであり、デザインの感性と機能的な精度を融合させています。ブルックリンにインスパイアされた美学からミニマリストの細部まで、私たちは気取らずに職人技を大切にしています。',
    techStack: '技術スタック',
    joinUs: '参加する',
    joinDescription: '私たちは常に才能あるデベロッパーをチームに迎え入れています',
    contactUs: 'お問い合わせ',
    projectStats: 'プロジェクト統計',
    completedProjects: '完了したプロジェクト',
    codeLines: 'コード行数',
    teamExperience: 'チーム経験',
    support: '技術サポート'
  },
  
  // 设置和个人资料
  settings: {
    profile: 'プロフィール設定',
    account: 'アカウント',
    appearance: '外観',
    language: '言語',
    theme: {
      title: 'テーマ',
      light: 'ライト',
      dark: 'ダーク',
      system: 'システム'
    },
    notifications: '通知',
    security: 'セキュリティ',
    changePassword: 'パスワード変更',
    oldPassword: '古いパスワード',
    newPassword: '新しいパスワード',
    confirmPassword: '新しいパスワードを確認'
  },
  
  // 任务看板
  taskBoard: {
    title: 'タスクボード',
    description: 'クリックして詳細を表示',
    loading: '読み込み中...',
    rowsPerPage: 'ページあたりの行数',
    taskNo: 'タスク番号',
    createdAt: '作成日時',
    status: '状態',
    target: 'ターゲット',
    pagination: {
      showing: '表示中',
      to: 'から',
      of: '件中',
      results: '結果',
      previous: '前へ',
      next: '次へ'
    },
    modal: {
      title: 'タスク詳細',
      taskNo: 'タスク番号',
      taskId: 'タスクID',
      outTaskId: '外部タスクID',
      createdAt: '作成日時',
      updatedAt: '更新日時',
      status: '状態',
      taskType: 'タスクタイプ',
      target: 'ターゲット'
    },
    renderingComponent: 'コンポーネントをレンダリング中...'
  },
  
  // 个人资料
  profile: {
    general: '一般',
    security: 'セキュリティ',
    notifications: '通知',
    teamMembers: 'チームメンバー',
    logout: 'ログアウト',
    title: 'プロフィール',
    personalInfo: {
      name: '名前',
      emailAddress: 'メールアドレス',
      mobile: 'モバイル',
      department: '部門',
      wecom: '企業WeChat'
    },
    languageAndDates: {
      title: '言語と日付',
      description: 'アカウント全体で使用する言語と日付形式を選択してください。',
      language: '言語',
      dateFormat: '日付形式',
      automaticTimezone: '自動タイムゾーン'
    },
    avatar: {
      uploadTitle: 'アバターのアップロードと切り抜き',
      cancel: 'キャンセル',
      save: '保存',
      success: 'アバターが正常に更新されました！',
      failed: 'アバターの更新に失敗しました。もう一度お試しください。',
      noCropped: '利用可能な切り抜き画像がありません。',
      noCropper: 'クロッパーインスタンスが利用できません。'
    },
    actions: {
      update: '更新',
      save: '保存',
      uploadAvatar: 'アバターをアップロード'
    },
    messages: {
      invalidEmail: '無効なメールアドレスです。',
      verificationSent: '確認メールが{email}に送信されました。',
      updateSuccess: 'プロフィールが正常に更新されました！',
      updateFailed: 'プロフィールの更新に失敗しました。理由: {message}',
      updateError: 'プロフィールの更新中にエラーが発生しました。もう一度お試しください。',
      languageUpdated: '言語が{language}に更新されました'
    }
  },

  // 通用组件
  components: {
    messageInfo: {
      close: '閉じる'
    },
    loadingSpinner: {
      loading: '読み込み中...'
    }
  },

  // 404错误页面
  notFound: {
    pageNotFound: 'ページが見つかりません',
    waitingForContent: 'ここに空白を埋めるのをお待ちしています',
    backToHome: 'ホームに戻る'
  },
  
  // 登录页面
  login: {
    title: 'アカウントにサインイン',
    rememberMe: 'ログイン情報を記憶する',
    loginWithAccount: 'ユーザー名でサインイン',
    loginWithWecom: '企業WeChatでサインイン',
    validatingCredentials: '認証情報を検証中...',
    wecomLoginSuccess: '企業WeChatログイン成功',
    invalidCredentials: '無効または期限切れの認証情報',
    validationFailed: '検証に失敗しました: ',
    loginFailed: 'ログインに失敗しました: ',
    loggingIn: 'サインイン中...',
    loginSuccess: 'ログイン成功',
    checkCredentials: 'ログインに失敗しました。ユーザー名とパスワードを確認してください',
    systemError: 'システムエラー: '
  }
}
