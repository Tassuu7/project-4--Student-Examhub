/**
 * ExamHub - Main Application Entrypoint
 * Unifies Auth, Role-based Dashboards, Examination Engine, Question Bank, and Live Proctoring.
 */

import React, { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ToastProvider, useToast } from './contexts/ToastContext';
import { LoginPage } from './pages/auth/LoginPage';
import { ExamList } from './components/exams/ExamList';
import { ExamFormModal } from './components/exams/ExamFormModal';
import { ExamAutoGenerateModal } from './components/exams/ExamAutoGenerateModal';
import { ExamResultsModal } from './components/exams/ExamResultsModal';
import { StudentExamPortal } from './components/exams/StudentExamPortal';
import { ExamTakingInterface } from './components/exams/ExamTakingInterface';
import { ExamResultScorecard } from './components/exams/ExamResultScorecard';
import { QuestionList } from './components/questions/QuestionList';
import { SubjectListModal } from './components/subjects/SubjectListModal';
import { AnalyticsDashboard } from './components/analytics/AnalyticsDashboard';
import { LiveProctoringDashboard } from './components/proctoring/LiveProctoringDashboard';
import { StudentCertificatesTab } from './components/certificates/StudentCertificatesTab';
import { UnifiedSystemNavigation, ExamHubNavigationTab } from './components/navigation/UnifiedSystemNavigation';
import { PrincipalDashboard } from './components/principal/PrincipalDashboard';
import { TeacherStudentMonitoring } from './components/teacher/TeacherStudentMonitoring';
import { TeacherFeedbackView } from './components/teacher/TeacherFeedbackView';
import { StudentResultsList } from './components/student/StudentResultsList';
import { StudentFeedbackView } from './components/student/StudentFeedbackView';
import { ThemeToggle } from './components/common/ThemeToggle';
import { Exam, ExamResult } from './types/exam';
import { examService } from './services/examService';
import { LoadingSpinner } from './components/common/LoadingSpinner';
import {
  GraduationCap,
  BookOpen,
  CalendarCheck,
  Layers,
  LogOut,
  User,
  ShieldCheck,
  Award,
  Sparkles,
  ArrowRightLeft,
  TrendingUp,
  ShieldAlert,
  Search,
} from 'lucide-react';

function ExamHubContent() {
  const { user, isAuthenticated, isLoading, logout, login } = useAuth();
  const { showToast } = useToast();

  // Navigation tabs for Teacher/Admin/Student
  const [activeTab, setActiveTab] = useState<ExamHubNavigationTab>('exams');

  // Ensure role has an appropriate initial tab
  React.useEffect(() => {
    if (user?.role === 'admin' && activeTab === 'exams') {
      setActiveTab('principal_dashboard');
    }
  }, [user?.role]);

  // Modal states for Teacher/Admin
  const [showExamCreateModal, setShowExamCreateModal] = useState(false);
  const [selectedExamForEdit, setSelectedExamForEdit] = useState<Exam | null>(null);
  const [showExamAutoModal, setShowExamAutoModal] = useState(false);
  const [selectedExamForResults, setSelectedExamForResults] = useState<Exam | null>(null);
  const [showSubjectModal, setShowSubjectModal] = useState(false);

  // Active student examination mode
  const [activeAttemptExamId, setActiveAttemptExamId] = useState<string | null>(null);

  // Active scorecard view mode
  const [activeScorecard, setActiveScorecard] = useState<ExamResult | null>(null);
  const [loadingScorecard, setLoadingScorecard] = useState(false);

  // Quick demo switch loading
  const [switchingRole, setSwitchingRole] = useState(false);

  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-stone-50 text-stone-600">
        <LoadingSpinner size="lg" />
        <p className="mt-4 text-xs font-semibold uppercase tracking-wider text-stone-400">
          Initializing ExamHub System...
        </p>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <LoginPage />;
  }

  // If a student is taking an exam in real-time, take over the screen
  if (activeAttemptExamId) {
    return (
      <ExamTakingInterface
        examId={activeAttemptExamId}
        onFinishExam={(result) => {
          setActiveAttemptExamId(null);
          setActiveScorecard(result);
        }}
        onExit={() => setActiveAttemptExamId(null)}
      />
    );
  }

  // If inspecting a detailed post-submission or teacher scorecard
  if (activeScorecard) {
    return (
      <div className="min-h-screen bg-stone-100 dark:bg-zinc-950 p-4 sm:p-8">
        <ExamResultScorecard
          result={activeScorecard}
          onBack={() => setActiveScorecard(null)}
        />
      </div>
    );
  }

  const handleStudentViewResult = async (attemptId: string) => {
    try {
      setLoadingScorecard(true);
      const res = await examService.getAttemptResult(attemptId);
      setActiveScorecard(res);
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to load scorecard', 'error');
    } finally {
      setLoadingScorecard(false);
    }
  };

  const handleDemoSwitch = async (username: string) => {
    try {
      setSwitchingRole(true);
      await login(username, 'password123');
      // Reset view state
      setActiveScorecard(null);
      setActiveAttemptExamId(null);
      setSelectedExamForResults(null);
      if (username === 'principal_sharma' || username === 'admin') {
        setActiveTab('principal_dashboard');
      } else {
        setActiveTab('exams');
      }
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Switch failed', 'error');
    } finally {
      setSwitchingRole(false);
    }
  };

  const isStudent = user.role === 'student';
  const isTeacher = user.role === 'teacher';
  const isPrincipal = user.role === 'admin';
  const isStaff = isTeacher || isPrincipal;

  return (
    <div id="examhub-shell" className="min-h-screen bg-stone-100 dark:bg-zinc-950 flex flex-col font-sans">
      {/* Top Application Navigation Bar */}
      <header className="bg-white dark:bg-zinc-900 border-b border-stone-200 dark:border-zinc-800 sticky top-0 z-30 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo & Brand */}
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-amber-600 text-white flex items-center justify-center shadow-sm">
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div>
                  <span className="text-base font-extrabold tracking-tight text-stone-900 dark:text-stone-50">
                    ExamHub
                  </span>
                  <span className="hidden sm:inline-block ml-2 text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-stone-100 dark:bg-zinc-800 text-stone-600 dark:text-zinc-400">
                    Production System
                  </span>
                </div>
              </div>

              {/* Quick Subjects Action for Staff */}
              {isStaff && (
                <div className="hidden md:flex items-center gap-1 border-l border-stone-200 dark:border-zinc-800 pl-4">
                  <button
                    id="nav-tab-subjects"
                    onClick={() => setShowSubjectModal(true)}
                    className="px-3 py-1.5 text-xs font-semibold rounded-lg text-stone-600 dark:text-stone-400 hover:text-stone-900 hover:bg-stone-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1.5"
                  >
                    <Layers className="w-4 h-4 text-amber-600" />
                    Manage Subjects
                  </button>
                </div>
              )}
            </div>

            {/* Right Controls: Role Switcher & User Profile */}
            <div className="flex items-center gap-3">
              {/* Quick Persona Switcher for easy demo grading */}
              <div className="hidden lg:flex items-center gap-1.5 px-2 py-1 rounded-xl bg-stone-50 dark:bg-zinc-800/80 border border-stone-200 dark:border-zinc-700/60 text-xs">
                <span className="text-[10px] text-stone-400 font-bold uppercase tracking-wider flex items-center gap-1">
                  <ArrowRightLeft className="w-3 h-3" /> Demo:
                </span>
                <button
                  onClick={() => handleDemoSwitch('principal_sharma')}
                  disabled={switchingRole || user.username === 'principal_sharma' || (isPrincipal && user.username === 'admin')}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-colors ${
                    isPrincipal
                      ? 'bg-purple-600 text-white shadow-xs'
                      : 'text-stone-600 hover:bg-stone-200/60 dark:text-stone-300'
                  }`}
                >
                  Principal (Dr. Sharma)
                </button>
                <button
                  onClick={() => handleDemoSwitch('teacher_smith')}
                  disabled={switchingRole || user.username === 'teacher_smith'}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-colors ${
                    user.username === 'teacher_smith'
                      ? 'bg-amber-600 text-white shadow-xs'
                      : 'text-stone-600 hover:bg-stone-200/60 dark:text-stone-300'
                  }`}
                >
                  Teacher (Prof. Smith)
                </button>
                <button
                  onClick={() => handleDemoSwitch('student_alice')}
                  disabled={switchingRole || user.username === 'student_alice'}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-colors ${
                    user.username === 'student_alice'
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-stone-600 hover:bg-stone-200/60 dark:text-stone-300'
                  }`}
                >
                  Student (Alice)
                </button>
              </div>

              {/* User Avatar & Role */}
              <div className="flex items-center gap-2.5 pl-2 border-l border-stone-200 dark:border-zinc-800">
                <div className="w-8 h-8 rounded-full bg-stone-200 dark:bg-zinc-800 text-stone-700 dark:text-zinc-300 flex items-center justify-center font-bold text-xs">
                  {user.full_name?.charAt(0) || user.username.charAt(0).toUpperCase()}
                </div>
                <div className="hidden sm:block text-left">
                  <p className="text-xs font-bold text-stone-900 dark:text-stone-100 leading-tight">
                    {user.full_name}
                  </p>
                  <span
                    className={`inline-block text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.2 rounded ${
                      isPrincipal
                        ? 'bg-purple-100 text-purple-700 dark:bg-purple-950/50 dark:text-purple-300'
                        : isTeacher
                        ? 'bg-amber-100 text-amber-800 dark:bg-amber-950/50 dark:text-amber-300'
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-950/50 dark:text-blue-300'
                    }`}
                  >
                    {isPrincipal ? 'Principal' : isTeacher ? 'Teacher' : 'Student'}
                  </span>
                </div>
              </div>

              <ThemeToggle />

              <button
                id="btn-logout"
                onClick={() => logout()}
                className="p-2 text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 rounded-lg hover:bg-stone-100 dark:hover:bg-zinc-800 transition-colors"
                title="Sign out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Unified Enterprise Navigation Suite */}
      <UnifiedSystemNavigation
        currentTab={activeTab}
        onSelectTab={setActiveTab}
        userRole={user.role as 'admin' | 'teacher' | 'student'}
      />

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 1. STUDENT DASHBOARD */}
        {isStudent && (
          <div>
            {activeTab === 'exams' && (
              <StudentExamPortal
                onStartExam={(examId) => setActiveAttemptExamId(examId)}
                onViewResult={(attemptId) => handleStudentViewResult(attemptId)}
              />
            )}
            {activeTab === 'results' && (
              <StudentResultsList
                onViewScorecard={(result) => setActiveScorecard(result)}
              />
            )}
            {activeTab === 'feedback' && (
              <StudentFeedbackView />
            )}
            {activeTab === 'certificates' && (
              <StudentCertificatesTab />
            )}
          </div>
        )}

        {/* 2. PRINCIPAL DASHBOARD */}
        {isPrincipal && (
          <div>
            {activeTab === 'principal_dashboard' && (
              <PrincipalDashboard
                onNavigateToExams={() => setActiveTab('exams')}
                onNavigateToMonitoring={() => setActiveTab('student_monitoring')}
                onNavigateToCertificates={() => setActiveTab('certificates')}
              />
            )}
            {activeTab === 'exams' && (
              <ExamList
                onCreateClick={() => {
                  setSelectedExamForEdit(null);
                  setShowExamCreateModal(true);
                }}
                onAutoGenerateClick={() => setShowExamAutoModal(true)}
                onViewResults={(exam) => setSelectedExamForResults(exam)}
                onEditExam={(exam) => {
                  setSelectedExamForEdit(exam);
                  setShowExamCreateModal(true);
                }}
              />
            )}
            {activeTab === 'student_monitoring' && (
              <TeacherStudentMonitoring />
            )}
            {activeTab === 'feedback' && (
              <TeacherFeedbackView />
            )}
            {activeTab === 'analytics' && (
              <AnalyticsDashboard />
            )}
            {activeTab === 'certificates' && (
              <StudentCertificatesTab />
            )}
          </div>
        )}

        {/* 3. TEACHER DASHBOARD */}
        {isTeacher && (
          <div>
            {activeTab === 'exams' && (
              <ExamList
                onCreateClick={() => {
                  setSelectedExamForEdit(null);
                  setShowExamCreateModal(true);
                }}
                onAutoGenerateClick={() => setShowExamAutoModal(true)}
                onViewResults={(exam) => setSelectedExamForResults(exam)}
                onEditExam={(exam) => {
                  setSelectedExamForEdit(exam);
                  setShowExamCreateModal(true);
                }}
              />
            )}
            {activeTab === 'questions' && (
              <QuestionList userRole="teacher" />
            )}
            {activeTab === 'student_monitoring' && (
              <TeacherStudentMonitoring />
            )}
            {activeTab === 'feedback' && (
              <TeacherFeedbackView />
            )}
            {activeTab === 'proctoring' && (
              <LiveProctoringDashboard />
            )}
            {activeTab === 'certificates' && (
              <StudentCertificatesTab />
            )}
          </div>
        )}
      </main>

      {/* Teacher/Admin Modals */}
      {showExamCreateModal && (
        <ExamFormModal
          isOpen={showExamCreateModal}
          examToEdit={selectedExamForEdit}
          onClose={() => {
            setShowExamCreateModal(false);
            setSelectedExamForEdit(null);
          }}
          onSuccess={() => {
            setShowExamCreateModal(false);
            setSelectedExamForEdit(null);
            setActiveTab('exams');
          }}
        />
      )}

      {showExamAutoModal && (
        <ExamAutoGenerateModal
          isOpen={showExamAutoModal}
          onClose={() => setShowExamAutoModal(false)}
          onSuccess={() => {
            setShowExamAutoModal(false);
            setActiveTab('exams');
          }}
        />
      )}

      {selectedExamForResults && (
        <ExamResultsModal
          exam={selectedExamForResults}
          isOpen={Boolean(selectedExamForResults)}
          onClose={() => setSelectedExamForResults(null)}
          onViewScorecard={(result) => {
            setSelectedExamForResults(null);
            setActiveScorecard(result);
          }}
        />
      )}

      {showSubjectModal && (
        <SubjectListModal
          isOpen={showSubjectModal}
          onClose={() => setShowSubjectModal(false)}
          userRole={user.role as 'admin' | 'teacher'}
        />
      )}
    </div>
  );
}

export default function App() {
  return (
    <ToastProvider>
      <AuthProvider>
        <ExamHubContent />
      </AuthProvider>
    </ToastProvider>
  );
}
