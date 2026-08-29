import React, { useState } from 'react';
import {
  Flame, Calendar, CheckCircle2, Play, Check, Sparkles,
  TrendingUp, Target, Plus, BarChart2, Layers
} from 'lucide-react';
import { Sprint, Task, Language } from '../types';
import { Translations } from '../data/translations';

interface SprintManagerProps {
  sprints: Sprint[];
  tasks: Task[];
  onStartSprint: (sprintId: string) => void;
  onCompleteSprint: (sprintId: string) => void;
  onOpenAiSprintSummary: (sprint: Sprint) => void;
  t: Translations;
}

export const SprintManager: React.FC<SprintManagerProps> = ({
  sprints,
  tasks,
  onStartSprint,
  onCompleteSprint,
  onOpenAiSprintSummary,
  t,
}) => {
  const activeSprint = sprints.find(s => s.status === 'ACTIVE') || sprints[0];
  const activeTasks = tasks.filter(t => t.sprint_id === activeSprint?.id);
  const doneTasks = activeTasks.filter(t => t.status === 'DONE');
  const inProgressTasks = activeTasks.filter(t => ['IN_PROGRESS', 'CODE_REVIEW', 'QA'].includes(t.status));

  const totalPoints = activeSprint?.total_story_points || 24;
  const completedPoints = activeSprint?.completed_story_points || 11;
  const progressPercent = totalPoints > 0 ? Math.round((completedPoints / totalPoints) * 100) : 0;

  return (
    <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 flex-1 overflow-y-auto pb-24 lg:pb-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Flame className="w-5 h-5 text-amber-500" />
            <span>{t.sprintsTitle}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t.sprintsSubtitle}</p>
        </div>

        <div className="flex items-center space-x-2">
          {activeSprint && activeSprint.status === 'ACTIVE' && (
            <>
              <button
                onClick={() => onOpenAiSprintSummary(activeSprint)}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 text-xs font-medium transition-colors cursor-pointer"
              >
                <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                <span>{t.modeRetroSummary}</span>
              </button>
              <button
                onClick={() => onCompleteSprint(activeSprint.id)}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium transition-colors shadow-sm cursor-pointer"
              >
                <Check className="w-3.5 h-3.5" />
                <span>{t.completeSprint}</span>
              </button>
            </>
          )}
        </div>
      </div>

      {/* Active Sprint Summary Bento */}
      {activeSprint && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Card 1: Goal & Schedule */}
          <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold uppercase">
                  {activeSprint.status}
                </span>
                <h3 className="text-base font-bold text-slate-100">{activeSprint.name}</h3>
              </div>
              <div className="flex items-center space-x-1 text-xs text-slate-400">
                <Calendar className="w-3.5 h-3.5" />
                <span>{activeSprint.start_date} → {activeSprint.end_date}</span>
              </div>
            </div>

            <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3 text-xs text-slate-300">
              <span className="font-semibold text-slate-400 block mb-1">🎯 {t.sprintGoal}:</span>
              <p>{activeSprint.goal}</p>
            </div>

            {/* Velocity & Story Points Progress */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400">{t.burndownProgress}:</span>
                <span className="font-mono text-slate-100 font-bold">
                  {completedPoints} / {totalPoints} {t.storyPointsShort} ({progressPercent}%)
                </span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-blue-500 to-emerald-500 h-2.5 rounded-full transition-all duration-500"
                  style={{ width: `${progressPercent}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Card 2: Sprint Metrics */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 flex flex-col justify-between">
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{t.sprintVelocity} & {t.onTrack}</h4>
            
            <div className="grid grid-cols-2 gap-2 text-center">
              <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                <div className="text-xl font-bold text-blue-400 font-mono">{activeSprint.velocity}</div>
                <div className="text-[10px] text-slate-400">{t.ptsPerSprint}</div>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                <div className="text-xl font-bold text-emerald-400 font-mono">{doneTasks.length}</div>
                <div className="text-[10px] text-slate-400">{t.columnDone}</div>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                <div className="text-xl font-bold text-amber-400 font-mono">{inProgressTasks.length}</div>
                <div className="text-[10px] text-slate-400">{t.columnInProgress}</div>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                <div className="text-xl font-bold text-purple-400 font-mono">0</div>
                <div className="text-[10px] text-slate-400">{t.priorityCritical}</div>
              </div>
            </div>

            <div className="text-[11px] text-slate-400 text-center">
              {t.onTrack} • 92% {t.membersActive}
            </div>
          </div>
        </div>
      )}

      {/* Sprints List Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <Layers className="w-4 h-4 text-blue-400" />
            <span>{t.navSprints} & {t.allSprints}</span>
          </h3>
        </div>

        <div className="divide-y divide-slate-800">
          {sprints.map((sprint) => {
            const sprintTasks = tasks.filter(t => t.sprint_id === sprint.id);
            return (
              <div key={sprint.id} className="p-4 hover:bg-slate-800/40 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                      sprint.status === 'ACTIVE'
                        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                        : sprint.status === 'COMPLETED'
                        ? 'bg-slate-700 text-slate-300'
                        : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                    }`}>
                      {sprint.status}
                    </span>
                    <h4 className="text-sm font-semibold text-slate-100">{sprint.name}</h4>
                  </div>
                  <p className="text-xs text-slate-400">{sprint.goal}</p>
                </div>

                <div className="flex items-center space-x-4 text-xs">
                  <div className="text-right">
                    <div className="font-mono text-slate-200">{sprintTasks.length} {t.openTasks} ({sprint.total_story_points} {t.storyPointsShort})</div>
                    <div className="text-[10px] text-slate-400">{sprint.start_date} → {sprint.end_date}</div>
                  </div>

                  {sprint.status === 'PLANNING' && (
                    <button
                      onClick={() => onStartSprint(sprint.id)}
                      className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs shadow-sm transition-colors cursor-pointer"
                    >
                      <Play className="w-3 h-3 fill-current" />
                      <span>{t.startNewSprint}</span>
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

