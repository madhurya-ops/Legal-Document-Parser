import { LoginData, SignupData, AuthResponse, User, ProfileData } from '../types/auth';
import { api } from './api';

const TOKEN_KEY = 'auth_token';

export const login = async (credentials: LoginData): Promise<AuthResponse> => {
  const response = await api.post('/auth/login', credentials);
  
  if (response.data.access_token) {
    localStorage.setItem(TOKEN_KEY, response.data.access_token);
  }
  
  return response.data;
};

export const register = async (userData: SignupData): Promise<AuthResponse> => {
  const response = await api.post('/auth/signup', userData);
  
  if (response.data.access_token) {
    localStorage.setItem(TOKEN_KEY, response.data.access_token);
  }
  
  return response.data;
};

export const logout = (): void => {
  localStorage.removeItem(TOKEN_KEY);
};

export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

export const refreshToken = async (token: string): Promise<AuthResponse> => {
  const response = await api.post('/auth/refresh', { refresh_token: token });
  
  if (response.data.access_token) {
    localStorage.setItem(TOKEN_KEY, response.data.access_token);
  }
  
  return response.data;
};

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const updateProfile = async (data: ProfileData): Promise<User> => {
  const response = await api.put('/auth/me', data);
  return response.data;
};

export const forgotPassword = async (email: string): Promise<void> => {
  await api.post('/auth/forgot-password', { email });
};

export const resetPassword = async (token: string, password: string): Promise<void> => {
  await api.post('/auth/reset-password', { token, password });
};

export const verifyEmail = async (token: string): Promise<void> => {
  await api.post('/auth/verify-email', { token });
};

export const changePassword = async (oldPassword: string, newPassword: string): Promise<void> => {
  await api.post('/auth/change-password', {
    old_password: oldPassword,
    new_password: newPassword
  });
};

