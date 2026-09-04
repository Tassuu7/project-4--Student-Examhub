import React from 'react';
import { ShieldAlert, ArrowLeft } from 'lucide-react';
import { useAuth } from '@/src/contexts/AuthContext.tsx';

export const UnauthorizedPage: React.FC<{ onBack?: () => void }> = ({ onBack }) => {
  const { user, logout } = useAuth();

  return (
    <div id="unauthorized-page" className="min-h-screen bg-stone-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white p-8 rounded-xl shadow-sm border border-stone-200 text-center">
        <div className="w-12 h-12 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <ShieldAlert className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-stone-900 mb-2">Access Restricted</h2>
        <p className="text-sm text-stone-600 mb-6">
          Your role (<span className="font-semibold uppercase text-stone-800">{user?.role}</span>) does not have sufficient permissions to view this resource.
        </p>
        <div className="flex gap-3 justify-center">
          {onBack && (
            <button
              id="unauthorized-back-btn"
              onClick={onBack}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-stone-700 bg-stone-100 hover:bg-stone-200 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Go Back</span>
            </button>
          )}
          <button
            id="unauthorized-logout-btn"
            onClick={logout}
            className="px-4 py-2 text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 rounded-lg transition-colors"
          >
            Sign In with Different Account
          </button>
        </div>
      </div>
    </div>
  );
};
