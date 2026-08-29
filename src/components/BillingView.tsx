import React, { useState } from 'react';
import {
  CreditCard, Check, Sparkles, Shield, Download, Tag,
  ArrowRight, AlertCircle, CheckCircle2, Zap, DollarSign
} from 'lucide-react';
import { Plan, PlanTier, Invoice, Workspace, Language } from '../types';
import { Translations } from '../data/translations';

interface BillingViewProps {
  currentWorkspace: Workspace;
  plans: Plan[];
  invoices: Invoice[];
  onUpgradePlan: (plan: Plan, billingCycle: 'monthly' | 'yearly', gateway: 'stripe' | 'payme' | 'click', couponCode?: string) => void;
  t: Translations;
}

export const BillingView: React.FC<BillingViewProps> = ({
  currentWorkspace,
  plans,
  invoices,
  onUpgradePlan,
  t,
}) => {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');
  const [selectedPlanForUpgrade, setSelectedPlanForUpgrade] = useState<Plan | null>(null);
  const [selectedGateway, setSelectedGateway] = useState<'stripe' | 'payme' | 'click'>('stripe');
  const [couponCode, setCouponCode] = useState('');
  const [appliedDiscount, setAppliedDiscount] = useState<number | null>(null);
  const [couponError, setCouponError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleApplyCoupon = (e: React.FormEvent) => {
    e.preventDefault();
    setCouponError(null);
    if (couponCode.toUpperCase() === 'LAUNCH2026') {
      setAppliedDiscount(25); // 25% off
    } else {
      setCouponError('Invalid or expired promotional coupon code.');
    }
  };

  const handleCheckout = () => {
    if (!selectedPlanForUpgrade) return;
    setIsProcessing(true);
    setTimeout(() => {
      onUpgradePlan(selectedPlanForUpgrade, billingCycle, selectedGateway, couponCode);
      setIsProcessing(false);
      setSuccessMessage(`Workspace successfully upgraded to ${selectedPlanForUpgrade.name} via ${selectedGateway.toUpperCase()}!`);
      setSelectedPlanForUpgrade(null);
    }, 1200);
  };

  return (
    <div className="p-6 space-y-8 flex-1 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <CreditCard className="w-5 h-5 text-blue-500" />
            <span>{t.billingTitle}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">{t.billingSubtitle}</p>
        </div>

        {/* Monthly / Yearly Switch */}
        <div className="flex items-center space-x-3 bg-slate-900 p-1 rounded-xl border border-slate-800 self-start md:self-auto">
          <button
            onClick={() => setBillingCycle('monthly')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              billingCycle === 'monthly' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {t.monthly}
          </button>
          <button
            onClick={() => setBillingCycle('yearly')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition-all cursor-pointer ${
              billingCycle === 'yearly' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span>{t.yearly}</span>
            <span className="px-1.5 py-0.2 bg-emerald-500/20 text-emerald-300 text-[10px] rounded font-bold">20% OFF</span>
          </button>
        </div>
      </div>

      {successMessage && (
        <div className="p-4 rounded-xl bg-emerald-950/60 border border-emerald-800 text-emerald-300 text-xs flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span className="font-semibold">{successMessage}</span>
        </div>
      )}

      {/* Usage Resource Bars */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-300 uppercase tracking-wider">{t.activePlan}: {currentWorkspace.plan_tier}</span>
          <span className="text-xs text-blue-400 font-mono font-semibold">Active & Healthy</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-950/60 rounded-lg border border-slate-800 space-y-2">
            <div className="flex justify-between text-slate-400">
              <span>{t.teamMembers}:</span>
              <span className="font-mono text-slate-200">5 / 10</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-1.5">
              <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '50%' }}></div>
            </div>
          </div>

          <div className="p-3 bg-slate-950/60 rounded-lg border border-slate-800 space-y-2">
            <div className="flex justify-between text-slate-400">
              <span>{t.projects}:</span>
              <span className="font-mono text-slate-200">2 / ∞</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-1.5">
              <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: '20%' }}></div>
            </div>
          </div>

          <div className="p-3 bg-slate-950/60 rounded-lg border border-slate-800 space-y-2">
            <div className="flex justify-between text-slate-400">
              <span>AI Token Generations:</span>
              <span className="font-mono text-slate-200">84 / 250</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-1.5">
              <div className="bg-indigo-500 h-1.5 rounded-full" style={{ width: '33%' }}></div>
            </div>
          </div>

          <div className="p-3 bg-slate-950/60 rounded-lg border border-slate-800 space-y-2">
            <div className="flex justify-between text-slate-400">
              <span>Storage Used:</span>
              <span className="font-mono text-slate-200">1.2 GB / 10 GB</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-1.5">
              <div className="bg-purple-500 h-1.5 rounded-full" style={{ width: '12%' }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Subscription Plans Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {plans.map((plan) => {
          const isCurrent = currentWorkspace.plan_tier === plan.tier;
          const price = billingCycle === 'yearly' ? plan.yearly_price : plan.monthly_price;

          return (
            <div
              key={plan.id}
              className={`bg-slate-900 rounded-2xl p-6 flex flex-col justify-between space-y-5 transition-all relative ${
                plan.is_popular
                  ? 'border-2 border-blue-500 shadow-lg shadow-blue-500/10'
                  : 'border border-slate-800 hover:border-slate-700'
              }`}
            >
              {plan.is_popular && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-[10px] uppercase font-bold tracking-wider px-3 py-0.5 rounded-full shadow">
                  {t.popular}
                </span>
              )}

              <div className="space-y-4">
                <div>
                  <h3 className="text-base font-bold text-slate-100">{plan.name}</h3>
                  <p className="text-xs text-slate-400 mt-1 min-h-[32px]">{plan.description}</p>
                </div>

                <div className="flex items-baseline space-x-1 font-mono">
                  <span className="text-3xl font-extrabold text-slate-100">${price}</span>
                  <span className="text-xs text-slate-400">/{billingCycle === 'yearly' ? 'year' : 'mo'}</span>
                </div>

                <div className="space-y-2.5 pt-2 border-t border-slate-800 text-xs">
                  <div className="flex items-center space-x-2 text-slate-300">
                    <Check className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />
                    <span>{plan.max_members === 0 ? 'Unlimited' : plan.max_members} {t.teamMembers}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-slate-300">
                    <Check className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />
                    <span>{plan.max_projects === 0 ? 'Unlimited' : `${plan.max_projects} Active`} {t.projects}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-slate-300">
                    <Check className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />
                    <span>{plan.max_ai_generations_per_month} AI Gen / mo</span>
                  </div>
                  <div className="flex items-center space-x-2 text-slate-300">
                    <Check className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />
                    <span>{plan.has_git_integrations ? 'GitHub / GitLab VCS' : 'No VCS Integrations'}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-slate-300">
                    <Check className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />
                    <span>{plan.has_advanced_reports ? 'Analytics & Reports' : 'Basic Metrics'}</span>
                  </div>
                </div>
              </div>

              <div>
                {isCurrent ? (
                  <button
                    disabled
                    className="w-full py-2 bg-slate-800 text-slate-400 rounded-xl text-xs font-semibold cursor-default"
                  >
                    {t.activePlan}
                  </button>
                ) : (
                  <button
                    onClick={() => setSelectedPlanForUpgrade(plan)}
                    className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-semibold shadow-sm transition-colors cursor-pointer"
                  >
                    {plan.monthly_price === 0 ? t.currentPlanTier : t.upgradePlan}
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Invoices List */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200">{t.invoices}</h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="p-3">Invoice ID</th>
                <th className="p-3">{t.activePlan}</th>
                <th className="p-3">{t.amount}</th>
                <th className="p-3">{t.paymentGateway}</th>
                <th className="p-3">{t.status}</th>
                <th className="p-3">{t.date}</th>
                <th className="p-3 text-right">{t.downloadReceipt}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {invoices.map((inv) => (
                <tr key={inv.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="p-3 font-mono font-semibold text-blue-400">{inv.invoice_number}</td>
                  <td className="p-3">{inv.plan_name}</td>
                  <td className="p-3 font-mono font-bold text-slate-100">${inv.amount.toFixed(2)} USD</td>
                  <td className="p-3 text-slate-300">{inv.payment_method}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-semibold">
                      {inv.status}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400">{inv.paid_at}</td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => {
                        const blob = new Blob([`Invoice: ${inv.invoice_number}\nPlan: ${inv.plan_name}\nAmount: $${inv.amount}\nDate: ${inv.paid_at}`], { type: 'text/plain' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `Invoice-${inv.invoice_number}.txt`;
                        a.click();
                      }}
                      className="p-1 hover:text-blue-400 text-slate-400 cursor-pointer"
                      title={t.downloadReceipt}
                    >
                      <Download className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Multi-Gateway Checkout Modal */}
      {selectedPlanForUpgrade && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg p-6 space-y-5 shadow-2xl animate-in fade-in zoom-in-95 duration-150 text-xs">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-slate-100">{t.upgradePlan}: {selectedPlanForUpgrade.name}</h3>
              <button
                onClick={() => setSelectedPlanForUpgrade(null)}
                className="text-slate-400 hover:text-slate-200 cursor-pointer"
              >
                ✕
              </button>
            </div>

            {/* Select Gateway */}
            <div className="space-y-2">
              <label className="text-[11px] font-semibold text-slate-400 uppercase">{t.paymentGateway}</label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => setSelectedGateway('stripe')}
                  className={`p-3 rounded-xl border text-center transition-all cursor-pointer ${
                    selectedGateway === 'stripe'
                      ? 'bg-blue-600/20 border-blue-500 text-blue-300 font-bold'
                      : 'bg-slate-950 border-slate-800 text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  <CreditCard className="w-5 h-5 mx-auto mb-1 text-blue-400" />
                  <div className="text-xs">Stripe</div>
                  <div className="text-[9px] text-slate-500">Cards / Global</div>
                </button>

                <button
                  type="button"
                  onClick={() => setSelectedGateway('payme')}
                  className={`p-3 rounded-xl border text-center transition-all cursor-pointer ${
                    selectedGateway === 'payme'
                      ? 'bg-emerald-600/20 border-emerald-500 text-emerald-300 font-bold'
                      : 'bg-slate-950 border-slate-800 text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  <DollarSign className="w-5 h-5 mx-auto mb-1 text-emerald-400" />
                  <div className="text-xs">Payme</div>
                  <div className="text-[9px] text-slate-500">Uzbekistan (UZS)</div>
                </button>

                <button
                  type="button"
                  onClick={() => setSelectedGateway('click')}
                  className={`p-3 rounded-xl border text-center transition-all cursor-pointer ${
                    selectedGateway === 'click'
                      ? 'bg-purple-600/20 border-purple-500 text-purple-300 font-bold'
                      : 'bg-slate-950 border-slate-800 text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  <Zap className="w-5 h-5 mx-auto mb-1 text-purple-400" />
                  <div className="text-xs">Click</div>
                  <div className="text-[9px] text-slate-500">Merchant Pay</div>
                </button>
              </div>
            </div>

            {/* Promotional Coupon Applicator */}
            <form onSubmit={handleApplyCoupon} className="space-y-1">
              <label className="text-[11px] font-semibold text-slate-400 uppercase">{t.promoCode}</label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="Enter code..."
                  value={couponCode}
                  onChange={(e) => setCouponCode(e.target.value)}
                  className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 uppercase font-mono"
                />
                <button
                  type="submit"
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-medium cursor-pointer"
                >
                  {t.applyPromo}
                </button>
              </div>
              {appliedDiscount && (
                <div className="text-emerald-400 text-[11px] pt-1">
                  ✓ {appliedDiscount}% coupon discount applied!
                </div>
              )}
              {couponError && (
                <div className="text-rose-400 text-[11px] pt-1">{couponError}</div>
              )}
            </form>

            {/* Total Price Calculation */}
            <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 space-y-1 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Base Plan ({billingCycle}):</span>
                <span className="font-mono text-slate-200">
                  ${billingCycle === 'yearly' ? selectedPlanForUpgrade.yearly_price : selectedPlanForUpgrade.monthly_price}
                </span>
              </div>
              {appliedDiscount && (
                <div className="flex justify-between text-emerald-400">
                  <span>Coupon Discount ({appliedDiscount}%):</span>
                  <span className="font-mono">
                    -${((billingCycle === 'yearly' ? selectedPlanForUpgrade.yearly_price : selectedPlanForUpgrade.monthly_price) * (appliedDiscount / 100)).toFixed(2)}
                  </span>
                </div>
              )}
              <div className="flex justify-between font-bold text-slate-100 pt-1 border-t border-slate-800 text-sm">
                <span>Total:</span>
                <span className="font-mono text-blue-400">
                  ${(
                    (billingCycle === 'yearly' ? selectedPlanForUpgrade.yearly_price : selectedPlanForUpgrade.monthly_price) *
                    (1 - (appliedDiscount ? appliedDiscount / 100 : 0))
                  ).toFixed(2)} USD
                </span>
              </div>
            </div>

            {/* Actions */}
            <div className="flex space-x-2 pt-2 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setSelectedPlanForUpgrade(null)}
                className="flex-1 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-medium cursor-pointer"
              >
                {t.cancel}
              </button>
              <button
                type="button"
                onClick={handleCheckout}
                disabled={isProcessing}
                className="flex-1 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl font-semibold shadow-sm transition-all flex items-center justify-center space-x-1.5 cursor-pointer"
              >
                <span>{isProcessing ? 'Processing Transaction...' : `${t.payViaGateway} ${selectedGateway.toUpperCase()}`}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

