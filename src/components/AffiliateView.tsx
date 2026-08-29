import React, { useState } from 'react';
import {
  Share2, Copy, Check, DollarSign, Users, TrendingUp,
  Gift, ExternalLink, ArrowUpRight, CheckCircle2
} from 'lucide-react';
import { User } from '../types';

interface AffiliateViewProps {
  currentUser: User;
}

export const AffiliateView: React.FC<AffiliateViewProps> = ({ currentUser }) => {
  const [copied, setCopied] = useState(false);
  const referralCode = currentUser.referral_code || 'DEVTEAM2026';
  const referralLink = `https://devteam.io/register?ref=${referralCode}`;

  const handleCopyLink = () => {
    navigator.clipboard.writeText(referralLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 flex-1 overflow-y-auto pb-24 lg:pb-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Share2 className="w-5 h-5 text-emerald-400" />
            <span>Referral & Affiliate Partner Program</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">Earn 20% recurring lifetime commissions for every dev team you refer to DevTeam SaaS.</p>
        </div>

        <button
          onClick={() => alert("Payout request of $428.00 submitted for review!")}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-sm transition-colors"
        >
          <DollarSign className="w-3.5 h-3.5" />
          <span>Request Payout ($428.00)</span>
        </button>
      </div>

      {/* Share Link Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-100">Your Unique Partner Link</h3>
            <p className="text-xs text-slate-400">Share with CTOs, engineering managers, and agencies.</p>
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="text"
              readOnly
              value={referralLink}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-blue-400 font-mono w-64 md:w-80 select-all"
            />
            <button
              onClick={handleCopyLink}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-sm transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied Link' : 'Copy'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Affiliate Metrics Bento */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Referral Clicks</span>
          <div className="text-2xl font-bold font-mono text-slate-100">1,240</div>
          <span className="text-[11px] text-slate-500">From Twitter, GitHub, Blogs</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Workspaces Created</span>
          <div className="text-2xl font-bold font-mono text-blue-400">48</div>
          <span className="text-[11px] text-slate-500">Signups converted</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Paid Upgrades</span>
          <div className="text-2xl font-bold font-mono text-emerald-400">14</div>
          <span className="text-[11px] text-slate-500">Pro & Business tiers</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-2">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Total Earned (All-time)</span>
          <div className="text-2xl font-bold font-mono text-purple-400">$1,280.00</div>
          <span className="text-[11px] text-emerald-400 font-semibold">$428.00 available to withdraw</span>
        </div>
      </div>
    </div>
  );
};
