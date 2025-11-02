// Company User API service (authenticated endpoints)
import { ApiClient } from '../lib/api';
import type {
  CompanyUser,
  CompanyUserPermissions,
  InviteCompanyUserRequest,
  AssignRoleRequest,
  UserInvitationLink,
  CompanyUsersFilters
} from '../types/companyUser';

export class CompanyUserService {
  private static readonly BASE_PATH = '/company';

  /**
   * Invite a user to the company
   * @param companyId - Company ID
   * @param request - Invitation request data
   * @param currentUserId - Current user ID (from auth context)
   * @returns Invitation link for sharing
   */
  static async inviteUser(
    companyId: string,
    request: InviteCompanyUserRequest,
    currentUserId: string
  ): Promise<UserInvitationLink> {
    try {
      const response = await ApiClient.authenticatedRequest<UserInvitationLink>(
        `${this.BASE_PATH}/${companyId}/users/invite?current_user_id=${currentUserId}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request),
        }
      );
      return response;
    } catch (error: any) {
      console.error('Error inviting user:', error);
      
      // Translate error messages for better UX
      if (error.message.includes('already') || error.message.includes('ya está')) {
        throw new Error('Este email ya está vinculado a la empresa');
      }
      if (error.message.includes('invalid') || error.message.includes('inválido')) {
        throw new Error('Email inválido');
      }
      if (error.message.includes('permission') || error.message.includes('permisos')) {
        throw new Error('No tienes permisos para invitar usuarios');
      }
      
      throw error;
    }
  }

  /**
   * Get list of company users
   * @param companyId - Company ID
   * @param filters - Optional filters (active_only, role, search)
   * @returns Array of company users
   */
  static async getCompanyUsers(
    companyId: string,
    filters?: CompanyUsersFilters
  ): Promise<CompanyUser[]> {
    try {
      const queryParams = new URLSearchParams();
      
      if (filters?.active_only !== undefined) {
        queryParams.append('active_only', filters.active_only.toString());
      }
      if (filters?.role) {
        queryParams.append('role', filters.role);
      }
      if (filters?.search) {
        queryParams.append('search', filters.search);
      }

      const endpoint = `${this.BASE_PATH}/${companyId}/users${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
      
      const response = await ApiClient.authenticatedRequest<CompanyUser[]>(endpoint);
      return response;
    } catch (error: any) {
      console.error('Error fetching company users:', error);
      throw error;
    }
  }

  /**
   * Remove a user from the company
   * @param companyId - Company ID
   * @param userId - User ID to remove
   * @param currentUserId - Current user ID (from auth context)
   */
  static async removeCompanyUser(
    companyId: string,
    userId: string,
    currentUserId: string
  ): Promise<void> {
    try {
      await ApiClient.authenticatedRequest(
        `${this.BASE_PATH}/${companyId}/users/${userId}?current_user_id=${currentUserId}`,
        {
          method: 'DELETE',
        }
      );
    } catch (error: any) {
      console.error('Error removing company user:', error);
      
      // Translate error messages for better UX
      if (error.message.includes('last admin') || error.message.includes('último administrador')) {
        throw new Error('No se puede eliminar el último administrador de la empresa');
      }
      if (error.message.includes('yourself') || error.message.includes('eliminarte')) {
        throw new Error('No puedes eliminarte a ti mismo');
      }
      if (error.message.includes('permission') || error.message.includes('permisos')) {
        throw new Error('No tienes permisos para eliminar usuarios');
      }
      
      throw error;
    }
  }

  /**
   * Assign a role to a company user
   * @param companyId - Company ID
   * @param userId - User ID
   * @param request - Role assignment request
   * @returns Updated company user
   */
  static async assignRoleToUser(
    companyId: string,
    userId: string,
    request: AssignRoleRequest
  ): Promise<CompanyUser> {
    try {
      const response = await ApiClient.authenticatedRequest<CompanyUser>(
        `${this.BASE_PATH}/${companyId}/users/${userId}/role`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request),
        }
      );
      return response;
    } catch (error: any) {
      console.error('Error assigning role:', error);
      
      // Translate error messages for better UX
      if (error.message.includes('last admin') || error.message.includes('último administrador')) {
        throw new Error('No se puede quitar el rol de administrador al último admin de la empresa');
      }
      if (error.message.includes('invalid') || error.message.includes('inválido')) {
        throw new Error('Rol inválido');
      }
      if (error.message.includes('permission') || error.message.includes('permisos')) {
        throw new Error('No tienes permisos para cambiar roles');
      }
      
      throw error;
    }
  }

  /**
   * Get user permissions
   * @param companyId - Company ID
   * @param userId - User ID
   * @returns User permissions
   * @note This endpoint may need to be verified in the backend implementation
   */
  static async getUserPermissions(
    companyId: string,
    userId: string
  ): Promise<CompanyUserPermissions> {
    try {
      // Note: This endpoint pattern may need adjustment based on backend implementation
      const response = await ApiClient.authenticatedRequest<CompanyUserPermissions>(
        `${this.BASE_PATH}/${companyId}/users/user/${userId}/permissions`
      );
      return response;
    } catch (error: any) {
      console.error('Error fetching user permissions:', error);
      throw error;
    }
  }
}

