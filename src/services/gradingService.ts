/**
 * ExamHub - Grading & Normalization Service
 */

import { api } from './apiClient';
import { GradeCurveResult } from '../types/grading';

export const gradingService = {
  applyCurve: (examId: string, method: string, targetMean?: number): Promise<GradeCurveResult> => {
    return api.post<GradeCurveResult>('/grading/curve', {
      exam_id: examId,
      method,
      target_mean: targetMean,
    });
  },

  adjustScore: (payload: {
    attempt_id: string;
    question_id: string;
    new_marks: number;
    adjustment_reason: string;
  }): Promise<unknown> => {
    return api.post('/grading/adjust', payload);
  },
};
