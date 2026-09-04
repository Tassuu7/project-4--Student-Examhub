/**
 * ExamHub - Principal's Executive Dashboard
 * Provides institutional oversight of exams, faculty, academic pass rates,
 * student honor rolls, intervention watchlists, and credential issuance.
 */

import React, { useState } from 'react';
import {
  Building2,
  Users,
  GraduationCap,
  Award,
  TrendingUp,
  AlertTriangle,
  BookOpen,
  CalendarCheck,
  ShieldCheck,
  CheckCircle2,
  FileText,
  Search,
  ChevronRight,
  Sparkles,
} from 'lucide-react';

interface PrincipalDashboardProps {
  onNavigateToExams?: () => void;
  onNavigateToMonitoring?: () => void;
  onNavigateToCertificates?: () => void;
}

export const PrincipalDashboard: React.FC<PrincipalDashboardProps> = ({
  onNavigateToExams,
  onNavigateToMonitoring,
  onNavigateToCertificates,
}) => {
  const [selectedDept, setSelectedDept] = useState('ALL');

  return (
    <div className="space-y-6">
      {/* Principal Welcome Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-stone-900 via-stone-800 to-stone-900 text-white shadow-md border border-stone-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 border border-amber-500/30">
              Institutional Executive Portal
            </span>
            <span className="text-xs text-stone-400">Academic Term 2026-Q3</span>
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight">
            Welcome, Dr. Ramesh Sharma
          </h1>
          <p className="text-xs text-stone-300 max-w-2xl mt-1">
            Institutional console for curriculum monitoring, faculty test oversight, school-wide pass rates, and academic certifications.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-white/10 backdrop-blur-xs text-center border border-white/10">
            <span className="text-[10px] uppercase font-bold text-stone-300 block">Accreditation</span>
            <span className="text-sm font-extrabold text-amber-400 flex items-center gap-1 justify-center">
              <ShieldCheck className="w-3.5 h-3.5" /> Grade A+
            </span>
          </div>
          <div className="p-3 rounded-xl bg-white/10 backdrop-blur-xs text-center border border-white/10">
            <span className="text-[10px] uppercase font-bold text-stone-300 block">Active Term</span>
            <span className="text-sm font-extrabold text-white">Fall 2026</span>
          </div>
        </div>
      </div>

      {/* Institutional KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>Enrolled Students</span>
            <GraduationCap className="w-4 h-4 text-blue-600" />
          </div>
          <p className="text-2xl font-extrabold text-stone-900 dark:text-stone-100 mt-2">
            7
          </p>
          <span className="text-[10px] text-emerald-600 font-semibold mt-1 inline-block">
            100% active cohort
          </span>
        </div>

        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>Teaching Faculty</span>
            <Users className="w-4 h-4 text-amber-600" />
          </div>
          <p className="text-2xl font-extrabold text-stone-900 dark:text-stone-100 mt-2">
            3
          </p>
          <span className="text-[10px] text-stone-400 mt-1 inline-block">
            CS, DS & SE Depts
          </span>
        </div>

        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>Examinations Held</span>
            <CalendarCheck className="w-4 h-4 text-purple-600" />
          </div>
          <p className="text-2xl font-extrabold text-stone-900 dark:text-stone-100 mt-2">
            3
          </p>
          <span className="text-[10px] text-purple-600 font-semibold mt-1 inline-block">
            21 Question Bank Items
          </span>
        </div>

        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>School Pass Rate</span>
            <TrendingUp className="w-4 h-4 text-emerald-600" />
          </div>
          <p className="text-2xl font-extrabold text-emerald-600 mt-2">
            85.7%
          </p>
          <span className="text-[10px] text-emerald-600 font-semibold mt-1 inline-block">
            Exceeds 75% target
          </span>
        </div>

        <div className="p-4 rounded-xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
          <div className="flex items-center justify-between text-xs text-stone-500 dark:text-zinc-400">
            <span>Certificates Issued</span>
            <Award className="w-4 h-4 text-amber-500" />
          </div>
          <p className="text-2xl font-extrabold text-amber-500 mt-2">
            2
          </p>
          <span className="text-[10px] text-stone-400 mt-1 inline-block">
            Verified Credentials
          </span>
        </div>
      </div>

      {/* Main Grid: Departmental Breakdown & Academic Watchlists */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Department Progress & Examination Oversight */}
        <div className="lg:col-span-2 space-y-6">
          {/* Department Breakdown */}
          <div className="p-5 rounded-2xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2">
                <Building2 className="w-4 h-4 text-amber-600" />
                Department Academic Performance
              </h3>
              <span className="text-xs text-stone-400">Term Aggregate</span>
            </div>

            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-stone-800 dark:text-stone-200">
                    Computer Science & Engineering (Prof. Robert Smith)
                  </span>
                  <span className="text-emerald-600 font-bold">88.5% Pass Rate</span>
                </div>
                <div className="w-full h-2.5 bg-stone-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: '88.5%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] text-stone-400 mt-1">
                  <span>Enrolled: 5 Students &bull; 2 Active Exams</span>
                  <span>Average GPA: 3.6 / 4.0</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-stone-800 dark:text-stone-200">
                    Software Engineering (Prof. Rajesh Patel)
                  </span>
                  <span className="text-blue-600 font-bold">82.0% Pass Rate</span>
                </div>
                <div className="w-full h-2.5 bg-stone-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: '82%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] text-stone-400 mt-1">
                  <span>Enrolled: 2 Students &bull; 1 Scheduled Exam</span>
                  <span>Average GPA: 3.3 / 4.0</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-stone-800 dark:text-stone-200">
                    Data Science & Analytics (Dr. Angela Chen)
                  </span>
                  <span className="text-purple-600 font-bold">78.0% Pass Rate</span>
                </div>
                <div className="w-full h-2.5 bg-stone-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                  <div className="h-full bg-purple-500 rounded-full" style={{ width: '78%' }}></div>
                </div>
                <div className="flex justify-between text-[10px] text-stone-400 mt-1">
                  <span>Enrolled: 3 Students &bull; 1 Scheduled Exam</span>
                  <span>Average GPA: 3.1 / 4.0</span>
                </div>
              </div>
            </div>
          </div>

          {/* Active Examination Oversight Table */}
          <div className="p-5 rounded-2xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2">
                <CalendarCheck className="w-4 h-4 text-purple-600" />
                Examinations Oversight
              </h3>
              {onNavigateToExams && (
                <button
                  onClick={onNavigateToExams}
                  className="text-xs text-amber-600 hover:text-amber-700 font-semibold flex items-center gap-1"
                >
                  Manage All Tests <ChevronRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>

            <div className="space-y-3">
              <div className="p-3.5 rounded-xl border border-stone-100 dark:border-zinc-800/80 bg-stone-50/50 dark:bg-zinc-800/30 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300">
                      Completed
                    </span>
                    <strong className="text-xs font-bold text-stone-900 dark:text-stone-100">
                      Data Structures Fundamentals Quiz
                    </strong>
                  </div>
                  <p className="text-[11px] text-stone-500 mt-1">
                    CS201 &bull; Prof. Robert Smith &bull; 7 Submissions Evaluated &bull; Average Score: 68.8%
                  </p>
                </div>
                <span className="text-xs font-bold text-emerald-600">85.7% Pass</span>
              </div>

              <div className="p-3.5 rounded-xl border border-stone-100 dark:border-zinc-800/80 bg-stone-50/50 dark:bg-zinc-800/30 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800 dark:bg-amber-950/50 dark:text-amber-300">
                      Active Now
                    </span>
                    <strong className="text-xs font-bold text-stone-900 dark:text-stone-100">
                      Python Programming Midterm Assessment
                    </strong>
                  </div>
                  <p className="text-[11px] text-stone-500 mt-1">
                    CS101 &bull; Prof. Robert Smith &bull; 30 Mins Duration &bull; 8 Questions
                  </p>
                </div>
                <span className="text-xs font-bold text-amber-600">Taking Window Open</span>
              </div>

              <div className="p-3.5 rounded-xl border border-stone-100 dark:border-zinc-800/80 bg-stone-50/50 dark:bg-zinc-800/30 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800 dark:bg-blue-950/50 dark:text-blue-300">
                      Scheduled
                    </span>
                    <strong className="text-xs font-bold text-stone-900 dark:text-stone-100">
                      DBMS & SQL Proficiency Examination
                    </strong>
                  </div>
                  <p className="text-[11px] text-stone-500 mt-1">
                    DS202 &bull; Prof. Robert Smith &bull; 45 Mins Duration &bull; 4 Questions
                  </p>
                </div>
                <span className="text-xs font-bold text-blue-600">Opens Tomorrow</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Col: Honor Roll & Academic Intervention Watchlist */}
        <div className="space-y-6">
          {/* Honor Roll */}
          <div className="p-5 rounded-2xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2">
                <Award className="w-4 h-4 text-amber-500" />
                Honor Roll (Top Achievers)
              </h3>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-50 text-amber-800 dark:bg-amber-950/40 dark:text-amber-300">
                GPA &ge; 3.8
              </span>
            </div>

            <div className="space-y-3">
              <div className="p-3 rounded-xl border border-stone-100 dark:border-zinc-800 bg-stone-50/50 dark:bg-zinc-800/40 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 flex items-center justify-center font-bold text-xs">
                    G
                  </div>
                  <div>
                    <strong className="text-xs font-bold text-stone-900 dark:text-stone-100 block">
                      Grace Hopper
                    </strong>
                    <span className="text-[10px] text-stone-400">STU007 &bull; Computer Science</span>
                  </div>
                </div>
                <span className="text-xs font-extrabold text-emerald-600">100.0%</span>
              </div>

              <div className="p-3 rounded-xl border border-stone-100 dark:border-zinc-800 bg-stone-50/50 dark:bg-zinc-800/40 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 flex items-center justify-center font-bold text-xs">
                    A
                  </div>
                  <div>
                    <strong className="text-xs font-bold text-stone-900 dark:text-stone-100 block">
                      Alice Walker
                    </strong>
                    <span className="text-[10px] text-stone-400">STU001 &bull; Computer Science</span>
                  </div>
                </div>
                <span className="text-xs font-extrabold text-emerald-600">87.5%</span>
              </div>

              <div className="p-3 rounded-xl border border-stone-100 dark:border-zinc-800 bg-stone-50/50 dark:bg-zinc-800/40 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-800 dark:bg-blue-950/60 dark:text-blue-300 flex items-center justify-center font-bold text-xs">
                    H
                  </div>
                  <div>
                    <strong className="text-xs font-bold text-stone-900 dark:text-stone-100 block">
                      Henry Ford
                    </strong>
                    <span className="text-[10px] text-stone-400">STU008 &bull; Software Engineering</span>
                  </div>
                </div>
                <span className="text-xs font-extrabold text-blue-600">68.8%</span>
              </div>
            </div>
          </div>

          {/* Academic Intervention Needed */}
          <div className="p-5 rounded-2xl border border-rose-200 dark:border-rose-900/50 bg-rose-50/30 dark:bg-rose-950/20 shadow-xs">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-rose-900 dark:text-rose-200 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-rose-600" />
                Intervention Watchlist
              </h3>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-100 text-rose-800 dark:bg-rose-900/50 dark:text-rose-300">
                Action Required
              </span>
            </div>

            <div className="p-3.5 rounded-xl bg-white dark:bg-zinc-900 border border-rose-200 dark:border-rose-800/60 space-y-2">
              <div className="flex items-center justify-between">
                <div>
                  <strong className="text-xs font-bold text-stone-900 dark:text-stone-100 block">
                    Frank Wright (STU006)
                  </strong>
                  <span className="text-[10px] text-stone-400">Freshman &bull; Computer Science</span>
                </div>
                <span className="text-xs font-extrabold text-rose-600">25.0% (Grade F)</span>
              </div>
              <p className="text-[11px] text-stone-600 dark:text-zinc-400 bg-rose-50/50 dark:bg-rose-950/30 p-2 rounded border border-rose-100 dark:border-rose-900/40">
                Flagged for extra tutoring on Linked Lists & Stacks. Faculty has recommended weekly support clinic.
              </p>
            </div>
          </div>

          {/* Quick Registry Link */}
          <div className="p-5 rounded-2xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs flex items-center justify-between">
            <div>
              <strong className="text-xs font-bold text-stone-900 dark:text-stone-100 block">
                Issued Credentials Registry
              </strong>
              <p className="text-[11px] text-stone-500 mt-0.5">
                2 digitally verifiable certificates active
              </p>
            </div>
            {onNavigateToCertificates && (
              <button
                onClick={onNavigateToCertificates}
                className="px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs shadow-xs transition-colors"
              >
                View Registry
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
