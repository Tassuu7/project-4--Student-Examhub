/**
 * ExamHub - Teacher Student Monitoring & Performance Analytics
 * Enables instructors to monitor individual and class-level academic progress,
 * identify learning gaps, track difficulty metrics, and provide timely interventions.
 */

import React, { useState } from 'react';
import {
  Users,
  Search,
  TrendingUp,
  AlertTriangle,
  Award,
  CheckCircle2,
  Filter,
  BarChart3,
  MessageSquare,
  ChevronRight,
  BookOpen,
} from 'lucide-react';

interface StudentRosterItem {
  id: string;
  name: string;
  rollNumber: string;
  department: string;
  gradeLevel: string;
  examsAttempted: number;
  averageScore: number;
  highestScore: number;
  status: 'Honor Roll' | 'On Track' | 'Needs Support';
  recentSubject: string;
}

interface TeacherStudentMonitoringProps {
  onOpenFeedback?: (studentName: string, studentId: string) => void;
}

const SYNTHETIC_ROSTER: StudentRosterItem[] = [
  {
    id: 's1',
    name: 'Alice Walker',
    rollNumber: 'STU001',
    department: 'Computer Science',
    gradeLevel: 'Senior',
    examsAttempted: 3,
    averageScore: 89.8,
    highestScore: 92.0,
    status: 'Honor Roll',
    recentSubject: 'Data Structures & Algorithms',
  },
  {
    id: 's7',
    name: 'Grace Hopper',
    rollNumber: 'STU007',
    department: 'Computer Science',
    gradeLevel: 'Senior',
    examsAttempted: 2,
    averageScore: 95.0,
    highestScore: 100.0,
    status: 'Honor Roll',
    recentSubject: 'Data Structures & Algorithms',
  },
  {
    id: 's2',
    name: 'Bob Miller',
    rollNumber: 'STU002',
    department: 'Computer Science',
    gradeLevel: 'Junior',
    examsAttempted: 2,
    averageScore: 70.3,
    highestScore: 78.0,
    status: 'On Track',
    recentSubject: 'Data Structures & Algorithms',
  },
  {
    id: 's8',
    name: 'Henry Ford',
    rollNumber: 'STU008',
    department: 'Software Engineering',
    gradeLevel: 'Sophomore',
    examsAttempted: 2,
    averageScore: 68.8,
    highestScore: 72.0,
    status: 'On Track',
    recentSubject: 'Data Structures & Algorithms',
  },
  {
    id: 's4',
    name: 'David Kim',
    rollNumber: 'STU004',
    department: 'Software Engineering',
    gradeLevel: 'Sophomore',
    examsAttempted: 2,
    averageScore: 60.6,
    highestScore: 65.0,
    status: 'On Track',
    recentSubject: 'Data Structures & Algorithms',
  },
  {
    id: 's5',
    name: 'Eva Green',
    rollNumber: 'STU005',
    department: 'Computer Science',
    gradeLevel: 'Junior',
    examsAttempted: 2,
    averageScore: 49.4,
    highestScore: 55.0,
    status: 'Needs Support',
    recentSubject: 'Data Structures & Algorithms',
  },
  {
    id: 's6',
    name: 'Frank Wright',
    rollNumber: 'STU006',
    department: 'Computer Science',
    gradeLevel: 'Freshman',
    examsAttempted: 1,
    averageScore: 25.0,
    highestScore: 25.0,
    status: 'Needs Support',
    recentSubject: 'Data Structures & Algorithms',
  },
];

export const TeacherStudentMonitoring: React.FC<TeacherStudentMonitoringProps> = ({ onOpenFeedback }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');

  const filteredRoster = SYNTHETIC_ROSTER.filter((s) => {
    const matchesSearch =
      s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.rollNumber.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDept = departmentFilter === 'ALL' || s.department === departmentFilter;
    const matchesStatus = statusFilter === 'ALL' || s.status === statusFilter;
    return matchesSearch && matchesDept && matchesStatus;
  });

  const avgScore = (SYNTHETIC_ROSTER.reduce((acc, s) => acc + s.averageScore, 0) / SYNTHETIC_ROSTER.length).toFixed(1);
  const honorRollCount = SYNTHETIC_ROSTER.filter((s) => s.status === 'Honor Roll').length;
  const supportCount = SYNTHETIC_ROSTER.filter((s) => s.status === 'Needs Support').length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-stone-200 dark:border-zinc-800 pb-5">
        <div>
          <h2 className="text-xl font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <Users className="w-5 h-5 text-amber-600" />
            Student Performance Monitoring
          </h2>
          <p className="text-xs text-stone-500 dark:text-zinc-400 mt-1">
            Track student outcomes, monitor learning velocity, identify at-risk learners, and assign interventions.
          </p>
        </div>
      </div>

      {/* Summary Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>Enrolled Students</span>
            <Users className="w-4 h-4 text-amber-600" />
          </div>
          <p className="text-2xl font-bold text-stone-900 dark:text-stone-100 mt-2">
            {SYNTHETIC_ROSTER.length}
          </p>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 inline-block">
            100% active learners
          </span>
        </div>

        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>Cohort Average</span>
            <TrendingUp className="w-4 h-4 text-blue-600" />
          </div>
          <p className="text-2xl font-bold text-stone-900 dark:text-stone-100 mt-2">
            {avgScore}%
          </p>
          <span className="text-[11px] text-stone-400 mt-1 inline-block">
            Benchmark: 70.0% target
          </span>
        </div>

        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>Honor Roll (&ge;85%)</span>
            <Award className="w-4 h-4 text-emerald-600" />
          </div>
          <p className="text-2xl font-bold text-emerald-600 mt-2">
            {honorRollCount} Students
          </p>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 inline-block">
            Top academic tier
          </span>
        </div>

        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>Intervention Needed</span>
            <AlertTriangle className="w-4 h-4 text-rose-600" />
          </div>
          <p className="text-2xl font-bold text-rose-600 mt-2">
            {supportCount} Students
          </p>
          <span className="text-[11px] text-rose-600 font-semibold mt-1 inline-block">
            Requires tutorial session
          </span>
        </div>
      </div>

      {/* Curriculum Topic Mastery & Difficulty Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="p-5 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2 mb-4">
            <BarChart3 className="w-4 h-4 text-amber-600" />
            Subject & Topic Mastery Breakdown
          </h3>
          <div className="space-y-3.5">
            <div>
              <div className="flex justify-between text-xs font-semibold text-stone-700 dark:text-zinc-300 mb-1">
                <span>Python Syntax & Procedural Logic</span>
                <span className="text-emerald-600">88.5% Mastery</span>
              </div>
              <div className="w-full h-2 bg-stone-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full" style={{ width: '88.5%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-stone-700 dark:text-zinc-300 mb-1">
                <span>Linear Data Structures (Arrays & Lists)</span>
                <span className="text-emerald-600">82.0% Mastery</span>
              </div>
              <div className="w-full h-2 bg-stone-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full" style={{ width: '82%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-stone-700 dark:text-zinc-300 mb-1">
                <span>SQL Queries & Database Normalization</span>
                <span className="text-blue-600">76.4% Mastery</span>
              </div>
              <div className="w-full h-2 bg-stone-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 rounded-full" style={{ width: '76.4%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-stone-700 dark:text-zinc-300 mb-1">
                <span>Trees, Graphs & Recursive Analysis</span>
                <span className="text-amber-600">58.2% (Revision Required)</span>
              </div>
              <div className="w-full h-2 bg-stone-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 rounded-full" style={{ width: '58.2%' }}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="p-5 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2 mb-4">
            <TrendingUp className="w-4 h-4 text-blue-600" />
            Assessment Question Difficulty Accuracy
          </h3>
          <div className="grid grid-cols-3 gap-3">
            <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/50 text-center">
              <span className="text-xs font-bold text-emerald-700 dark:text-emerald-300 uppercase tracking-wider block">
                Easy Questions
              </span>
              <p className="text-2xl font-extrabold text-emerald-600 mt-2">92.4%</p>
              <span className="text-[10px] text-emerald-700/80 mt-1 block">Class Accuracy</span>
            </div>

            <div className="p-4 rounded-xl bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800/50 text-center">
              <span className="text-xs font-bold text-blue-700 dark:text-blue-300 uppercase tracking-wider block">
                Medium Questions
              </span>
              <p className="text-2xl font-extrabold text-blue-600 mt-2">73.8%</p>
              <span className="text-[10px] text-blue-700/80 mt-1 block">Class Accuracy</span>
            </div>

            <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/50 text-center">
              <span className="text-xs font-bold text-amber-700 dark:text-amber-300 uppercase tracking-wider block">
                Hard Questions
              </span>
              <p className="text-2xl font-extrabold text-amber-600 mt-2">52.1%</p>
              <span className="text-[10px] text-amber-700/80 mt-1 block">Class Accuracy</span>
            </div>
          </div>

          <div className="mt-4 p-3 rounded-lg bg-stone-50 dark:bg-zinc-800/60 border border-stone-200 dark:border-zinc-700/60 text-xs text-stone-600 dark:text-zinc-400">
            <strong className="text-stone-900 dark:text-stone-200 font-semibold block mb-0.5">
              Instructional Insight:
            </strong>
            Students demonstrate exceptional proficiency with Easy & Medium items. Recommend scheduling a 30-minute review session focused on Hard graph search algorithms.
          </div>
        </div>
      </div>

      {/* Roster Filters & Search */}
      <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-stone-400" />
          <input
            type="text"
            placeholder="Search student by name or roll number..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-stone-200 dark:border-zinc-700 bg-stone-50 dark:bg-zinc-800 text-stone-900 dark:text-stone-100 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <select
            value={departmentFilter}
            onChange={(e) => setDepartmentFilter(e.target.value)}
            className="text-xs border border-stone-200 dark:border-zinc-700 bg-stone-50 dark:bg-zinc-800 text-stone-700 dark:text-zinc-300 rounded-lg px-2.5 py-2"
          >
            <option value="ALL">All Departments</option>
            <option value="Computer Science">Computer Science</option>
            <option value="Software Engineering">Software Engineering</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="text-xs border border-stone-200 dark:border-zinc-700 bg-stone-50 dark:bg-zinc-800 text-stone-700 dark:text-zinc-300 rounded-lg px-2.5 py-2"
          >
            <option value="ALL">All Academic Statuses</option>
            <option value="Honor Roll">Honor Roll</option>
            <option value="On Track">On Track</option>
            <option value="Needs Support">Needs Support</option>
          </select>
        </div>
      </div>

      {/* Student Roster Table */}
      <div className="rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-stone-200 dark:border-zinc-800 bg-stone-50/75 dark:bg-zinc-800/50 text-stone-500 dark:text-zinc-400 font-semibold uppercase tracking-wider">
                <th className="py-3 px-4">Student</th>
                <th className="py-3 px-4">Roll Number</th>
                <th className="py-3 px-4">Department</th>
                <th className="py-3 px-4">Exams Taken</th>
                <th className="py-3 px-4">Average Score</th>
                <th className="py-3 px-4">Highest Score</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100 dark:divide-zinc-800/60">
              {filteredRoster.map((s) => (
                <tr key={s.id} className="hover:bg-stone-50/50 dark:hover:bg-zinc-800/30 transition-colors">
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2.5">
                      <div className="w-7 h-7 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 flex items-center justify-center font-bold text-xs">
                        {s.name.charAt(0)}
                      </div>
                      <div>
                        <span className="font-semibold text-stone-900 dark:text-stone-100 block">
                          {s.name}
                        </span>
                        <span className="text-[10px] text-stone-400">{s.gradeLevel}</span>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-4 font-mono font-semibold text-stone-600 dark:text-zinc-300">
                    {s.rollNumber}
                  </td>
                  <td className="py-3 px-4 text-stone-600 dark:text-zinc-300">
                    {s.department}
                  </td>
                  <td className="py-3 px-4 text-stone-700 dark:text-zinc-200 font-semibold">
                    {s.examsAttempted}
                  </td>
                  <td className="py-3 px-4 font-bold text-stone-900 dark:text-stone-100">
                    {s.averageScore}%
                  </td>
                  <td className="py-3 px-4 font-bold text-emerald-600">
                    {s.highestScore}%
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                        s.status === 'Honor Roll'
                          ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300'
                          : s.status === 'On Track'
                          ? 'bg-blue-100 text-blue-800 dark:bg-blue-950/50 dark:text-blue-300'
                          : 'bg-rose-100 text-rose-800 dark:bg-rose-950/50 dark:text-rose-300'
                      }`}
                    >
                      {s.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => onOpenFeedback && onOpenFeedback(s.name, s.id)}
                      className="px-2.5 py-1 text-[11px] font-semibold rounded-lg bg-stone-100 hover:bg-stone-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 text-stone-700 dark:text-zinc-200 transition-colors inline-flex items-center gap-1"
                    >
                      <MessageSquare className="w-3 h-3 text-amber-600" />
                      Feedback
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
