export type Language = 'uz' | 'ru' | 'en';

export interface Translations {
  // Brand & Header
  brandName: string;
  tagline: string;
  sprintActive: string;
  searchPlaceholder: string;
  swaggerApi: string;
  newTask: string;
  newProject: string;
  activeTimer: string;
  stopTimer: string;
  startTimer: string;
  workspace: string;
  switchWorkspace: string;
  currentRole: string;
  logout: string;
  signIn: string;
  signUp: string;
  getStarted: string;
  liveDemo: string;
  
  // Navigation
  navDashboard: string;
  navProjects: string;
  navKanban: string;
  navTasks: string;
  navSprints: string;
  navTimeTracker: string;
  navAiStudio: string;
  navIntegrations: string;
  navAutomations: string;
  navTeam: string;
  navAnalytics: string;
  navBilling: string;
  navAffiliates: string;
  navSuperAdmin: string;
  navSwagger: string;
  navSettings: string;
  navLanding: string;
  managementSection: string;

  // Stats & Dashboard
  activeProjects: string;
  openTasks: string;
  sprintVelocity: string;
  teamCapacity: string;
  ptsPerSprint: string;
  acrossColumns: string;
  membersActive: string;
  burndownProgress: string;
  ptsDone: string;
  percentDone: string;
  recentTasks: string;
  viewAll: string;
  onTrack: string;
  atRisk: string;
  offTrack: string;
  priorityCritical: string;
  priorityHigh: string;
  priorityMedium: string;
  priorityLow: string;

  // Kanban Board
  kanbanTitle: string;
  kanbanSubtitle: string;
  allProjects: string;
  allAssignees: string;
  allSprints: string;
  assignedToMe: string;
  filterBySearch: string;
  columnBacklog: string;
  columnTodo: string;
  columnInProgress: string;
  columnCodeReview: string;
  columnQa: string;
  columnDone: string;
  noTasksInColumn: string;
  storyPointsShort: string;
  wipLimit: string;

  // Task Details Modal
  taskDetails: string;
  description: string;
  noDescription: string;
  subtasksAndCriteria: string;
  addSubtask: string;
  enterSubtaskTitle: string;
  timeLogs: string;
  logTime: string;
  minutes: string;
  hours: string;
  dependencies: string;
  addDependency: string;
  comments: string;
  writeComment: string;
  postComment: string;
  properties: string;
  assignee: string;
  reporter: string;
  priority: string;
  status: string;
  dueDate: string;
  estimatedHours: string;
  actualLogged: string;
  unassigned: string;
  saveChanges: string;
  close: string;
  deleteTask: string;

  // Projects View
  projectsTitle: string;
  projectsSubtitle: string;
  techStack: string;
  milestones: string;
  budgetAndSpend: string;
  lead: string;
  viewProjectDetails: string;
  noProjectsFound: string;
  createProjectTitle: string;
  projectKey: string;
  projectName: string;
  projectBudget: string;
  projectDeadline: string;

  // Sprints View
  sprintsTitle: string;
  sprintsSubtitle: string;
  startNewSprint: string;
  completeSprint: string;
  sprintGoal: string;
  totalStoryPoints: string;
  completedStoryPoints: string;
  estimatedVelocity: string;
  daysRemaining: string;

  // Time Tracker View
  timeTrackerTitle: string;
  timeTrackerSubtitle: string;
  currentRunningTimer: string;
  manualTimeLog: string;
  selectTask: string;
  durationInMinutes: string;
  workDescription: string;
  isBillable: string;
  logWorkTime: string;
  recentTimeEntries: string;
  billable: string;
  nonBillable: string;

  // AI Studio View
  aiStudioTitle: string;
  aiStudioSubtitle: string;
  aiConnected: string;
  actionMode: string;
  modeBreakdown: string;
  modeEstimate: string;
  modeCodeStub: string;
  modeRetroSummary: string;
  modeBugTriage: string;
  featureTitleOrStory: string;
  technicalContext: string;
  generateWithAi: string;
  generatingWithAi: string;
  aiOutput: string;
  copyOutput: string;
  copiedToClipboard: string;

  // Integrations View
  integrationsTitle: string;
  integrationsSubtitle: string;
  gitIntegrations: string;
  paymentGateways: string;
  infrastructureServices: string;
  connected: string;
  configured: string;
  notConfigured: string;
  testConnection: string;
  configureWebhook: string;

  // Automations View
  automationsTitle: string;
  automationsSubtitle: string;
  createNewRule: string;
  triggerEvent: string;
  actionEvent: string;
  activeStatus: string;
  timesExecuted: string;
  lastRun: string;

  // Billing & Plans View
  billingTitle: string;
  billingSubtitle: string;
  monthly: string;
  annual: string;
  save20Percent: string;
  currentPlanBadge: string;
  mostPopularBadge: string;
  upgradePlan: string;
  starterPlan: string;
  proPlan: string;
  businessPlan: string;
  enterprisePlan: string;
  invoicesHistory: string;
  invoiceNumber: string;
  billingDate: string;
  amount: string;
  paymentMethod: string;
  downloadPdf: string;

  // Team & RBAC View
  teamTitle: string;
  teamSubtitle: string;
  inviteTeammate: string;
  memberName: string;
  email: string;
  role: string;
  joinedDate: string;
  roleOwner: string;
  roleAdmin: string;
  roleProjectManager: string;
  roleLeadDeveloper: string;
  roleDeveloper: string;
  roleClient: string;
  roleViewer: string;

  // Affiliates View
  affiliatesTitle: string;
  affiliatesSubtitle: string;
  totalClicks: string;
  referredTeams: string;
  monthlyRecurring: string;
  totalPaidOut: string;
  yourReferralLink: string;
  copyLink: string;
  requestPayout: string;

  // SuperAdmin View
  superAdminTitle: string;
  superAdminSubtitle: string;
  totalTenants: string;
  totalUsers: string;
  monthlyRecurringMrr: string;
  systemUptime: string;
  healthy: string;

  // Swagger API Docs
  swaggerTitle: string;
  swaggerSubtitle: string;
  standardFormatNote: string;
  endpointsCount: string;
  testApiCall: string;

  // Settings
  settingsTitle: string;
  settingsSubtitle: string;
  generalSettings: string;
  workspaceName: string;
  customDomain: string;
  apiTokens: string;
  saveSettings: string;
  languageSelect: string;

  // Common UI
  actions: string;
  cancel: string;
  save: string;
  create: string;
  delete: string;
  edit: string;
  loading: string;
  success: string;
  error: string;
}

export const TRANSLATIONS: Record<Language, Translations> = {
  uz: {
    // Brand & Header
    brandName: 'DevTeam',
    tagline: 'Dasturchilar jamoasi uchun SaaS platforma',
    sprintActive: 'Sprint 24 Faol',
    searchPlaceholder: 'Vazifalar, sprintlar, kodlarni qidirish...',
    swaggerApi: 'Swagger API',
    newTask: 'Yangi Vazifa',
    newProject: 'Yangi Loyiha',
    activeTimer: 'Taymer Ishlamoqda',
    stopTimer: 'Taymerni To\'xtatish',
    startTimer: 'Taymerni Boshlash',
    workspace: 'Ish Maydoni',
    switchWorkspace: 'Maydonni Almashtirish',
    currentRole: 'Joriy Rol',
    logout: 'Chiqish',
    signIn: 'Kirish',
    signUp: 'Ro\'yxatdan o\'tish',
    getStarted: 'Bepul Boshlash',
    liveDemo: 'Jonli Demo',

    // Navigation
    navDashboard: 'Boshqaruv Paneli',
    navProjects: 'Loyihalar',
    navKanban: 'Kanban Doskasi',
    navTasks: 'Barcha Vazifalar',
    navSprints: 'Sprintlar & Tezlik',
    navTimeTracker: 'Vaqt Kuzatuvi',
    navAiStudio: 'Gemini AI Studio',
    navIntegrations: 'Integratsiyalar',
    navAutomations: 'Avtomatlashtirish',
    navTeam: 'Jamoa & Huquqlar',
    navAnalytics: 'Tahlil & Metrikalar',
    navBilling: 'Tariflar & To\'lovlar',
    navAffiliates: 'Hamkorlik Dasturi',
    navSuperAdmin: 'SuperAdmin Paneli',
    navSwagger: 'OpenAPI / Swagger',
    navSettings: 'Sozlamalar',
    navLanding: 'Bosh Sahifa',
    managementSection: 'BOSHQARUV & TIZIM',

    // Stats & Dashboard
    activeProjects: 'Faol Loyihalar',
    openTasks: 'Ochiq Vazifalar',
    sprintVelocity: 'Sprint Tezligi',
    teamCapacity: 'Jamoa Sig\'imi',
    ptsPerSprint: 'ball / sprint',
    acrossColumns: '4 ta ustunda',
    membersActive: 'a\'zolar (92% faol)',
    burndownProgress: 'Bajarilish Grafigi',
    ptsDone: 'Ball Bajarildi',
    percentDone: 'Bajarildi',
    recentTasks: 'Muhim Vazifalar',
    viewAll: 'Barchasini Ko\'rish →',
    onTrack: 'Reja Bo\'yicha',
    atRisk: 'Xavf Ostida',
    offTrack: 'Kechikmoqda',
    priorityCritical: 'KRITIK',
    priorityHigh: 'YUQORI',
    priorityMedium: 'O\'RTA',
    priorityLow: 'PAST',

    // Kanban Board
    kanbanTitle: 'Faol Kanban Doskasi',
    kanbanSubtitle: 'Sprint 24 • Real vaqtdagi holatlar va WIP cheklovlari',
    allProjects: 'Barcha Loyihalar',
    allAssignees: 'Barcha Mas\'ullar',
    allSprints: 'Barcha Sprintlar',
    assignedToMe: 'Menga Biriktirilgan',
    filterBySearch: 'Qidiruv orqali filtrlash...',
    columnBacklog: 'Beklog (Backlog)',
    columnTodo: 'Bajarilishi Kerak (To Do)',
    columnInProgress: 'Jarayonda (In Progress)',
    columnCodeReview: 'Kod Tekshiruvi (Code Review)',
    columnQa: 'QA Testlash (QA)',
    columnDone: 'Bajarildi (Done)',
    noTasksInColumn: 'Ushbu ustunda vazifalar yo\'q',
    storyPointsShort: 'SP',
    wipLimit: 'WIP Cheklovi',

    // Task Details Modal
    taskDetails: 'Vazifa Tafsilotlari',
    description: 'Tavsif',
    noDescription: 'Batafsil tavsif berilmagan.',
    subtasksAndCriteria: 'Kichik Vazifalar & Qabul Mezonlari',
    addSubtask: 'Kichik Vazifa Qo\'shish',
    enterSubtaskTitle: 'Kichik vazifa nomini kiriting...',
    timeLogs: 'Sarflangan Vaqtlar',
    logTime: 'Vaqt Kiritish',
    minutes: 'daqiqa',
    hours: 'soat',
    dependencies: 'Bog\'liq Vazifalar',
    addDependency: 'Bog\'liqlik Qo\'shish',
    comments: 'Izohlar',
    writeComment: 'Izoh qoldiring...',
    postComment: 'Yuborish',
    properties: 'Xususiyatlar',
    assignee: 'Mas\'ul Xodim',
    reporter: 'Muallif',
    priority: 'Muhimlik Darajasi',
    status: 'Holat',
    dueDate: 'Topshirish Muddati',
    estimatedHours: 'Rejalashtirilgan Vaqt',
    actualLogged: 'Haqiqiy Sarflangan',
    unassigned: 'Biriktirilmagan',
    saveChanges: 'O\'zgarishlarni Saqlash',
    close: 'Yopish',
    deleteTask: 'Vazifani O\'chirish',

    // Projects View
    projectsTitle: 'Dasturiy Ta\'minot Loyihalari',
    projectsSubtitle: 'Repozitoriylar, bosqichlar, byudjet va jamoa unumdorligini boshqarish',
    techStack: 'Texnologiyalar',
    milestones: 'Bosqichlar (Milestones)',
    budgetAndSpend: 'Byudjet & Xarajat',
    lead: 'Loyiha Rahbari',
    viewProjectDetails: 'Loyihani Ko\'rish →',
    noProjectsFound: 'Bu ish maydonida loyihalar topilmadi.',
    createProjectTitle: 'Yangi Loyiha Yaratish',
    projectKey: 'Loyiha Kaliti (Key)',
    projectName: 'Loyiha Nomi',
    projectBudget: 'Byudjet ($ USD)',
    projectDeadline: 'Muddati',

    // Sprints View
    sprintsTitle: 'Agile Sprintlar & Jamoa Tezligi',
    sprintsSubtitle: '2 haftalik iteratsiyalarni rejalashtiring, burndown grafiklarini kuzating',
    startNewSprint: 'Yangi Sprint Boshlash',
    completeSprint: 'Sprintni Yakunlash',
    sprintGoal: 'Sprint Maqsadi',
    totalStoryPoints: 'Jami Story Pointlar',
    completedStoryPoints: 'Bajarilgan Ballar',
    estimatedVelocity: 'O\'rtacha Tezlik',
    daysRemaining: 'Qolgan Kunlar',

    // Time Tracker View
    timeTrackerTitle: 'Vaqt Kuzatuvi & Ish Unumdorligi',
    timeTrackerSubtitle: 'Ish vaqtini hisoblang, to\'lovli soatlarni qayd eting',
    currentRunningTimer: 'Joriy Faol Taymer',
    manualTimeLog: 'Qo\'lda Vaqt Kiritish',
    selectTask: 'Vazifani Tanlang',
    durationInMinutes: 'Davomiyligi (daqiqada)',
    workDescription: 'Bajarilgan ish tavsifi...',
    isBillable: 'Mijozga hisoblanadigan vaqt (Billable)',
    logWorkTime: 'Vaqtni Saqlash',
    recentTimeEntries: 'So\'nggi Kiritilgan Vaqtlar',
    billable: 'To\'lovli',
    nonBillable: 'To\'lovsiz',

    // AI Studio View
    aiStudioTitle: 'DevTeam Gemini AI Studio',
    aiStudioSubtitle: 'Jira darajasidagi vazifalar tavsifi, qabul mezonlari va murakkablikni baholash',
    aiConnected: 'Gemini AI Ulandi',
    actionMode: 'Harakat Turi',
    modeBreakdown: 'Funksiyani Vazifalarga Bo\'lish & Qabul Mezonlari',
    modeEstimate: 'Story Pointlar & Murakkablik Tahlili',
    modeCodeStub: 'Django / React Dastlabki Kodini Yaratish',
    modeRetroSummary: 'Sprint Retrospektivasi Xulosasi',
    modeBugTriage: 'Xatolikni Tahlil Qilish & Yechim',
    featureTitleOrStory: 'Funksiya Nomi / User Story',
    technicalContext: 'Texnik Kontekst & Cheklovlar',
    generateWithAi: 'Gemini AI bilan Yaratish',
    generatingWithAi: 'Gemini AI tahlil qilmoqda...',
    aiOutput: 'AI Natijasi',
    copyOutput: 'Nusxalash',
    copiedToClipboard: 'Nusxalandi!',

    // Integrations View
    integrationsTitle: 'Tizim Integratsiyalari & Webhooklar',
    integrationsSubtitle: 'GitHub, GitLab, Stripe, Payme, Click va backend xizmatlarini boshqarish',
    gitIntegrations: 'Git Versiyalar Boshqaruvi',
    paymentGateways: 'To\'lov Tizimlari',
    infrastructureServices: 'Infratuzilma & Backend',
    connected: 'Ulangan',
    configured: 'Sozlangan',
    notConfigured: 'Sozlanmagan',
    testConnection: 'Ulanishni Tekshirish',
    configureWebhook: 'Webhookni Sozlash',

    // Automations View
    automationsTitle: 'Avtomatlashtirish Qoidalari',
    automationsSubtitle: 'Agar-Bu-Bo\'lsa-Shuni-Qil (IFTTT) ish oqimlarini avtomatlashtirish',
    createNewRule: 'Yangi Qoida Yaratish',
    triggerEvent: 'Boshlovchi Hodisa (Trigger)',
    actionEvent: 'Bajariladigan Harakat (Action)',
    activeStatus: 'Faol Holat',
    timesExecuted: 'Marta Ishga Tushdi',
    lastRun: 'So\'nggi Ishga Tushish',

    // Billing & Plans View
    billingTitle: 'SaaS Obuna Tariflari',
    billingSubtitle: 'Jamoa hajmi va ehtiyojlariga mos professional rejalar',
    monthly: 'Oylik To\'lov',
    annual: 'Yillik To\'lov',
    save20Percent: '20% Tejash',
    currentPlanBadge: 'Joriy Tarif',
    mostPopularBadge: 'Eng Ommabop',
    upgradePlan: 'Tarifni Yangilash',
    starterPlan: 'Starter (Boshlang\'ich)',
    proPlan: 'Professional (Pro)',
    businessPlan: 'Business (Biznes)',
    enterprisePlan: 'Enterprise (Korporativ)',
    invoicesHistory: 'To\'lov Tarixi & Invoyslar',
    invoiceNumber: 'Invoys №',
    billingDate: 'To\'lov Sanasi',
    amount: 'Summa',
    paymentMethod: 'To\'lov Usuli',
    downloadPdf: 'PDF Yuklab Olish',

    // Team & RBAC View
    teamTitle: 'Jamoa A\'zolari & Huquqlar Boshqaruvi',
    teamSubtitle: 'Dasturchilar, loyiha menejerlari va batafsil RBAC rollari',
    inviteTeammate: 'Hamkasbni Taklif Qilish',
    memberName: 'Xodim',
    email: 'Elektron Pochta',
    role: 'Rol',
    joinedDate: 'Qo\'shilgan Sana',
    roleOwner: 'Maydon Egasi (Owner)',
    roleAdmin: 'Administrator',
    roleProjectManager: 'Loyiha Menejeri (PM)',
    roleLeadDeveloper: 'Bosh Dasturchi (Lead Dev)',
    roleDeveloper: 'Dasturchi (Developer)',
    roleClient: 'Mijoz (Client)',
    roleViewer: 'Kuzatuvchi (Viewer)',

    // Affiliates View
    affiliatesTitle: 'Hamkorlik & Referal Dasturi',
    affiliatesSubtitle: 'Har bir taklif qilingan to\'lovchi jamoa uchun har oy 30% doimiy komissiya oling',
    totalClicks: 'Jami Bosilishlar',
    referredTeams: 'Taklif Qilingan Jamoalar',
    monthlyRecurring: 'Oylik Doimiy Daromad',
    totalPaidOut: 'Jami To\'lab Berilgan',
    yourReferralLink: 'Sizning Referal Havolangiz',
    copyLink: 'Havolani Nusxalash',
    requestPayout: 'Pulni Yechishni So\'rash',

    // SuperAdmin View
    superAdminTitle: 'SuperAdmin Boshqaruv Markazi',
    superAdminSubtitle: 'Global SaaS ko\'rsatkichlari, oylik daromad (MRR) va tizim barqarorligi',
    totalTenants: 'Jami Tashkilotlar',
    totalUsers: 'Jami Foydalanuvchilar',
    monthlyRecurringMrr: 'Oylik Daromad (MRR)',
    systemUptime: 'Tizim Barqarorligi (Uptime)',
    healthy: 'Barcha xizmatlar a\'lo holatda',

    // Swagger API Docs
    swaggerTitle: 'OpenAPI 3.0 & REST API Hujjatlari',
    swaggerSubtitle: 'drf-spectacular orqali avtomatik generatsiya qilingan interaktiv API',
    standardFormatNote: 'Barcha javoblar standart { success, message, data, errors } formatida qaytariladi.',
    endpointsCount: 'ta API Endpoint',
    testApiCall: 'So\'rovni Sinash',

    // Settings
    settingsTitle: 'Ish Maydoni & Tizim Sozlamalari',
    settingsSubtitle: 'Brending, maxsus domenlar, API kalitlari va til parametrlarini sozlash',
    generalSettings: 'Umumiy Ma\'lumotlar',
    workspaceName: 'Ish Maydoni Nomi',
    customDomain: 'Maxsus Domen',
    apiTokens: 'API Tokenlari',
    saveSettings: 'Sozlamalarni Saqlash',
    languageSelect: 'Tizim Tili (Interface Language)',

    // Common UI
    actions: 'Amallar',
    cancel: 'Bekor Qilish',
    save: 'Saqlash',
    create: 'Yaratish',
    delete: 'O\'chirish',
    edit: 'Tahrirlash',
    loading: 'Yuklanmoqda...',
    success: 'Muvaffaqiyatli!',
    error: 'Xatolik yuz berdi!',
  },

  ru: {
    // Brand & Header
    brandName: 'DevTeam',
    tagline: 'SaaS платформа для команд разработчиков',
    sprintActive: 'Спринт 24 Активен',
    searchPlaceholder: 'Поиск задач, спринтов, коммитов...',
    swaggerApi: 'Swagger API',
    newTask: 'Новая Задача',
    newProject: 'Новый Проект',
    activeTimer: 'Таймер Запущен',
    stopTimer: 'Остановить Таймер',
    startTimer: 'Запустить Таймер',
    workspace: 'Пространство',
    switchWorkspace: 'Сменить Пространство',
    currentRole: 'Текущая Роль',
    logout: 'Выйти',
    signIn: 'Войти',
    signUp: 'Регистрация',
    getStarted: 'Начать Бесплатно',
    liveDemo: 'Живое Демо',

    // Navigation
    navDashboard: 'Панель Управления',
    navProjects: 'Проекты',
    navKanban: 'Канбан Доска',
    navTasks: 'Все Задачи',
    navSprints: 'Спринты & Скорость',
    navTimeTracker: 'Учет Времени',
    navAiStudio: 'Gemini AI Студия',
    navIntegrations: 'Интеграции',
    navAutomations: 'Автоматизация',
    navTeam: 'Команда & Права',
    navAnalytics: 'Аналитика & Метрики',
    navBilling: 'Тарифы & Оплата',
    navAffiliates: 'Партнерская Программа',
    navSuperAdmin: 'СуперАдмин Панель',
    navSwagger: 'OpenAPI / Swagger',
    navSettings: 'Настройки',
    navLanding: 'Главная Страница',
    managementSection: 'УПРАВЛЕНИЕ & СИСТЕМА',

    // Stats & Dashboard
    activeProjects: 'Активные Проекты',
    openTasks: 'Открытые Задачи',
    sprintVelocity: 'Скорость Спринта',
    teamCapacity: 'Загрузка Команды',
    ptsPerSprint: 'очков / спринт',
    acrossColumns: 'в 4 колонках',
    membersActive: 'участников (92% активны)',
    burndownProgress: 'График Сгорания Задач',
    ptsDone: 'Очков Завершено',
    percentDone: 'Выполнено',
    recentTasks: 'Приоритетные Задачи',
    viewAll: 'Смотреть Все →',
    onTrack: 'В Графике',
    atRisk: 'Есть Риск',
    offTrack: 'С Отставанием',
    priorityCritical: 'КРИТИЧЕСКИЙ',
    priorityHigh: 'ВЫСОКИЙ',
    priorityMedium: 'СРЕДНИЙ',
    priorityLow: 'НИЗКИЙ',

    // Kanban Board
    kanbanTitle: 'Активная Канбан Доска',
    kanbanSubtitle: 'Спринт 24 • Отслеживание статусов в реальном времени и лимиты WIP',
    allProjects: 'Все Проекты',
    allAssignees: 'Все Исполнители',
    allSprints: 'Все Спринты',
    assignedToMe: 'Назначено Мне',
    filterBySearch: 'Фильтр по названию...',
    columnBacklog: 'Бэклог (Backlog)',
    columnTodo: 'К Выполнению (To Do)',
    columnInProgress: 'В Работе (In Progress)',
    columnCodeReview: 'Код Ревью (Code Review)',
    columnQa: 'QA Тестирование (QA)',
    columnDone: 'Завершено (Done)',
    noTasksInColumn: 'В этой колонке нет задач',
    storyPointsShort: 'SP',
    wipLimit: 'Лимит WIP',

    // Task Details Modal
    taskDetails: 'Детали Задачи',
    description: 'Описание',
    noDescription: 'Подробное описание отсутствует.',
    subtasksAndCriteria: 'Подзадачи & Критерии Приемки',
    addSubtask: 'Добавить Подзадачу',
    enterSubtaskTitle: 'Введите название подзадачи...',
    timeLogs: 'Залогированное Время',
    logTime: 'Залогировать Время',
    minutes: 'мин',
    hours: 'ч',
    dependencies: 'Зависимости Задачи',
    addDependency: 'Добавить Зависимость',
    comments: 'Комментарии',
    writeComment: 'Оставьте комментарий...',
    postComment: 'Отправить',
    properties: 'Свойства',
    assignee: 'Исполнитель',
    reporter: 'Автор',
    priority: 'Приоритет',
    status: 'Статус',
    dueDate: 'Срок Сдачи',
    estimatedHours: 'Оценка Времени',
    actualLogged: 'Фактически Потрачено',
    unassigned: 'Не назначен',
    saveChanges: 'Сохранить Изменения',
    close: 'Закрыть',
    deleteTask: 'Удалить Задачу',

    // Projects View
    projectsTitle: 'Проекты Разработки',
    projectsSubtitle: 'Управление репозиториями, вехами, бюджетом и скоростью команды',
    techStack: 'Стек Технологий',
    milestones: 'Контрольные Точки (Milestones)',
    budgetAndSpend: 'Бюджет & Расходы',
    lead: 'Тимлид Проекта',
    viewProjectDetails: 'Подробнее о Проекте →',
    noProjectsFound: 'В этом пространстве проектов пока нет.',
    createProjectTitle: 'Создать Новый Проект',
    projectKey: 'Ключ Проекта (Key)',
    projectName: 'Название Проекта',
    projectBudget: 'Бюджет ($ USD)',
    projectDeadline: 'Дедлайн',

    // Sprints View
    sprintsTitle: 'Agile Спринты & Скорость',
    sprintsSubtitle: 'Планируйте двухнедельные итерации и отслеживайте графики сгорания',
    startNewSprint: 'Начать Новый Спринт',
    completeSprint: 'Завершить Спринт',
    sprintGoal: 'Цель Спринта',
    totalStoryPoints: 'Всего Story Points',
    completedStoryPoints: 'Завершено Очков',
    estimatedVelocity: 'Расчетная Скорость',
    daysRemaining: 'Дней Осталось',

    // Time Tracker View
    timeTrackerTitle: 'Учет Времени & Продуктивность',
    timeTrackerSubtitle: 'Отслеживайте рабочие часы и оплачиваемое время по задачам',
    currentRunningTimer: 'Активный Таймер',
    manualTimeLog: 'Ручной Ввод Времени',
    selectTask: 'Выберите Задачу',
    durationInMinutes: 'Длительность (в минутах)',
    workDescription: 'Описание выполненной работы...',
    isBillable: 'Оплачиваемое клиентом время (Billable)',
    logWorkTime: 'Сохранить Время',
    recentTimeEntries: 'Последние Записи Времени',
    billable: 'Оплачиваемое',
    nonBillable: 'Неоплачиваемое',

    // AI Studio View
    aiStudioTitle: 'DevTeam Gemini AI Студия',
    aiStudioSubtitle: 'Генерация описаний задач уровня Jira, критериев приемки и оценка сложности',
    aiConnected: 'Gemini AI Подключен',
    actionMode: 'Режим Работы',
    modeBreakdown: 'Декомпозиция фичи на задачи и критерии приемки',
    modeEstimate: 'Оценка Story Points и анализ сложности',
    modeCodeStub: 'Генерация заготовки кода Django / React',
    modeRetroSummary: 'Итоги ретроспективы спринта',
    modeBugTriage: 'Анализ бага и варианты исправления',
    featureTitleOrStory: 'Название фичи / User Story',
    technicalContext: 'Технический контекст & ограничения',
    generateWithAi: 'Сгенерировать с Gemini AI',
    generatingWithAi: 'Gemini AI генерирует...',
    aiOutput: 'Результат AI',
    copyOutput: 'Копировать',
    copiedToClipboard: 'Скопировано в буфер обмена!',

    // Integrations View
    integrationsTitle: 'Интеграции Системы & Вебхуки',
    integrationsSubtitle: 'Управление GitHub, GitLab, Stripe, Payme, Click и бекенд-сервисами',
    gitIntegrations: 'Контроль Версий Git',
    paymentGateways: 'Платежные Шлюзы',
    infrastructureServices: 'Инфраструктура & Сервисы',
    connected: 'Подключено',
    configured: 'Настроено',
    notConfigured: 'Не настроено',
    testConnection: 'Проверить Подключение',
    configureWebhook: 'Настроить Вебхук',

    // Automations View
    automationsTitle: 'Правила Автоматизации',
    automationsSubtitle: 'Создание рабочих процессов Если-То (IFTTT) без кода',
    createNewRule: 'Создать Новое Правило',
    triggerEvent: 'Событие-Триггер (Trigger)',
    actionEvent: 'Выполняемое Действие (Action)',
    activeStatus: 'Активно',
    timesExecuted: 'Раз Выполнено',
    lastRun: 'Последний Запуск',

    // Billing & Plans View
    billingTitle: 'Тарифные Планы SaaS',
    billingSubtitle: 'Гибкие тарифы под масштабы и потребности вашей команды',
    monthly: 'Ежемесячно',
    annual: 'Ежегодно',
    save20Percent: 'Скидка 20%',
    currentPlanBadge: 'Текущий Тариф',
    mostPopularBadge: 'Самый Популярный',
    upgradePlan: 'Перейти на Тариф',
    starterPlan: 'Starter (Начальный)',
    proPlan: 'Professional (Про)',
    businessPlan: 'Business (Бизнес)',
    enterprisePlan: 'Enterprise (Корпоративный)',
    invoicesHistory: 'История Счетов & Оплат',
    invoiceNumber: 'Счет №',
    billingDate: 'Дата Оплаты',
    amount: 'Сумма',
    paymentMethod: 'Способ Оплаты',
    downloadPdf: 'Скачать PDF',

    // Team & RBAC View
    teamTitle: 'Участники Команды & Права Доступа',
    teamSubtitle: 'Управление разработчиками, менеджерами проектов и ролями RBAC',
    inviteTeammate: 'Пригласить Коллегу',
    memberName: 'Участник',
    email: 'Электронная Почта',
    role: 'Роль',
    joinedDate: 'Дата Вступления',
    roleOwner: 'Владелец (Owner)',
    roleAdmin: 'Администратор',
    roleProjectManager: 'Менеджер Проектов (PM)',
    roleLeadDeveloper: 'Тимлид (Lead Dev)',
    roleDeveloper: 'Разработчик (Developer)',
    roleClient: 'Клиент (Client)',
    roleViewer: 'Наблюдатель (Viewer)',

    // Affiliates View
    affiliatesTitle: 'Партнерская & Реферальная Программа',
    affiliatesSubtitle: 'Получайте 30% ежемесячных регулярных выплат с каждой привлеченной команды',
    totalClicks: 'Всего Переходов',
    referredTeams: 'Привлеченных Команд',
    monthlyRecurring: 'Ежемесячный Доход',
    totalPaidOut: 'Всего Выплачено',
    yourReferralLink: 'Ваша Реферальная Ссылка',
    copyLink: 'Скопировать Ссылку',
    requestPayout: 'Запросить Выплату',

    // SuperAdmin View
    superAdminTitle: 'Консоль СуперАдминистратора',
    superAdminSubtitle: 'Глобальные метрики SaaS, регулярный доход (MRR) и здоровье платформы',
    totalTenants: 'Всего Организаций',
    totalUsers: 'Всего Пользователей',
    monthlyRecurringMrr: 'Ежемесячный Доход (MRR)',
    systemUptime: 'Аптайм Системы (Uptime)',
    healthy: 'Все сервисы работают стабильно',

    // Swagger API Docs
    swaggerTitle: 'Документация OpenAPI 3.0 & REST API',
    swaggerSubtitle: 'Интерактивный просмотр эндпоинтов, сгенерированных drf-spectacular',
    standardFormatNote: 'Все ответы возвращаются в едином формате { success, message, data, errors }.',
    endpointsCount: 'эндпоинтов API',
    testApiCall: 'Тестировать Запрос',

    // Settings
    settingsTitle: 'Настройки Пространства & Системы',
    settingsSubtitle: 'Брендинг, кастомные домены, токены API и языковые настройки',
    generalSettings: 'Общие Настройки',
    workspaceName: 'Название Пространства',
    customDomain: 'Собственный Домен',
    apiTokens: 'Токены API',
    saveSettings: 'Сохранить Настройки',
    languageSelect: 'Язык Интерфейса (Language)',

    // Common UI
    actions: 'Действия',
    cancel: 'Отмена',
    save: 'Сохранить',
    create: 'Создать',
    delete: 'Удалить',
    edit: 'Редактировать',
    loading: 'Загрузка...',
    success: 'Успешно!',
    error: 'Произошла ошибка!',
  },

  en: {
    // Brand & Header
    brandName: 'DevTeam',
    tagline: 'SaaS Platform for Software Engineering Teams',
    sprintActive: 'Sprint 24 Active',
    searchPlaceholder: 'Search tasks, sprints, commits...',
    swaggerApi: 'Swagger API',
    newTask: 'New Task',
    newProject: 'New Project',
    activeTimer: 'Timer Running',
    stopTimer: 'Stop Timer',
    startTimer: 'Start Timer',
    workspace: 'Workspace',
    switchWorkspace: 'Switch Workspace',
    currentRole: 'Current Role',
    logout: 'Sign Out',
    signIn: 'Sign In',
    signUp: 'Sign Up',
    getStarted: 'Get Started Free',
    liveDemo: 'Live Demo',

    // Navigation
    navDashboard: 'Dashboard',
    navProjects: 'Projects',
    navKanban: 'Kanban Board',
    navTasks: 'All Tasks',
    navSprints: 'Sprints & Velocity',
    navTimeTracker: 'Time Tracker',
    navAiStudio: 'Gemini AI Studio',
    navIntegrations: 'Integrations',
    navAutomations: 'Automations',
    navTeam: 'Team & Access',
    navAnalytics: 'Analytics & Metrics',
    navBilling: 'Billing & Plans',
    navAffiliates: 'Affiliate Program',
    navSuperAdmin: 'SuperAdmin Panel',
    navSwagger: 'OpenAPI / Swagger',
    navSettings: 'Settings',
    navLanding: 'Landing Page',
    managementSection: 'MANAGEMENT & SYSTEM',

    // Stats & Dashboard
    activeProjects: 'Active Projects',
    openTasks: 'Open Tasks',
    sprintVelocity: 'Sprint Velocity',
    teamCapacity: 'Team Capacity',
    ptsPerSprint: 'pts / sprint',
    acrossColumns: 'across 4 columns',
    membersActive: 'members (92% active)',
    burndownProgress: 'Burndown Progress',
    ptsDone: 'Points Completed',
    percentDone: 'Done',
    recentTasks: 'Priority Tasks',
    viewAll: 'View All →',
    onTrack: 'On Track',
    atRisk: 'At Risk',
    offTrack: 'Off Track',
    priorityCritical: 'CRITICAL',
    priorityHigh: 'HIGH',
    priorityMedium: 'MEDIUM',
    priorityLow: 'LOW',

    // Kanban Board
    kanbanTitle: 'Active Kanban Board',
    kanbanSubtitle: 'Sprint 24 • Real-time status progression and WIP monitoring',
    allProjects: 'All Projects',
    allAssignees: 'All Assignees',
    allSprints: 'All Sprints',
    assignedToMe: 'Assigned to Me',
    filterBySearch: 'Filter by title or key...',
    columnBacklog: 'Backlog',
    columnTodo: 'To Do',
    columnInProgress: 'In Progress',
    columnCodeReview: 'Code Review',
    columnQa: 'QA Testing',
    columnDone: 'Done',
    noTasksInColumn: 'No tasks in this column',
    storyPointsShort: 'SP',
    wipLimit: 'WIP Limit',

    // Task Details Modal
    taskDetails: 'Task Details',
    description: 'Description',
    noDescription: 'No detailed description provided.',
    subtasksAndCriteria: 'Subtasks & Acceptance Criteria',
    addSubtask: 'Add Subtask',
    enterSubtaskTitle: 'Enter subtask title...',
    timeLogs: 'Logged Time',
    logTime: 'Log Time',
    minutes: 'mins',
    hours: 'hrs',
    dependencies: 'Task Dependencies',
    addDependency: 'Add Dependency',
    comments: 'Comments',
    writeComment: 'Leave a comment...',
    postComment: 'Post Comment',
    properties: 'Properties',
    assignee: 'Assignee',
    reporter: 'Reporter',
    priority: 'Priority',
    status: 'Status',
    dueDate: 'Due Date',
    estimatedHours: 'Estimated Hours',
    actualLogged: 'Actual Logged',
    unassigned: 'Unassigned',
    saveChanges: 'Save Changes',
    close: 'Close',
    deleteTask: 'Delete Task',

    // Projects View
    projectsTitle: 'Software Projects',
    projectsSubtitle: 'Manage repositories, milestones, budgets, and engineering velocity',
    techStack: 'Tech Stack',
    milestones: 'Milestones',
    budgetAndSpend: 'Budget & Spend',
    lead: 'Project Lead',
    viewProjectDetails: 'Project Details →',
    noProjectsFound: 'No projects found in this workspace.',
    createProjectTitle: 'Create New Project',
    projectKey: 'Project Key',
    projectName: 'Project Name',
    projectBudget: 'Budget ($ USD)',
    projectDeadline: 'Deadline',

    // Sprints View
    sprintsTitle: 'Agile Sprints & Velocity',
    sprintsSubtitle: 'Plan 2-week iterations, track burndown charts, and analyze team capacity',
    startNewSprint: 'Start New Sprint',
    completeSprint: 'Complete Sprint',
    sprintGoal: 'Sprint Goal',
    totalStoryPoints: 'Total Story Points',
    completedStoryPoints: 'Completed Points',
    estimatedVelocity: 'Estimated Velocity',
    daysRemaining: 'Days Remaining',

    // Time Tracker View
    timeTrackerTitle: 'Time Tracker & Productivity',
    timeTrackerSubtitle: 'Track logged hours, billable ratios, and team member time sheets',
    currentRunningTimer: 'Active Running Timer',
    manualTimeLog: 'Manual Time Log',
    selectTask: 'Select Task',
    durationInMinutes: 'Duration (in minutes)',
    workDescription: 'Work log description...',
    isBillable: 'Billable to client',
    logWorkTime: 'Save Time Log',
    recentTimeEntries: 'Recent Time Entries',
    billable: 'Billable',
    nonBillable: 'Non-Billable',

    // AI Studio View
    aiStudioTitle: 'DevTeam Gemini AI Studio',
    aiStudioSubtitle: 'Generate Jira-grade user stories, acceptance criteria, story points, and test scenarios',
    aiConnected: 'Gemini AI Connected',
    actionMode: 'Action Mode',
    modeBreakdown: 'Breakdown Feature into Tasks & Acceptance Criteria',
    modeEstimate: 'Estimate Story Points & Complexity Analysis',
    modeCodeStub: 'Generate Django / React Implementation Stub',
    modeRetroSummary: 'Sprint Retrospective Summary',
    modeBugTriage: 'Bug Triage & Root Cause Analysis',
    featureTitleOrStory: 'Feature Title / User Story',
    technicalContext: 'Technical Context & Constraints',
    generateWithAi: 'Generate with Gemini AI',
    generatingWithAi: 'Generating with Gemini AI...',
    aiOutput: 'AI Output',
    copyOutput: 'Copy Output',
    copiedToClipboard: 'Copied to clipboard!',

    // Integrations View
    integrationsTitle: 'System Integrations & Webhooks',
    integrationsSubtitle: 'Manage GitHub, GitLab, Stripe, Payme, Click, and backend infrastructure',
    gitIntegrations: 'Git Version Control',
    paymentGateways: 'Payment Gateways',
    infrastructureServices: 'Infrastructure & Backend',
    connected: 'Connected',
    configured: 'Configured',
    notConfigured: 'Not Configured',
    testConnection: 'Test Connection',
    configureWebhook: 'Configure Webhook',

    // Automations View
    automationsTitle: 'Automation Rules',
    automationsSubtitle: 'No-code If-This-Then-That (IFTTT) developer workflow automation',
    createNewRule: 'Create New Rule',
    triggerEvent: 'Trigger Event',
    actionEvent: 'Action Event',
    activeStatus: 'Active',
    timesExecuted: 'Times Executed',
    lastRun: 'Last Run',

    // Billing & Plans View
    billingTitle: 'SaaS Subscription Plans',
    billingSubtitle: 'Scale your engineering workflow with custom user seats, storage, and AI limits',
    monthly: 'Monthly',
    annual: 'Annual',
    save20Percent: 'Save 20%',
    currentPlanBadge: 'Current Plan',
    mostPopularBadge: 'Most Popular',
    upgradePlan: 'Upgrade Plan',
    starterPlan: 'Starter',
    proPlan: 'Professional',
    businessPlan: 'Business',
    enterprisePlan: 'Enterprise',
    invoicesHistory: 'Invoices & Billing History',
    invoiceNumber: 'Invoice #',
    billingDate: 'Billing Date',
    amount: 'Amount',
    paymentMethod: 'Payment Method',
    downloadPdf: 'Download PDF',

    // Team & RBAC View
    teamTitle: 'Team Members & Access Control',
    teamSubtitle: 'Manage developers, project managers, fine-grained RBAC roles, and invites',
    inviteTeammate: 'Invite Teammate',
    memberName: 'Member',
    email: 'Email',
    role: 'Role',
    joinedDate: 'Joined Date',
    roleOwner: 'Workspace Owner',
    roleAdmin: 'Administrator',
    roleProjectManager: 'Project Manager (PM)',
    roleLeadDeveloper: 'Lead Developer',
    roleDeveloper: 'Developer',
    roleClient: 'Client Viewer',
    roleViewer: 'Read-only Viewer',

    // Affiliates View
    affiliatesTitle: 'Referral & Affiliate Partner Program',
    affiliatesSubtitle: 'Earn 30% recurring monthly commissions on every paying engineering team you refer',
    totalClicks: 'Total Clicks',
    referredTeams: 'Referred Teams',
    monthlyRecurring: 'Monthly Recurring',
    totalPaidOut: 'Total Paid Out',
    yourReferralLink: 'Your Unique Referral Link',
    copyLink: 'Copy Link',
    requestPayout: 'Request Payout',

    // SuperAdmin View
    superAdminTitle: 'SuperAdmin SaaS Console',
    superAdminSubtitle: 'Global platform telemetry, monthly recurring revenue (MRR), and system uptime',
    totalTenants: 'Total Tenants',
    totalUsers: 'Total Users',
    monthlyRecurringMrr: 'Monthly Recurring (MRR)',
    systemUptime: 'API System Uptime',
    healthy: 'All systems operating normally',

    // Swagger API Docs
    swaggerTitle: 'OpenAPI 3.0 & REST API Documentation',
    swaggerSubtitle: 'Interactive Swagger UI generated via drf-spectacular',
    standardFormatNote: 'All endpoints return standardized { success, message, data, errors } format.',
    endpointsCount: 'API Endpoints',
    testApiCall: 'Test API Call',

    // Settings
    settingsTitle: 'Workspace & System Settings',
    settingsSubtitle: 'Configure tenant custom domains, branding, webhook tokens, and language',
    generalSettings: 'General Profile & Identity',
    workspaceName: 'Workspace Name',
    customDomain: 'Custom Domain',
    apiTokens: 'API Access Tokens',
    saveSettings: 'Save Settings',
    languageSelect: 'Interface Language',

    // Common UI
    actions: 'Actions',
    cancel: 'Cancel',
    save: 'Save',
    create: 'Create',
    delete: 'Delete',
    edit: 'Edit',
    loading: 'Loading...',
    success: 'Success!',
    error: 'An error occurred!',
  }
};
