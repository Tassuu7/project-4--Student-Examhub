/**
 * ExamHub - Question Bank TypeScript Types
 */

export type QuestionDifficulty = 'Easy' | 'Medium' | 'Hard';
export type CorrectOption = 'A' | 'B' | 'C' | 'D';

export interface Question {
  id: string;
  subject_id: string;
  subject_code: string;
  subject_name: string;
  teacher_id?: string;
  teacher_name?: string;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct_answer: CorrectOption;
  marks: number;
  difficulty: QuestionDifficulty;
  topic?: string;
  explanation?: string;
  is_active: boolean;
  used_in_exam_count: number;
  created_at: string;
  updated_at: string;
}

export interface QuestionFormData {
  subject_id: string;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct_answer: CorrectOption;
  marks: number;
  difficulty: QuestionDifficulty;
  topic?: string;
  explanation?: string;
}

export interface QuestionFilters {
  subject_id?: string;
  difficulty?: QuestionDifficulty;
  topic?: string;
  search?: string;
  page?: number;
  page_size?: number;
}

export interface BulkImportResult {
  total_processed: number;
  imported_count: number;
  failed_count: number;
  errors: string[];
}
