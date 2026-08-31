import React from 'react';
import {
  Bell, Check, X, Trash2, CheckCircle2, AlertTriangle,
  GitPullRequest, CreditCard, MessageSquare
} from 'lucide-react';
import { NotificationItem } from '../types';

interface NotificationModalProps {
  notifications: NotificationItem[];
  onClose: () => void;
  onMarkAllRead: () => void;
  onClearAll: () => void;
}

export const NotificationModal: React.FC<NotificationModalProps> = ({
  notifications,
  onClose,
  onMarkAllRead,
  onClearAll,
}) => {
  const getIcon = (type: string) => {
    switch (type) {
      case 'TASK_ASSIGNED':
        return <CheckCircle2 className="w-4 h-4 text-blue-400" />;
      case 'CODE_REVIEW':
        return <GitPullRequest className="w-4 h-4 text-purple-400" />;
      case 'PAYMENT_SUCCESS':
        return <CreditCard className="w-4 h-4 text-emerald-400" />;
      default:
        return <Bell className="w-4 h-4 text-amber-400" />;
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-start justify-center sm:justify-end p-3 sm:p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden mt-12 sm:mt-12 animate-in fade-in slide-in-from-top-4 duration-150 text-xs">
        {/* Header */}
        <div className="p-3.5 sm:p-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bell className="w-4 h-4 text-blue-400" />
            <h3 className="font-bold text-slate-100">Notifications</h3>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={onMarkAllRead}
              className="text-[11px] text-blue-400 hover:text-blue-300 font-medium cursor-pointer"
            >
              Mark all read
            </button>
            <button
              onClick={onClose}
              className="p-1 text-slate-400 hover:text-slate-200 cursor-pointer"
              aria-label="Close"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Notifications List */}
        <div className="divide-y divide-slate-800 max-h-[60vh] sm:max-h-96 overflow-y-auto">
          {notifications.map((n) => (
            <div
              key={n.id}
              className={`p-3.5 sm:p-4 flex items-start space-x-3 transition-colors ${
                n.is_read ? 'bg-slate-900/60' : 'bg-slate-850/90'
              }`}
            >
              <div className="mt-0.5 shrink-0">{getIcon(n.notification_type)}</div>
              <div className="space-y-1 flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <h4 className="font-semibold text-slate-100 truncate">{n.title}</h4>
                  <span className="text-[10px] text-slate-500 whitespace-nowrap">{n.created_at}</span>
                </div>
                <p className="text-slate-300 text-[11px] leading-relaxed break-words">{n.message}</p>
              </div>
            </div>
          ))}

          {notifications.length === 0 && (
            <div className="p-8 text-center text-slate-500">
              No notifications right now.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
