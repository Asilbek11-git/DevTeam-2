import React from 'react';
import {
  BarChart3, DollarSign, TrendingUp, Users, AlertTriangle,
  CreditCard, Zap, Shield, ArrowUpRight, ArrowDownRight, CheckCircle2
} from 'lucide-react';
import { Language } from '../types';
import { Translations } from '../data/translations';

interface SuperAdminDashboardProps {
  t?: Translations;
}

export const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ t }) => {
  const kpis = [
    { title: t?.mrr || 'Monthly Recurring Revenue (MRR)', value: '$14,850', change: '+24.5%', isPositive: true, icon: DollarSign },
    { title: t?.arr || 'Annual Recurring Revenue (ARR)', value: '$178,200', change: '+28.0%', isPositive: true, icon: TrendingUp },
    { title: t?.payingCustomers || 'Paying SaaS Customers', value: '248', change: '+18 this month', isPositive: true, icon: Users },
    { title: t?.churnRate || 'Net Revenue Churn Rate', value: '1.8%', change: '-0.4%', isPositive: true, icon: CheckCircle2 },
  ];

  const gateways = [
    { name: 'Stripe (Cards & Global)', amount: '$10,098.00', percentage: 68, color: '#3B82F6' },
    { name: 'Payme (Central Asia / UZS)', amount: '$3,118.50', percentage: 21, color: '#10B981' },
    { name: 'Click (Merchant Payments)', amount: '$1,633.50', percentage: 11, color: '#8B5CF6' },
  ];

  const customerHealth = [
    { name: 'NexusTech Solutions Inc.', plan: 'PRO', mrr: '$29.00', health: 'HEALTHY', score: 96, risk: 'Low' },
    { name: 'FinCore Labs AMM', plan: 'BUSINESS', mrr: '$79.00', health: 'HEALTHY', score: 92, risk: 'Low' },
    { name: 'CloudScale DevOps Ltd', plan: 'ENTERPRISE', mrr: '$199.00', health: 'HEALTHY', score: 98, risk: 'Low' },
    { name: 'AppVenture Studio', plan: 'PRO', mrr: '$29.00', health: 'WARNING', score: 62, risk: 'Medium (Inactive 10 days)' },
    { name: 'LegacyTech Partners', plan: 'BUSINESS', mrr: '$79.00', health: 'CRITICAL', score: 41, risk: 'High (Payment retry failed)' },
  ];

  return (
    <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 flex-1 overflow-y-auto pb-24 lg:pb-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-purple-400" />
            <span>{t?.superAdminTitle || 'SuperAdmin Executive SaaS Revenue Analytics'}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t?.superAdminSubtitle || 'Platform-wide subscription revenue, multi-gateway clearing, and retention telemetry.'}</p>
        </div>

        <span className="px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 text-xs font-bold font-mono">
          SuperAdmin Mode
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 shadow-sm">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">{kpi.title}</span>
                <div className="p-2 rounded-lg bg-slate-800 text-purple-400">
                  <Icon className="w-4 h-4" />
                </div>
              </div>

              <div className="flex items-baseline justify-between">
                <span className="text-2xl font-bold text-slate-100 font-mono">{kpi.value}</span>
                <span className="text-xs font-bold text-emerald-400 flex items-center">
                  <ArrowUpRight className="w-3.5 h-3.5" />
                  <span>{kpi.change}</span>
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Gateway Breakdown & Subscription Tiers Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Card 1: Multi-Gateway Revenue Split */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-sm">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">{t?.paymentGateway || 'Multi-Gateway Revenue Distribution'}</h3>

          <div className="space-y-4 pt-1">
            {gateways.map((gw, idx) => (
              <div key={idx} className="space-y-1.5 text-xs">
                <div className="flex justify-between text-slate-300">
                  <span className="font-semibold">{gw.name}</span>
                  <span className="font-mono text-slate-100 font-bold">{gw.amount} ({gw.percentage}%)</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                  <div className="h-2.5 rounded-full transition-all duration-500" style={{ width: `${gw.percentage}%`, backgroundColor: gw.color }}></div>
                </div>
              </div>
            ))}
          </div>

          <div className="pt-3 border-t border-slate-800/80 text-[11px] text-slate-400 flex items-center justify-between">
            <span>Automated settlement to primary merchant treasury bank.</span>
            <span className="text-emerald-400 font-mono font-semibold">All Gateways Synced</span>
          </div>
        </div>

        {/* Card 2: Tier Breakdown */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 flex flex-col justify-between">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Active Workspace Subscriptions</h3>

          <div className="space-y-2 text-xs">
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
              <span className="text-slate-400">Enterprise ($199/mo)</span>
              <span className="font-mono font-bold text-purple-400">22 accounts</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
              <span className="text-slate-400">Business ($79/mo)</span>
              <span className="font-mono font-bold text-blue-400">68 accounts</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
              <span className="text-slate-400">Professional ($29/mo)</span>
              <span className="font-mono font-bold text-emerald-400">158 accounts</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
              <span className="text-slate-400">Free Tier</span>
              <span className="font-mono font-bold text-slate-400">1,420 workspaces</span>
            </div>
          </div>

          <div className="text-[10px] text-slate-500 text-center">
            Free-to-Paid conversion rate: 14.8% (Top quartile SaaS benchmark)
          </div>
        </div>
      </div>

      {/* Customer Health Scores & Churn Risk Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200">{t?.customerHealth || 'Customer Health Scores & Churn Risk Telemetry'}</h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="p-3">Workspace</th>
                <th className="p-3">Plan Tier</th>
                <th className="p-3">MRR</th>
                <th className="p-3">Health Score</th>
                <th className="p-3">{t?.status || 'Status'}</th>
                <th className="p-3">Risk Assessment</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {customerHealth.map((c, i) => (
                <tr key={i} className="hover:bg-slate-800/40 transition-colors">
                  <td className="p-3 font-semibold text-slate-100">{c.name}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 text-[10px] font-mono">
                      {c.plan}
                    </span>
                  </td>
                  <td className="p-3 font-mono font-bold text-slate-100">{c.mrr}</td>
                  <td className="p-3 font-mono font-bold text-blue-400">{c.score} / 100</td>
                  <td className="p-3">
                    {c.health === 'HEALTHY' && (
                      <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-semibold">
                        Healthy
                      </span>
                    )}
                    {c.health === 'WARNING' && (
                      <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-semibold">
                        Warning
                      </span>
                    )}
                    {c.health === 'CRITICAL' && (
                      <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-semibold">
                        Critical
                      </span>
                    )}
                  </td>
                  <td className="p-3 text-slate-400">{c.risk}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

