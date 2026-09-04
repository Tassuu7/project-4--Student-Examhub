import React from 'react';
import {
  BookOpen,
  BarChart3,
  ShieldCheck,
  Award,
  FileText,
  Users,
  MessageSquare,
  LayoutDashboard,
  CheckCircle2
} from 'lucide-react';

export type ExamHubNavigationTab =
  | 'principal_dashboard'
  | 'exams'
  | 'questions'
  | 'student_monitoring'
  | 'feedback'
  | 'proctoring'
  | 'results'
  | 'certificates'
  | 'analytics';

interface NavProps {
  currentTab: ExamHubNavigationTab;
  onSelectTab: (tab: ExamHubNavigationTab) => void;
  userRole: 'admin' | 'teacher' | 'student';
}

export const UnifiedSystemNavigation: React.FC<NavProps> = ({ currentTab, onSelectTab, userRole }) => {
  // 1. Principal / Admin: Executive Overview, Exam Oversight, Student Monitoring, Feedback, Analytics, Certificates
  const principalTabs = [
    { id: 'principal_dashboard', label: 'Executive Overview', icon: LayoutDashboard },
    { id: 'exams', label: 'Examinations Oversight', icon: BookOpen },
    { id: 'student_monitoring', label: 'Student Performance', icon: Users },
    { id: 'feedback', label: 'Teacher Feedback', icon: MessageSquare },
    { id: 'analytics', label: 'Analytics Lab', icon: BarChart3 },
    { id: 'certificates', label: 'Certificates', icon: Award },
  ];

  // 2. Teacher: Examinations, Question Bank, Student Monitoring, Student Feedback, Live Proctoring, Certificates
  const teacherTabs = [
    { id: 'exams', label: 'Examinations', icon: BookOpen },
    { id: 'questions', label: 'Question Bank', icon: FileText },
    { id: 'student_monitoring', label: 'Student Monitoring', icon: Users },
    { id: 'feedback', label: 'Student Feedback', icon: MessageSquare },
    { id: 'proctoring', label: 'Live Proctoring', icon: ShieldCheck },
    { id: 'certificates', label: 'Certificates', icon: Award },
  ];

  // 3. Student: My Examinations, My Results, Teacher Feedback, My Certificates
  const studentTabs = [
    { id: 'exams', label: 'My Examinations', icon: BookOpen },
    { id: 'results', label: 'My Results', icon: CheckCircle2 },
    { id: 'feedback', label: 'Teacher Feedback', icon: MessageSquare },
    { id: 'certificates', label: 'My Certificates', icon: Award },
  ];

  const tabs =
    userRole === 'admin'
      ? principalTabs
      : userRole === 'teacher'
      ? teacherTabs
      : studentTabs;

  return (
    <nav className="bg-white dark:bg-zinc-900 border-b border-stone-200 dark:border-zinc-800 shadow-xs px-4">
      <div className="flex space-x-1 overflow-x-auto py-2 scrollbar-none max-w-7xl mx-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id as ExamHubNavigationTab)}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-400 shadow-xs border border-amber-200/60 dark:border-amber-900/40'
                  : 'text-stone-600 dark:text-zinc-400 hover:text-stone-900 dark:hover:text-zinc-100 hover:bg-stone-50 dark:hover:bg-zinc-800'
              }`}
            >
              <Icon
                className={`w-4 h-4 ${
                  isActive ? 'text-amber-600 dark:text-amber-400' : 'text-stone-400 dark:text-zinc-500'
                }`}
              />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
