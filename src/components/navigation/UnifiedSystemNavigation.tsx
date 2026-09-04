import React from 'react';
import {
  BookOpen,
  BrainCircuit,
  BarChart3,
  ShieldCheck,
  Award,
  Calendar,
  Layers,
  Fingerprint,
  Building2,
  FileSearch,
  Sigma,
  HelpCircle,
  FileText,
  Clock,
  Settings
} from 'lucide-react';

export type ExamHubNavigationTab =
  | 'exams'
  | 'questions'
  | 'adaptive_cat'
  | 'analytics'
  | 'proctoring'
  | 'certificates'
  | 'qti'
  | 'rubrics'
  | 'accreditation'
  | 'biometrics'
  | 'plagiarism'
  | 'scheduling'
  | 'curriculum'
  | 'reports'
  | 'tenancy'
  | 'student_review'
  | 'audit'
  | 'verify';

interface NavProps {
  currentTab: ExamHubNavigationTab;
  onSelectTab: (tab: ExamHubNavigationTab) => void;
  userRole: 'admin' | 'teacher' | 'student';
}

export const UnifiedSystemNavigation: React.FC<NavProps> = ({ currentTab, onSelectTab, userRole }) => {
  const adminTeacherTabs = [
    { id: 'exams', label: 'Examinations', icon: BookOpen },
    { id: 'questions', label: 'Item Studio', icon: FileText },
    { id: 'adaptive_cat', label: 'Adaptive CAT', icon: BrainCircuit },
    { id: 'analytics', label: 'Analytics Lab', icon: BarChart3 },
    { id: 'proctoring', label: 'Live Proctoring', icon: ShieldCheck },
    { id: 'certificates', label: 'Certificates', icon: Award },
    { id: 'qti', label: 'QTI Exchange', icon: Layers },
    { id: 'rubrics', label: 'Rubrics & Kappa', icon: Settings },
    { id: 'accreditation', label: 'Accreditation OBE', icon: Award },
    { id: 'biometrics', label: 'Biometrics Hub', icon: Fingerprint },
    { id: 'plagiarism', label: 'Collusion Auditor', icon: FileSearch },
    { id: 'scheduling', label: 'Timetable Grid', icon: Calendar },
    { id: 'curriculum', label: 'Curriculum Blueprint', icon: BookOpen },
    { id: 'reports', label: 'SIS Transcripts', icon: FileText },
    { id: 'tenancy', label: 'Tenant Admin', icon: Building2 },
    ...(userRole === 'admin' ? [{ id: 'audit', label: 'Audit Trail', icon: ShieldCheck }] : [])
  ];

  const studentTabs = [
    { id: 'exams', label: 'My Examinations', icon: BookOpen },
    { id: 'adaptive_cat', label: 'Adaptive Testing', icon: BrainCircuit },
    { id: 'student_review', label: 'Post-Exam Review', icon: FileText },
    { id: 'certificates', label: 'My Certificates', icon: Award },
    { id: 'verify', label: 'Verify Code', icon: FileSearch }
  ];

  const tabs = userRole === 'student' ? studentTabs : adminTeacherTabs;

  return (
    <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm px-4">
      <div className="flex space-x-1 overflow-x-auto py-2 scrollbar-none">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id as ExamHubNavigationTab)}
              className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 shadow-xs'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700/50'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-blue-600 dark:text-blue-400' : 'text-gray-400'}`} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
