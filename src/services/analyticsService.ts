/**
 * ExamHub - Analytics & Psychometrics Service
 */

import { api } from './apiClient';
import { ExamAnalyticsResponse, SystemOverviewAnalytics } from '../types/analytics';

export const analyticsService = {
  getExamAnalytics: (examId: string): Promise<ExamAnalyticsResponse> => {
    return api.get<ExamAnalyticsResponse>(`/analytics/exam/${examId}`);
  },

  getSystemOverview: (): Promise<SystemOverviewAnalytics> => {
    return api.get<SystemOverviewAnalytics>('/analytics/overview');
  },

  getStudentTrend: (studentId: string): Promise<unknown> => {
    return api.get(`/analytics/student/${studentId}/trend`);
  },

  getSubjectTrend: (subjectId: string): Promise<unknown> => {
    return api.get(`/analytics/subject/${subjectId}/trend`);
  },

  compareCohorts: (cohortAId: string, cohortBId: string): Promise<unknown> => {
    return api.post('/analytics/compare-cohorts', {
      cohort_a_exam_id: cohortAId,
      cohort_b_exam_id: cohortBId,
    });
  },
};
