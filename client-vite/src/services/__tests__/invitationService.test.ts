/**
 * Unit tests for InvitationService
 * 
 * Tests the public invitation API endpoints:
 * - getInvitationByToken
 * - acceptInvitation
 */

import { InvitationService } from '../invitationService';
import { api } from '../../lib/api';
import type { CompanyUserInvitation, AcceptInvitationRequest } from '../../types/companyUser';

// Mock api
jest.mock('../../lib/api');
const mockedApi = api as jest.Mocked<typeof api>;

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
        token: 'token-abc',
        status: 'pending',
        expires_at: new Date(Date.now() + 86400000).toISOString(),
        invitation_link: 'https://example.com/invitations/accept?token=token-abc'
      };

      mockedApi.get = jest.fn().mockResolvedValue(mockInvitation);

      const result = await InvitationService.getInvitationByToken('token-abc');

      expect(result).toEqual(mockInvitation);
      expect(mockedApi.get).toHaveBeenCalledWith('/invitations/token-abc');
    });

    it('should handle error when invitation is not found', async () => {
      mockedApi.get = jest.fn().mockRejectedValue(
        new Error('Invitation not found')
      );

      await expect(
        InvitationService.getInvitationByToken('invalid-token')
      ).rejects.toThrow('Invitation not found');
    });

    it('should handle error when invitation is expired', async () => {
      mockedApi.get = jest.fn().mockRejectedValue(
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
      mockedApi.post = jest.fn().mockResolvedValue(mockResponse);

      await InvitationService.acceptInvitation(request);

      expect(mockedApi.post).toHaveBeenCalledWith('/invitations/accept', request);
    });

    it('should accept invitation for existing user successfully', async () => {
      const request: AcceptInvitationRequest = {
        token: 'token-abc',
        user_id: 'user-123'
      };

      const mockResponse = { message: 'Invitation accepted successfully' };
      mockedApi.post = jest.fn().mockResolvedValue(mockResponse);

      await InvitationService.acceptInvitation(request);

      expect(mockedApi.post).toHaveBeenCalledWith('/invitations/accept', request);
    });

    it('should handle error when token is invalid', async () => {
      const request: AcceptInvitationRequest = {
        token: 'invalid-token',
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      };

      mockedApi.post = jest.fn().mockRejectedValue(
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

      mockedApi.post = jest.fn().mockRejectedValue(
        new Error('Email already exists in company')
      );

      await expect(
        InvitationService.acceptInvitation(request)
      ).rejects.toThrow('Email already exists in company');
    });
  });
});

