export interface FormConstants {
  research_areas: string[];
  degree_types: string[];
  academic_years: string[];
  institutions: string[];
}

export interface ProjectFormData {
  title: string;
  abstract?: string;
  keywords?: string;
  research_area?: string;
  custom_research_area?: string;
  degree_type?: string;
  custom_degree_type?: string;
  academic_year?: string;
  institution?: string;
  custom_institution?: string;
  department?: string;
  supervisor?: string;
  author_name: string;
  author_email?: string;
  meta_description?: string;
  meta_keywords?: string;
  is_published?: boolean;
}

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  institution?: string;
  department?: string;
  phone?: string;
  role: string;
  is_active: boolean;
  created_at: string;
  
  // Extended Profile Fields
  about?: string;
  disciplines?: string[];
  research_interests?: string;
  office_location?: string;
  office_hours?: string;
  is_profile_public: boolean;
  profile_slug?: string;
  has_profile_picture: boolean;
  profile_url?: string;
}

export interface UserProfile {
  id: number;
  full_name: string;
  email: string;
  institution?: string;
  department?: string;
  about?: string;
  disciplines?: string[];
  research_interests?: string;
  office_location?: string;
  office_hours?: string;
  profile_picture_url?: string;
  supervised_projects?: ProjectSummary[];
}

export interface ProjectSummary {
  id: number;
  title: string;
  slug: string;
  author_name: string;
  academic_year?: string;
  degree_type?: string;
}

export interface ProjectFigure {
  id: number;
  project_id: number;
  title: string;
  caption?: string;
  order_index: number;
  filename: string;
  size: number;
  content_type: string;
  width?: number;
  height?: number;
  url: string;
  created_at: string;
}

export interface SupervisorInfo {
  id: string;
  name: string;
  email: string;
  institution: string;
  title: string;
}

export interface Project {
  id: number;
  title: string;
  slug: string;
  abstract?: string;
  keywords?: string;
  research_area?: string;
  degree_type?: string;
  academic_year?: string;
  institution?: string;
  department?: string;
  supervisor?: string;
  author_name: string;
  author_email?: string;
  is_published: boolean;
  publication_date: string;
  view_count: number;
  download_count: number;
  document_url?: string;
  document_filename?: string;
  document_size?: number;
  document_public_id?: string;
  document_storage?: string;
  created_by_id?: number;
  created_at: string;
  meta_description?: string;
  meta_keywords?: string;
  
  // New fields
  supervisor_id?: number;
  supervisor_user?: UserProfile;
  figures?: ProjectFigure[];
}

export interface DashboardStats {
  total_projects: number;
  published_projects: number;
  draft_projects: number;
  total_users: number;
  active_users: number;
  inactive_users: number;
  total_downloads: number;
  total_views: number;
  recent_projects: Array<{
    id: number;
    title: string;
    author_name: string;
    created_at: string;
    is_published: boolean;
  }>;
  research_areas: Array<{
    name: string;
    count: number;
  }>;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    username: string;
    email: string;
    full_name: string;
    role: string;
    institution?: string;
    department?: string;
  };
}

// Password Reset Types
export interface PasswordResetRequest {
  email: string;
}

export interface PasswordResetConfirm {
  token: string;
  new_password: string;
}

export interface PasswordResetResponse {
  message: string;
}

export interface TokenVerificationResponse {
  valid: boolean;
  email: string;
  username: string;
}

// Change Password Types
export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

// File Info Types
export interface ProjectFileInfo {
  filename?: string;
  size?: number;
  content_type?: string;
  storage?: string;
  download_count: number;
  view_count: number;
  available: boolean;
}

export interface ApiError {
  detail: string | Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
  message?: string;
}

// Form Validation Types
export interface ValidationError {
  field: string;
  message: string;
}

// Pagination Types
export interface PaginationParams {
  skip?: number;
  limit?: number;
}

// Search and Filter Types
export interface ProjectFilters extends PaginationParams {
  search?: string;
  research_area?: string;
  degree_type?: string;
  is_published?: boolean;
}

export interface UserFilters extends PaginationParams {
  search?: string;
  role?: string;
  is_active?: boolean;
}
