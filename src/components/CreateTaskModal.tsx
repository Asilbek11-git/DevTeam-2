import React, { useState } from 'react';
import { X, Plus, Sparkles } from 'lucide-react';
import { Task, TaskPriority, TaskStatus, User, Project, Sprint } from '../types';

interface CreateTaskModalProps {
  defaultStatus?: TaskStatus;
  projects: Project[];
  sprints: Sprint[];
  users: User[];
  onClose: () => void;
  onCreate: (taskData: Partial<Task>) => void;
}

export const CreateTaskModal: React.FC<CreateTaskModalProps> = ({
  defaultStatus = 'TODO',
  projects,
  sprints,
  users,
  onClose,
  onCreate,
}) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [projectId, setProjectId] = useState(projects[0]?.id || '');
  const [sprintId, setSprintId] = useState(sprints[0]?.id || '');
  const [priority, setPriority] = useState<TaskPriority>('HIGH');
  const [status, setStatus] = useState<TaskStatus>(defaultStatus);
  const [assigneeId, setAssigneeId] = useState(users[1]?.id || users[0]?.id || '');
  const [storyPoints, setStoryPoints] = useState(3);
  const [estimatedHours, setEstimatedHours] = useState(8);
  const [dueDate, setDueDate] = useState('2026-09-05');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    const proj = projects.find(p => p.id === projectId) || projects[0];
    const assignee = users.find(u => u.id === assigneeId) || users[0];
    const key = `${proj?.key || 'DEV'}-${Math.floor(Math.random() * 800) + 100}`;

    onCreate({
      title: title.trim(),
      description: description.trim(),
      project_id: projectId,
      project_key: proj?.key || 'DEV',
      project_name: proj?.name || 'Main Project',
      sprint_id: sprintId,
      key,
      priority,
      status,
      assignee,
      reporter: users[0],
      story_points: storyPoints,
      estimated_hours: estimatedHours,
      actual_hours: 0,
      due_date: dueDate,
      tags: ['backend', 'feature'],
      subtasks: [],
      dependencies: [],
      time_logs: [],
      comments: [],
    });

    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl p-6 space-y-4 shadow-2xl animate-in fade-in zoom-in-95 duration-150 text-xs">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-slate-100">Create New Development Task</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label className="text-slate-400 font-medium">Task Title</label>
            <input
              type="text"
              required
              placeholder="e.g. Implement Webhook Signature Verification"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 font-medium focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="text-slate-400 font-medium">Project</label>
              <select
                value={projectId}
                onChange={(e) => setProjectId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
              >
                {projects.map(p => (
                  <option key={p.id} value={p.id}>[{p.key}] {p.name}</option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-slate-400 font-medium">Sprint</label>
              <select
                value={sprintId}
                onChange={(e) => setSprintId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100"
              >
                {sprints.map(s => (
                  <option key={s.id} value={s.id}>{s.name.split(':')[0]}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div className="space-y-1">
              <label className="text-slate-400 font-medium">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as TaskPriority)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-100"
              >
                <option value="CRITICAL">Critical</option>
                <option value="HIGH">High</option>
                <option value="MEDIUM">Medium</option>
                <option value="LOW">Low</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-slate-400 font-medium">Assignee</label>
              <select
                value={assigneeId}
                onChange={(e) => setAssigneeId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-100"
              >
                {users.map(u => (
                  <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-slate-400 font-medium">Story Points</label>
              <input
                type="number"
                min="1"
                max="21"
                value={storyPoints}
                onChange={(e) => setStoryPoints(parseInt(e.target.value) || 1)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-100 font-mono"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-slate-400 font-medium">Description & Architecture Notes</label>
            <textarea
              rows={3}
              placeholder="Describe requirements, acceptance criteria, or API changes..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-slate-200 font-mono focus:outline-none focus:border-blue-500"
            />
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
              Create Task
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
