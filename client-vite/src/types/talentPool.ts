/**
 * Talent Pool Types
 * Phase 8: TypeScript types for talent pool management
 */

// Talent Pool Status Enum
export const TalentPoolStatus = {
  ACTIVE: 'active',
  CONTACTED: 'contacted',
  HIRED: 'hired',
  NOT_INTERESTED: 'not_interested',
  ARCHIVED: 'archived'
} as const;
export type TalentPoolStatus = typeof TalentPoolStatus[keyof typeof TalentPoolStatus];

// Talent Pool Entry Interface
export interface TalentPoolEntry {
  id: string;
  company_id: string;
  candidate_id: string;
  source_application_id: string | null;
  source_position_id: string | null;
  added_reason: string | null;
  tags: string[];
  rating: number | null;
  notes: string | null;
  status: TalentPoolStatus;
  added_by_user_id: string | null;
  created_at: string;
  updated_at: string;
}

// Request Types
export interface AddToTalentPoolRequest {
  candidate_id: string;
  added_reason?: string | null;
  tags?: string[];
  rating?: number | null;
  notes?: string | null;
  status?: TalentPoolStatus;
  source_application_id?: string | null;
  source_position_id?: string | null;
}

export interface UpdateTalentPoolEntryRequest {
  added_reason?: string | null;
  tags?: string[];
  rating?: number | null;
  notes?: string | null;
}

export interface ChangeTalentPoolStatusRequest {
  status: TalentPoolStatus;
}

// Filter Types
export interface TalentPoolFilters {
  status?: TalentPoolStatus;
  tags?: string[];
  min_rating?: number;
  search_term?: string;
}

// Helper Functions
export function getTalentPoolStatusLabel(status: TalentPoolStatus): string {
  const labels: Record<TalentPoolStatus, string> = {
    [TalentPoolStatus.ACTIVE]: 'Active',
    [TalentPoolStatus.CONTACTED]: 'Contacted',
    [TalentPoolStatus.HIRED]: 'Hired',
    [TalentPoolStatus.NOT_INTERESTED]: 'Not Interested',
    [TalentPoolStatus.ARCHIVED]: 'Archived'
  };
  return labels[status];
}

export function getTalentPoolStatusColor(status: TalentPoolStatus): string {
  const colors: Record<TalentPoolStatus, string> = {
    [TalentPoolStatus.ACTIVE]: 'bg-green-100 text-green-800 border-green-200',
    [TalentPoolStatus.CONTACTED]: 'bg-blue-100 text-blue-800 border-blue-200',
    [TalentPoolStatus.HIRED]: 'bg-purple-100 text-purple-800 border-purple-200',
    [TalentPoolStatus.NOT_INTERESTED]: 'bg-gray-100 text-gray-800 border-gray-200',
    [TalentPoolStatus.ARCHIVED]: 'bg-yellow-100 text-yellow-800 border-yellow-200'
  };
  return colors[status];
}

export function getRatingStars(rating: number | null): string {
  if (!rating) return '☆☆☆☆☆';
  return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

export function getRatingColor(rating: number | null): string {
  if (!rating) return 'text-gray-400';
  if (rating >= 4) return 'text-green-600';
  if (rating >= 3) return 'text-yellow-600';
  return 'text-red-600';
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
  return `${Math.floor(diffDays / 365)} years ago`;
}
