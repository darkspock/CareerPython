/**
 * TypeScript interfaces for Resume with hybrid structure
 *
 * Supports both new hybrid structure (GeneralData + VariableSection[])
 * and legacy compatibility fields for gradual migration.
 */

// New hybrid structure interfaces
export interface GeneralData {
  cv_title: string;
  name: string;
  email: string;
  phone: string;
}

export interface VariableSection {
  key: string;
  title: string;
  content: string; // HTML content
  order: number;
}

export interface ResumeContent {
  // New hybrid structure
  general_data: GeneralData;
  variable_sections: VariableSection[];

  // Legacy compatibility fields (maintained for backward compatibility)
  experiencia_profesional: string;
  educacion: string;
  proyectos: string;
  habilidades: string;
  datos_personales: {
    name?: string;
    email?: string;
    phone?: string;
    location?: string;
    linkedin_url?: string;
    cv_title?: string;
  };
}

export interface AIGeneratedContent {
  ai_summary?: string;
  ai_key_aspects: string[];
  ai_skills_recommendations: string[];
  ai_achievements: string[];
  ai_intro_letter?: string;
}

export interface FormattingPreferences {
  template: string;
  color_scheme: string;
  font_family: string;
  include_photo: boolean;
  sections_order: string[];
}

export interface Resume {
  id: string;
  candidate_id: string;
  name: string;
  resume_type: string;
  status: string;
  ai_enhancement_status: string;
  content: ResumeContent;
  ai_generated_content?: AIGeneratedContent;
  formatting_preferences: FormattingPreferences;
  general_data: Record<string, any>;
  custom_content: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Request interfaces for API calls
export interface UpdateResumeContentRequest {
  // New hybrid structure fields
  general_data?: Partial<GeneralData>;
  variable_sections?: VariableSection[];

  // Legacy compatibility fields
  experiencia_profesional?: string;
  educacion?: string;
  proyectos?: string;
  habilidades?: string;
  datos_personales?: Record<string, any>;

  // Common fields
  custom_content?: Record<string, any>;
  preserve_ai_content?: boolean;
}

// Variable section management interfaces
export interface AddVariableSectionRequest {
  section_key: string;
  section_title: string;
  section_content?: string;
  section_order?: number;
}

export interface UpdateVariableSectionRequest {
  section_key: string;
  section_content?: string;
  section_title?: string;
  section_order?: number;
}

export interface RemoveVariableSectionRequest {
  section_key: string;
}

export interface ReorderVariableSectionsRequest {
  sections_order: Array<{ key: string; order: number }>;
}

// Default sections configuration
export const DEFAULT_SECTIONS: Omit<VariableSection, 'content'>[] = [
  { key: 'summary', title: 'Professional Summary', order: 1 },
  { key: 'experience', title: 'Work Experience', order: 2 },
  { key: 'education', title: 'Education', order: 3 },
  { key: 'skills', title: 'Skills', order: 4 },
  { key: 'projects', title: 'Projects', order: 5 },
];

// Utility type for section keys
export type SectionKey = 'summary' | 'experience' | 'education' | 'skills' | 'projects' | string;

// HTML sanitization options
export interface SanitizationConfig {
  allowedTags: string[];
  allowedAttributes: Record<string, string[]>;
  removeScriptTags: boolean;
  removeStyleTags: boolean;
  removeEventHandlers: boolean;
}

export const DEFAULT_SANITIZATION: SanitizationConfig = {
  allowedTags: [
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span', 'div'
  ],
  allowedAttributes: {
    'a': ['href', 'target', 'rel'],
    'span': ['class'],
    'div': ['class'],
  },
  removeScriptTags: true,
  removeStyleTags: true,
  removeEventHandlers: true,
};
