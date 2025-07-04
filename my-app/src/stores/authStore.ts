import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, LoginData, SignupData, ProfileData } from '../types/auth';
import * as authService from '../services/auth';

interface AuthStore {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  token: string | null;
  
  // Actions
  login: (credentials: LoginData) => Promise<void>;
  logout: () => void;
  register: (userData: SignupData) => Promise<void>;
  refreshToken: () => Promise<void>;
  updateProfile: (data: ProfileData) => Promise<void>;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      token: null,

      login: async (credentials: LoginData) => {
        try {
          set({ isLoading: true });
          const response = await authService.login(credentials);
          
          set({
            user: response.user,
            token: response.access_token,
            isAuthenticated: true,
            isLoading: false
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: () => {
        authService.logout();
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false
        });
      },

      register: async (userData: SignupData) => {
        try {
          set({ isLoading: true });
          const response = await authService.register(userData);
          
          set({
            user: response.user,
            token: response.access_token,
            isAuthenticated: true,
            isLoading: false
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      refreshToken: async () => {
        try {
          const { token } = get();
          if (!token) return;
          
          const response = await authService.refreshToken(token);
          set({
            token: response.access_token,
            user: response.user || get().user
          });
        } catch (error) {
          // If refresh fails, logout
          get().logout();
          throw error;
        }
      },

      updateProfile: async (data: ProfileData) => {
        try {
          set({ isLoading: true });
          const updatedUser = await authService.updateProfile(data);
          
          set({
            user: updatedUser,
            isLoading: false
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      setUser: (user: User | null) => {
        set({ 
          user, 
          isAuthenticated: !!user 
        });
      },

      setToken: (token: string | null) => {
        set({ token });
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      }
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated
      })
    }
  )
);
