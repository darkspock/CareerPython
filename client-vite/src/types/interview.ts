// Interview Types
export interface Interview {
  id: string;
  candidate_id: string;
  interview_type: InterviewType;
  status: InterviewStatus;
  template_id?: string;
  scheduled_at?: string;
  started_at?: string;
  completed_at?: string;
  score?: number;
  notes?: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export const InterviewType = {
  TECHNICAL: 'TECHNICAL',
  BEHAVIORAL: 'BEHAVIORAL',
  SYSTEM_DESIGN: 'SYSTEM_DESIGN',
  CODING: 'CODING',
  COMPREHENSIVE: 'COMPREHENSIVE',
  QUICK: 'QUICK'
} as const;

export type InterviewType = typeof InterviewType[keyof typeof InterviewType];

export const InterviewStatus = {
  SCHEDULED: 'SCHEDULED',
  IN_PROGRESS: 'IN_PROGRESS',
  PAUSED: 'PAUSED',
  COMPLETED: 'COMPLETED',
  CANCELLED: 'CANCELLED',
  FAILED: 'FAILED'
} as const;

export type InterviewStatus = typeof InterviewStatus[keyof typeof InterviewStatus];

export const QuestionType = {
  TEXT: 'TEXT',
  MULTIPLE_CHOICE: 'MULTIPLE_CHOICE',
  RATING: 'RATING',
  CODE: 'CODE',
  FILE_UPLOAD: 'FILE_UPLOAD'
} as const;

export type QuestionType = typeof QuestionType[keyof typeof QuestionType];

// Interview List Response
export interface InterviewListResponse {
  interviews: Interview[];
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
  filters_applied: Record<string, any>;
}

// Interview Progress
export interface InterviewProgress {
  interview_id: string;
  status: string;
  current_section?: string;
  sections_completed: string[];
  total_questions: number;
  answered_questions: number;
  completion_percentage: number;
  is_paused: boolean;
  pause_reason?: string;
  current_question?: ConversationalQuestion;
  can_resume: boolean;
}

export interface ConversationalQuestion {
  question_id: string;
  question_text: string;
  section: string;
  context?: string;
  is_follow_up: boolean;
}

// Interview Templates
export interface InterviewTemplate {
  id: string;
  name: string;
  description: string;
  interview_type: InterviewType;
  is_active: boolean;
  questions?: InterviewQuestion[];
  created_at: string;
  updated_at: string;
}

export interface InterviewQuestion {
  id: string;
  question_text: string;
  category: QuestionCategory;
  difficulty: QuestionDifficulty;
  estimated_time_minutes?: number;
}

export const QuestionCategory = {
  TECHNICAL: 'TECHNICAL',
  BEHAVIORAL: 'BEHAVIORAL',
  SITUATIONAL: 'SITUATIONAL',
  CODING: 'CODING',
  SYSTEM_DESIGN: 'SYSTEM_DESIGN',
  GENERAL: 'GENERAL'
} as const;

export type QuestionCategory = typeof QuestionCategory[keyof typeof QuestionCategory];

export const QuestionDifficulty = {
  EASY: 'EASY',
  MEDIUM: 'MEDIUM',
  HARD: 'HARD'
} as const;

export type QuestionDifficulty = typeof QuestionDifficulty[keyof typeof QuestionDifficulty];

// Template Search Results
export interface TemplateSearchResult {
  template: InterviewTemplate;
  relevance_score: number;
  match_highlights: Record<string, string[]>;
  usage_stats: {
    usage_count: number;
    completion_rate: number;
    average_duration_minutes: number;
    last_used: string;
  };
  rating_stats: {
    average_rating: number;
    rating_count: number;
    five_star_percentage: number;
  };
}

export interface TemplateSearchResponse {
  results: TemplateSearchResult[];
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
  search_suggestions: string[];
}

// Template Recommendations
export interface TemplateRecommendation {
  template: InterviewTemplate;
  recommendation_score: number;
  recommendation_reasons: string[];
  estimated_duration: number;
  difficulty_match: 'perfect' | 'good' | 'challenging';
  previous_usage: boolean;
}

export interface TemplateRecommendationResponse {
  recommendations: TemplateRecommendation[];
  recommendation_strategy: string;
  candidate_profile_summary: Record<string, any>;
}

// Analytics
export interface InterviewAnalytics {
  analytics_period: string;
  date_range: {
    start_date?: string;
    end_date?: string;
  };
  metrics: {
    total_interviews: number;
    completed_interviews: number;
    in_progress_interviews: number;
    cancelled_interviews: number;
    completion_rate: number;
    average_score: number;
    average_duration_minutes: number;
  };
  trends?: {
    period: string;
    trend_direction: string;
    growth_rate: number;
    data_points: Array<{
      date: string;
      metrics: {
        total_interviews: number;
        completion_rate: number;
        average_score: number;
      };
    }>;
  };
  comparisons?: {
    current_period: {
      total_interviews: number;
      completion_rate: number;
      average_score: number;
    };
    previous_period: {
      total_interviews: number;
      completion_rate: number;
      average_score: number;
    };
    percentage_change: Record<string, number>;
    performance_indicators: string[];
  };
  insights: string[];
  recommendations: string[];
  generated_at: string;
}

export interface PerformanceReport {
  performance_summary: {
    overall_score: number;
    total_interviews: number;
    performance_trend: string;
  };
  category_breakdown: Array<{
    category: string;
    average_score: number;
    question_count: number;
    strengths: string[];
    improvement_areas: string[];
  }>;
  key_insights: string[];
  recommendations: string[];
  improvement_trajectory: string;
  report_generated_at: string;
}

// AI Interview Features
export interface AIInterviewFeaturesStatus {
  ai_service_status: string;
  features_available: {
    conversational_interview: boolean;
    question_generation: boolean;
    response_analysis: boolean;
    progress_tracking: boolean;
    pause_resume: boolean;
  };
  subscription_features: {
    tier: string;
    unlimited_interviews: boolean;
    advanced_analysis: boolean;
    priority_processing: boolean;
  };
  current_limits: {
    daily_interviews: number;
    questions_per_session: number;
  };
}

export interface AIInterviewAnalysis {
  interview_id: string;
  analysis_timestamp: string;
  overall_score: number;
  analysis_categories: {
    communication_skills: {
      score: number;
      strengths: string[];
      improvements: string[];
    };
    technical_competency: {
      score: number;
      strengths: string[];
      improvements: string[];
    };
    experience_depth: {
      score: number;
      strengths: string[];
      improvements: string[];
    };
    cultural_fit: {
      score: number;
      strengths: string[];
      improvements: string[];
    };
  };
  key_insights: string[];
  recommended_actions: string[];
  ai_confidence: number;
}

// Real-time Features
export interface RealtimeStatus {
  interview_id: string;
  status: string;
  progress: {
    completion_percentage: number;
    answered_questions: number;
    total_questions: number;
    current_section?: string;
    sections_completed: string[];
  };
  session_info: {
    is_paused: boolean;
    can_resume: boolean;
    pause_reason?: string;
    active: boolean;
  };
  current_question?: {
    question_id: string;
    question_text: string;
    section: string;
  };
  ai_suggestions?: {
    next_steps: string[];
    tips: string[];
    estimated_time_remaining?: number;
  };
  timestamp: string;
}

// Filters and Search
export interface InterviewFilters {
  status?: InterviewStatus;
  type?: InterviewType;
  page?: number;
  page_size?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  scheduled_after?: string;
  scheduled_before?: string;
  completed_after?: string;
  completed_before?: string;
  min_score?: number;
  max_score?: number;
}

export interface TemplateFilters {
  search_term?: string;
  interview_type?: InterviewType;
  difficulty_level?: QuestionDifficulty;
  is_active?: boolean;
  page?: number;
  page_size?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}