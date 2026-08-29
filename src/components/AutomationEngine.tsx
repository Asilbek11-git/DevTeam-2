import React, { useState } from 'react';
import {
  Cpu, Plus, Zap, ArrowRight, CheckCircle2, AlertTriangle,
  Play, Power, Trash2, Sliders, Bell
} from 'lucide-react';
import { AutomationRule, Language } from '../types';
import { Translations } from '../data/translations';

interface AutomationEngineProps {
  rules: AutomationRule[];
  onToggleRule: (ruleId: string) => void;
  onCreateRule: (newRule: Partial<AutomationRule>) => void;
  t: Translations;
}

export const AutomationEngine: React.FC<AutomationEngineProps> = ({
  rules,
  onToggleRule,
  onCreateRule,
  t,
}) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [ruleName, setRuleName] = useState('');
  const [triggerType, setTriggerType] = useState<'PR_MERGED' | 'TASK_STATUS_CHANGED' | 'TASK_OVERDUE'>('PR_MERGED');
  const [actionType, setActionType] = useState<'MOVE_TASK_TO' | 'NOTIFY_ROLE' | 'ASSIGN_TO_USER'>('MOVE_TASK_TO');

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!ruleName.trim()) return;

    let trigger_label = 'When Pull Request is merged into main';
    if (triggerType === 'TASK_STATUS_CHANGED') trigger_label = 'When task status moves to Code Review';
    if (triggerType === 'TASK_OVERDUE') trigger_label = 'When task passes due date without completion';

    let action_label = 'Move linked task to status QA & Test';
    if (actionType === 'NOTIFY_ROLE') action_label = 'Send instant notification to Lead Developer';
    if (actionType === 'ASSIGN_TO_USER') action_label = 'Auto-assign task to QA Specialist';

    onCreateRule({
      name: ruleName.trim(),
      trigger: triggerType,
      trigger_label,
      action: actionType,
      action_label,
      is_active: true,
      execution_count: 0,
    });

    setRuleName('');
    setModalOpen(false);
  };

  return (
    <div className="p-6 space-y-6 flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-blue-500" />
            <span>{t.automationTitle}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t.automationSubtitle}</p>
        </div>

        <button
          onClick={() => setModalOpen(true)}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition-colors shadow-sm cursor-pointer"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>{t.newRule}</span>
        </button>
      </div>

      {/* Rules List Grid */}
      <div className="grid grid-cols-1 gap-4">
        {rules.map((rule) => (
          <div
            key={rule.id}
            className="bg-slate-900 border border-slate-800 hover:border-slate-700/80 rounded-xl p-5 shadow-sm space-y-3 transition-all"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex items-center space-x-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                  rule.is_active ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30' : 'bg-slate-800 text-slate-500'
                }`}>
                  <Zap className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-100">{rule.name}</h3>
                  <span className="text-[10px] text-slate-500 font-mono">
                    Triggered {rule.execution_count} times {rule.last_triggered ? `• Last ran: ${rule.last_triggered}` : ''}
                  </span>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <button
                  onClick={() => onToggleRule(rule.id)}
                  className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center space-x-1.5 transition-colors cursor-pointer ${
                    rule.is_active
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                      : 'bg-slate-800 text-slate-400 border border-slate-700'
                  }`}
                >
                  <Power className="w-3 h-3" />
                  <span>{rule.is_active ? t.enabled : t.disabled}</span>
                </button>
              </div>
            </div>

            {/* Visual Workflow Flow */}
            <div className="bg-slate-950/70 rounded-lg p-3.5 border border-slate-800/80 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-[10px] text-slate-400 uppercase bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                  {t.whenTrigger}
                </span>
                <span className="text-slate-200 font-medium">{rule.trigger_label}</span>
              </div>

              <ArrowRight className="w-4 h-4 text-slate-600 hidden md:block" />

              <div className="flex items-center space-x-2">
                <span className="font-semibold text-[10px] text-blue-400 uppercase bg-blue-950/40 px-2 py-0.5 rounded border border-blue-800/40">
                  {t.thenAction}
                </span>
                <span className="text-blue-200 font-medium">{rule.action_label}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal: New Rule */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl animate-in fade-in zoom-in-95 duration-150">
            <h3 className="text-base font-bold text-slate-100">{t.newRule}</h3>

            <form onSubmit={handleCreate} className="space-y-4 text-xs">
              <div className="space-y-1">
                <label className="text-slate-400 font-medium">{t.ruleName}</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Move to QA on PR Merge"
                  value={ruleName}
                  onChange={(e) => setRuleName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="space-y-1">
                <label className="text-slate-400 font-medium">{t.whenTrigger}</label>
                <select
                  value={triggerType}
                  onChange={(e) => setTriggerType(e.target.value as any)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                >
                  <option value="PR_MERGED">Pull Request Merged into main branch</option>
                  <option value="TASK_STATUS_CHANGED">Task Status changes to Code Review</option>
                  <option value="TASK_OVERDUE">Task passes Due Date without completion</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-slate-400 font-medium">{t.thenAction}</label>
                <select
                  value={actionType}
                  onChange={(e) => setActionType(e.target.value as any)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                >
                  <option value="MOVE_TASK_TO">Move linked task to status QA & Test</option>
                  <option value="NOTIFY_ROLE">Send notification alert to Lead Developers</option>
                  <option value="ASSIGN_TO_USER">Auto-assign task to QA Specialist</option>
                </select>
              </div>

              <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-medium cursor-pointer"
                >
                  {t.cancel}
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold shadow-sm cursor-pointer"
                >
                  {t.saveRule}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

