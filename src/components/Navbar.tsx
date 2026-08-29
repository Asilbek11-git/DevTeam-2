import React, { useState } from 'react';
import {
  Code2, Bell, Plus, Sparkles, ChevronDown, Check,
  User, Shield, LogOut, BookOpen, Layers, CheckCircle2, Globe, Languages, Menu
} from 'lucide-react';
import { Workspace, User as UserType, NotificationItem, WorkspaceRole, Language } from '../types';
import { Translations } from '../data/translations';

interface NavbarProps {
  currentWorkspace: Workspace;
  workspaces: Workspace[];
  onSelectWorkspace: (ws: Workspace) => void;
  currentUser: UserType;
  users: UserType[];
  onSwitchUser: (user: UserType) => void;
  currentRole: WorkspaceRole;
  onChangeRole: (role: WorkspaceRole) => void;
  notifications: NotificationItem[];
  onOpenNotifications: () => void;
  onOpenCreateTask: () => void;
  onOpenAiStudio: () => void;
  onNavigate: (view: string) => void;
  currentView: string;
  lang: Language;
  onSelectLanguage?: (lang: Language) => void;
  onLanguageChange?: (lang: Language) => void;
  t: Translations;
  onToggleMobileSidebar?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentWorkspace,
  workspaces,
  onSelectWorkspace,
  currentUser,
  users,
  onSwitchUser,
  currentRole,
  onChangeRole,
  notifications,
  onOpenNotifications,
  onOpenCreateTask,
  onOpenAiStudio,
  onNavigate,
  currentView,
  lang,
  onSelectLanguage,
  onLanguageChange,
  t,
  onToggleMobileSidebar,
}) => {
  const [workspaceMenuOpen, setWorkspaceMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [langMenuOpen, setLangMenuOpen] = useState(false);

  const handleLanguageChange = (newLang: Language) => {
    if (onSelectLanguage) onSelectLanguage(newLang);
    if (onLanguageChange) onLanguageChange(newLang);
    setLangMenuOpen(false);
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;

  const roles: WorkspaceRole[] = [
    'OWNER',
    'ADMIN',
    'PROJECT_MANAGER',
    'LEAD_DEVELOPER',
    'DEVELOPER',
    'CLIENT',
    'VIEWER'
  ];

  const languages: { code: Language; label: string; flag: string }[] = [
    { code: 'uz', label: 'O\'zbekcha', flag: '🇺🇿' },
    { code: 'ru', label: 'Русский', flag: '🇷🇺' },
    { code: 'en', label: 'English', flag: '🇬🇧' },
  ];

  const currentLangObj = languages.find(l => l.code === lang) || languages[0];

  return (
    <header className="sticky top-0 z-40 bg-slate-900 border-b border-slate-800 text-slate-100 px-3 sm:px-4 py-2 sm:py-2.5 flex items-center justify-between shadow-sm">
      {/* Brand & Workspace Selector */}
      <div className="flex items-center space-x-2 sm:space-x-4">
        {/* Mobile Hamburger Drawer Toggle */}
        <button
          onClick={onToggleMobileSidebar}
          className="lg:hidden p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
          aria-label="Open sidebar navigation"
        >
          <Menu className="w-5 h-5" />
        </button>

        <button
          onClick={() => onNavigate('landing')}
          className="flex items-center space-x-1.5 sm:space-x-2 text-blue-400 hover:text-blue-300 font-bold text-base sm:text-lg transition-colors group cursor-pointer"
        >
          <div className="w-7 h-7 sm:w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 group-hover:scale-105 transition-transform">
            <Code2 className="w-4 h-4 sm:w-5 h-5" />
          </div>
          <span className="tracking-tight text-white font-semibold flex items-center">
            {t.brandName}
            <span className="text-blue-400 text-[10px] sm:text-xs ml-1 px-1 sm:px-1.5 py-0.2 rounded bg-blue-500/20 border border-blue-500/30 hidden xs:inline-block">SaaS</span>
          </span>
        </button>

        <div className="h-5 w-px bg-slate-800 hidden sm:block"></div>

        {/* Workspace Dropdown */}
        <div className="relative">
          <button
            onClick={() => setWorkspaceMenuOpen(!workspaceMenuOpen)}
            className="flex items-center space-x-1.5 sm:space-x-2 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/80 rounded-lg px-2 sm:px-3 py-1.5 text-xs text-slate-200 transition-colors"
          >
            <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: currentWorkspace.brand_color }}></div>
            <span className="font-medium truncate max-w-[80px] sm:max-w-[150px]">{currentWorkspace.name}</span>
            <span className="px-1.5 py-0.2 bg-blue-500/20 text-blue-300 text-[10px] rounded font-semibold border border-blue-500/30 hidden md:inline-block">
              {currentWorkspace.plan_tier}
            </span>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
          </button>

          {workspaceMenuOpen && (
            <div className="absolute left-0 mt-1.5 w-64 bg-slate-900 border border-slate-700 rounded-xl shadow-xl py-2 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
              <div className="px-3 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                {t.workspace} ({workspaces.length})
              </div>
              {workspaces.map((ws) => (
                <button
                  key={ws.id}
                  onClick={() => {
                    onSelectWorkspace(ws);
                    setWorkspaceMenuOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 text-xs flex items-center justify-between hover:bg-slate-800 transition-colors ${
                    ws.id === currentWorkspace.id ? 'text-blue-400 bg-blue-900/20 font-medium' : 'text-slate-300'
                  }`}
                >
                  <div className="flex items-center space-x-2.5 truncate">
                    <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: ws.brand_color }}></div>
                    <span className="truncate">{ws.name}</span>
                  </div>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-400">
                    {ws.plan_tier}
                  </span>
                </button>
              ))}
              <div className="border-t border-slate-800 my-1 pt-1">
                <button
                  onClick={() => {
                    setWorkspaceMenuOpen(false);
                    onNavigate('team');
                  }}
                  className="w-full text-left px-3 py-1.5 text-xs text-blue-400 hover:bg-slate-800 flex items-center space-x-2"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>{t.switchWorkspace}</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Quick Action & Controls */}
      <div className="flex items-center space-x-1.5 sm:space-x-2.5">
        {/* Language Selector Dropdown */}
        <div className="relative">
          <button
            onClick={() => setLangMenuOpen(!langMenuOpen)}
            className="flex items-center space-x-1 sm:space-x-1.5 bg-slate-800/90 hover:bg-slate-800 border border-slate-700 rounded-lg px-2 sm:px-2.5 py-1.5 text-xs text-slate-200 transition-colors cursor-pointer shadow-sm hover:border-slate-600"
            title="Switch Language / Tilni tanlash / Выбрать язык"
          >
            <span className="text-sm">{currentLangObj.flag}</span>
            <span className="font-medium hidden sm:inline">{currentLangObj.label}</span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {langMenuOpen && (
            <div className="absolute right-0 mt-1.5 w-44 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl py-1.5 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
              <div className="px-3 py-1 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                {t.languageSelect}
              </div>
              {languages.map((l) => (
                <button
                  key={l.code}
                  onClick={() => handleLanguageChange(l.code)}
                  className={`w-full text-left px-3 py-2 text-xs flex items-center justify-between hover:bg-slate-800 transition-colors ${
                    l.code === lang ? 'text-blue-400 bg-blue-900/20 font-semibold' : 'text-slate-300'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <span className="text-sm">{l.flag}</span>
                    <span>{l.label}</span>
                  </div>
                  {l.code === lang && <Check className="w-3.5 h-3.5 text-blue-400" />}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Swagger API Explorer Button */}
        <button
          onClick={() => onNavigate('api_docs')}
          className={`hidden sm:flex items-center space-x-1.5 text-xs px-2.5 py-1.5 rounded-lg border transition-all ${
            currentView === 'api_docs'
              ? 'bg-purple-900/30 text-purple-300 border-purple-500/40'
              : 'bg-slate-800/60 text-slate-300 border-slate-700 hover:bg-slate-800'
          }`}
          title={t.swaggerApi}
        >
          <BookOpen className="w-3.5 h-3.5 text-purple-400" />
          <span className="hidden md:inline font-mono">/api/docs</span>
        </button>

        {/* AI Assistant Studio Button */}
        <button
          onClick={onOpenAiStudio}
          className="flex items-center space-x-1 sm:space-x-1.5 text-xs px-2 sm:px-2.5 py-1.5 rounded-lg bg-gradient-to-r from-blue-600/20 to-indigo-600/20 border border-blue-500/30 text-blue-300 hover:border-blue-400 transition-all shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 text-blue-400 animate-pulse" />
          <span className="font-medium hidden sm:inline">AI Studio</span>
        </button>

        {/* Quick New Task Button */}
        <button
          onClick={onOpenCreateTask}
          className="flex items-center space-x-1 sm:space-x-1.5 text-xs px-2.5 sm:px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium shadow-sm transition-colors"
        >
          <Plus className="w-3.5 h-3.5" />
          <span className="hidden xs:inline">{t.newTask}</span>
        </button>

        {/* Notifications */}
        <button
          onClick={onOpenNotifications}
          className="relative p-2 rounded-lg bg-slate-800/80 hover:bg-slate-800 border border-slate-700 text-slate-300 transition-colors"
          aria-label="Notifications"
        >
          <Bell className="w-4 h-4" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-[10px] text-white font-bold flex items-center justify-center animate-bounce">
              {unreadCount}
            </span>
          )}
        </button>

        <div className="h-5 w-px bg-slate-800 hidden xs:block"></div>

        {/* User & Role Switcher */}
        <div className="relative">
          <button
            onClick={() => setUserMenuOpen(!userMenuOpen)}
            className="flex items-center space-x-1.5 sm:space-x-2 bg-slate-800/80 hover:bg-slate-800 border border-slate-700 rounded-lg px-2 sm:px-2.5 py-1 text-xs text-slate-200"
          >
            <div className="w-6 h-6 rounded-full bg-blue-500 text-white font-bold flex items-center justify-center text-[10px]">
              {currentUser.first_name[0]}{currentUser.last_name[0]}
            </div>
            <div className="text-left hidden lg:block">
              <div className="font-medium leading-tight text-slate-100">{currentUser.first_name} {currentUser.last_name}</div>
              <div className="text-[10px] text-slate-400">{currentRole}</div>
            </div>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {userMenuOpen && (
            <div className="absolute right-0 mt-1.5 w-64 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl py-2 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
              <div className="px-3 py-2 border-b border-slate-800">
                <div className="text-xs font-semibold text-slate-200">{currentUser.first_name} {currentUser.last_name}</div>
                <div className="text-[11px] text-slate-400 truncate">{currentUser.email}</div>
                <div className="text-[10px] text-blue-400 mt-0.5">{currentUser.job_title}</div>
              </div>

              {/* 1-Click Role Switcher */}
              <div className="px-3 py-1.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                {t.currentRole} (RBAC)
              </div>
              <div className="px-2 grid grid-cols-2 gap-1 mb-2">
                {roles.map(r => (
                  <button
                    key={r}
                    onClick={() => {
                      onChangeRole(r);
                      setUserMenuOpen(false);
                    }}
                    className={`text-[10px] px-2 py-1 rounded text-left font-medium transition-colors ${
                      currentRole === r
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-800/60 text-slate-300 hover:bg-slate-800'
                    }`}
                  >
                    {r.replace('_', ' ')}
                  </button>
                ))}
              </div>

              {/* Switch User Demo */}
              <div className="px-3 py-1.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider border-t border-slate-800 pt-1.5">
                {t.teamTitle}
              </div>
              {users.map(u => (
                <button
                  key={u.id}
                  onClick={() => {
                    onSwitchUser(u);
                    setUserMenuOpen(false);
                  }}
                  className={`w-full text-left px-3 py-1.5 text-xs flex items-center justify-between hover:bg-slate-800 ${
                    u.id === currentUser.id ? 'text-blue-400 bg-blue-900/20 font-medium' : 'text-slate-300'
                  }`}
                >
                  <span className="truncate">{u.first_name} {u.last_name} ({u.job_title.split(' ')[0]})</span>
                  {u.id === currentUser.id && <Check className="w-3 h-3 text-blue-400" />}
                </button>
              ))}

              <div className="border-t border-slate-800 mt-2 pt-1">
                <button
                  onClick={() => {
                    setUserMenuOpen(false);
                    onNavigate('landing');
                  }}
                  className="w-full text-left px-3 py-1.5 text-xs text-slate-400 hover:bg-slate-800 flex items-center space-x-2"
                >
                  <Globe className="w-3.5 h-3.5" />
                  <span>{t.navLanding}</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

