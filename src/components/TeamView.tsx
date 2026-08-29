import React, { useState } from 'react';
import {
  Users, UserPlus, Shield, ShieldCheck, Mail, Calendar,
  MoreVertical, Trash2, CheckCircle2, AlertCircle, Laptop
} from 'lucide-react';
import { WorkspaceMember, WorkspaceRole, User, Language } from '../types';
import { Translations } from '../data/translations';

interface TeamViewProps {
  members: WorkspaceMember[];
  onInviteMember: (email: string, role: WorkspaceRole) => void;
  onUpdateRole: (memberId: string, newRole: WorkspaceRole) => void;
  onRemoveMember: (memberId: string) => void;
  t: Translations;
}

export const TeamView: React.FC<TeamViewProps> = ({
  members,
  onInviteMember,
  onUpdateRole,
  onRemoveMember,
  t,
}) => {
  const [inviteModalOpen, setInviteModalOpen] = useState(false);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState<WorkspaceRole>('DEVELOPER');

  const handleInvite = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inviteEmail.trim()) return;
    onInviteMember(inviteEmail.trim(), inviteRole);
    setInviteEmail('');
    setInviteModalOpen(false);
  };

  const getRoleBadge = (role: WorkspaceRole) => {
    switch (role) {
      case 'OWNER':
        return <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 text-[10px] font-bold">Owner</span>;
      case 'ADMIN':
        return <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[10px] font-bold">Admin</span>;
      case 'PROJECT_MANAGER':
        return <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-semibold">Project Manager</span>;
      case 'LEAD_DEVELOPER':
        return <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-[10px] font-semibold">Lead Developer</span>;
      case 'DEVELOPER':
        return <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px]">Developer</span>;
      default:
        return <span className="px-2 py-0.5 rounded bg-slate-700 text-slate-300 text-[10px]">{role}</span>;
    }
  };

  return (
    <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 flex-1 overflow-y-auto pb-24 lg:pb-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Users className="w-5 h-5 text-blue-500" />
            <span>{t.teamTitle}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t.teamSubtitle}</p>
        </div>

        <button
          onClick={() => setInviteModalOpen(true)}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition-colors shadow-sm cursor-pointer"
        >
          <UserPlus className="w-3.5 h-3.5" />
          <span>{t.inviteMember}</span>
        </button>
      </div>

      {/* Members List Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200">{t.activeMembers} ({members.length})</h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="p-3">{t.user}</th>
                <th className="p-3">{t.jobTitle}</th>
                <th className="p-3">{t.role}</th>
                <th className="p-3">{t.status}</th>
                <th className="p-3">{t.joinedDate}</th>
                <th className="p-3 text-right">{t.actions}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {members.map((m) => (
                <tr key={m.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="p-3">
                    <div className="flex items-center space-x-2.5">
                      <div className="w-7 h-7 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs">
                        {m.user.first_name[0]}{m.user.last_name[0]}
                      </div>
                      <div>
                        <div className="font-semibold text-slate-100">{m.user.first_name} {m.user.last_name}</div>
                        <div className="text-[11px] text-slate-400">{m.user.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="p-3 text-slate-300">{m.user.job_title}</td>
                  <td className="p-3">
                    <select
                      value={m.role}
                      disabled={m.role === 'OWNER'}
                      onChange={(e) => onUpdateRole(m.id, e.target.value as WorkspaceRole)}
                      className="bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs font-semibold"
                    >
                      <option value="OWNER">Owner</option>
                      <option value="ADMIN">Admin</option>
                      <option value="PROJECT_MANAGER">Project Manager</option>
                      <option value="LEAD_DEVELOPER">Lead Developer</option>
                      <option value="DEVELOPER">Developer</option>
                      <option value="CLIENT">Client</option>
                      <option value="VIEWER">Viewer</option>
                    </select>
                  </td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-semibold">
                      {t.active}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400">{m.joined_at}</td>
                  <td className="p-3 text-right">
                    {m.role !== 'OWNER' && (
                      <button
                        onClick={() => onRemoveMember(m.id)}
                        className="p-1 hover:text-rose-400 text-slate-500 transition-colors cursor-pointer"
                        title="Remove member"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Active User Sessions */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
        <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
          <Laptop className="w-4 h-4 text-blue-400" />
          <span>{t.activeSessions}</span>
        </h3>

        <div className="divide-y divide-slate-800/80 text-xs">
          <div className="py-2.5 flex items-center justify-between">
            <div className="space-y-0.5">
              <span className="text-slate-200 font-semibold">MacBook Pro (Chrome 128 / macOS Sequoia)</span>
              <div className="text-[11px] text-slate-400">IP: 198.51.100.42 • New York, USA ({t.currentSession})</div>
            </div>
            <span className="text-[10px] text-emerald-400 font-semibold px-2 py-0.5 rounded bg-emerald-950/40 border border-emerald-800">
              {t.active}
            </span>
          </div>

          <div className="py-2.5 flex items-center justify-between">
            <div className="space-y-0.5">
              <span className="text-slate-200 font-semibold">Ubuntu Linux (CLI Token & Git Webhook Sync)</span>
              <div className="text-[11px] text-slate-400">IP: 203.0.113.19 • Frankfurt, Germany</div>
            </div>
            <button className="text-[11px] text-rose-400 hover:text-rose-300 cursor-pointer">{t.revokeSession}</button>
          </div>
        </div>
      </div>

      {/* Invite Modal */}
      {inviteModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl animate-in fade-in zoom-in-95 duration-150 text-xs">
            <h3 className="text-base font-bold text-slate-100">{t.inviteMember}</h3>

            <form onSubmit={handleInvite} className="space-y-4">
              <div className="space-y-1">
                <label className="text-slate-400 font-medium">Work Email Address</label>
                <input
                  type="email"
                  required
                  placeholder="engineer@company.com"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="space-y-1">
                <label className="text-slate-400 font-medium">{t.role}</label>
                <select
                  value={inviteRole}
                  onChange={(e) => setInviteRole(e.target.value as WorkspaceRole)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
                >
                  <option value="ADMIN">Admin</option>
                  <option value="PROJECT_MANAGER">Project Manager</option>
                  <option value="LEAD_DEVELOPER">Lead Developer</option>
                  <option value="DEVELOPER">Developer</option>
                  <option value="CLIENT">Client</option>
                </select>
              </div>

              <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setInviteModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-medium cursor-pointer"
                >
                  {t.cancel}
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold shadow-sm cursor-pointer"
                >
                  {t.inviteMember}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

