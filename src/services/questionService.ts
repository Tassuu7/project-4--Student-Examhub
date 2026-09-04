/**
 * ExamHub - Question Bank API Service
 */

import { api } from '@/src/services/apiClient.ts';
import { Question, QuestionFormData, QuestionFilters, BulkImportResult } from '@/src/types/question.ts';

export interface PaginatedQuestions {
  items: Question[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export class QuestionService {
  static async listQuestions(filters: QuestionFilters = {}): Promise<PaginatedQuestions> {
    const params = new URLSearchParams();
    if (filters.subject_id) params.append('subject_id', filters.subject_id);
    if (filters.difficulty) params.append('difficulty', filters.difficulty);
    if (filters.topic) params.append('topic', filters.topic);
    if (filters.search) params.append('search', filters.search);
    params.append('page', (filters.page || 1).toString());
    params.append('page_size', (filters.page_size || 20).toString());

    return api.get<PaginatedQuestions>(`/questions?${params.toString()}`);
  }

  static async getQuestion(id: string): Promise<Question> {
    return api.get<Question>(`/questions/${id}`);
  }

  static async createQuestion(data: QuestionFormData): Promise<Question> {
    return api.post<Question>('/questions', data);
  }

  static async updateQuestion(id: string, data: Partial<QuestionFormData>): Promise<Question> {
    return api.put<Question>(`/questions/${id}`, data);
  }

  static async deleteQuestion(id: string): Promise<void> {
    await api.delete(`/questions/${id}`);
  }

  static async downloadTemplate(): Promise<Blob> {
    const token = localStorage.getItem('examhub_token');
    const response = await fetch('/api/v1/questions/template.csv', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.blob();
  }

  static async exportCsv(subjectId?: string): Promise<Blob> {
    const token = localStorage.getItem('examhub_token');
    const url = subjectId
      ? `/api/v1/questions/export.csv?subject_id=${subjectId}`
      : '/api/v1/questions/export.csv';
    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.blob();
  }

  static async importCsv(file: File): Promise<BulkImportResult> {
    const formData = new FormData();
    formData.append('file', file);
    const token = localStorage.getItem('examhub_token');

    const response = await fetch('/api/v1/questions/import', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.error || data.detail || 'CSV upload failed');
    }

    return response.json();
  }
}

export const questionService = QuestionService;
