import React from 'react';
import {
  LayoutDashboard, Flame, FolderGit2, Clock, GitPullRequest,
  Cpu, Sparkles, CreditCard, Users, BarChart3, Share2, FileCode2, ChevronRight, CheckCircle2
} from 'lucide-react';
import { Workspace, PlanTier, Language } from '../types';
import { Translations } from '../data/translations';

interface SidebarProps {
  currentView: string;
  onNavigate: (view: string) => void;
  currentWorkspace: Workspace;
  tasksCount: number;
  projectsCount: number;
  t: Translations;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentView,
  onNavigate,
  currentWorkspace,
  tasksCount,
  projectsCount,
  t,
}) => {
  const navSections = [
    {
      title: t.navKanban + ' & ' + t.navSprints,
      items: [
        { id: 'kanban', label: t.navKanban, icon: LayoutDashboard, badge: tasksCount },
        { id: 'sprints', label: t.navSprints, icon: Flame },
        { id: 'projects', label: t.navProjects, icon: FolderGit2, badge: projectsCount },
        { id: 'timetracker', label: t.navTimeTracker, icon: Clock },
      ]
    },
    {
      title: t.navIntegrations + ' & AI',
      items: [
        { id: 'integrations', label: t.navIntegrations, icon: GitPullRequest, tag: 'Live' },
        { id: 'automations', label: t.navAutomations, icon: Cpu },
        { id: 'ai_studio', label: t.navAiStudio, icon: Sparkles, highlight: true },
      ]
    },
    {
      title: t.managementSection,
      items: [
        { id: 'billing', label: t.navBilling, icon: CreditCard },
        { id: 'team', label: t.navTeam, icon: Users },
        { id: 'superadmin', label: t.navSuperAdmin, icon: BarChart3, tag: 'Admin' },
        { id: 'affiliates', label: t.navAffiliates, icon: Share2 },
        { id: 'api_docs', label: t.navSwagger, icon: FileCode2 },
      ]
    }
  ];

  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-800 text-slate-300 flex flex-col justify-between select-none h-[calc(100vh-53px)] sticky top-[53px] overflow-y-auto">
      <div className="p-3 space-y-5">
        {navSections.map((section, idx) => (
          <div key={idx} className="space-y-1">
            <div className="px-2 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
              {section.title}
            </div>
            <div className="space-y-0.5 mt-1">
              {section.items.map((item) => {
                const Icon = item.icon;
                const isActive = currentView === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => onNavigate(item.id)}
                    className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all group cursor-pointer ${
                      isActive
                        ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900 border border-transparent'
                    }`}
                  >
                    <div className="flex items-center space-x-2.5">
                      <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-500 group-hover:text-slate-300'} ${item.highlight ? 'text-indigo-400' : ''}`} />
                      <span className={item.highlight ? 'bg-gradient-to-r from-blue-400 to-indigo-300 bg-clip-text text-transparent font-semibold' : ''}>
                        {item.label}
                      </span>
                    </div>

                    {item.badge !== undefined && (
                      <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono ${
                        isActive ? 'bg-blue-500/20 text-blue-300' : 'bg-slate-800 text-slate-400'
                      }`}>
                        {item.badge}
                      </span>
                    )}

                    {item.tag && (
                      <span className={`text-[9px] px-1.5 py-0.2 rounded font-bold uppercase tracking-wider ${
                        item.tag === 'Admin' ? 'bg-purple-900/30 text-purple-300 border border-purple-800/40' : 'bg-emerald-900/30 text-emerald-300 border border-emerald-800/40'
                      }`}>
                        {item.tag}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Plan Usage & Upgrade Callout */}
      <div className="p-3 border-t border-slate-800 bg-slate-900/50">
        <div className="bg-gradient-to-br from-slate-900 to-slate-800/80 border border-slate-700/80 rounded-xl p-3 shadow-inner">
          <div className="flex items-center justify-between text-xs mb-1.5">
            <span className="font-semibold text-slate-200">{currentWorkspace.plan_tier} {t.currentPlanBadge}</span>
            <span className="text-[10px] text-blue-400 bg-blue-500/10 px-1.5 py-0.5 rounded border border-blue-500/20">{t.connected}</span>
          </div>

          <div className="space-y-1.5 text-[11px] text-slate-400">
            <div className="flex justify-between">
              <span>{t.navProjects}:</span>
              <span className="text-slate-200 font-mono">{projectsCount} / {currentWorkspace.plan_tier === 'FREE' ? '2' : '∞'}</span>
            </div>
            <div className="w-full bg-slate-700/60 rounded-full h-1.5 overflow-hidden">
              <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: currentWorkspace.plan_tier === 'FREE' ? `${(projectsCount/2)*100}%` : '25%' }}></div>
            </div>
          </div>

          {currentWorkspace.plan_tier === 'FREE' && (
            <button
              onClick={() => onNavigate('billing')}
              className="mt-2.5 w-full py-1.5 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium text-xs shadow-sm transition-all cursor-pointer"
            >
              {t.upgradePlan}
            </button>
          )}
        </div>
      </div>
    </aside>
  );
};

