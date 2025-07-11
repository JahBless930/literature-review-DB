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
  supervisor_id?: number;  // Add this
  supervisor_user?: UserProfile;  // Add this
  author_name: string;
  author_email?: string;
  is_published: boolean;
  publication_date: string;
  view_count: number;
  download_count: number;
  document_url?: string;
  document_filename?: string;
  document_size?: number;
  document_storage?: string;
  meta_description?: string;
  figures?: ProjectFigure[];  // Add this
}

export interface ProjectSummary {
  id: number;
  title: string;
  slug: string;
  abstract?: string;
  research_area?: string;
  degree_type?: string;
  institution?: string;
  author_name: string;
  publication_date: string;
  view_count?: number;
  download_count?: number;
  is_published?: boolean;
}

// Add these new interfaces
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
  profile_slug?: string;
  supervised_projects?: ProjectSummary[];
}

export interface SupervisorInfo {
  id: string;
  name: string;
  email: string;
  institution: string;
  title: string;
}

// Existing interfaces...
export interface SearchFilters {
  query?: string;
  research_area?: string;
  degree_type?: string;
  institution?: string;
  academic_year?: string;
}

export interface SearchResponse {
  projects: ProjectSummary[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
  filters: SearchFilters;
}

export interface SiteStats {
  total_projects: number;
  total_institutions: number;
  total_research_areas: number;
  total_downloads: number;
}

export interface ApiError {
  message: string;
  status?: number;
}

export interface PaginationParams {
  page?: number;
  limit?: number;
  search?: string;
}

export interface DownloadResponse {
  download_url: string;
  filename: string;
}
