import React, { useState } from 'react';
import {
  BookOpen, Play, CheckCircle2, Copy, Check, Terminal,
  ExternalLink, Key, ShieldCheck, FileCode2
} from 'lucide-react';

interface Endpoint {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  tag: string;
  summary: string;
  requestBody?: any;
  responseExample: any;
}

export const SwaggerApiDocs: React.FC = () => {
  const endpoints: Endpoint[] = [
    {
      method: 'GET',
      path: '/api/v1/health/',
      tag: 'System',
      summary: 'Service health check and version metadata',
      responseExample: {
        success: true,
        message: "DevTeam service is operational",
        data: { status: "healthy", service: "DevTeam SaaS", version: "1.0.0" },
        errors: null
      }
    },
    {
      method: 'POST',
      path: '/api/v1/auth/login/',
      tag: 'Authentication',
      summary: 'Authenticate user and issue JWT Access & Refresh tokens',
      requestBody: {
        email: "alex@devteam.io",
        password: "AdminSecure2026!"
      },
      responseExample: {
        success: true,
        message: "Login successful",
        data: {
          user: { id: "u-1", email: "alex@devteam.io", role: "SUPERADMIN" },
          tokens: {
            access: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            refresh: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
          }
        },
        errors: null
      }
    },
    {
      method: 'GET',
      path: '/api/v1/projects/',
      tag: 'Projects',
      summary: 'List tenant-scoped projects and active milestone status',
      responseExample: {
        success: true,
        message: "Projects retrieved",
        data: [
          {
            id: "proj-1",
            key: "PAY",
            name: "NextGen Crypto & Fiat Payment Gateway",
            health: "ON_TRACK",
            spent_budget: 11400.0,
            budget: 24000.0
          }
        ],
        errors: null
      }
    },
    {
      method: 'POST',
      path: '/api/v1/ai/generate/',
      tag: 'AI Intelligence',
      summary: 'Generate task specification or complexity estimate via Gemini API',
      requestBody: {
        action: "generate_task_description",
        title: "Implement Redis Rate Limiting",
        context: "Protect /auth endpoints against brute force attacks"
      },
      responseExample: {
        success: true,
        message: "AI generation completed",
        data: {
          description: "### Specification\n- Rate limit: 100 req/min\n- Key: rate_limit:{ip}:{endpoint}"
        },
        errors: null
      }
    },
    {
      method: 'GET',
      path: '/api/v1/analytics/summary/',
      tag: 'Reports & Revenue',
      summary: 'SuperAdmin SaaS revenue, MRR, ARR, and gateway shares',
      responseExample: {
        success: true,
        message: "Metrics retrieved",
        data: {
          mrr: 14850.00,
          arr: 178200.00,
          paying_workspaces: 248,
          churn_rate: "1.8%"
        },
        errors: null
      }
    }
  ];

  const [selectedEndpoint, setSelectedEndpoint] = useState<Endpoint>(endpoints[1]);
  const [activeTab, setActiveTab] = useState<'console' | 'schema'>('console');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<any>(null);
  const [copied, setCopied] = useState(false);

  const handleExecute = () => {
    setIsExecuting(true);
    setTimeout(() => {
      setExecutionResult(selectedEndpoint.responseExample);
      setIsExecuting(false);
    }, 400);
  };

  const getMethodBadge = (method: string) => {
    switch (method) {
      case 'GET':
        return <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 font-mono font-bold text-[10px]">GET</span>;
      case 'POST':
        return <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono font-bold text-[10px]">POST</span>;
      case 'PUT':
        return <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 font-mono font-bold text-[10px]">PUT</span>;
      default:
        return <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 font-mono font-bold text-[10px]">DELETE</span>;
    }
  };

  return (
    <div className="p-6 space-y-6 flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <BookOpen className="w-5 h-5 text-purple-400" />
            <span>OpenAPI 3.0 & Swagger UI REST API Console</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">Explore endpoints, test live JSON requests, and inspect standardized {`{ success, data, errors }`} contracts.</p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 font-mono border border-slate-700">
            OpenAPI 3.0.3 Spec
          </span>
          <span className="px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 font-mono font-semibold">
            v1.0.0
          </span>
        </div>
      </div>

      {/* Main Swagger Explorer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Endpoints Sidebar */}
        <div className="lg:col-span-5 space-y-2">
          <div className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">
            Available Endpoints ({endpoints.length})
          </div>

          <div className="space-y-1.5">
            {endpoints.map((ep, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setSelectedEndpoint(ep);
                  setExecutionResult(null);
                }}
                className={`w-full text-left p-3 rounded-xl border transition-all flex items-center justify-between ${
                  selectedEndpoint.path === ep.path && selectedEndpoint.method === ep.method
                    ? 'bg-slate-900 border-purple-500/60 shadow-sm'
                    : 'bg-slate-950/60 border-slate-800 hover:bg-slate-900'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    {getMethodBadge(ep.method)}
                    <span className="font-mono text-xs font-semibold text-slate-200">{ep.path}</span>
                  </div>
                  <div className="text-[11px] text-slate-400 line-clamp-1">{ep.summary}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Request & Response Live Console */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-5 flex flex-col justify-between shadow-sm">
          <div className="space-y-4">
            {/* Endpoint Header */}
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2">
                {getMethodBadge(selectedEndpoint.method)}
                <span className="font-mono text-sm font-bold text-slate-100">{selectedEndpoint.path}</span>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-semibold uppercase">
                {selectedEndpoint.tag}
              </span>
            </div>

            <p className="text-xs text-slate-300">{selectedEndpoint.summary}</p>

            {/* Request Body preview */}
            {selectedEndpoint.requestBody && (
              <div className="space-y-1.5">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Request Payload (JSON)</span>
                <pre className="p-3 bg-slate-950 rounded-xl font-mono text-xs text-slate-200 border border-slate-800 overflow-x-auto">
                  {JSON.stringify(selectedEndpoint.requestBody, null, 2)}
                </pre>
              </div>
            )}

            {/* Execute Button */}
            <button
              onClick={handleExecute}
              disabled={isExecuting}
              className="w-full py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white rounded-xl text-xs font-semibold shadow-sm flex items-center justify-center space-x-2 transition-all"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{isExecuting ? 'Sending Request...' : 'Send API Request (Execute)'}</span>
            </button>

            {/* Response Area */}
            {executionResult && (
              <div className="space-y-1.5 pt-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider flex items-center space-x-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Response (HTTP 200 OK)</span>
                  </span>
                  <span className="text-[10px] text-slate-500 font-mono">Response time: 42ms</span>
                </div>
                <pre className="p-3 bg-slate-950 rounded-xl font-mono text-xs text-emerald-300/90 border border-slate-800 overflow-x-auto max-h-60 leading-relaxed">
                  {JSON.stringify(executionResult, null, 2)}
                </pre>
              </div>
            )}
          </div>

          <div className="pt-3 border-t border-slate-800 text-[11px] text-slate-500 text-center">
            Standard REST envelope enforces strict <code className="text-slate-400">success</code>, <code className="text-slate-400">data</code>, and <code className="text-slate-400">errors</code> attributes.
          </div>
        </div>
      </div>
    </div>
  );
};
