/**
 * Custom hooks for company user operations
 * 
 * Provides React hooks for managing company user-related operations:
 * - useCompanyUsers: Fetch list of company users with filters
 * - useInviteUser: Invite a new user to the company
 * - useRemoveUser: Remove a user from the company
 * - useAssignRole: Assign or change a user's role
 * - useUserPermissions: Fetch a user's permissions
 */

// Custom hooks for company user operations
import { useState, useEffect, useCallback } from 'react';
import { CompanyUserService } from '../services/companyUserService';
import { getCompanyId, getUserId } from '../utils/companyAuth';
import type {
  CompanyUser,
  CompanyUsersFilters,
  InviteCompanyUserRequest,
  AssignRoleRequest,
  UserInvitationLink,
  CompanyUserPermissions
} from '../types/companyUser';

/**
 * Hook to fetch company users
 */
export function useCompanyUsers(filters?: CompanyUsersFilters) {
  const [users, setUsers] = useState<CompanyUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const companyId = getCompanyId();

  const fetchUsers = useCallback(async () => {
    if (!companyId) {
      setError('No se pudo obtener el ID de la empresa');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await CompanyUserService.getCompanyUsers(companyId, filters);
      setUsers(data);
    } catch (err: any) {
      setError(err.message || 'Error al cargar usuarios');
      setUsers([]);
    } finally {
      setLoading(false);
    }
  }, [companyId, filters]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const refresh = useCallback(() => {
    fetchUsers();
  }, [fetchUsers]);

  return {
    users,
    loading,
    error,
    refresh,
    companyId
  };
}

/**
 * Hook to invite a user
 */
export function useInviteUser() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [invitationLink, setInvitationLink] = useState<UserInvitationLink | null>(null);

  const companyId = getCompanyId();
  const currentUserId = getUserId();

  const inviteUser = useCallback(async (request: InviteCompanyUserRequest) => {
    if (!companyId || !currentUserId) {
      setError('No se pudo obtener el ID de la empresa o del usuario actual');
      return null;
    }

    try {
      setLoading(true);
      setError(null);
      setInvitationLink(null);

      const link = await CompanyUserService.inviteUser(companyId, request, currentUserId);
      setInvitationLink(link);
      return link;
    } catch (err: any) {
      setError(err.message || 'Error al invitar usuario');
      return null;
    } finally {
      setLoading(false);
    }
  }, [companyId, currentUserId]);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setInvitationLink(null);
  }, []);

  return {
    inviteUser,
    loading,
    error,
    invitationLink,
    reset,
    companyId,
    currentUserId
  };
}

/**
 * Hook to remove a company user
 */
export function useRemoveUser() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const companyId = getCompanyId();
  const currentUserId = getUserId();

  const removeUser = useCallback(async (userId: string) => {
    if (!companyId || !currentUserId) {
      setError('No se pudo obtener el ID de la empresa o del usuario actual');
      return false;
    }

    try {
      setLoading(true);
      setError(null);

      await CompanyUserService.removeCompanyUser(companyId, userId, currentUserId);
      return true;
    } catch (err: any) {
      setError(err.message || 'Error al eliminar usuario');
      return false;
    } finally {
      setLoading(false);
    }
  }, [companyId, currentUserId]);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
  }, []);

  return {
    removeUser,
    loading,
    error,
    reset,
    companyId,
    currentUserId
  };
}

/**
 * Hook to assign a role to a user
 */
export function useAssignRole() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const companyId = getCompanyId();

  const assignRole = useCallback(async (userId: string, request: AssignRoleRequest) => {
    if (!companyId) {
      setError('No se pudo obtener el ID de la empresa');
      return false;
    }

    try {
      setLoading(true);
      setError(null);

      await CompanyUserService.assignRoleToUser(companyId, userId, request);
      return true;
    } catch (err: any) {
      setError(err.message || 'Error al asignar rol');
      return false;
    } finally {
      setLoading(false);
    }
  }, [companyId]);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
  }, []);

  return {
    assignRole,
    loading,
    error,
    reset,
    companyId
  };
}

/**
 * Hook to get user permissions
 */
export function useUserPermissions(userId: string | null) {
  const [permissions, setPermissions] = useState<CompanyUserPermissions | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const companyId = getCompanyId();

  const fetchPermissions = useCallback(async () => {
    if (!companyId || !userId) {
      setError('No se pudo obtener el ID de la empresa o del usuario');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await CompanyUserService.getUserPermissions(companyId, userId);
      setPermissions(data);
    } catch (err: any) {
      setError(err.message || 'Error al cargar permisos');
      setPermissions(null);
    } finally {
      setLoading(false);
    }
  }, [companyId, userId]);

  useEffect(() => {
    if (userId) {
      fetchPermissions();
    }
  }, [userId, fetchPermissions]);

  const refresh = useCallback(() => {
    fetchPermissions();
  }, [fetchPermissions]);

  return {
    permissions,
    loading,
    error,
    refresh
  };
}

