import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { UserProfile, UserRole } from '@/src/types/auth.ts';
import { AuthService } from '@/src/services/authService.ts';
import { useToast } from '@/src/contexts/ToastContext.tsx';

interface AuthContextType {
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (usernameOrEmail: string, pass: string) => Promise<UserProfile>;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<void>;
  hasRole: (roles: UserRole | UserRole[]) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(() => AuthService.getStoredUser());
  const [token, setToken] = useState<string | null>(() => AuthService.getStoredToken());
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const { showSuccess, showError } = useToast();

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = AuthService.getStoredToken();
      if (storedToken) {
        try {
          const freshUser = await AuthService.getCurrentUser();
          setUser(freshUser);
          setToken(storedToken);
        } catch {
          await AuthService.logout();
          setUser(null);
          setToken(null);
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (usernameOrEmail: string, pass: string): Promise<UserProfile> => {
    try {
      const data = await AuthService.login({ username_or_email: usernameOrEmail, password: pass });
      setUser(data.user);
      setToken(data.access_token);
      showSuccess(`Welcome back, ${data.user.full_name}!`);
      return data.user;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Invalid credentials';
      showError(msg);
      throw err;
    }
  };

  const logout = async () => {
    await AuthService.logout();
    setUser(null);
    setToken(null);
    showSuccess('You have been signed out.');
  };

  const refreshProfile = async () => {
    try {
      const fresh = await AuthService.getCurrentUser();
      setUser(fresh);
    } catch {
      // Ignored if offline
    }
  };

  const hasRole = (roles: UserRole | UserRole[]): boolean => {
    if (!user) return false;
    const allowed = Array.isArray(roles) ? roles : [roles];
    return allowed.includes(user.role);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        login,
        logout,
        refreshProfile,
        hasRole,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
