/**
 * ExamHub - Subject API Service
 */

import { api } from '@/src/services/apiClient.ts';
import { Subject, SubjectFormData } from '@/src/types/subject.ts';

export interface PaginatedSubjects {
  items: Subject[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export class SubjectService {
  static async listSubjects(search?: string, department?: string, page: number = 1, pageSize: number = 50): Promise<PaginatedSubjects> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (department) params.append('department', department);
    params.append('page', page.toString());
    params.append('page_size', pageSize.toString());

    return api.get<PaginatedSubjects>(`/subjects?${params.toString()}`);
  }

  static async getSubject(id: string): Promise<Subject> {
    return api.get<Subject>(`/subjects/${id}`);
  }

  static async createSubject(data: SubjectFormData): Promise<Subject> {
    return api.post<Subject>('/subjects', data);
  }

  static async updateSubject(id: string, data: Partial<SubjectFormData>): Promise<Subject> {
    return api.put<Subject>(`/subjects/${id}`, data);
  }

  static async assignTeacher(subjectId: string, teacherId: string): Promise<void> {
    await api.post(`/subjects/${subjectId}/teachers`, { teacher_id: teacherId });
  }

  static async removeTeacher(subjectId: string, teacherId: string): Promise<void> {
    await api.delete(`/subjects/${subjectId}/teachers/${teacherId}`);
  }
}
