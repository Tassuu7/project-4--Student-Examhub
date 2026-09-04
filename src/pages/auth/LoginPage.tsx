import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { ShieldCheck, GraduationCap, BookOpen, KeyRound, User, ArrowRight } from 'lucide-react';
import { LoadingSpinner } from '../../components/common/LoadingSpinner';

interface LoginPageProps {
  onLoginSuccess?: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  const { login } = useAuth();
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!usernameOrEmail.trim() || !password.trim()) {
      setError('Please enter both your identifier and password.');
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await login(usernameOrEmail.trim(), password);
      if (onLoginSuccess) {
        onLoginSuccess();
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Invalid credentials. Please verify your login details.');
    } finally {
      setSubmitting(false);
    }
  };

  const setDemoCredentials = (u: string, p: string) => {
    setUsernameOrEmail(u);
    setPassword(p);
    setError(null);
  };

  return (
    <div id="login-container" className="min-h-screen bg-stone-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-amber-600 rounded-xl flex items-center justify-center text-white shadow-md">
            <GraduationCap className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-stone-900 tracking-tight">ExamHub</h1>
            <p className="text-xs uppercase tracking-wider text-stone-700 font-semibold">Production Examination System</p>
          </div>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <div id="login-card" className="bg-white py-8 px-6 shadow-sm border border-stone-200 rounded-xl sm:px-10">
          <h2 className="text-lg font-semibold text-stone-800 mb-6">Sign In to Your Account</h2>

          {error && (
            <div id="login-error-alert" className="mb-5 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="username-input" className="block text-xs font-semibold text-stone-700 uppercase tracking-wider mb-1.5">
                Username or Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-stone-400">
                  <User className="w-4 h-4" />
                </div>
                <input
                  id="username-input"
                  type="text"
                  required
                  value={usernameOrEmail}
                  onChange={(e) => setUsernameOrEmail(e.target.value)}
                  placeholder="e.g. principal_sharma, teacher_smith, student_alice"
                  className="block w-full pl-10 pr-3 py-2.5 bg-stone-50 border border-stone-300 rounded-lg text-sm text-stone-900 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:bg-white transition-colors"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password-input" className="block text-xs font-semibold text-stone-700 uppercase tracking-wider mb-1.5">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-stone-400">
                  <KeyRound className="w-4 h-4" />
                </div>
                <input
                  id="password-input"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="block w-full pl-10 pr-3 py-2.5 bg-stone-50 border border-stone-300 rounded-lg text-sm text-stone-900 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:bg-white transition-colors"
                />
              </div>
            </div>

            <button
              id="login-submit-button"
              type="submit"
              disabled={submitting}
              className="w-full mt-2 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-medium text-sm shadow-sm transition-colors disabled:opacity-50"
            >
              {submitting ? (
                <LoadingSpinner size="sm" />
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="mt-8 pt-6 border-t border-stone-200">
            <p className="text-xs font-semibold uppercase tracking-wider text-stone-500 mb-3 text-center">
              Quick Synthetic Demo Accounts
            </p>
            <div className="grid grid-cols-3 gap-2">
              <button
                id="demo-principal-button"
                type="button"
                onClick={() => setDemoCredentials('principal_sharma', 'password123')}
                className="p-2.5 text-left rounded-lg border border-stone-200 hover:border-stone-400 bg-stone-50 hover:bg-stone-100 transition-colors"
              >
                <div className="flex items-center gap-1.5 text-xs font-semibold text-stone-800">
                  <ShieldCheck className="w-3.5 h-3.5 text-purple-600" />
                  <span>Principal</span>
                </div>
                <p className="text-[11px] text-stone-500 mt-0.5">Dr. Sharma</p>
              </button>

              <button
                id="demo-teacher-button"
                type="button"
                onClick={() => setDemoCredentials('teacher_smith', 'password123')}
                className="p-2.5 text-left rounded-lg border border-stone-200 hover:border-stone-400 bg-stone-50 hover:bg-stone-100 transition-colors"
              >
                <div className="flex items-center gap-1.5 text-xs font-semibold text-stone-800">
                  <BookOpen className="w-3.5 h-3.5 text-amber-600" />
                  <span>Teacher</span>
                </div>
                <p className="text-[11px] text-stone-500 mt-0.5">Prof. Smith</p>
              </button>

              <button
                id="demo-student-button"
                type="button"
                onClick={() => setDemoCredentials('student_alice', 'password123')}
                className="p-2.5 text-left rounded-lg border border-stone-200 hover:border-stone-400 bg-stone-50 hover:bg-stone-100 transition-colors"
              >
                <div className="flex items-center gap-1.5 text-xs font-semibold text-stone-800">
                  <GraduationCap className="w-3.5 h-3.5 text-blue-600" />
                  <span>Student</span>
                </div>
                <p className="text-[11px] text-stone-500 mt-0.5">Alice (STU001)</p>
              </button>
            </div>
            <p className="text-[11px] text-stone-400 text-center mt-3">
              Password for all demo accounts: <span className="font-mono text-stone-600">password123</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
