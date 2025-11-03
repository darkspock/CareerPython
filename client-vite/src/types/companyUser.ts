// Company User and Invitation types

export type CompanyUserRole = 'admin' | 'recruiter' | 'viewer';

export type CompanyUserStatus = 'active' | 'inactive';

export type CompanyUserInvitationStatus =
  | 'pending'
  | 'accepted'
  | 'rejected'
  | 'expired'
  | 'cancelled';

export interface CompanyUserPermissions {
  can_create_candidates: boolean;
  can_delete_candidates: boolean;
  can_view_candidates: boolean;
  can_invite_candidates: boolean;
  can_add_comments: boolean;
  can_manage_users: boolean;
  can_change_settings: boolean;
  can_change_phase: boolean;
  can_view_analytics: boolean;
}

export interface CompanyUser {
  id: string;
  company_id: string;
  user_id: string;
  email?: string;
  role: CompanyUserRole;
  permissions: CompanyUserPermissions;
  status: CompanyUserStatus;
  company_roles?: string[]; // IDs of assigned CompanyRole
  created_at: string;
  updated_at: string;
}

export interface CompanyUserInvitation {
  id: string;
  company_id: string;
  email: string;
  invited_by_user_id: string;
  token: string;
  status: CompanyUserInvitationStatus;
  expires_at: string;
  accepted_at: string | null;
  rejected_at: string | null;
  created_at: string;
  updated_at: string;
  invitation_link: string;
}

export interface UserInvitationLink {
  invitation_id: string;
  invitation_link: string;
  expires_at: string;
  email: string;
}

export interface InviteCompanyUserRequest {
  email: string;
  role?: CompanyUserRole;
}

export interface AcceptInvitationRequest {
  token: string;
  // Caso A: Usuario nuevo
  email?: string;
  name?: string;
  password?: string;
  // Caso B: Usuario existente
  user_id?: string;
}

export interface AssignRoleRequest {
  role: CompanyUserRole;
  permissions?: Partial<CompanyUserPermissions>;
  company_roles?: string[]; // IDs of CompanyRole to assign
}

export interface CompanyUsersFilters {
  active_only?: boolean;
  role?: CompanyUserRole;
  search?: string;
}

// Constants for UI
export const COMPANY_USER_ROLE_OPTIONS = [
  { value: 'admin', label: 'Administrador' },
  { value: 'recruiter', label: 'Reclutador' },
  { value: 'viewer', label: 'Visualizador' }
] as const;

export const COMPANY_USER_STATUS_OPTIONS = [
  { value: 'active', label: 'Activo' },
  { value: 'inactive', label: 'Inactivo' }
] as const;

export const COMPANY_USER_INVITATION_STATUS_OPTIONS = [
  { value: 'pending', label: 'Pendiente' },
  { value: 'accepted', label: 'Aceptada' },
  { value: 'rejected', label: 'Rechazada' },
  { value: 'expired', label: 'Expirada' },
  { value: 'cancelled', label: 'Cancelada' }
] as const;

// Helper functions
export const getCompanyUserRoleColor = (role: CompanyUserRole): string => {
  switch (role) {
    case 'admin': return 'bg-purple-100 text-purple-800';
    case 'recruiter': return 'bg-blue-100 text-blue-800';
    case 'viewer': return 'bg-gray-100 text-gray-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getCompanyUserRoleLabel = (role: CompanyUserRole): string => {
  const option = COMPANY_USER_ROLE_OPTIONS.find(opt => opt.value === role);
  return option?.label || role;
};

export const getCompanyUserStatusColor = (status: CompanyUserStatus): string => {
  switch (status) {
    case 'active': return 'bg-green-100 text-green-800';
    case 'inactive': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getInvitationStatusColor = (status: CompanyUserInvitationStatus): string => {
  switch (status) {
    case 'pending': return 'bg-yellow-100 text-yellow-800';
    case 'accepted': return 'bg-green-100 text-green-800';
    case 'rejected': return 'bg-red-100 text-red-800';
    case 'expired': return 'bg-gray-100 text-gray-800';
    case 'cancelled': return 'bg-gray-100 text-gray-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getInvitationStatusLabel = (status: CompanyUserInvitationStatus): string => {
  const option = COMPANY_USER_INVITATION_STATUS_OPTIONS.find(opt => opt.value === status);
  return option?.label || status;
};

export const isInvitationExpired = (expiresAt: string): boolean => {
  return new Date(expiresAt) < new Date();
};

export const getDaysUntilExpiration = (expiresAt: string): number => {
  const now = new Date();
  const expires = new Date(expiresAt);
  const diffTime = expires.getTime() - now.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
};

