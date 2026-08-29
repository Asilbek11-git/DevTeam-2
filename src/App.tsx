import React, { useState } from 'react';
import {
  INITIAL_USERS,
  INITIAL_PLANS,
  INITIAL_WORKSPACES,
  INITIAL_MEMBERS,
  INITIAL_PROJECTS,
  INITIAL_COLUMNS,
  INITIAL_SPRINTS,
  INITIAL_TASKS,
  INITIAL_INVOICES,
  INITIAL_AUTOMATIONS,
  INITIAL_NOTIFICATIONS,
} from './data/initialData';
import {
  User, Workspace, WorkspaceMember, Project, BoardColumn,
  Sprint, Task, Plan, Invoice, AutomationRule, NotificationItem,
  WorkspaceRole, TaskStatus, Language
} from './types';
import { TRANSLATIONS } from './data/translations';

// Components
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { LandingPage } from './components/LandingPage';
import { KanbanBoard } from './components/KanbanBoard';
import { SprintManager } from './components/SprintManager';
import { ProjectList } from './components/ProjectList';
import { TaskDetailModal } from './components/TaskDetailModal';
import { TimeTrackerView } from './components/TimeTrackerView';
import { IntegrationsView } from './components/IntegrationsView';
import { AutomationEngine } from './components/AutomationEngine';
import { AiStudioView } from './components/AiStudioView';
import { BillingView } from './components/BillingView';
import { TeamView } from './components/TeamView';
import { SuperAdminDashboard } from './components/SuperAdminDashboard';
import { AffiliateView } from './components/AffiliateView';
import { SwaggerApiDocs } from './components/SwaggerApiDocs';
import { NotificationModal } from './components/NotificationModal';
import { CreateTaskModal } from './components/CreateTaskModal';
import { CreateProjectModal } from './components/CreateProjectModal';

export default function App() {
  // Global State
  const [lang, setLang] = useState<Language>('uz');
  const t = TRANSLATIONS[lang] || TRANSLATIONS.uz;

  const [currentView, setCurrentView] = useState<string>('kanban');
  const [users, setUsers] = useState<User[]>(INITIAL_USERS);
  const [currentUser, setCurrentUser] = useState<User>(INITIAL_USERS[0]);
  const [currentRole, setCurrentRole] = useState<WorkspaceRole>('OWNER');
  
  const [workspaces, setWorkspaces] = useState<Workspace[]>(INITIAL_WORKSPACES);
  const [currentWorkspace, setCurrentWorkspace] = useState<Workspace>(INITIAL_WORKSPACES[0]);
  const [members, setMembers] = useState<WorkspaceMember[]>(INITIAL_MEMBERS);
  const [plans, setPlans] = useState<Plan[]>(INITIAL_PLANS);
  const [invoices, setInvoices] = useState<Invoice[]>(INITIAL_INVOICES);
  
  const [projects, setProjects] = useState<Project[]>(INITIAL_PROJECTS);
  const [columns, setColumns] = useState<BoardColumn[]>(INITIAL_COLUMNS);
  const [sprints, setSprints] = useState<Sprint[]>(INITIAL_SPRINTS);
  const [tasks, setTasks] = useState<Task[]>(INITIAL_TASKS);
  
  const [automations, setAutomations] = useState<AutomationRule[]>(INITIAL_AUTOMATIONS);
  const [notifications, setNotifications] = useState<NotificationItem[]>(INITIAL_NOTIFICATIONS);

  // Modals state
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [createTaskModalOpen, setCreateTaskModalOpen] = useState(false);
  const [createTaskDefaultStatus, setCreateTaskDefaultStatus] = useState<TaskStatus>('TODO');
  const [createProjectModalOpen, setCreateProjectModalOpen] = useState(false);
  const [notificationModalOpen, setNotificationModalOpen] = useState(false);

  // Task Status Update (with Automation trigger execution)
  const handleUpdateTaskStatus = (taskId: string, newStatus: TaskStatus) => {
    setTasks(prev => prev.map(t => {
      if (t.id === taskId) {
        return { ...t, status: newStatus };
      }
      return t;
    }));

    // Trigger automation check
    if (newStatus === 'CODE_REVIEW') {
      // Find automation rule
      const rule = automations.find(a => a.trigger === 'TASK_STATUS_CHANGED' && a.is_active);
      if (rule) {
        setNotifications(prev => [
          {
            id: `n-${Date.now()}`,
            title: 'Automation Triggered: Code Review Alert',
            message: `Task status transitioned to Code Review -> Notification dispatched to Lead Developers.`,
            notification_type: 'CODE_REVIEW',
            created_at: 'Just now',
            is_read: false,
          },
          ...prev
        ]);
      }
    }
  };

  // Full Task Update
  const handleUpdateTask = (updatedTask: Task) => {
    setTasks(prev => prev.map(t => t.id === updatedTask.id ? updatedTask : t));
    if (selectedTask?.id === updatedTask.id) {
      setSelectedTask(updatedTask);
    }
  };

  // Delete Task
  const handleDeleteTask = (taskId: string) => {
    setTasks(prev => prev.filter(t => t.id !== taskId));
    setSelectedTask(null);
  };

  // Log Time on Task
  const handleLogTime = (taskId: string, durationMinutes: number, note: string, isBillable: boolean) => {
    const newLog = {
      id: `tl-${Date.now()}`,
      task_id: taskId,
      user: currentUser,
      description: note,
      start_time: new Date().toISOString(),
      duration_minutes: durationMinutes,
      is_billable: isBillable,
    };

    setTasks(prev => prev.map(t => {
      if (t.id === taskId) {
        return {
          ...t,
          time_logs: [...(t.time_logs || []), newLog],
          actual_hours: +(t.actual_hours + durationMinutes / 60).toFixed(2),
        };
      }
      return t;
    }));
  };

  // Webhook Simulator Action
  const handleSimulateWebhook = (event: 'commit' | 'pr_opened' | 'pr_merged', payload: any) => {
    if (event === 'commit') {
      const target = tasks.find(t => t.key === payload.task_key);
      if (target) {
        const comment = {
          id: `c-${Date.now()}`,
          task_id: target.id,
          author: { ...currentUser, first_name: 'GitHub', last_name: 'Bot' },
          content: `🔗 Linked Git Commit \`${payload.sha}\`: "${payload.message}" by @${payload.author}`,
          created_at: new Date().toISOString(),
        };
        handleUpdateTask({ ...target, comments: [...(target.comments || []), comment] });
      }
    } else if (event === 'pr_opened') {
      const target = tasks.find(t => t.key === payload.task_key);
      if (target) {
        handleUpdateTask({ ...target, status: 'CODE_REVIEW' });
      }
    } else if (event === 'pr_merged') {
      const target = tasks.find(t => t.key === payload.task_key);
      if (target) {
        // Automation moves task to QA
        handleUpdateTask({ ...target, status: 'QA' });
        setNotifications(prev => [
          {
            id: `n-${Date.now()}`,
            title: `PR #${payload.pr_number} Merged -> Moved to QA`,
            message: `Pull Request merged into main branch. Automated rule advanced ${payload.task_key} to QA & Test.`,
            notification_type: 'CODE_REVIEW',
            created_at: 'Just now',
            is_read: false,
          },
          ...prev
        ]);
      }
    }
  };

  // AI Task Description Generator (Mock Gemini Response)
  const handleGenerateAiDescription = async (title: string): Promise<string> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(`### 📌 Specification: ${title}\n\n#### 🎯 Objective:\nEnsure high reliability, idempotency, and security for the payment and task orchestrator.\n\n#### ✅ Definition of Done & Acceptance Criteria:\n- [ ] Core algorithm implemented with unit test coverage > 90%.\n- [ ] Idempotent caching layer validates duplicate payload signatures.\n- [ ] Standard JSON response format returned for all success/error branches.\n- [ ] Code reviewed and approved by Lead Developer.`);
      }, 1000);
    });
  };

  // Plan Upgrade
  const handleUpgradePlan = (plan: Plan, billingCycle: 'monthly' | 'yearly', gateway: 'stripe' | 'payme' | 'click', couponCode?: string) => {
    const updatedWs = { ...currentWorkspace, plan_tier: plan.tier };
    setCurrentWorkspace(updatedWs);
    setWorkspaces(prev => prev.map(w => w.id === updatedWs.id ? updatedWs : w));

    // Create Invoice record
    const price = billingCycle === 'yearly' ? plan.yearly_price : plan.monthly_price;
    const discount = couponCode?.toUpperCase() === 'LAUNCH2026' ? 0.75 : 1.0;
    const finalAmount = price * discount;

    const newInvoice: Invoice = {
      id: `inv-${Date.now()}`,
      invoice_number: `INV-2026-00${Math.floor(Math.random() * 900) + 100}`,
      amount: finalAmount,
      currency: 'USD',
      status: 'PAID',
      payment_method: `${gateway.toUpperCase()} Gateway`,
      paid_at: new Date().toISOString().replace('T', ' ').substring(0, 19),
      plan_name: `${plan.name} (${billingCycle})`,
    };

    setInvoices(prev => [newInvoice, ...prev]);
  };

  // Persona 1-Click Select
  const handleSelectPersona = (email: string) => {
    const found = users.find(u => u.email === email);
    if (found) {
      setCurrentUser(found);
      if (found.role === 'SUPERADMIN') setCurrentRole('OWNER');
      else if (found.job_title.includes('Manager')) setCurrentRole('PROJECT_MANAGER');
      else if (found.job_title.includes('Lead')) setCurrentRole('LEAD_DEVELOPER');
      else setCurrentRole('DEVELOPER');
    }
    setCurrentView('kanban');
  };

  // Render Public Landing Page
  if (currentView === 'landing') {
    return (
      <LandingPage
        onEnterApp={() => setCurrentView('kanban')}
        onSelectPersona={handleSelectPersona}
        plans={plans}
      />
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-blue-600 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        currentWorkspace={currentWorkspace}
        workspaces={workspaces}
        onSelectWorkspace={setCurrentWorkspace}
        currentUser={currentUser}
        users={users}
        onSwitchUser={setCurrentUser}
        currentRole={currentRole}
        onChangeRole={setCurrentRole}
        notifications={notifications}
        onOpenNotifications={() => setNotificationModalOpen(true)}
        onOpenCreateTask={() => {
          setCreateTaskDefaultStatus('TODO');
          setCreateTaskModalOpen(true);
        }}
        onOpenAiStudio={() => setCurrentView('ai_studio')}
        onNavigate={setCurrentView}
        currentView={currentView}
        lang={lang}
        onLanguageChange={setLang}
        t={t}
      />

      {/* Main Layout Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          currentView={currentView}
          onNavigate={setCurrentView}
          currentWorkspace={currentWorkspace}
          tasksCount={tasks.length}
          projectsCount={projects.length}
          t={t}
        />

        {/* View Router */}
        <main className="flex-1 flex flex-col overflow-hidden bg-slate-950">
          {currentView === 'kanban' && (
            <KanbanBoard
              tasks={tasks}
              columns={columns}
              sprints={sprints}
              users={users}
              onUpdateTaskStatus={handleUpdateTaskStatus}
              onSelectTask={setSelectedTask}
              onOpenCreateTask={(defaultStatus) => {
                setCreateTaskDefaultStatus(defaultStatus || 'TODO');
                setCreateTaskModalOpen(true);
              }}
              t={t}
            />
          )}

          {currentView === 'sprints' && (
            <SprintManager
              sprints={sprints}
              tasks={tasks}
              onStartSprint={(sprintId) => {
                setSprints(prev => prev.map(s => s.id === sprintId ? { ...s, status: 'ACTIVE' } : s));
              }}
              onCompleteSprint={(sprintId) => {
                setSprints(prev => prev.map(s => s.id === sprintId ? { ...s, status: 'COMPLETED' } : s));
              }}
              onOpenAiSprintSummary={() => setCurrentView('ai_studio')}
              t={t}
            />
          )}

          {currentView === 'projects' && (
            <ProjectList
              projects={projects}
              currentWorkspace={currentWorkspace}
              onSelectProject={(p) => setCurrentView('kanban')}
              onOpenCreateProject={() => setCreateProjectModalOpen(true)}
              t={t}
            />
          )}

          {currentView === 'timetracker' && (
            <TimeTrackerView
              tasks={tasks}
              currentUser={currentUser}
              onLogTime={handleLogTime}
              t={t}
            />
          )}

          {currentView === 'integrations' && (
            <IntegrationsView
              tasks={tasks}
              onSimulateWebhook={handleSimulateWebhook}
            />
          )}

          {currentView === 'automations' && (
            <AutomationEngine
              rules={automations}
              onToggleRule={(ruleId) => {
                setAutomations(prev => prev.map(r => r.id === ruleId ? { ...r, is_active: !r.is_active } : r));
              }}
              onCreateRule={(newRule) => {
                setAutomations(prev => [
                  {
                    id: `auto-${Date.now()}`,
                    workspace_id: currentWorkspace.id,
                    name: newRule.name || 'New Rule',
                    trigger: newRule.trigger || 'PR_MERGED',
                    trigger_label: newRule.trigger_label || '',
                    action: newRule.action || 'MOVE_TASK_TO',
                    action_label: newRule.action_label || '',
                    is_active: true,
                    execution_count: 0,
                  },
                  ...prev
                ]);
              }}
              t={t}
            />
          )}

          {currentView === 'ai_studio' && (
            <AiStudioView
              tasks={tasks}
              sprints={sprints}
              t={t}
            />
          )}

          {currentView === 'billing' && (
            <BillingView
              currentWorkspace={currentWorkspace}
              plans={plans}
              invoices={invoices}
              onUpgradePlan={handleUpgradePlan}
              t={t}
            />
          )}

          {currentView === 'team' && (
            <TeamView
              members={members}
              onInviteMember={(email, role) => {
                const newUser: User = {
                  id: `u-${Date.now()}`,
                  email,
                  username: email.split('@')[0],
                  first_name: email.split('@')[0],
                  last_name: 'Member',
                  role: 'USER',
                  job_title: 'Software Developer',
                  timezone: 'UTC',
                };
                setUsers(prev => [...prev, newUser]);
                setMembers(prev => [
                  ...prev,
                  {
                    id: `m-${Date.now()}`,
                    workspace_id: currentWorkspace.id,
                    user: newUser,
                    role,
                    is_active: true,
                    joined_at: new Date().toISOString().split('T')[0],
                  }
                ]);
              }}
              onUpdateRole={(memberId, newRole) => {
                setMembers(prev => prev.map(m => m.id === memberId ? { ...m, role: newRole } : m));
              }}
              onRemoveMember={(memberId) => {
                setMembers(prev => prev.filter(m => m.id !== memberId));
              }}
              t={t}
            />
          )}

          {currentView === 'superadmin' && (
            <SuperAdminDashboard t={t} />
          )}

          {currentView === 'affiliates' && (
            <AffiliateView currentUser={currentUser} />
          )}

          {currentView === 'api_docs' && (
            <SwaggerApiDocs />
          )}
        </main>
      </div>

      {/* Task Detail Modal */}
      {selectedTask && (
        <TaskDetailModal
          task={selectedTask}
          allTasks={tasks}
          users={users}
          onClose={() => setSelectedTask(null)}
          onUpdateTask={handleUpdateTask}
          onDeleteTask={handleDeleteTask}
          onGenerateAiDescription={handleGenerateAiDescription}
        />
      )}

      {/* Create Task Modal */}
      {createTaskModalOpen && (
        <CreateTaskModal
          defaultStatus={createTaskDefaultStatus}
          projects={projects}
          sprints={sprints}
          users={users}
          onClose={() => setCreateTaskModalOpen(false)}
          onCreate={(newTaskData) => {
            const created: Task = {
              id: `task-${Date.now()}`,
              workspace_id: currentWorkspace.id,
              project_id: newTaskData.project_id || projects[0]?.id || '',
              project_key: newTaskData.project_key || 'DEV',
              project_name: newTaskData.project_name || 'Main Project',
              sprint_id: newTaskData.sprint_id,
              key: newTaskData.key || `DEV-${Math.floor(Math.random() * 900) + 100}`,
              title: newTaskData.title || '',
              description: newTaskData.description || '',
              status: newTaskData.status || 'TODO',
              priority: newTaskData.priority || 'HIGH',
              assignee: newTaskData.assignee || currentUser,
              reporter: currentUser,
              due_date: newTaskData.due_date || '2026-09-05',
              estimated_hours: newTaskData.estimated_hours || 8,
              actual_hours: 0,
              story_points: newTaskData.story_points || 3,
              tags: newTaskData.tags || ['feature'],
              order: tasks.length,
              subtasks: [],
              dependencies: [],
              time_logs: [],
              comments: [],
              created_at: new Date().toISOString(),
            };
            setTasks(prev => [created, ...prev]);
          }}
        />
      )}

      {/* Create Project Modal */}
      {createProjectModalOpen && (
        <CreateProjectModal
          users={users}
          onClose={() => setCreateProjectModalOpen(false)}
          onCreate={(newProjectData) => {
            const created: Project = {
              id: `proj-${Date.now()}`,
              workspace_id: currentWorkspace.id,
              name: newProjectData.name || 'New Project',
              key: newProjectData.key || 'NP',
              description: newProjectData.description || '',
              status: 'ACTIVE',
              health: 'ON_TRACK',
              start_date: newProjectData.start_date || new Date().toISOString().split('T')[0],
              deadline: newProjectData.deadline || '2026-11-30',
              owner: newProjectData.owner || currentUser,
              lead: newProjectData.lead || currentUser,
              tech_stack: newProjectData.tech_stack || ['Python', 'Django'],
              repository_url: newProjectData.repository_url || '',
              budget: newProjectData.budget || 20000,
              spent_budget: 0,
              tags: ['new'],
              milestones: newProjectData.milestones || [],
            };
            setProjects(prev => [created, ...prev]);
          }}
        />
      )}

      {/* Notifications Drawer */}
      {notificationModalOpen && (
        <NotificationModal
          notifications={notifications}
          onClose={() => setNotificationModalOpen(false)}
          onMarkAllRead={() => {
            setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
          }}
          onClearAll={() => setNotifications([])}
        />
      )}
    </div>
  );
}

