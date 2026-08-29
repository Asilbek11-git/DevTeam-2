import React, { useState } from 'react';
import {
  Sparkles, Bot, CheckSquare, Zap, BookOpen, Copy, Check,
  Send, RefreshCw, BarChart2, Layers, ShieldCheck
} from 'lucide-react';
import { Task, Sprint, Language } from '../types';
import { Translations } from '../data/translations';

interface AiStudioViewProps {
  tasks: Task[];
  sprints: Sprint[];
  onApplyGeneratedTask?: (title: string, description: string) => void;
  t: Translations;
}

export const AiStudioView: React.FC<AiStudioViewProps> = ({
  tasks,
  sprints,
  onApplyGeneratedTask,
  t,
}) => {
  const [activeTab, setActiveTab] = useState<'task_gen' | 'estimator' | 'retrospective' | 'release_notes'>('task_gen');
  const [taskPrompt, setTaskPrompt] = useState('Implement Redis Rate Limiting middleware for public API endpoints');
  const [contextPrompt, setContextPrompt] = useState('Protect /api/v1/auth/login and payment webhook endpoints against brute force attacks. Support 100 requests per minute with sliding window.');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedOutput, setGeneratedOutput] = useState<string>('');
  const [copied, setCopied] = useState(false);

  // Estimator state
  const [estimateResult, setEstimateResult] = useState<{ points: number; hours: number; reasoning: string; risks: string[] } | null>(null);

  const handleGenerateTask = async () => {
    setIsGenerating(true);
    // Call AI logic
    setTimeout(() => {
      setGeneratedOutput(`### 📌 Task Overview: ${taskPrompt}

#### 🎯 Problem Statement & Objective:
Unauthenticated traffic to sensitive endpoints must be rate-limited using a sliding window algorithm in Redis to prevent credential stuffing and DDOS exhaustion.

#### 📋 Technical Requirements & Architecture:
- Implement a custom Django REST Framework rate-limiting throttle class backed by Redis cache pool.
- Key format: \`rate_limit:{ip}:{endpoint_hash}\` with a 60-second sliding TTL.
- Return HTTP 429 Too Many Requests with standard \`Retry-After\` and JSON error response envelope.
- Provide bypass whitelist for trusted webhook provider IP ranges (Stripe, Payme, Click).

#### ✅ Definition of Done & Acceptance Criteria:
- [ ] DRF throttle middleware class implemented in \`apps.core.throttling\`.
- [ ] Redis sliding window evaluation script runs with sub-millisecond latency.
- [ ] HTTP 429 status code returned with proper JSON error payload.
- [ ] Integration test suite confirms rate limit resets cleanly after 60 seconds.
- [ ] Prometheus / Grafana metrics counter incremented on throttled requests.`);
      setIsGenerating(false);
    }, 1200);
  };

  const handleEstimateComplexity = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setEstimateResult({
        points: 5,
        hours: 12.5,
        reasoning: 'Requires Redis connection pooling, atomic Lua script execution for sliding window, and thorough integration testing with mock Redis cache.',
        risks: [
          'Redis failover latency if connection pool is starved during traffic spikes',
          'IP spoofing vulnerability if X-Forwarded-For header is not sanitized behind proxy'
        ]
      });
      setIsGenerating(false);
    }, 1000);
  };

  const handleGenerateRetrospective = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setGeneratedOutput(`### 📊 AI Sprint Retrospective Summary

#### 🌟 What Went Well (Wins):
- Completed 11 out of 24 planned story points with zero production incidents.
- Successfully implemented HMAC-SHA256 signature verification for Payme & Click gateways.
- Redis idempotency key locking prevented multiple duplicate charges during testing.

#### ⚠️ Areas for Improvement (Blockers Encountered):
- External webhook test sandbox experienced 15-minute downtime during QA verification.
- Task PAY-101 was temporarily blocked by PAY-102 due to dependency ordering.

#### 💡 Action Items for Next Sprint:
1. Increase automated unit test coverage on payment refund handlers.
2. Setup dedicated mock webhook receiver to decouple QA from external vendor sandboxes.`);
      setIsGenerating(false);
    }, 1200);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedOutput);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="p-6 space-y-6 flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <span>{t.aiStudioTitle}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t.aiStudioSubtitle}</p>
        </div>

        <div className="flex items-center space-x-2">
          <span className="px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-semibold font-mono">
            Gemini 2.5 Flash
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-4 text-xs font-medium">
        <button
          onClick={() => { setActiveTab('task_gen'); setGeneratedOutput(''); }}
          className={`pb-2.5 border-b-2 transition-colors cursor-pointer ${
            activeTab === 'task_gen' ? 'border-indigo-500 text-indigo-300 font-semibold' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          {t.modeTaskSpec}
        </button>
        <button
          onClick={() => { setActiveTab('estimator'); setEstimateResult(null); }}
          className={`pb-2.5 border-b-2 transition-colors cursor-pointer ${
            activeTab === 'estimator' ? 'border-indigo-500 text-indigo-300 font-semibold' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          {t.modeComplexityEstimator}
        </button>
        <button
          onClick={() => { setActiveTab('retrospective'); setGeneratedOutput(''); }}
          className={`pb-2.5 border-b-2 transition-colors cursor-pointer ${
            activeTab === 'retrospective' ? 'border-indigo-500 text-indigo-300 font-semibold' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          {t.modeRetroSummary}
        </button>
      </div>

      {/* Tab 1: Task Spec Generator */}
      {activeTab === 'task_gen' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-sm text-xs">
            <h3 className="text-sm font-bold text-slate-100">{t.promptPlaceholder}</h3>
            
            <div className="space-y-1.5">
              <label className="text-slate-400 font-medium">{t.taskTitle}</label>
              <input
                type="text"
                value={taskPrompt}
                onChange={(e) => setTaskPrompt(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 font-medium focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-slate-400 font-medium">{t.description}</label>
              <textarea
                rows={4}
                value={contextPrompt}
                onChange={(e) => setContextPrompt(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-slate-200 font-mono focus:outline-none focus:border-indigo-500 leading-relaxed"
              />
            </div>

            <button
              onClick={handleGenerateTask}
              disabled={isGenerating}
              className="w-full py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-lg font-semibold shadow-sm flex items-center justify-center space-x-2 transition-all cursor-pointer"
            >
              <Sparkles className="w-4 h-4" />
              <span>{isGenerating ? t.aiGenerating : t.generateAiContent}</span>
            </button>
          </div>

          {/* Output Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 flex flex-col justify-between text-xs">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="font-semibold text-slate-300">{t.generatedSpecification}</span>
              {generatedOutput && (
                <button
                  onClick={handleCopy}
                  className="flex items-center space-x-1 text-indigo-400 hover:text-indigo-300 font-medium cursor-pointer"
                >
                  {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? t.copiedText : t.copyText}</span>
                </button>
              )}
            </div>

            <div className="bg-slate-950/80 rounded-lg p-4 font-mono text-slate-200 overflow-y-auto max-h-[350px] leading-relaxed whitespace-pre-wrap flex-1 border border-slate-800/80">
              {generatedOutput || (
                <span className="text-slate-500 italic">{t.aiPlaceholderDescription}</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Complexity Estimator */}
      {activeTab === 'estimator' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6 text-xs">
          <div className="space-y-2 max-w-xl">
            <h3 className="text-sm font-bold text-slate-100">{t.modeComplexityEstimator}</h3>
            <p className="text-slate-400">{t.aiStudioSubtitle}</p>
          </div>

          <div className="flex items-center space-x-3">
            <input
              type="text"
              value={taskPrompt}
              onChange={(e) => setTaskPrompt(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 font-medium"
            />
            <button
              onClick={handleEstimateComplexity}
              disabled={isGenerating}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-semibold flex items-center space-x-2 cursor-pointer"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>{isGenerating ? t.aiGenerating : t.generateAiContent}</span>
            </button>
          </div>

          {estimateResult && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-slate-800 animate-in fade-in duration-200">
              <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 text-center space-y-1">
                <span className="text-slate-400 text-[10px] uppercase font-bold">{t.storyPoints}</span>
                <div className="text-3xl font-mono font-bold text-indigo-400">{estimateResult.points} {t.storyPointsShort}</div>
                <span className="text-[11px] text-slate-500">Fibonacci scale</span>
              </div>

              <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 text-center space-y-1">
                <span className="text-slate-400 text-[10px] uppercase font-bold">{t.duration}</span>
                <div className="text-3xl font-mono font-bold text-blue-400">{estimateResult.hours} {t.hours}</div>
                <span className="text-[11px] text-slate-500">Code review & QA</span>
              </div>

              <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-2">
                <span className="text-slate-400 text-[10px] uppercase font-bold">{t.atRisk}</span>
                <ul className="list-disc list-inside space-y-1 text-[11px] text-amber-300/90">
                  {estimateResult.risks.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 3: Retrospective Summarizer */}
      {activeTab === 'retrospective' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4 text-xs">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-100">{t.modeRetroSummary}</h3>
              <p className="text-slate-400">{t.sprintsSubtitle}</p>
            </div>
            <button
              onClick={handleGenerateRetrospective}
              disabled={isGenerating}
              className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-lg font-semibold flex items-center space-x-2 cursor-pointer"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>{isGenerating ? t.aiGenerating : t.generateAiContent}</span>
            </button>
          </div>

          <div className="bg-slate-950/80 rounded-xl p-4 font-mono text-slate-200 border border-slate-800 whitespace-pre-wrap leading-relaxed min-h-[200px]">
            {generatedOutput || t.aiPlaceholderDescription}
          </div>
        </div>
      )}
    </div>
  );
};

