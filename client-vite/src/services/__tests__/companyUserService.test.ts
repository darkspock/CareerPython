/**
 * Unit tests for CompanyUserService
 * 
 * Tests the authenticated company user API endpoints:
 * - inviteUser
 * - getCompanyUsers
 * - removeCompanyUser
 * - assignRoleToUser
 * - getUserPermissions
 */

import { CompanyUserService } from '../companyUserService';
import { api } from '../../lib/api';
import type {
  InviteCompanyUserRequest,
  AssignRoleRequest,
  CompanyUsersFilters,
  CompanyUser,
  CompanyUserPermissions,
  UserInvitationLink
} from '../../types/companyUser';

// Mock api
jest.mock('../../lib/api');
const mockedApi = api as jest.Mocked<typeof api>;

describe('CompanyUserService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('inviteUser', () => {
    it('should invite user successfully', async () => {
      const mockLink: UserInvitationLink = {
        invitation_id: 'inv-123',
        invitation_link: 'https://example.com/invitations/accept?token=token-abc',
        expires_at: new Date(Date.now() + 86400000).toISOString(),
        email: 'newuser@example.com'
      };

      const request: InviteCompanyUserRequest = {
        email: 'newuser@example.com',
        role: 'recruiter'
      };

      mockedApi.authenticatedRequest = jest.fn().mockResolvedValue(mockLink);

      const result = await CompanyUserService.inviteUser(
        'comp-123',
        request,
        'user-456'
      );

      expect(result).toEqual(mockLink);
      expect(mockedApi.authenticatedRequest).toHaveBeenCalledWith(
        '/company/comp-123/users/invite?current_user_id=user-456',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(request)
        })
      );
    });

    it('should handle error when email already exists', async () => {
      const request: InviteCompanyUserRequest = {
        email: 'existing@example.com',
        role: 'recruiter'
      };

      mockedApi.authenticatedRequest = jest.fn().mockRejectedValue(
        new Error('Email already exists in company')
      );

      await expect(
        CompanyUserService.inviteUser('comp-123', request, 'user-456')
      ).rejects.toThrow('Email already exists in company');
    });
  });

  describe('getCompanyUsers', () => {
    it('should fetch company users successfully', async () => {
      const mockUsers: CompanyUser[] = [
        {
          id: 'cu-1',
          company_id: 'comp-123',
          user_id: 'user-1',
          role: 'admin',
          permissions: {
            can_manage_users: true,
            can_manage_positions: true,
            can_view_resumes: true,
            can_manage_resumes: true,
            can_invite_users: true,
            can_assign_roles: true
          },
          status: 'active',
          created_at: new Date().toISOString()
        }
      ];

      mockedApi.authenticatedRequest = jest.fn().mockResolvedValue(mockUsers);

      const result = await CompanyUserService.getCompanyUsers('comp-123');

      expect(result).toEqual(mockUsers);
      expect(mockedApi.authenticatedRequest).toHaveBeenCalledWith('/company/comp-123/users');
    });

    it('should fetch company users with filters', async () => {
      const filters: CompanyUsersFilters = {
        active_only: true,
        role: 'admin',
        search: 'test'
      };

      mockedApi.authenticatedRequest = jest.fn().mockResolvedValue([]);

      await CompanyUserService.getCompanyUsers('comp-123', filters);

      expect(mockedApi.authenticatedRequest).toHaveBeenCalledWith(
        '/company/comp-123/users?active_only=true&role=admin&search=test'
      );
    });
  });

  describe('removeCompanyUser', () => {
    it('should remove company user successfully', async () => {
      mockedApi.authenticatedRequest = jest.fn().mockResolvedValue({});

      await CompanyUserService.removeCompanyUser(
        'comp-123',
        'user-456',
        'current-user-789'
      );

      expect(mockedApi.authenticatedRequest).toHaveBeenCalledWith(
        '/company/comp-123/users/user-456?current_user_id=current-user-789',
        expect.objectContaining({
          method: 'DELETE'
        })
      );
    });

    it('should handle error when trying to remove last admin', async () => {
      mockedApi.authenticatedRequest = jest.fn().mockRejectedValue(
        new Error('Cannot remove the last administrator')
      );

      await expect(
        CompanyUserService.removeCompanyUser('comp-123', 'user-456', 'current-user-789')
      ).rejects.toThrow('Cannot remove the last administrator');
    });

    it('should handle error when trying to remove self', async () => {
      mockedApi.authenticatedRequest = jest.fn().mockRejectedValue(
        new Error('Cannot remove yourself')
      );

      await expect(
        CompanyUserService.removeCompanyUser('comp-123', 'user-456', 'user-456')
      ).rejects.toThrow('Cannot remove yourself');
    });
  });

  describe('assignRoleToUser', () => {
    it('should assign role to user successfully', async () => {
      const request: AssignRoleRequest = {
        role: 'admin'
      };

      const mockUser: CompanyUser = {
        id: 'cu-1',
        company_id: 'comp-123',
        user_id: 'user-456',
        role: 'admin',
        permissions: {
          can_manage_users: true,
          can_manage_positions: true,
          can_view_resumes: true,
          can_manage_resumes: true,
          can_invite_users: true,
          can_assign_roles: true
        },
        status: 'active',
        created_at: new Date().toISOString()
      };

      mockedApi.authenticatedRequest = jest.fn().mockResolvedValue(mockUser);

      const result = await CompanyUserService.assignRoleToUser(
        'comp-123',
        'user-456',
        request
      );

      expect(result).toEqual(mockUser);
      expect(mockedApi.authenticatedRequest).toHaveBeenCalledWith(
        '/company/comp-123/users/user-456/role',
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify(request)
        })
      );
    });
  });

  describe('getUserPermissions', () => {
    it('should fetch user permissions successfully', async () => {
      const mockPermissions: CompanyUserPermissions = {
        can_manage_users: true,
        can_manage_positions: true,
        can_view_resumes: true,
        can_manage_resumes: false,
        can_invite_users: true,
        can_assign_roles: true
      };

      mockedApi.authenticatedRequest = jest.fn().mockResolvedValue(mockPermissions);

      const result = await CompanyUserService.getUserPermissions(
        'comp-123',
        'user-456'
      );

      expect(result).toEqual(mockPermissions);
      expect(mockedApi.authenticatedRequest).toHaveBeenCalledWith(
        '/company/comp-123/users/user/user-456/permissions'
      );
    });
  });
});

