/**
 * ExamHub - Student Feedback API Client Service
 */

import { api } from './apiClient';

export interface FeedbackRecord {
  id: string;
  exam_id: string;
  exam_name: string;
  subject_code: string;
  subject_name: string;
  student_id: string;
  student_name: string;
  student_roll_number: string;
  teacher_id: string;
  teacher_name: string;
  attempt_id?: string | null;
  feedback_text: string;
  rating: number;
  created_at: string;
  updated_at: string;
}

export interface FeedbackCreatePayload {
  exam_id: string;
  student_id: string;
  attempt_id?: string | null;
  feedback_text: string;
  rating?: number;
}

export const feedbackService = {
  submitFeedback: async (payload: FeedbackCreatePayload): Promise<FeedbackRecord> => {
    return api.post<FeedbackRecord>('/feedbacks', payload);
  },

  getStudentFeedbacks: async (studentId: string): Promise<FeedbackRecord[]> => {
    return api.get<FeedbackRecord[]>(`/feedbacks/student/${studentId}`);
  },

  getExamFeedbacks: async (examId: string): Promise<FeedbackRecord[]> => {
    return api.get<FeedbackRecord[]>(`/feedbacks/exam/${examId}`);
  },

  listAllFeedbacks: async (): Promise<FeedbackRecord[]> => {
    return api.get<FeedbackRecord[]>('/feedbacks');
  },
};
