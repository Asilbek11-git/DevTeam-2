import React, { useState } from 'react';
import {
  GitPullRequest, GitCommit, GitBranch, Github, Play, CheckCircle2,
  Copy, Check, ShieldCheck, RefreshCw, Zap, ArrowRight, ExternalLink
} from 'lucide-react';
import { Task, TaskStatus } from '../types';

interface IntegrationsViewProps {
  tasks: Task[];
  onSimulateWebhook: (event: 'commit' | 'pr_opened' | 'pr_merged', payload: any) => void;
}

export const IntegrationsView: React.FC<IntegrationsViewProps> = ({
  tasks,
  onSimulateWebhook,
}) => {
  const [selectedTaskKey, setSelectedTaskKey] = useState('PAY-101');
  const [commitMessage, setCommitMessage] = useState('[PAY-101] Fix HMAC-SHA256 signature verifier edge cases');
  const [prTitle, setPrTitle] = useState('[PAY-102] Implement Redis Idempotency Key Lock');
  const [branchName, setBranchName] = useState('feat/redis-idempotency');
  const [copied, setCopied] = useState(false);
  const [eventLogs, setEventLogs] = useState<Array<{ id: string; time: string; event: string; status: string; details: string }>>([
    {
      id: 'evt-1',
      time: '10:15:22 AM',
      event: 'github:push',
      status: 'PROCESSED',
      details: 'Commit 8f1b2c4 linked to task PAY-103 by dmitry_be',
    },
    {
      id: 'evt-2',
      time: '11:42:05 AM',
      event: 'github:pull_request.opened',
      status: 'TRIGGERED_AUTOMATION',
      details: 'PR #42 opened -> Automation rule moved PAY-102 to CODE_REVIEW',
    }
  ]);

  const handleCopyWebhookUrl = () => {
    navigator.clipboard.writeText('https://api.devteam.io/api/v1/integrations/webhooks/github/');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const runCommitSimulation = () => {
    onSimulateWebhook('commit', {
      task_key: selectedTaskKey,
      message: commitMessage,
      sha: Math.random().toString(36).substring(2, 9),
      author: 'sarahchen-dev',
    });

    setEventLogs(prev => [
      {
        id: `evt-${Date.now()}`,
        time: new Date().toLocaleTimeString(),
        event: 'github:push',
        status: 'PROCESSED',
        details: `Simulated commit referencing ${selectedTaskKey} ingested into audit stream.`,
      },
      ...prev
    ]);
  };

  const runPrOpenSimulation = () => {
    onSimulateWebhook('pr_opened', {
      task_key: 'PAY-102',
      title: prTitle,
      branch: branchName,
      pr_number: Math.floor(Math.random() * 50) + 40,
    });

    setEventLogs(prev => [
      {
        id: `evt-${Date.now()}`,
        time: new Date().toLocaleTimeString(),
        event: 'github:pull_request.opened',
        status: 'TRIGGERED_AUTOMATION',
        details: `PR opened for PAY-102 -> Automatically transitioned task to CODE_REVIEW.`,
      },
      ...prev
    ]);
  };

  const runPrMergeSimulation = () => {
    onSimulateWebhook('pr_merged', {
      task_key: 'PAY-102',
      title: prTitle,
      pr_number: 42,
    });

    setEventLogs(prev => [
      {
        id: `evt-${Date.now()}`,
        time: new Date().toLocaleTimeString(),
        event: 'github:pull_request.closed',
        status: 'TRIGGERED_AUTOMATION',
        details: `PR #42 merged into main -> Automation Rule auto-moved task PAY-102 to QA & Test.`,
      },
      ...prev
    ]);
  };

  return (
    <div className="p-6 space-y-6 flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <GitPullRequest className="w-5 h-5 text-purple-400" />
            <span>GitHub & GitLab VCS Webhook Engine</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">Automate task status transitions, commit linking, and pull request reviews in real-time.</p>
        </div>

        <div className="flex items-center space-x-2">
          <span className="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span>Webhook Listener Active</span>
          </span>
        </div>
      </div>

      {/* Connection & Webhook Endpoint Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-white">
              <Github className="w-6 h-6" />
            </div>
            <div>
              <div className="text-sm font-bold text-slate-100 flex items-center space-x-2">
                <span>nexustech / payment-core</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold">Connected</span>
              </div>
              <p className="text-xs text-slate-400">Listening for push, pull_request, and commit_comment events.</p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handleCopyWebhookUrl}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-mono font-medium transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied URL!' : 'Copy Webhook URL'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Interactive Webhook Simulator Panel */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-sm">
        <div className="flex items-center space-x-2">
          <Zap className="w-4 h-4 text-amber-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wide">Interactive VCS Webhook Simulator</h3>
        </div>
        <p className="text-xs text-slate-400">Trigger live simulated GitHub webhook payloads to test automated task board updates in real time.</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          {/* Action 1: Git Push */}
          <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 space-y-3 flex flex-col justify-between">
            <div className="space-y-2">
              <span className="text-xs font-bold text-blue-400 flex items-center space-x-1">
                <GitCommit className="w-3.5 h-3.5" />
                <span>1. Simulate Git Push (Commit)</span>
              </span>
              <p className="text-[11px] text-slate-400">Links git commit SHA to task history via regex key match.</p>
              <input
                type="text"
                value={commitMessage}
                onChange={(e) => setCommitMessage(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono"
              />
            </div>

            <button
              onClick={runCommitSimulation}
              className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors"
            >
              <Play className="w-3 h-3 fill-current" />
              <span>Simulate Commit Webhook</span>
            </button>
          </div>

          {/* Action 2: Open PR */}
          <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 space-y-3 flex flex-col justify-between">
            <div className="space-y-2">
              <span className="text-xs font-bold text-purple-400 flex items-center space-x-1">
                <GitPullRequest className="w-3.5 h-3.5" />
                <span>2. Simulate PR Opened</span>
              </span>
              <p className="text-[11px] text-slate-400">Auto-moves linked task [PAY-102] to Code Review column.</p>
              <input
                type="text"
                value={prTitle}
                onChange={(e) => setPrTitle(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono"
              />
            </div>

            <button
              onClick={runPrOpenSimulation}
              className="w-full py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors"
            >
              <Play className="w-3 h-3 fill-current" />
              <span>Simulate Open PR Webhook</span>
            </button>
          </div>

          {/* Action 3: Merge PR */}
          <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 space-y-3 flex flex-col justify-between">
            <div className="space-y-2">
              <span className="text-xs font-bold text-emerald-400 flex items-center space-x-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>3. Simulate PR Merged</span>
              </span>
              <p className="text-[11px] text-slate-400">Executes Automation Rule: moves task PAY-102 directly to QA.</p>
              <div className="p-2.5 rounded bg-slate-900 border border-slate-800 text-[11px] text-slate-300 font-mono">
                PR #42 merged into `main` branch
              </div>
            </div>

            <button
              onClick={runPrMergeSimulation}
              className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors"
            >
              <Play className="w-3 h-3 fill-current" />
              <span>Simulate Merge PR Webhook</span>
            </button>
          </div>
        </div>
      </div>

      {/* Webhook Activity Stream */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Live Webhook Ingestion Feed</h3>
          <span className="text-[11px] text-slate-500 font-mono">Real-time Celery queue</span>
        </div>

        <div className="divide-y divide-slate-800">
          {eventLogs.map((log) => (
            <div key={log.id} className="p-3.5 flex items-center justify-between text-xs hover:bg-slate-800/30 transition-colors">
              <div className="flex items-center space-x-3">
                <span className="font-mono text-[10px] text-slate-500">{log.time}</span>
                <span className="px-2 py-0.5 rounded bg-slate-800 text-purple-300 border border-slate-700 font-mono text-[10px]">
                  {log.event}
                </span>
                <span className="text-slate-200">{log.details}</span>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-semibold border border-emerald-500/30">
                {log.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
