import React, { useState, useEffect } from 'react';
import {
  Clock, Play, Square, Calendar, Download, Plus, CheckCircle2,
  DollarSign, BarChart2, Tag, User as UserIcon
} from 'lucide-react';
import { Task, TimeLog, User, Language } from '../types';
import { Translations } from '../data/translations';

interface TimeTrackerViewProps {
  tasks: Task[];
  currentUser: User;
  onLogTime: (taskId: string, durationMinutes: number, note: string, isBillable: boolean) => void;
  t: Translations;
}

export const TimeTrackerView: React.FC<TimeTrackerViewProps> = ({
  tasks,
  currentUser,
  onLogTime,
  t,
}) => {
  const [selectedTaskId, setSelectedTaskId] = useState(tasks[0]?.id || '');
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [manualNote, setManualNote] = useState('');
  const [manualMinutes, setManualMinutes] = useState(60);
  const [isBillable, setIsBillable] = useState(true);

  // Aggregate all time logs across tasks
  const allLogs: Array<TimeLog & { task_key: string; task_title: string }> = [];
  tasks.forEach(t => {
    t.time_logs?.forEach(log => {
      allLogs.push({
        ...log,
        task_key: t.key,
        task_title: t.title,
      });
    });
  });

  // Sort by start_time desc
  allLogs.sort((a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime());

  const totalMinutes = allLogs.reduce((acc, l) => acc + l.duration_minutes, 0);
  const billableMinutes = allLogs.filter(l => l.is_billable).reduce((acc, l) => acc + l.duration_minutes, 0);
  const totalHours = (totalMinutes / 60).toFixed(1);
  const billableHours = (billableMinutes / 60).toFixed(1);

  useEffect(() => {
    let interval: any = null;
    if (isTimerRunning) {
      interval = setInterval(() => setSeconds(s => s + 1), 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isTimerRunning]);

  const formatTimer = (s: number) => {
    const hrs = Math.floor(s / 3600);
    const mins = Math.floor((s % 3600) / 60);
    const secs = s % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStopAndSave = () => {
    setIsTimerRunning(false);
    const mins = Math.max(1, Math.round(seconds / 60));
    if (selectedTaskId) {
      onLogTime(selectedTaskId, mins, manualNote || 'Live work session', isBillable);
    }
    setSeconds(0);
    setManualNote('');
  };

  const handleSaveManual = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedTaskId || manualMinutes <= 0) return;
    onLogTime(selectedTaskId, manualMinutes, manualNote || 'Manual timesheet entry', isBillable);
    setManualNote('');
  };

  return (
    <div className="p-6 space-y-6 flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Clock className="w-5 h-5 text-blue-500" />
            <span>{t.timeTrackerTitle}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t.timeTrackerSubtitle}</p>
        </div>

        <button
          onClick={() => {
            const csvContent = "data:text/csv;charset=utf-8," + 
              "Task,Engineer,Description,Duration(min),Type,Date\n" + 
              allLogs.map(l => `${l.task_key},"${l.user?.first_name || ''} ${l.user?.last_name || ''}","${l.description}",${l.duration_minutes},${l.is_billable ? 'Billable' : 'Non-billable'},${new Date(l.start_time).toLocaleDateString()}`).join("\n");
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "timesheet.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium transition-colors cursor-pointer"
        >
          <Download className="w-3.5 h-3.5" />
          <span>{t.exportTimesheet}</span>
        </button>
      </div>

      {/* Hero Live Tracker & Metrics Bento */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Stopwatch Controller */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-sm">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{t.activeStopwatch}</h3>
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
            <div className="space-y-1">
              <span className="text-[10px] text-slate-400">{t.currentTask}:</span>
              <select
                value={selectedTaskId}
                onChange={(e) => setSelectedTaskId(e.target.value)}
                className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-blue-500 max-w-xs block"
              >
                {tasks.map(t => (
                  <option key={t.id} value={t.id}>[{t.key}] {t.title}</option>
                ))}
              </select>
            </div>

            <div className="flex items-center space-x-4">
              <div className="font-mono text-2xl font-bold text-blue-400 bg-slate-900 px-4 py-2 rounded-xl border border-slate-800 tracking-wider">
                {formatTimer(seconds)}
              </div>

              {!isTimerRunning ? (
                <button
                  type="button"
                  onClick={() => setIsTimerRunning(true)}
                  className="flex items-center space-x-1.5 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold shadow-sm transition-colors cursor-pointer"
                >
                  <Play className="w-4 h-4 fill-current" />
                  <span>{t.startTimer}</span>
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleStopAndSave}
                  className="flex items-center space-x-1.5 px-4 py-2.5 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-semibold shadow-sm transition-colors cursor-pointer"
                >
                  <Square className="w-4 h-4 fill-current" />
                  <span>{t.stopTimer}</span>
                </button>
              )}
            </div>
          </div>

          {/* Quick Manual Entry Form */}
          <form onSubmit={handleSaveManual} className="flex flex-wrap items-center gap-2 pt-2 text-xs">
            <input
              type="text"
              placeholder={t.whatAreYouWorkingOn}
              value={manualNote}
              onChange={(e) => setManualNote(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 min-w-[200px]"
            />
            <input
              type="number"
              min="5"
              step="5"
              value={manualMinutes}
              onChange={(e) => setManualMinutes(parseInt(e.target.value) || 0)}
              className="w-20 bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-200 font-mono text-xs text-center"
              title="Minutes"
            />
            <label className="flex items-center space-x-1.5 text-slate-300 cursor-pointer bg-slate-950 px-2.5 py-1.5 rounded-lg border border-slate-700">
              <input
                type="checkbox"
                checked={isBillable}
                onChange={(e) => setIsBillable(e.target.checked)}
                className="rounded border-slate-700 text-blue-600 focus:ring-0 w-3.5 h-3.5"
              />
              <span className="text-[11px]">{t.billableHours}</span>
            </label>
            <button
              type="submit"
              className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-medium cursor-pointer"
            >
              {t.addManualLog}
            </button>
          </form>
        </div>

        {/* Metrics Bento */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 flex flex-col justify-between">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{t.weeklySummary}</h3>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-950/60 border border-slate-800">
              <div className="space-y-0.5">
                <span className="text-[10px] text-slate-400 uppercase">{t.totalLogged}</span>
                <div className="text-xl font-bold font-mono text-slate-100">{totalHours} hrs</div>
              </div>
              <Clock className="w-6 h-6 text-blue-500" />
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-950/60 border border-slate-800">
              <div className="space-y-0.5">
                <span className="text-[10px] text-slate-400 uppercase">{t.billableHours}</span>
                <div className="text-xl font-bold font-mono text-emerald-400">{billableHours} hrs</div>
              </div>
              <DollarSign className="w-6 h-6 text-emerald-500" />
            </div>
          </div>

          <div className="text-[10px] text-slate-500 text-center">
            {Math.round((+billableHours / (+totalHours || 1)) * 100)}% {t.activeBillableShare}
          </div>
        </div>
      </div>

      {/* Timesheet Logs Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <span>{t.recentEntries} ({allLogs.length})</span>
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="p-3">{t.taskTitle}</th>
                <th className="p-3">{t.assignee}</th>
                <th className="p-3">{t.description}</th>
                <th className="p-3">{t.duration}</th>
                <th className="p-3">{t.type}</th>
                <th className="p-3">{t.date}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {allLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="p-3 font-mono font-semibold text-blue-400">{log.task_key}</td>
                  <td className="p-3 font-medium text-slate-200">{log.user?.first_name} {log.user?.last_name}</td>
                  <td className="p-3 text-slate-300">{log.description}</td>
                  <td className="p-3 font-mono font-bold text-slate-100">{log.duration_minutes} min ({(log.duration_minutes / 60).toFixed(1)}h)</td>
                  <td className="p-3">
                    {log.is_billable ? (
                      <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-semibold">{t.billableHours}</span>
                    ) : (
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">{t.nonBillable}</span>
                    )}
                  </td>
                  <td className="p-3 text-slate-400">{new Date(log.start_time).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

