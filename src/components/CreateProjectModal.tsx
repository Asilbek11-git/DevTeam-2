import React, { useState } from 'react';
import { X, FolderGit2 } from 'lucide-react';
import { Project, User, ProjectHealth } from '../types';

interface CreateProjectModalProps {
  users: User[];
  onClose: () => void;
  onCreate: (projectData: Partial<Project>) => void;
}

export const CreateProjectModal: React.FC<CreateProjectModalProps> = ({
  users,
  onClose,
  onCreate,
}) => {
  const [name, setName] = useState('');
  const [key, setKey] = useState('');
  const [description, setDescription] = useState('');
  const [techStackStr, setTechStackStr] = useState('Python 3.12, Django 5, PostgreSQL, Redis, Docker');
  const [budget, setBudget] = useState(25000);
  const [deadline, setDeadline] = useState('2026-10-31');
  const [ownerId, setOwnerId] = useState(users[0]?.id || '');
  const [leadId, setLeadId] = useState(users[1]?.id || users[0]?.id || '');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !key.trim()) return;

    const owner = users.find(u => u.id === ownerId) || users[0];
    const lead = users.find(u => u.id === leadId) || users[0];
    const tech_stack = techStackStr.split(',').map(s => s.trim()).filter(Boolean);

    onCreate({
      name: name.trim(),
      key: key.trim().toUpperCase(),
      description: description.trim(),
      tech_stack,
      budget,
      spent_budget: 0,
      start_date: new Date().toISOString().split('T')[0],
      deadline,
      health: 'ON_TRACK',
      status: 'ACTIVE',
      owner,
      lead,
      repository_url: `https://github.com/nexustech/${key.toLowerCase()}`,
      tags: ['core', 'saas'],
      milestones: [
        {
          id: `m-${Date.now()}`,
          workspace_id: 'ws-1',
          project_id: `p-${Date.now()}`,
          name: 'Milestone 1: Core Architecture & Setup',
          deadline,
          status: 'IN_PROGRESS',
          progress: 10,
        }
      ]
    });

    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl p-6 space-y-4 shadow-2xl animate-in fade-in zoom-in-95 duration-150 text-xs">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-slate-100 flex items-center space-x-2">
            <FolderGit2 className="w-4 h-4 text-blue-500" />
            <span>Create New Project & Milestone</span>
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-3 gap-3">
            <div className="col-span-2 space-y-1">
              <label className="text-slate-400 font-medium">Project Name</label>
              <input
                type="text"
                required
                placeholder="e.g. NextGen Microservices Engine"
                value={name}
                onChange={(e) => {
                  setName(e.target.value);
                  if (!key) {
                    const initials = e.target.value.split(' ').map(w => w[0]).join('').substring(0, 4).toUpperCase();
                    setKey(initials);
                  }
                }}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 font-medium focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="space-y-1">
              <label className="text-slate-400 font-medium">Project Key</label>
              <input
                type="text"
                required
                maxLength={6}
                placeholder="e.g. NME"
                value={key}
                onChange={(e) => setKey(e.target.value.toUpperCase())}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-blue-400 font-mono font-bold uppercase focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-slate-400 font-medium">Description</label>
            <textarea
              rows={2}
              placeholder="Scope and deliverables..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="space-y-1">
            <label className="text-slate-400 font-medium">Tech Stack (comma separated)</label>
            <input
              type="text"
              value={techStackStr}
              onChange={(e) => setTechStackStr(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 font-mono"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="text-slate-400 font-medium">Budget ($ USD)</label>
              <input
                type="number"
                min="1000"
                step="1000"
                value={budget}
                onChange={(e) => setBudget(parseInt(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 font-mono"
              />
            </div>

            <div className="space-y-1">
              <label className="text-slate-400 font-medium">Target Deadline</label>
              <input
                type="date"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
              />
            </div>
          </div>

          <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold shadow-sm"
            >
              Create Project
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
