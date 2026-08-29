import React, { useState } from 'react';
import {
  Plus, Search, Filter, AlertCircle, CheckCircle2, Clock,
  MoreVertical, Tag, MessageSquare, Paperclip, ChevronRight, User, Flame
} from 'lucide-react';
import { Task, BoardColumn, TaskStatus, TaskPriority, User as UserType, Sprint, Language } from '../types';
import { Translations } from '../data/translations';

interface KanbanBoardProps {
  tasks: Task[];
  columns: BoardColumn[];
  sprints: Sprint[];
  users: UserType[];
  onUpdateTaskStatus: (taskId: string, newStatus: TaskStatus) => void;
  onSelectTask: (task: Task) => void;
  onOpenCreateTask: (defaultStatus?: TaskStatus) => void;
  t: Translations;
}

export const KanbanBoard: React.FC<KanbanBoardProps> = ({
  tasks,
  columns,
  sprints,
  users,
  onUpdateTaskStatus,
  onSelectTask,
  onOpenCreateTask,
  t,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [priorityFilter, setPriorityFilter] = useState<string>('ALL');
  const [assigneeFilter, setAssigneeFilter] = useState<string>('ALL');
  const [sprintFilter, setSprintFilter] = useState<string>('ALL');
  const [draggedTaskId, setDraggedTaskId] = useState<string | null>(null);

  // Filter tasks
  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          task.key.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesPriority = priorityFilter === 'ALL' || task.priority === priorityFilter;
    const matchesAssignee = assigneeFilter === 'ALL' || task.assignee?.id === assigneeFilter;
    const matchesSprint = sprintFilter === 'ALL' || task.sprint_id === sprintFilter;
    return matchesSearch && matchesPriority && matchesAssignee && matchesSprint;
  });

  const getPriorityBadge = (priority: TaskPriority) => {
    switch (priority) {
      case 'CRITICAL':
        return <span className="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-bold">{t.priorityCritical}</span>;
      case 'HIGH':
        return <span className="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-semibold">{t.priorityHigh}</span>;
      case 'MEDIUM':
        return <span className="px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[10px]">{t.priorityMedium}</span>;
      default:
        return <span className="px-1.5 py-0.5 rounded bg-slate-700/50 text-slate-400 text-[10px]">{t.priorityLow}</span>;
    }
  };

  const getColumnTitle = (status: TaskStatus, fallback: string) => {
    switch (status) {
      case 'BACKLOG': return t.columnBacklog;
      case 'TODO': return t.columnTodo;
      case 'IN_PROGRESS': return t.columnInProgress;
      case 'CODE_REVIEW': return t.columnCodeReview;
      case 'QA': return t.columnQa;
      case 'DONE': return t.columnDone;
      default: return fallback;
    }
  };

  const handleDragStart = (e: React.DragEvent, taskId: string) => {
    e.dataTransfer.setData('taskId', taskId);
    setDraggedTaskId(taskId);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent, targetStatus: TaskStatus) => {
    e.preventDefault();
    const taskId = e.dataTransfer.getData('taskId') || draggedTaskId;
    if (taskId) {
      onUpdateTaskStatus(taskId, targetStatus);
    }
    setDraggedTaskId(null);
  };

  return (
    <div className="p-6 space-y-5 flex-1 flex flex-col h-full overflow-hidden">
      {/* Board Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <span>{t.kanbanTitle}</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30 font-normal">
              {filteredTasks.length} {t.openTasks}
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t.kanbanSubtitle}</p>
        </div>

        {/* Filters Bar */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          {/* Search */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder={t.filterBySearch}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 w-40 sm:w-48"
            />
          </div>

          {/* Priority Filter */}
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="ALL">{t.allProjects}</option>
            <option value="CRITICAL">{t.priorityCritical}</option>
            <option value="HIGH">{t.priorityHigh}</option>
            <option value="MEDIUM">{t.priorityMedium}</option>
            <option value="LOW">{t.priorityLow}</option>
          </select>

          {/* Assignee Filter */}
          <select
            value={assigneeFilter}
            onChange={(e) => setAssigneeFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="ALL">{t.allAssignees}</option>
            {users.map(u => (
              <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>
            ))}
          </select>

          {/* Sprint Filter */}
          <select
            value={sprintFilter}
            onChange={(e) => setSprintFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="ALL">{t.allSprints}</option>
            {sprints.map(s => (
              <option key={s.id} value={s.id}>{s.name.split(':')[0]}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Kanban Columns Grid */}
      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3.5 overflow-x-auto pb-4 items-start">
        {columns.map((col) => {
          const colTasks = filteredTasks.filter(t => t.status === col.status_mapping);
          const isOverWip = col.wip_limit > 0 && colTasks.length > col.wip_limit;
          const displayTitle = getColumnTitle(col.status_mapping, col.title);

          return (
            <div
              key={col.id}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, col.status_mapping)}
              className="bg-slate-900/60 border border-slate-800 rounded-xl flex flex-col max-h-full min-w-[240px] flex-shrink-0 transition-colors"
            >
              {/* Column Header */}
              <div className="p-3 border-b border-slate-800/80 flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: col.color }}></div>
                  <span className="font-semibold text-xs text-slate-200 truncate max-w-[130px]">{displayTitle}</span>
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono font-medium ${
                    isOverWip ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-slate-800 text-slate-400'
                  }`}>
                    {colTasks.length}{col.wip_limit > 0 ? ` / ${col.wip_limit}` : ''}
                  </span>
                </div>

                <button
                  onClick={() => onOpenCreateTask(col.status_mapping)}
                  className="p-1 text-slate-400 hover:text-blue-400 hover:bg-slate-800 rounded transition-colors cursor-pointer"
                  title={`${t.actions}: ${displayTitle}`}
                >
                  <Plus className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* WIP Warning */}
              {isOverWip && (
                <div className="px-3 py-1 bg-rose-950/40 border-b border-rose-800/50 text-[10px] text-rose-300 flex items-center space-x-1">
                  <AlertCircle className="w-3 h-3 flex-shrink-0 text-rose-400" />
                  <span>{t.wipLimit}: ({colTasks.length}/{col.wip_limit})</span>
                </div>
              )}

              {/* Tasks List */}
              <div className="p-2 space-y-2 overflow-y-auto min-h-[350px] max-h-[calc(100vh-250px)]">
                {colTasks.map((task) => {
                  const completedSubtasks = task.subtasks?.filter(s => s.is_completed).length || 0;
                  const totalSubtasks = task.subtasks?.length || 0;

                  return (
                    <div
                      key={task.id}
                      draggable
                      onDragStart={(e) => handleDragStart(e, task.id)}
                      onClick={() => onSelectTask(task)}
                      className="p-3 bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 hover:border-blue-500/50 rounded-lg shadow-sm cursor-grab active:cursor-grabbing transition-all group hover:scale-[1.01]"
                    >
                      {/* Top Meta: Key & Priority */}
                      <div className="flex items-center justify-between text-[11px] mb-1.5">
                        <span className="font-mono font-semibold text-blue-400">{task.key}</span>
                        {getPriorityBadge(task.priority)}
                      </div>

                      {/* Title */}
                      <h4 className="text-xs font-medium text-slate-100 group-hover:text-blue-300 transition-colors leading-snug line-clamp-2">
                        {task.title}
                      </h4>

                      {/* Dependencies Badge */}
                      {task.dependencies && task.dependencies.length > 0 && (
                        <div className="mt-2 text-[10px] text-amber-300/90 flex items-center space-x-1 bg-amber-500/10 px-1.5 py-0.5 rounded border border-amber-500/20">
                          <AlertCircle className="w-2.5 h-2.5 text-amber-400" />
                          <span>{t.dependencies}: {task.dependencies.map(d => d.predecessor_key).join(', ')}</span>
                        </div>
                      )}

                      {/* Subtasks Progress */}
                      {totalSubtasks > 0 && (
                        <div className="mt-2 text-[10px] text-slate-400 flex items-center space-x-1.5">
                          <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                          <span>{completedSubtasks}/{totalSubtasks} {t.subtasksAndCriteria.split('&')[0].trim()}</span>
                        </div>
                      )}

                      {/* Bottom Footer: Story points, comments, assignee */}
                      <div className="mt-3 pt-2 border-t border-slate-700/50 flex items-center justify-between text-[10px] text-slate-400">
                        <div className="flex items-center space-x-2">
                          <span className="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 text-slate-300 font-mono">
                            {task.story_points} {t.storyPointsShort}
                          </span>
                          {task.comments?.length > 0 && (
                            <span className="flex items-center space-x-0.5 text-slate-400">
                              <MessageSquare className="w-2.5 h-2.5" />
                              <span>{task.comments.length}</span>
                            </span>
                          )}
                        </div>

                        {/* Assignee Avatar */}
                        {task.assignee ? (
                          <div
                            className="w-5 h-5 rounded-full bg-blue-600 text-white flex items-center justify-center text-[9px] font-bold"
                            title={`${task.assignee.first_name} ${task.assignee.last_name}`}
                          >
                            {task.assignee.first_name[0]}{task.assignee.last_name[0]}
                          </div>
                        ) : (
                          <div className="w-5 h-5 rounded-full bg-slate-700 text-slate-400 flex items-center justify-center">
                            <User className="w-3 h-3" />
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}

                {colTasks.length === 0 && (
                  <div className="h-24 border-2 border-dashed border-slate-800 rounded-lg flex items-center justify-center text-slate-600 text-[11px] p-2 text-center">
                    {t.noTasksInColumn}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

