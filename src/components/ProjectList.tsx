import React, { useState } from 'react';
import {
  FolderGit2, Plus, Calendar, DollarSign, ExternalLink, GitBranch,
  CheckCircle2, AlertTriangle, Clock, Layers, Sparkles, User, Tag
} from 'lucide-react';
import { Project, ProjectHealth, Workspace, Language } from '../types';
import { Translations } from '../data/translations';

interface ProjectListProps {
  projects: Project[];
  currentWorkspace: Workspace;
  onSelectProject: (project: Project) => void;
  onOpenCreateProject: () => void;
  t: Translations;
}

export const ProjectList: React.FC<ProjectListProps> = ({
  projects,
  currentWorkspace,
  onSelectProject,
  onOpenCreateProject,
  t,
}) => {
  const [filter, setFilter] = useState<string>('ALL');

  const filteredProjects = projects.filter(p => {
    if (filter === 'ALL') return true;
    return p.status === filter;
  });

  const getHealthBadge = (health: ProjectHealth) => {
    switch (health) {
      case 'ON_TRACK':
        return <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-semibold flex items-center space-x-1"><CheckCircle2 className="w-2.5 h-2.5" /><span>{t.onTrack}</span></span>;
      case 'AT_RISK':
        return <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-semibold flex items-center space-x-1"><AlertTriangle className="w-2.5 h-2.5" /><span>{t.atRisk}</span></span>;
      default:
        return <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-semibold flex items-center space-x-1"><AlertTriangle className="w-2.5 h-2.5" /><span>{t.offTrack}</span></span>;
    }
  };

  return (
    <div className="p-6 space-y-6 flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <FolderGit2 className="w-5 h-5 text-blue-500" />
            <span>{t.projectsTitle}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t.projectsSubtitle}</p>
        </div>

        <div className="flex items-center space-x-3">
          {/* Status Filter */}
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="ALL">{t.allProjects}</option>
            <option value="ACTIVE">ACTIVE</option>
            <option value="PLANNING">PLANNING</option>
            <option value="COMPLETED">COMPLETED</option>
          </select>

          <button
            onClick={onOpenCreateProject}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition-colors shadow-sm cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>{t.newProject}</span>
          </button>
        </div>
      </div>

      {/* Project Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {filteredProjects.map((project) => {
          const budgetPercent = project.budget > 0 ? Math.round((project.spent_budget / project.budget) * 100) : 0;

          return (
            <div
              key={project.id}
              onClick={() => onSelectProject(project)}
              className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-5 shadow-sm space-y-4 hover:shadow-md transition-all cursor-pointer group"
            >
              {/* Card Header */}
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono font-bold text-xs text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                      {project.key}
                    </span>
                    <h3 className="text-base font-bold text-slate-100 group-hover:text-blue-300 transition-colors">
                      {project.name}
                    </h3>
                  </div>
                  <p className="text-xs text-slate-400 line-clamp-2">{project.description}</p>
                </div>
                {getHealthBadge(project.health)}
              </div>

              {/* Tech Stack Chips */}
              <div className="flex flex-wrap gap-1.5">
                {project.tech_stack.map((tech, i) => (
                  <span key={i} className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700/60 font-mono">
                    {tech}
                  </span>
                ))}
              </div>

              {/* Milestones Progress Section */}
              {project.milestones && project.milestones.length > 0 && (
                <div className="space-y-2 bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
                  <div className="text-[11px] font-semibold text-slate-300 flex items-center justify-between">
                    <span className="flex items-center space-x-1">
                      <Layers className="w-3 h-3 text-blue-400" />
                      <span>{project.milestones[0].name.split(':')[0]}</span>
                    </span>
                    <span className="font-mono text-emerald-400">{project.milestones[0].progress}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: `${project.milestones[0].progress}%` }}></div>
                  </div>
                </div>
              )}

              {/* Budget & Timeline Meta */}
              <div className="pt-3 border-t border-slate-800 grid grid-cols-2 gap-4 text-xs">
                <div className="space-y-1">
                  <span className="text-slate-500 text-[10px] uppercase font-semibold">{t.budgetAndSpend}</span>
                  <div className="font-mono text-slate-200 font-medium">
                    ${project.spent_budget.toLocaleString()} / ${project.budget.toLocaleString()} ({budgetPercent}%)
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1 overflow-hidden">
                    <div className="bg-blue-500 h-1 rounded-full" style={{ width: `${Math.min(100, budgetPercent)}%` }}></div>
                  </div>
                </div>

                <div className="space-y-1 text-right">
                  <span className="text-slate-500 text-[10px] uppercase font-semibold">{t.timelineAndDeadlines}</span>
                  <div className="text-slate-300 flex items-center justify-end space-x-1 text-[11px]">
                    <Calendar className="w-3 h-3 text-slate-400" />
                    <span>{project.start_date} → {project.deadline}</span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

