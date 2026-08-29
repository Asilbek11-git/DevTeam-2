export type Language = 'uz' | 'ru' | 'en';

export type GlobalRole = 'SUPERADMIN' | 'USER';

export type WorkspaceRole = 
  | 'OWNER'
  | 'ADMIN'
  | 'PROJECT_MANAGER'
  | 'LEAD_DEVELOPER'
  | 'DEVELOPER'
  | 'CLIENT'
  | 'VIEWER';

export type TaskStatus = 
  | 'BACKLOG'
  | 'TODO'
  | 'IN_PROGRESS'
  | 'CODE_REVIEW'
  | 'QA'
  | 'DONE'
  | 'CANCELLED';

export type TaskPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type ProjectHealth = 'ON_TRACK' | 'AT_RISK' | 'OFF_TRACK';

export type PlanTier = 'FREE' | 'PRO' | 'BUSINESS' | 'ENTERPRISE';

export type PaymentGatewayType = 'stripe' | 'payme' | 'click';

export interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: GlobalRole;
  avatar?: string;
  job_title: string;
  github_username?: string;
  timezone: string;
  referral_code?: string;
}

export interface WorkspaceMember {
  id: string;
  workspace_id: string;
  user: User;
  role: WorkspaceRole;
  is_active: boolean;
  joined_at: string;
}

export interface Workspace {
  id: string;
  name: string;
  slug: string;
  description: string;
  owner_id: string;
  timezone: string;
  language: string;
  brand_color: string;
  plan_tier: PlanTier;
  members_count: number;
}

export interface Milestone {
  id: string;
  workspace_id: string;
  project_id: string;
  name: string;
  deadline: string;
  status: 'PLANNED' | 'IN_PROGRESS' | 'COMPLETED' | 'DELAYED';
  progress: number;
}

export interface Project {
  id: string;
  workspace_id: string;
  name: string;
  key: string;
  description: string;
  status: 'PLANNING' | 'ACTIVE' | 'ON_HOLD' | 'COMPLETED' | 'ARCHIVED';
  health: ProjectHealth;
  start_date: string;
  deadline: string;
  owner: User;
  lead: User;
  tech_stack: string[];
  repository_url: string;
  budget: number;
  spent_budget: number;
  tags: string[];
  milestones: Milestone[];
}

export interface BoardColumn {
  id: string;
  board_id: string;
  title: string;
  status_mapping: TaskStatus;
  order: number;
  wip_limit: number;
  color: string;
}

export interface Sprint {
  id: string;
  workspace_id: string;
  project_id: string;
  name: string;
  goal: string;
  status: 'PLANNING' | 'ACTIVE' | 'COMPLETED';
  start_date: string;
  end_date: string;
  total_story_points: number;
  completed_story_points: number;
  velocity: number;
}

export interface Subtask {
  id: string;
  title: string;
  is_completed: boolean;
  assignee?: User;
}

export interface TaskDependency {
  id: string;
  predecessor_id: string;
  predecessor_key: string;
  successor_id: string;
  successor_key: string;
  dependency_type: 'BLOCKS' | 'RELATES_TO';
}

export interface TimeLog {
  id: string;
  task_id: string;
  user: User;
  description: string;
  start_time: string;
  duration_minutes: number;
  is_billable: boolean;
}

export interface TaskComment {
  id: string;
  task_id: string;
  author: User;
  content: string;
  created_at: string;
}

export interface Task {
  id: string;
  workspace_id: string;
  project_id: string;
  project_key: string;
  project_name: string;
  sprint_id?: string;
  milestone_id?: string;
  key: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  reporter: User;
  assignee: User;
  due_date: string;
  estimated_hours: number;
  actual_hours: number;
  story_points: number;
  tags: string[];
  order: number;
  subtasks: Subtask[];
  dependencies: TaskDependency[];
  time_logs: TimeLog[];
  comments: TaskComment[];
  created_at: string;
}

export interface Plan {
  id: string;
  name: string;
  tier: PlanTier;
  description: string;
  monthly_price: number;
  yearly_price: number;
  is_popular?: boolean;
  max_members: number;
  max_projects: number;
  max_storage_mb: number;
  max_ai_generations_per_month: number;
  max_automation_rules: number;
  has_git_integrations: boolean;
  has_advanced_reports: boolean;
  has_white_label: boolean;
  has_sso: boolean;
  has_priority_support: boolean;
}

export interface Invoice {
  id: string;
  invoice_number: string;
  amount: number;
  currency: string;
  status: 'PAID' | 'FAILED' | 'REFUNDED';
  payment_method: string;
  paid_at: string;
  plan_name: string;
}

export interface AutomationRule {
  id: string;
  workspace_id: string;
  name: string;
  trigger: 'TASK_STATUS_CHANGED' | 'PR_OPENED' | 'PR_MERGED' | 'TASK_OVERDUE';
  trigger_label: string;
  action: 'MOVE_TASK_TO' | 'NOTIFY_ROLE' | 'ASSIGN_TO_USER';
  action_label: string;
  is_active: boolean;
  execution_count: number;
  last_triggered?: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  notification_type: string;
  created_at: string;
  is_read: boolean;
  action_url?: string;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data: T | null;
  errors: string[] | null;
}
