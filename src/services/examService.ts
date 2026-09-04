/**
 * ExamHub - Exam Management & Execution API Client
 */

import { request } from './apiClient';
import {
  Exam,
  StudentPortalExam,
  ExamAttemptStartResponse,
  ExamResult,
  IntegritySummary,
  ExamCreateFormData,
  ExamAutoGenerateFormData,
  ExamStatus
} from '../types/exam';

export interface ExamListResponse {
  items: Exam[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface StudentListItem {
  id: string;
  student_id: string;
  student_id_code: string;
  full_name: string;
  email: string;
  department?: string;
  grade_level?: string;
}

export const examService = {
  // Teacher/Admin Exam CRUD
  async listExams(params?: {
    subject_id?: string;
    teacher_id?: string;
    status?: string;
    search?: string;
    page?: number;
    limit?: number;
  }): Promise<ExamListResponse> {
    const searchParams = new URLSearchParams();
    if (params?.subject_id) searchParams.append('subject_id', params.subject_id);
    if (params?.teacher_id) searchParams.append('teacher_id', params.teacher_id);
    if (params?.status) searchParams.append('status', params.status);
    if (params?.search) searchParams.append('search', params.search);
    if (params?.page) searchParams.append('page', params.page.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());

    const query = searchParams.toString();
    return request<ExamListResponse>(`/exams${query ? `?${query}` : ''}`);
  },

  async getExamDetails(examId: string): Promise<Exam> {
    return request<Exam>(`/exams/${examId}`);
  },

  async createExam(data: ExamCreateFormData): Promise<{ message: string; exam_id: string }> {
    return request<{ message: string; exam_id: string }>('/exams', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async updateExam(examId: string, data: Partial<ExamCreateFormData> & { status?: ExamStatus }): Promise<{ message: string; exam: Exam }> {
    return request<{ message: string; exam: Exam }>(`/exams/${examId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  async autoGenerateExam(data: ExamAutoGenerateFormData): Promise<{ message: string; exam_id: string }> {
    return request<{ message: string; exam_id: string }>('/exams/auto-generate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async updateExamStatus(examId: string, status: ExamStatus): Promise<{ message: string }> {
    return request<{ message: string }>(`/exams/${examId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  },

  async deleteExam(examId: string): Promise<{ message: string }> {
    return request<{ message: string }>(`/exams/${examId}`, {
      method: 'DELETE',
    });
  },

  async listAvailableStudents(): Promise<{ items: StudentListItem[]; total: number }> {
    return request<{ items: StudentListItem[]; total: number }>('/users/students');
  },

  async assignStudentsToExam(examId: string, studentIds: string[]): Promise<{ exam_id: string; assigned_count: number }> {
    return request<{ exam_id: string; assigned_count: number }>(`/exams/${examId}/students`, {
      method: 'POST',
      body: JSON.stringify({ student_ids: studentIds }),
    });
  },

  async assignQuestionsToExam(
    examId: string,
    questions: Array<{ question_id: string; marks_allocated: number }>
  ): Promise<{ exam_id: string; questions_count: number; total_marks: number }> {
    return request<{ exam_id: string; questions_count: number; total_marks: number }>(`/exams/${examId}/questions`, {
      method: 'POST',
      body: JSON.stringify({ questions }),
    });
  },

  async getExamResults(examId: string): Promise<{ items: ExamResult[]; total: number }> {
    return request<{ items: ExamResult[]; total: number }>(`/exams/${examId}/results`);
  },

  // Student Taking Portal
  async getStudentAssignedExams(): Promise<{ items: StudentPortalExam[]; total: number }> {
    return request<{ items: StudentPortalExam[]; total: number }>('/exams/student/portal');
  },

  async startExamAttempt(examId: string): Promise<ExamAttemptStartResponse> {
    return request<ExamAttemptStartResponse>(`/exams/${examId}/attempt/start`, {
      method: 'POST',
    });
  },

  async saveStudentAnswer(
    attemptId: string,
    questionId: string,
    selectedOption: string | null,
    isMarkedForReview: boolean = false
  ): Promise<{ question_id: string; selected_option: string | null; saved: boolean }> {
    return request(`/exams/attempt/${attemptId}/answer`, {
      method: 'POST',
      body: JSON.stringify({
        question_id: questionId,
        selected_option: selectedOption,
        is_marked_for_review: isMarkedForReview,
      }),
    });
  },

  async updateTimeRemaining(attemptId: string, secondsLeft: number): Promise<void> {
    await request(`/exams/attempt/${attemptId}/time`, {
      method: 'POST',
      body: JSON.stringify({ time_remaining_seconds: secondsLeft }),
    }).catch(() => {
      // Non-blocking ping
    });
  },

  async logProctoringEvent(attemptId: string, eventType: string, details?: string): Promise<void> {
    await request(`/exams/attempt/${attemptId}/proctoring`, {
      method: 'POST',
      body: JSON.stringify({ event_type: eventType, details: details || '' }),
    }).catch(() => {
      // Silent log failure prevention
    });
  },

  async submitAttempt(attemptId: string): Promise<ExamResult> {
    return request<ExamResult>(`/exams/attempt/${attemptId}/submit`, {
      method: 'POST',
    });
  },

  async autoSubmitAttempt(attemptId: string): Promise<ExamResult> {
    return request<ExamResult>(`/exams/attempt/${attemptId}/auto-submit`, {
      method: 'POST',
    });
  },

  async getAttemptResult(attemptId: string): Promise<ExamResult> {
    return request<ExamResult>(`/exams/attempt/${attemptId}/result`);
  },

  async getAttemptIntegrity(attemptId: string): Promise<IntegritySummary> {
    return request<IntegritySummary>(`/exams/attempt/${attemptId}/integrity`);
  }
};
