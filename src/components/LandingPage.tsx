import React from 'react';
import {
  Code2, Sparkles, CheckCircle2, ArrowRight, ShieldCheck,
  Zap, GitPullRequest, LayoutDashboard, Clock, CreditCard,
  Flame, BookOpen, Users, Star, Layers, DollarSign, Cpu
} from 'lucide-react';
import { User, Plan } from '../types';

interface LandingPageProps {
  onEnterApp: () => void;
  onSelectPersona: (userEmail: string) => void;
  plans: Plan[];
}

export const LandingPage: React.FC<LandingPageProps> = ({
  onEnterApp,
  onSelectPersona,
  plans,
}) => {
  const personas = [
    { email: 'admin@devteam.io', role: 'SuperAdmin / Architect', name: 'Alex Vance', badge: 'Revenue & Admin' },
    { email: 'elena.pm@devteam.io', role: 'Agile Project Manager', name: 'Elena Rostova', badge: 'Sprints & Milestones' },
    { email: 'sarah.lead@devteam.io', role: 'Lead Full-Stack Dev', name: 'Sarah Chen', badge: 'Code Review & Git' },
    { email: 'dmitry.py@devteam.io', role: 'Backend Python Engineer', name: 'Dmitry Ivanov', badge: 'Tasks & Time Logs' },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-blue-600 selection:text-white">
      {/* Top Banner & Nav */}
      <nav className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 px-3 sm:px-6 py-3 sm:py-4 flex items-center justify-between">
        <div className="flex items-center space-x-2 sm:space-x-2.5">
          <div className="w-7 h-7 sm:w-8 h-8 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <Code2 className="w-4 h-4 sm:w-5 h-5" />
          </div>
          <span className="font-bold text-base sm:text-lg text-white">DevTeam<span className="text-blue-400 text-[10px] sm:text-xs ml-1 px-1.5 py-0.5 rounded bg-blue-500/20 border border-blue-500/30">SaaS</span></span>
        </div>

        <div className="flex items-center space-x-2 sm:space-x-4 text-xs font-medium">
          <button
            onClick={onEnterApp}
            className="px-3 sm:px-4 py-1.5 sm:py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl font-semibold shadow-md shadow-blue-500/20 transition-all flex items-center space-x-1.5 cursor-pointer"
          >
            <span>Launch App</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative px-4 sm:px-6 pt-10 sm:pt-16 pb-14 sm:pb-20 max-w-6xl mx-auto text-center space-y-6 sm:space-y-8">
        <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-300 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-blue-400 animate-pulse shrink-0" />
          <span>Next-Generation SaaS Project Management</span>
        </div>

        <h1 className="text-3xl sm:text-5xl md:text-6xl font-extrabold text-slate-100 tracking-tight leading-tight max-w-4xl mx-auto">
          Ship Software Faster with <span className="bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">Agile Sprints, VCS & AI</span>
        </h1>

        <p className="text-sm sm:text-base md:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          The all-in-one developer workspace with multi-tenant workspaces, interactive Kanban with WIP limits, automated GitHub/GitLab webhook synchronization, live time tracking, and multi-gateway billing (Stripe, Payme, Click).
        </p>

        {/* 1-Click Persona Simulator */}
        <div className="pt-2 sm:pt-4 max-w-3xl mx-auto bg-slate-900/80 border border-slate-800 rounded-2xl p-3.5 sm:p-5 shadow-2xl space-y-3 text-left sm:text-center">
          <span className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
            ⚡ Instant 1-Click Interactive Demo Login:
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2 sm:gap-2.5">
            {personas.map((p, idx) => (
              <button
                key={idx}
                onClick={() => onSelectPersona(p.email)}
                className="p-3 bg-slate-950 hover:bg-blue-950/40 border border-slate-800 hover:border-blue-500/50 rounded-xl text-left transition-all group cursor-pointer"
              >
                <div className="text-xs font-bold text-slate-200 group-hover:text-blue-300 transition-colors">{p.name}</div>
                <div className="text-[11px] text-slate-400">{p.role}</div>
                <span className="mt-2 inline-block text-[9px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-mono">
                  {p.badge}
                </span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="px-4 sm:px-6 py-12 sm:py-16 bg-slate-900/50 border-t border-slate-800">
        <div className="max-w-6xl mx-auto space-y-8 sm:space-y-12">
          <div className="text-center space-y-2">
            <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-slate-100">Engineered for High-Velocity Dev Teams</h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">Everything you need to orchestrate software development from sprint backlog to production deployment.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6 text-xs">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
                <LayoutDashboard className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-100">Sprint Kanban & WIP Limits</h3>
              <p className="text-slate-400 leading-relaxed">
                Drag-and-drop Kanban board with column WIP enforcement, story point estimation, subtask checklists, and circular dependency graph detection.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
                <GitPullRequest className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-100">VCS Webhook Automation</h3>
              <p className="text-slate-400 leading-relaxed">
                Seamless GitHub and GitLab webhook listeners. Auto-link commit hashes to task IDs, move tasks to Code Review on PR creation, and advance to QA upon merge.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                <Sparkles className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-100">Gemini AI Studio</h3>
              <p className="text-slate-400 leading-relaxed">
                Auto-generate comprehensive technical specifications, Definition of Done acceptance criteria, Fibonacci complexity ratings, and sprint retrospectives.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                <CreditCard className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-100">Multi-Gateway Monetization</h3>
              <p className="text-slate-400 leading-relaxed">
                Pluggable billing architecture supporting Stripe (global cards), Payme (Central Asia / UZS), and Click. Includes discount coupons and affiliate tracking.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-amber-600/20 border border-amber-500/30 flex items-center justify-center text-amber-400">
                <Clock className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-100">Live Time Tracking</h3>
              <p className="text-slate-400 leading-relaxed">
                Integrated developer stopwatch and manual timesheet logs with billable tags, exportable reports, and budget consumption tracking per project.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-rose-600/20 border border-rose-500/30 flex items-center justify-center text-rose-400">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-100">Multi-Tenancy & RBAC</h3>
              <p className="text-slate-400 leading-relaxed">
                Strict workspace data isolation with 7 granular roles (Owner, Admin, PM, Lead Dev, Developer, Client, Viewer) and session security management.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="px-6 py-16 max-w-6xl mx-auto space-y-12">
        <div className="text-center space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-100">Simple, Transparent SaaS Pricing</h2>
          <p className="text-xs sm:text-sm text-slate-400">Scale from solo developer to enterprise agency with automated plan limit enforcement.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-5 text-xs">
          {plans.map((p) => (
            <div key={p.id} className={`bg-slate-900 rounded-2xl p-5 border space-y-4 flex flex-col justify-between ${
              p.is_popular ? 'border-blue-500 shadow-lg shadow-blue-500/10' : 'border-slate-800'
            }`}>
              <div className="space-y-3">
                <h3 className="text-base font-bold text-slate-100">{p.name}</h3>
                <div className="flex items-baseline space-x-1 font-mono">
                  <span className="text-3xl font-extrabold text-slate-100">${p.monthly_price}</span>
                  <span className="text-slate-400">/mo</span>
                </div>
                <p className="text-slate-400 text-[11px] min-h-[28px]">{p.description}</p>
                <div className="space-y-1.5 pt-2 border-t border-slate-800">
                  <div className="flex items-center space-x-1.5 text-slate-300">
                    <CheckCircle2 className="w-3.5 h-3.5 text-blue-400" />
                    <span>{p.max_members === 0 ? 'Unlimited' : p.max_members} Members</span>
                  </div>
                  <div className="flex items-center space-x-1.5 text-slate-300">
                    <CheckCircle2 className="w-3.5 h-3.5 text-blue-400" />
                    <span>{p.max_projects === 0 ? 'Unlimited' : `${p.max_projects} Active`} Projects</span>
                  </div>
                  <div className="flex items-center space-x-1.5 text-slate-300">
                    <CheckCircle2 className="w-3.5 h-3.5 text-blue-400" />
                    <span>{p.max_ai_generations_per_month} AI Gen / mo</span>
                  </div>
                </div>
              </div>

              <button
                onClick={onEnterApp}
                className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-semibold shadow-sm transition-colors"
              >
                Get Started
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 px-6 py-8 text-center text-xs text-slate-500 space-y-2">
        <div className="flex items-center justify-center space-x-2 text-slate-400">
          <Code2 className="w-4 h-4 text-blue-400" />
          <span className="font-semibold text-slate-200">DevTeam SaaS Platform</span>
          <span>•</span>
          <span>Python 3.12 / Django 5 / PostgreSQL / Redis / Celery / Gemini AI</span>
        </div>
        <p>© 2026 DevTeam Inc. All rights reserved. Licensed for commercial deployment.</p>
      </footer>
    </div>
  );
};
