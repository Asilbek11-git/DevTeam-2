import React, { useState } from 'react';
import {
  X, CheckSquare, Clock, AlertTriangle, MessageSquare, Paperclip,
  Sparkles, Play, Pause, Square, Plus, Trash2, Tag, Calendar, User,
  CheckCircle2, AlertCircle, ArrowRight
} from 'lucide-react';
import { Task, TaskStatus, TaskPriority, User as UserType, TaskDependency } from '../types';

interface TaskDetailModalProps {
  task: Task;
  allTasks: Task[];
  users: UserType[];
  onClose: () => void;
  onUpdateTask: (updatedTask: Task) => void;
  onDeleteTask: (taskId: string) => void;
  onGenerateAiDescription: (title: string) => Promise<string>;
}

export const TaskDetailModal: React.FC<TaskDetailModalProps> = ({
  task,
  allTasks,
  users,
  onClose,
  onUpdateTask,
  onDeleteTask,
  onGenerateAiDescription,
}) => {
  const [currentTask, setCurrentTask] = useState<Task>({ ...task });
  const [isAiGenerating, setIsAiGenerating] = useState(false);
  const [newSubtaskTitle, setNewSubtaskTitle] = useState('');
  const [newCommentText, setNewCommentText] = useState('');
  const [manualMinutes, setManualMinutes] = useState(60);
  const [timeDescription, setTimeDescription] = useState('');
  const [dependencyTargetId, setDependencyTargetId] = useState('');
  const [dependencyError, setDependencyError] = useState<string | null>(null);

  // Live stopwatch timer state
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [timerSeconds, setTimerSeconds] = useState(0);

  // Timer interval effect
  React.useEffect(() => {
    let interval: any = null;
    if (isTimerRunning) {
      interval = setInterval(() => {
        setTimerSeconds(s => s + 1);
      }, 1000);
    } else if (!isTimerRunning && timerSeconds !== 0) {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isTimerRunning, timerSeconds]);

  const formatTimer = (totalSeconds: number) => {
    const hrs = Math.floor(totalSeconds / 3600);
    const mins = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStopTimer = () => {
    setIsTimerRunning(false);
    const mins = Math.max(1, Math.round(timerSeconds / 60));
    const newLog = {
      id: `tl-${Date.now()}`,
      task_id: currentTask.id,
      user: users[0],
      description: `Live timer session (${formatTimer(timerSeconds)})`,
      start_time: new Date().toISOString(),
      duration_minutes: mins,
      is_billable: true,
    };
    const updated = {
      ...currentTask,
      time_logs: [...(currentTask.time_logs || []), newLog],
      actual_hours: +(currentTask.actual_hours + mins / 60).toFixed(2),
    };
    setCurrentTask(updated);
    onUpdateTask(updated);
    setTimerSeconds(0);
  };

  const handleAddManualLog = () => {
    if (manualMinutes <= 0) return;
    const newLog = {
      id: `tl-${Date.now()}`,
      task_id: currentTask.id,
      user: users[0],
      description: timeDescription || 'Manual development time logged',
      start_time: new Date().toISOString(),
      duration_minutes: manualMinutes,
      is_billable: true,
    };
    const updated = {
      ...currentTask,
      time_logs: [...(currentTask.time_logs || []), newLog],
      actual_hours: +(currentTask.actual_hours + manualMinutes / 60).toFixed(2),
    };
    setCurrentTask(updated);
    onUpdateTask(updated);
    setTimeDescription('');
  };

  const handleToggleSubtask = (subtaskId: string) => {
    const updatedSubtasks = currentTask.subtasks.map(s =>
      s.id === subtaskId ? { ...s, is_completed: !s.is_completed } : s
    );
    const updated = { ...currentTask, subtasks: updatedSubtasks };
    setCurrentTask(updated);
    onUpdateTask(updated);
  };

  const handleAddSubtask = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSubtaskTitle.trim()) return;
    const newSubtask = {
      id: `st-${Date.now()}`,
      title: newSubtaskTitle.trim(),
      is_completed: false,
    };
    const updated = { ...currentTask, subtasks: [...(currentTask.subtasks || []), newSubtask] };
    setCurrentTask(updated);
    onUpdateTask(updated);
    setNewSubtaskTitle('');
  };

  const handleAddComment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCommentText.trim()) return;
    const newComment = {
      id: `c-${Date.now()}`,
      task_id: currentTask.id,
      author: users[0],
      content: newCommentText.trim(),
      created_at: new Date().toISOString(),
    };
    const updated = { ...currentTask, comments: [...(currentTask.comments || []), newComment] };
    setCurrentTask(updated);
    onUpdateTask(updated);
    setNewCommentText('');
  };

  const handleAddDependency = () => {
    if (!dependencyTargetId) return;
    setDependencyError(null);

    // Dependency cycle detection:
    // If target task depends on this task (or target == currentTask), block it
    if (dependencyTargetId === currentTask.id) {
      setDependencyError("A task cannot depend on itself.");
      return;
    }

    const targetTask = allTasks.find(t => t.id === dependencyTargetId);
    if (!targetTask) return;

    // Check if targetTask already has a dependency on currentTask
    const isTargetBlockedByCurrent = targetTask.dependencies?.some(d => d.predecessor_id === currentTask.id);
    if (isTargetBlockedByCurrent) {
      setDependencyError(`Cycle detected! ${targetTask.key} already depends on ${currentTask.key}. Cannot create a circular deadlock.`);
      return;
    }

    const newDep: TaskDependency = {
      id: `dep-${Date.now()}`,
      predecessor_id: targetTask.id,
      predecessor_key: targetTask.key,
      successor_id: currentTask.id,
      successor_key: currentTask.key,
      dependency_type: 'BLOCKS',
    };

    const updated = { ...currentTask, dependencies: [...(currentTask.dependencies || []), newDep] };
    setCurrentTask(updated);
    onUpdateTask(updated);
    setDependencyTargetId('');
  };

  const handleAiImproveDescription = async () => {
    setIsAiGenerating(true);
    try {
      const generated = await onGenerateAiDescription(currentTask.title);
      const updated = { ...currentTask, description: generated };
      setCurrentTask(updated);
      onUpdateTask(updated);
    } catch (e) {
      console.error(e);
    } finally {
      setIsAiGenerating(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Modal Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90 sticky top-0 z-10">
          <div className="flex items-center space-x-3">
            <span className="px-2.5 py-1 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 text-xs font-mono font-bold">
              {currentTask.key}
            </span>
            <span className="text-xs text-slate-400 font-medium">in {currentTask.project_name}</span>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => onDeleteTask(currentTask.id)}
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-950/40 rounded-lg transition-colors"
              title="Delete Task"
            >
              <Trash2 className="w-4 h-4" />
            </button>
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-slate-200 text-xs">
          {/* Title & Status Controls */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2 space-y-2">
              <label className="text-[11px] font-semibold text-slate-400 uppercase">Task Title</label>
              <input
                type="text"
                value={currentTask.title}
                onChange={(e) => {
                  const updated = { ...currentTask, title: e.target.value };
                  setCurrentTask(updated);
                  onUpdateTask(updated);
                }}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm font-semibold text-slate-100 focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label className="text-[11px] font-semibold text-slate-400 uppercase">Status</label>
              <select
                value={currentTask.status}
                onChange={(e) => {
                  const updated = { ...currentTask, status: e.target.value as TaskStatus };
                  setCurrentTask(updated);
                  onUpdateTask(updated);
                }}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 font-semibold focus:outline-none focus:border-blue-500"
              >
                <option value="BACKLOG">Backlog</option>
                <option value="TODO">To Do</option>
                <option value="IN_PROGRESS">In Progress</option>
                <option value="CODE_REVIEW">Code Review</option>
                <option value="QA">QA & Test</option>
                <option value="DONE">Done</option>
                <option value="CANCELLED">Cancelled</option>
              </select>
            </div>
          </div>

          {/* Meta Grid: Priority, Assignee, Points, Due Date */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-950/60 p-3 rounded-xl border border-slate-800">
            <div>
              <span className="text-[10px] text-slate-400 block mb-1">Priority</span>
              <select
                value={currentTask.priority}
                onChange={(e) => {
                  const updated = { ...currentTask, priority: e.target.value as TaskPriority };
                  setCurrentTask(updated);
                  onUpdateTask(updated);
                }}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs"
              >
                <option value="CRITICAL">Critical</option>
                <option value="HIGH">High</option>
                <option value="MEDIUM">Medium</option>
                <option value="LOW">Low</option>
              </select>
            </div>

            <div>
              <span className="text-[10px] text-slate-400 block mb-1">Assignee</span>
              <select
                value={currentTask.assignee?.id || ''}
                onChange={(e) => {
                  const found = users.find(u => u.id === e.target.value);
                  if (found) {
                    const updated = { ...currentTask, assignee: found };
                    setCurrentTask(updated);
                    onUpdateTask(updated);
                  }
                }}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs"
              >
                {users.map(u => (
                  <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>
                ))}
              </select>
            </div>

            <div>
              <span className="text-[10px] text-slate-400 block mb-1">Story Points</span>
              <input
                type="number"
                min="1"
                max="21"
                value={currentTask.story_points}
                onChange={(e) => {
                  const updated = { ...currentTask, story_points: parseInt(e.target.value) || 1 };
                  setCurrentTask(updated);
                  onUpdateTask(updated);
                }}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs font-mono"
              />
            </div>

            <div>
              <span className="text-[10px] text-slate-400 block mb-1">Due Date</span>
              <input
                type="date"
                value={currentTask.due_date}
                onChange={(e) => {
                  const updated = { ...currentTask, due_date: e.target.value };
                  setCurrentTask(updated);
                  onUpdateTask(updated);
                }}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs"
              />
            </div>
          </div>

          {/* Description & AI Enhancer */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-[11px] font-semibold text-slate-400 uppercase">Specification & Description</label>
              <button
                type="button"
                onClick={handleAiImproveDescription}
                disabled={isAiGenerating}
                className="flex items-center space-x-1 px-2.5 py-1 rounded bg-indigo-600/20 hover:bg-indigo-600/30 border border-indigo-500/30 text-indigo-300 text-[11px] font-medium transition-colors"
              >
                <Sparkles className="w-3 h-3 text-indigo-400 animate-pulse" />
                <span>{isAiGenerating ? 'AI Generating Acceptance Criteria...' : 'AI Generate Acceptance Criteria'}</span>
              </button>
            </div>
            <textarea
              rows={6}
              value={currentTask.description}
              onChange={(e) => {
                const updated = { ...currentTask, description: e.target.value };
                setCurrentTask(updated);
                onUpdateTask(updated);
              }}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-xs text-slate-200 font-mono leading-relaxed focus:outline-none focus:border-blue-500"
              placeholder="Describe requirements, acceptance criteria, or code architecture..."
            />
          </div>

          {/* Subtasks Checklist */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-[11px] font-semibold text-slate-400 uppercase flex items-center space-x-1.5">
                <CheckSquare className="w-3.5 h-3.5 text-blue-400" />
                <span>Subtasks & Definition of Done ({currentTask.subtasks?.filter(s => s.is_completed).length || 0}/{currentTask.subtasks?.length || 0})</span>
              </label>
            </div>

            <div className="space-y-1.5 bg-slate-950/40 p-3 rounded-xl border border-slate-800">
              {currentTask.subtasks?.map(sub => (
                <div key={sub.id} className="flex items-center space-x-2.5 py-1">
                  <input
                    type="checkbox"
                    checked={sub.is_completed}
                    onChange={() => handleToggleSubtask(sub.id)}
                    className="rounded border-slate-700 text-blue-600 focus:ring-0 w-4 h-4 bg-slate-900 cursor-pointer"
                  />
                  <span className={`text-xs ${sub.is_completed ? 'line-through text-slate-500' : 'text-slate-200'}`}>
                    {sub.title}
                  </span>
                </div>
              ))}

              <form onSubmit={handleAddSubtask} className="flex items-center space-x-2 pt-2 border-t border-slate-800/80">
                <input
                  type="text"
                  placeholder="Add a new subtask..."
                  value={newSubtaskTitle}
                  onChange={(e) => setNewSubtaskTitle(e.target.value)}
                  className="flex-1 bg-slate-900 border border-slate-700 rounded px-2.5 py-1 text-xs text-slate-200 placeholder-slate-500"
                />
                <button
                  type="submit"
                  className="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-medium"
                >
                  Add
                </button>
              </form>
            </div>
          </div>

          {/* Dependencies & Cycle Prevention Section */}
          <div className="space-y-2">
            <label className="text-[11px] font-semibold text-slate-400 uppercase flex items-center space-x-1.5">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
              <span>Dependencies & Blocking Graph</span>
            </label>

            {dependencyError && (
              <div className="p-2.5 bg-rose-950/50 border border-rose-800 rounded-lg text-rose-300 text-xs flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
                <span>{dependencyError}</span>
              </div>
            )}

            <div className="bg-slate-950/40 p-3 rounded-xl border border-slate-800 space-y-2">
              {currentTask.dependencies && currentTask.dependencies.length > 0 ? (
                <div className="space-y-1.5">
                  {currentTask.dependencies.map(dep => (
                    <div key={dep.id} className="flex items-center justify-between text-xs bg-slate-900 p-2 rounded border border-slate-800">
                      <span className="flex items-center space-x-1.5 text-amber-300">
                        <span className="font-mono font-bold">{dep.predecessor_key}</span>
                        <ArrowRight className="w-3 h-3 text-slate-500" />
                        <span>BLOCKS this task ({currentTask.key})</span>
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-500 text-xs italic">No blocking dependencies.</p>
              )}

              <div className="flex items-center space-x-2 pt-2 border-t border-slate-800">
                <select
                  value={dependencyTargetId}
                  onChange={(e) => setDependencyTargetId(e.target.value)}
                  className="flex-1 bg-slate-900 border border-slate-700 rounded px-2.5 py-1 text-xs text-slate-200"
                >
                  <option value="">Select predecessor blocking task...</option>
                  {allTasks.filter(t => t.id !== currentTask.id).map(t => (
                    <option key={t.id} value={t.id}>[{t.key}] {t.title}</option>
                  ))}
                </select>
                <button
                  type="button"
                  onClick={handleAddDependency}
                  className="px-2.5 py-1 bg-amber-600 hover:bg-amber-500 text-white rounded text-xs font-medium"
                >
                  Add Blocker
                </button>
              </div>
            </div>
          </div>

          {/* Time Tracking Widget */}
          <div className="space-y-2">
            <label className="text-[11px] font-semibold text-slate-400 uppercase flex items-center space-x-1.5">
              <Clock className="w-3.5 h-3.5 text-blue-400" />
              <span>Time Tracking (Estimated: {currentTask.estimated_hours}h / Actual: {currentTask.actual_hours}h)</span>
            </label>

            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
              {/* Live Stopwatch */}
              <div className="flex items-center space-x-3">
                <div className="font-mono text-xl font-bold text-slate-100 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
                  {formatTimer(timerSeconds)}
                </div>
                {!isTimerRunning ? (
                  <button
                    type="button"
                    onClick={() => setIsTimerRunning(true)}
                    className="flex items-center space-x-1 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-medium shadow-sm transition-colors"
                  >
                    <Play className="w-3 h-3 fill-current" />
                    <span>Start Timer</span>
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={handleStopTimer}
                    className="flex items-center space-x-1 px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded-lg font-medium shadow-sm transition-colors"
                  >
                    <Square className="w-3 h-3 fill-current" />
                    <span>Stop & Log Time</span>
                  </button>
                )}
              </div>

              {/* Manual Entry */}
              <div className="flex items-center space-x-2">
                <input
                  type="number"
                  placeholder="Minutes"
                  value={manualMinutes}
                  onChange={(e) => setManualMinutes(parseInt(e.target.value) || 0)}
                  className="w-20 bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs font-mono"
                />
                <input
                  type="text"
                  placeholder="Work log note..."
                  value={timeDescription}
                  onChange={(e) => setTimeDescription(e.target.value)}
                  className="bg-slate-900 border border-slate-700 rounded px-2.5 py-1 text-xs text-slate-200 w-44"
                />
                <button
                  type="button"
                  onClick={handleAddManualLog}
                  className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded font-medium text-xs"
                >
                  Log
                </button>
              </div>
            </div>
          </div>

          {/* Comments & Mentions Thread */}
          <div className="space-y-2">
            <label className="text-[11px] font-semibold text-slate-400 uppercase flex items-center space-x-1.5">
              <MessageSquare className="w-3.5 h-3.5 text-blue-400" />
              <span>Discussion & User Mentions</span>
            </label>

            <div className="space-y-2">
              {currentTask.comments?.map(comment => (
                <div key={comment.id} className="p-3 bg-slate-950/60 rounded-xl border border-slate-800 space-y-1">
                  <div className="flex items-center justify-between text-[11px] text-slate-400">
                    <span className="font-semibold text-slate-300">{comment.author.first_name} {comment.author.last_name}</span>
                    <span>{new Date(comment.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                  </div>
                  <p className="text-slate-200 leading-relaxed">{comment.content}</p>
                </div>
              ))}

              <form onSubmit={handleAddComment} className="flex space-x-2 pt-2">
                <input
                  type="text"
                  placeholder="Write a comment... (use @username to mention team leads)"
                  value={newCommentText}
                  onChange={(e) => setNewCommentText(e.target.value)}
                  className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
                />
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium text-xs shadow-sm"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
