import React from 'react';
import {
  LayoutDashboard, Flame, FolderGit2, Sparkles, Menu, Clock
} from 'lucide-react';
import { Translations } from '../data/translations';

interface BottomNavProps {
  currentView: string;
  onNavigate: (view: string) => void;
  onToggleMenu: () => void;
  tasksCount: number;
  projectsCount: number;
  t: Translations;
}

export const BottomNav: React.FC<BottomNavProps> = ({
  currentView,
  onNavigate,
  onToggleMenu,
  tasksCount,
  projectsCount,
  t,
}) => {
  const navItems = [
    {
      id: 'kanban',
      label: t.navKanban || 'Kanban',
      icon: LayoutDashboard,
      badge: tasksCount > 0 ? tasksCount : undefined,
    },
    {
      id: 'sprints',
      label: t.navSprints || 'Sprints',
      icon: Flame,
    },
    {
      id: 'projects',
      label: t.navProjects || 'Projects',
      icon: FolderGit2,
      badge: projectsCount > 0 ? projectsCount : undefined,
    },
    {
      id: 'ai_studio',
      label: 'AI Studio',
      icon: Sparkles,
      highlight: true,
    },
  ];

  return (
    <nav
      id="mobile-bottom-nav"
      aria-label="Mobile Navigation"
      className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-slate-950/95 backdrop-blur-md border-t border-slate-800/90 px-2 py-1 flex items-center justify-around shadow-2xl safe-area-bottom"
    >
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = currentView === item.id;
        return (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={`flex-1 py-1.5 px-1 flex flex-col items-center justify-center relative rounded-xl transition-all select-none min-h-[48px] ${
              isActive
                ? 'text-blue-400 font-semibold'
                : 'text-slate-400 hover:text-slate-200 active:scale-95'
            }`}
          >
            <div className="relative">
              <Icon
                className={`w-5 h-5 transition-transform ${
                  isActive ? 'scale-110 text-blue-400' : 'text-slate-400'
                } ${item.highlight ? 'text-indigo-400 animate-pulse' : ''}`}
              />
              {item.badge !== undefined && (
                <span className="absolute -top-1 -right-2.5 bg-blue-600 text-white text-[9px] font-mono font-bold px-1 rounded-full border border-slate-950">
                  {item.badge}
                </span>
              )}
            </div>
            <span className="text-[10px] mt-0.5 tracking-tight truncate max-w-[64px]">
              {item.label}
            </span>
            {isActive && (
              <span className="absolute bottom-0 w-8 h-0.5 bg-blue-500 rounded-full" />
            )}
          </button>
        );
      })}

      {/* Menu / Drawer Trigger */}
      <button
        id="mobile-drawer-toggle"
        onClick={onToggleMenu}
        className="flex-1 py-1.5 px-1 flex flex-col items-center justify-center relative rounded-xl text-slate-400 hover:text-slate-200 active:scale-95 transition-all select-none min-h-[48px]"
        title="Open Full Menu"
      >
        <div className="w-5 h-5 flex items-center justify-center">
          <Menu className="w-5 h-5 text-slate-300" />
        </div>
        <span className="text-[10px] mt-0.5 tracking-tight">
          {t.actions || 'Menyu'}
        </span>
      </button>
    </nav>
  );
};
