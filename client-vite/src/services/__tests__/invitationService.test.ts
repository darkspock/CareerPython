/**
 * Unit tests for InvitationService
 * 
 * Tests the public invitation API endpoints:
 * - getInvitationByToken
 * - acceptInvitation
 */

import { InvitationService } from '../invitationService';
import { ApiClient } from '../../lib/api';
import type { CompanyUserInvitation, AcceptInvitationRequest } from '../../types/companyUser';

// Mock ApiClient
jest.mock('../../lib/api', () => ({
  ApiClient: {
    get: jest.fn(),
    post: jest.fn()
  }
}));
const mockedApiClient = ApiClient as jest.Mocked<typeof ApiClient>;

describe('InvitationService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getInvitationByToken', () => {
    it('should fetch invitation by token successfully', async () => {
      const mockInvitation: CompanyUserInvitation = {
        id: 'inv-123',
        company_id: 'comp-456',
        email: 'test@example.com',
        invited_by_user_id: 'user-123',
        token: 'token-abc',
        status: 'pending',
        expires_at: new Date(Date.now() + 86400000).toISOString(),
        accepted_at: null,
        rejected_at: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        invitation_link: 'https://example.com/invitations/accept?token=token-abc'
      };

      mockedApiClient.get = jest.fn().mockResolvedValue(mockInvitation);

      const result = await InvitationService.getInvitationByToken('token-abc');

      expect(result).toEqual(mockInvitation);
      expect(mockedApiClient.get).toHaveBeenCalledWith('/invitations/token-abc', undefined);
    });

    it('should handle error when invitation is not found', async () => {
      mockedApiClient.get = jest.fn().mockRejectedValue(
        new Error('Invitation not found')
      );

      await expect(
        InvitationService.getInvitationByToken('invalid-token')
      ).rejects.toThrow('Invitation not found');
    });

    it('should handle error when invitation is expired', async () => {
      mockedApiClient.get = jest.fn().mockRejectedValue(
        new Error('Invitation expired')
      );

      await expect(
        InvitationService.getInvitationByToken('expired-token')
      ).rejects.toThrow('Invitation expired');
    });
  });

  describe('acceptInvitation', () => {
    it('should accept invitation for new user successfully', async () => {
      const request: AcceptInvitationRequest = {
        token: 'token-abc',
        email: 'newuser@example.com',
        name: 'New User',
        password: 'password123'
      };

      const mockResponse = { message: 'Invitation accepted successfully' };
      mockedApiClient.post = jest.fn().mockResolvedValue(mockResponse);

      await InvitationService.acceptInvitation(request);

      expect(mockedApiClient.post).toHaveBeenCalledWith('/invitations/accept', request, undefined);
    });

    it('should accept invitation for existing user successfully', async () => {
      const request: AcceptInvitationRequest = {
        token: 'token-abc',
        user_id: 'user-123'
      };

      const mockResponse = { message: 'Invitation accepted successfully' };
      mockedApiClient.post = jest.fn().mockResolvedValue(mockResponse);

      await InvitationService.acceptInvitation(request);

      expect(mockedApiClient.post).toHaveBeenCalledWith('/invitations/accept', request, undefined);
    });

    it('should handle error when token is invalid', async () => {
      const request: AcceptInvitationRequest = {
        token: 'invalid-token',
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      };

      mockedApiClient.post = jest.fn().mockRejectedValue(
        new Error('Invalid invitation token')
      );

      await expect(
        InvitationService.acceptInvitation(request)
      ).rejects.toThrow('Invalid invitation token');
    });

    it('should handle error when email already exists', async () => {
      const request: AcceptInvitationRequest = {
        token: 'token-abc',
        email: 'existing@example.com',
        name: 'Test User',
        password: 'password123'
      };

      mockedApiClient.post = jest.fn().mockRejectedValue(
        new Error('Email already exists in company')
      );

      await expect(
        InvitationService.acceptInvitation(request)
      ).rejects.toThrow('Email already exists in company');
    });
  });
});

