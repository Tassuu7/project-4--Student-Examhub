/**
 * ExamHub - Authentication Client Service
 */

import { api } from '@/src/services/apiClient.ts';
import { AuthResponse, LoginCredentials, UserProfile } from '@/src/types/auth.ts';

export class AuthService {
  private static TOKEN_KEY = 'examhub_token';
  private static USER_KEY = 'examhub_user';

  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const data = await api.post<AuthResponse>('/auth/login', credentials);
    if (data.access_token) {
      localStorage.setItem(this.TOKEN_KEY, data.access_token);
      localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
    }
    return data;
  }

  static async getCurrentUser(): Promise<UserProfile> {
    const user = await api.get<UserProfile>('/auth/me');
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    return user;
  }

  static getStoredToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  static getStoredUser(): UserProfile | null {
    const raw = localStorage.getItem(this.USER_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  static async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } catch {
      // Best-effort logout
    } finally {
      localStorage.removeItem(this.TOKEN_KEY);
      localStorage.removeItem(this.USER_KEY);
    }
  }
}
