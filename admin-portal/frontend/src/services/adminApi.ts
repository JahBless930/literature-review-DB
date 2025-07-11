import axios, { AxiosResponse } from 'axios';
import { User, Project, DashboardStats, LoginRequest, AuthResponse, FormConstants, ProjectFigure } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001/api';

// Password Reset Types
interface PasswordResetResponse {
  message: string;
}

interface TokenVerificationResponse {
  valid: boolean;
  email: string;
  username: string;
}

class AdminApiService {
  private api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
  });

  constructor() {
    // Add auth token to requests
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('admin_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      
      // Don't override Content-Type if it's already set (like for multipart/form-data)
      if (config.method === 'post' && !config.headers['Content-Type'] && !(config.data instanceof FormData)) {
        config.headers['Content-Type'] = 'application/json';
      }
      
      return config;
    });

    // Handle auth errors and format error messages
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('admin_token');
          localStorage.removeItem('admin_user');
          window.location.href = '/login';
        }
        
        // Format error message for better display
        if (error.response?.data) {
          const errorData = error.response.data;
          
          // Handle FastAPI validation errors
          if (Array.isArray(errorData.detail)) {
            const messages = errorData.detail.map((err: any) => {
              if (typeof err === 'object' && err.msg) {
                return `${err.loc?.join(' → ') || 'Field'}: ${err.msg}`;
              }
              return err.toString();
            });
            error.message = messages.join(', ');
          } else if (typeof errorData.detail === 'string') {
            error.message = errorData.detail;
          } else if (errorData.message) {
            error.message = errorData.message;
          }
        }
        
        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      const formData = new FormData();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);
      
      console.log('Attempting login with:', credentials.username);
      
      const response = await this.api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      console.log('Login response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Login error:', error.response?.data || error.message);
      throw error;
    }
  }

  async logout(): Promise<void> {
    await this.api.post('/auth/logout');
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_user');
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get('/auth/me');
    return response.data;
  }

  async changePassword(currentPassword: string, newPassword: string): Promise<{ message: string }> {
    const response = await this.api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword
    });
    return response.data;
  }

  async forgotPassword(email: string): Promise<{ message: string }> {
    try {
      console.log('Sending email:', email); // Debug log
      
      const formData = new FormData();
      formData.append('email', email);
      
      const response = await this.api.post('/auth/forgot-password', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Forgot password error:', error);
      throw error;
    }
  }

  async resetPassword(token: string, newPassword: string): Promise<PasswordResetResponse> {
    const response = await this.api.post('/auth/reset-password', { 
      token, 
      new_password: newPassword 
    });
    return response.data;
  }

  async verifyResetToken(token: string): Promise<TokenVerificationResponse> {
    const response = await this.api.get('/auth/verify-reset-token', {
      params: { token }
    });
    return response.data;
  }

  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await this.api.get('/dashboard/stats');
    return response.data;
  }

  // Users
  async getUsers(): Promise<User[]> {
    const response = await this.api.get('/users/');
    return response.data;
  }

  async createUser(userData: any): Promise<User> {
    const response = await this.api.post('/users/', userData);
    return response.data;
  }

  async updateUser(userId: number, userData: any): Promise<User> {
    const response = await this.api.put(`/users/${userId}`, userData);
    return response.data;
  }

  async deleteUser(userId: number): Promise<void> {
    await this.api.delete(`/users/${userId}`);
  }

  async toggleUserStatus(userId: number): Promise<void> {
    await this.api.patch(`/users/${userId}/toggle-status`);
  }

  // Profile endpoints
  async updateProfile(data: FormData): Promise<User> {
    const response = await this.api.put('/users/profile', data, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  }

  async getProfilePicture(): Promise<string> {
    const response = await this.api.get('/users/profile/picture', {
      responseType: 'blob'
    });
    return URL.createObjectURL(response.data);
  }

  // Projects
  async getProjects(params?: {
    search?: string;
    research_area?: string;
    degree_type?: string;
    is_published?: boolean;
    skip?: number;
    limit?: number;
  }): Promise<Project[]> {
    const response = await this.api.get('/projects/', {
      params: {
        ...(params?.search && { search: params.search }),
        ...(params?.research_area && { research_area: params.research_area }),
        ...(params?.degree_type && { degree_type: params.degree_type }),
        ...(params?.is_published !== undefined && { is_published: params.is_published }),
        ...(params?.skip && { skip: params.skip }),
        ...(params?.limit && { limit: params.limit }),
      }
    });
    return response.data;
  }

  async createProject(projectData: FormData): Promise<Project> {
    const response = await this.api.post('/projects/', projectData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async updateProject(projectId: number, projectData: FormData): Promise<Project> {
    const response = await this.api.put(`/projects/${projectId}`, projectData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async deleteProject(projectId: number): Promise<void> {
    await this.api.delete(`/projects/${projectId}`);
  }

  async toggleProjectStatus(projectId: number): Promise<void> {
    await this.api.patch(`/projects/${projectId}/toggle-publish`);
  }

  async getResearchAreas(): Promise<string[]> {
    const response = await this.api.get('/projects/research-areas/list');
    return response.data;
  }

  async getDegreeTypes(): Promise<string[]> {
    const response = await this.api.get('/projects/degree-types/list');
    return response.data;
  }

  async deleteProjectFile(projectId: number): Promise<void> {
    await this.api.delete(`/projects/${projectId}/file`);
  }

  // Figure endpoints
  async uploadFigure(projectId: number, data: FormData): Promise<ProjectFigure> {
    const response = await this.api.post(`/projects/${projectId}/figures`, data, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  }

  async getProjectFigures(projectId: number): Promise<ProjectFigure[]> {
    const response = await this.api.get(`/projects/${projectId}/figures`);
    return response.data;
  }

  async deleteFigure(figureId: number): Promise<void> {
    await this.api.delete(`/figures/${figureId}`);
  }

  // Utilities
  async getFormConstants(): Promise<FormConstants> {
    const response = await this.api.get('/utils/constants');
    return response.data;
  }

  async getPredefinedResearchAreas(): Promise<string[]> {
    const response = await this.api.get('/utils/research-areas');
    return response.data.research_areas;
  }

  async getPredefinedDegreeTypes(): Promise<string[]> {
    const response = await this.api.get('/utils/degree-types');
    return response.data.degree_types;
  }

  async getAcademicYears(): Promise<string[]> {
    const response = await this.api.get('/utils/academic-years');
    return response.data.academic_years;
  }

  async getInstitutions(): Promise<string[]> {
    const response = await this.api.get('/utils/institutions');
    return response.data.institutions;
  }

  // Additional helper methods for better error handling
  private handleApiError(error: any): never {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }

  // Health check method
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await this.api.get('/health');
    return response.data;
  }

  // Generic get method for custom endpoints
  async get<T = any>(endpoint: string, config?: any): Promise<T> {
    const response = await this.api.get(endpoint, config);
    return response.data;
  }

  // Generic post method for custom endpoints
  async post<T = any>(endpoint: string, data?: any, config?: any): Promise<T> {
    const response = await this.api.post(endpoint, data, config);
    return response.data;
  }

  // Generic put method for custom endpoints
  async put<T = any>(endpoint: string, data?: any, config?: any): Promise<T> {
    const response = await this.api.put(endpoint, data, config);
    return response.data;
  }

  // Generic delete method for custom endpoints
  async delete<T = any>(endpoint: string, config?: any): Promise<T> {
    const response = await this.api.delete(endpoint, config);
    return response.data;
  }
}

export const adminApi = new AdminApiService();

// Export types for use in components
export type { PasswordResetResponse, TokenVerificationResponse };
