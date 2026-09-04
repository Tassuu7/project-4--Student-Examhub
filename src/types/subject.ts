/**
 * ExamHub - Subject TypeScript Types
 */

export interface TeacherAssignment {
  teacher_id: string;
  teacher_name: string;
  teacher_code: string;
  department?: string;
  assigned_at: string;
}

export interface Subject {
  id: string;
  code: string;
  name: string;
  description?: string;
  department?: string;
  is_active: boolean;
  question_count: number;
  exam_count: number;
  assigned_teachers: TeacherAssignment[];
  created_at: string;
  updated_at: string;
}

export interface SubjectFormData {
  code: string;
  name: string;
  description?: string;
  department?: string;
}
