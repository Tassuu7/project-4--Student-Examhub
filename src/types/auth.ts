/**
 * ExamHub - User Role and Authentication Types
 */

export type UserRole = 'admin' | 'teacher' | 'student';

export interface UserProfile {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  student_id?: string;
  student_code?: string;
  teacher_id?: string;
  teacher_code?: string;
  department?: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: UserProfile;
}

export interface LoginCredentials {
  username_or_email: string;
  password: string;
}

export interface AuthState {
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
