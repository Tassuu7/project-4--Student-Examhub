/**
 * ExamHub - Comprehensive Analytics & Reports Dashboard
 */

import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Award,
  Users,
  CheckCircle2,
  AlertTriangle,
  Download,
  Calendar,
  BookOpen,
  PieChart,
  BarChart3,
  Layers,
  Sparkles,
} from 'lucide-react';
import { Exam } from '../../types/exam';
import { ExamAnalyticsResponse, SystemOverviewAnalytics } from '../../types/analytics';
import { examService } from '../../services/examService';
import { analyticsService } from '../../services/analyticsService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { StatCard } from '../common/StatCard';
import { ScoreDistributionHistogram } from './ScoreDistributionHistogram';
import { QuestionDifficultyChart } from './QuestionDifficultyChart';

export const AnalyticsDashboard: React.FC = () => {
  const [exams, setExams] = useState<Exam[]>([]);
  const [selectedExamId, setSelectedExamId] = useState<string>('');
  const [analyticsData, setAnalyticsData] = useState<ExamAnalyticsResponse | null>(null);
  const [overview, setOverview] = useState<SystemOverviewAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingExam, setLoadingExam] = useState(false);

  const { showToast } = useToast();

  useEffect(() => {
    const init = async () => {
      try {
        setLoading(true);
        const [examsRes, overviewRes] = await Promise.all([
          examService.listExams(),
          analyticsService.getSystemOverview(),
        ]);
        setExams(examsRes.items || []);
        setOverview(overviewRes);

        if (examsRes.items && examsRes.items.length > 0) {
          setSelectedExamId(examsRes.items[0].id);
        }
      } catch (err: unknown) {
        showToast(err instanceof Error ? err.message : 'Failed to load dashboard data', 'error');
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  useEffect(() => {
    if (!selectedExamId) return;

    const loadExamAnalytics = async () => {
      try {
        setLoadingExam(true);
        const data = await analyticsService.getExamAnalytics(selectedExamId);
        setAnalyticsData(data);
      } catch (err: unknown) {
        showToast(err instanceof Error ? err.message : 'Failed to load exam psychometrics', 'error');
      } finally {
        setLoadingExam(false);
      }
    };
    loadExamAnalytics();
  }, [selectedExamId]);

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center">
        <LoadingSpinner size="lg" />
        <p className="mt-3 text-xs font-semibold text-zinc-500 uppercase tracking-wider">
          Computing Statistical Analytics...
        </p>
      </div>
    );
  }

  return (
    <div id="analytics-dashboard-container" className="space-y-8">
      {/* Top Header & Exam Selector */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-200 dark:border-zinc-800 pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50 flex items-center gap-2.5">
            <TrendingUp className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            Psychometrics & Performance Intelligence
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
            Deep-dive psychometric evaluation, Item Response Theory, grade distributions, and cohort analytics.
          </p>
        </div>

        {/* Exam Picker & Export Actions */}
        <div className="flex items-center gap-3">
          <select
            value={selectedExamId}
            onChange={(e) => setSelectedExamId(e.target.value)}
            className="px-3.5 py-2 text-xs font-semibold rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 shadow-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          >
            {exams.map((exam) => (
              <option key={exam.id} value={exam.id}>
                {exam.subject_code} &mdash; {exam.name}
              </option>
            ))}
          </select>

          {selectedExamId && (
            <a
              href={`/api/v1/export-import/exam/${selectedExamId}/csv`}
              download
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 hover:bg-zinc-50 dark:hover:bg-zinc-700 shadow-xs transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              Export CSV
            </a>
          )}
        </div>
      </div>

      {/* Global System KPIs */}
      {overview && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <StatCard
            label="Total Assessments Evaluated"
            value={overview.total_attempts_completed}
            subtext={`${overview.total_exams} registered exams`}
            icon={<BookOpen className="w-4 h-4 text-indigo-500" />}
            variant="info"
          />
          <StatCard
            label="Global Pass Rate"
            value={`${overview.global_pass_rate_pct}%`}
            subtext="Across all curricula"
            icon={<CheckCircle2 className="w-4 h-4 text-emerald-500" />}
            variant="success"
          />
          <StatCard
            label="Enrolled Students"
            value={overview.total_students}
            subtext={`${overview.total_teachers} instructors`}
            icon={<Users className="w-4 h-4 text-amber-500" />}
            variant="warning"
          />
          <StatCard
            label="Active Question Bank"
            value={overview.total_questions}
            subtext="Available for exams"
            icon={<Layers className="w-4 h-4 text-purple-500" />}
            variant="default"
          />
        </div>
      )}

      {/* Exam Specific Detailed Analytics */}
      {loadingExam ? (
        <div className="py-16 flex justify-center">
          <LoadingSpinner size="md" />
        </div>
      ) : !analyticsData ? (
        <div className="p-8 text-center rounded-2xl border border-dashed border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900">
          <AlertTriangle className="w-8 h-8 mx-auto text-amber-500 mb-2" />
          <p className="text-sm font-semibold">No assessment records found for this exam.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Exam Core Metrics Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <StatCard
              label="Candidates Evaluated"
              value={analyticsData.score_summary.evaluated_candidates}
              subtext={`Duration: ${analyticsData.duration_minutes} min`}
              variant="default"
            />
            <StatCard
              label="Mean Cohort Score"
              value={`${analyticsData.score_summary.mean_score} / ${analyticsData.total_marks}`}
              subtext={`Median: ${analyticsData.score_summary.median_score}`}
              variant="info"
            />
            <StatCard
              label="Pass Rate"
              value={`${analyticsData.pass_fail.pass_rate}%`}
              subtext={`${analyticsData.pass_fail.passed_count} passed, ${analyticsData.pass_fail.failed_count} failed`}
              variant={analyticsData.pass_fail.pass_rate >= 50 ? 'success' : 'danger'}
            />
            <StatCard
              label="Standard Deviation"
              value={`±${analyticsData.score_summary.standard_deviation}`}
              subtext={`Range: ${analyticsData.score_summary.range_score} marks`}
              variant="default"
            />
          </div>

          {/* Visual Histogram & Grade Distribution */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-8">
              <ScoreDistributionHistogram deciles={analyticsData.deciles} />
            </div>

            {/* Grade Tier Breakdown */}
            <div className="lg:col-span-4 bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
              <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 mb-1">
                Grade Distribution
              </h3>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-4">
                Letter tier allocations based on cohort scoring
              </p>

              <div className="space-y-2.5">
                {analyticsData.grade_distribution.map((g) => (
                  <div key={g.grade} className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <span
                        style={{ backgroundColor: g.color_code }}
                        className="w-3 h-3 rounded-full"
                      />
                      <span className="font-bold text-zinc-800 dark:text-zinc-200">
                        Grade {g.grade}
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="font-semibold text-zinc-600 dark:text-zinc-400">
                        {g.count} ({g.percentage}%)
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Topic Performance Breakdown */}
          {analyticsData.topic_performance.length > 0 && (
            <div className="bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
              <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 mb-3">
                Curriculum Topic Mastery
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {analyticsData.topic_performance.map((tp) => (
                  <div
                    key={tp.topic}
                    className="p-4 rounded-xl border border-zinc-100 dark:border-zinc-800 bg-zinc-50/60 dark:bg-zinc-800/40"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-bold text-xs text-zinc-900 dark:text-zinc-100">{tp.topic}</h4>
                      <span
                        className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                          tp.mastery_level === 'Mastered'
                            ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300'
                            : tp.mastery_level === 'Proficient'
                            ? 'bg-blue-100 text-blue-800 dark:bg-blue-950/60 dark:text-blue-300'
                            : 'bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300'
                        }`}
                      >
                        {tp.mastery_level}
                      </span>
                    </div>
                    <div className="flex justify-between text-[11px] text-zinc-500 mb-1">
                      <span>Accuracy</span>
                      <span className="font-bold text-zinc-800 dark:text-zinc-200">{tp.average_accuracy_percentage}%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-zinc-200 dark:bg-zinc-700 overflow-hidden">
                      <div
                        style={{ width: `${tp.average_accuracy_percentage}%` }}
                        className="h-full bg-indigo-600 rounded-full"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Question Level Psychometrics Table */}
          <QuestionDifficultyChart metrics={analyticsData.question_metrics} />

          {/* Top Performers and At-Risk Candidates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Top Performers */}
            <div className="bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
              <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 mb-3 flex items-center gap-1.5">
                <Award className="w-4 h-4 text-amber-500" />
                Top Performers (Honor Roll)
              </h3>
              <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
                {analyticsData.top_performers.slice(0, 4).map((c) => (
                  <div key={c.student_id} className="py-2.5 flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2.5">
                      <span className="w-6 h-6 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-950/50 dark:text-amber-300 font-bold flex items-center justify-center text-[11px]">
                        #{c.rank}
                      </span>
                      <div>
                        <p className="font-bold text-zinc-900 dark:text-zinc-100">{c.full_name}</p>
                        <span className="text-[10px] text-zinc-400">Roll: {c.roll_number}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="font-bold text-emerald-600 dark:text-emerald-400">
                        {c.percentage.toFixed(1)}%
                      </span>
                      <span className="block text-[10px] text-zinc-400">
                        {c.obtained_marks}/{c.total_marks} Marks
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* At-Risk Candidates */}
            <div className="bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
              <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 mb-3 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 text-rose-500" />
                At-Risk Candidates (Intervention Required)
              </h3>
              {analyticsData.at_risk_candidates.length === 0 ? (
                <p className="text-xs text-zinc-400 py-6 text-center">
                  All evaluated candidates successfully met the passing threshold!
                </p>
              ) : (
                <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
                  {analyticsData.at_risk_candidates.slice(0, 4).map((c) => (
                    <div key={c.student_id} className="py-2.5 flex items-center justify-between text-xs">
                      <div>
                        <p className="font-bold text-zinc-900 dark:text-zinc-100">{c.full_name}</p>
                        <span className="text-[10px] text-zinc-400">Roll: {c.roll_number}</span>
                      </div>
                      <div className="text-right">
                        <span className="font-bold text-rose-600 dark:text-rose-400">
                          {c.percentage.toFixed(1)}%
                        </span>
                        <span className="block text-[10px] text-rose-500 uppercase font-semibold">
                          Needs Support
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
