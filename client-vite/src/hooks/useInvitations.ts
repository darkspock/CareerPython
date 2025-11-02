/**
 * Custom hooks for invitation operations
 * 
 * Provides React hooks for managing invitation-related operations:
 * - useInvitation: Fetch invitation by token
 * - useAcceptInvitation: Accept an invitation
 */

// Custom hooks for invitation operations
import { useState, useEffect, useCallback } from 'react';
import { InvitationService } from '../services/invitationService';
import type {
  CompanyUserInvitation,
  AcceptInvitationRequest
} from '../types/companyUser';

/**
 * Hook to fetch an invitation by token
 * 
 * Automatically fetches invitation details when token is provided.
 * 
 * @param {string|null} token - The invitation token
 * @returns {Object} Hook return value
 * @returns {CompanyUserInvitation|null} return.invitation - The invitation data
 * @returns {boolean} return.loading - Whether the request is in progress
 * @returns {string|null} return.error - Error message if request failed
 * @returns {Function} return.refresh - Function to manually refresh the invitation
 */
export function useInvitation(token: string | null) {
  const [invitation, setInvitation] = useState<CompanyUserInvitation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchInvitation = useCallback(async () => {
    if (!token) {
      setError('Token no proporcionado');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await InvitationService.getInvitationByToken(token);
      setInvitation(data);
    } catch (err: any) {
      setError(err.message || 'Error al cargar la invitación');
      setInvitation(null);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchInvitation();
  }, [fetchInvitation]);

  const refresh = useCallback(() => {
    fetchInvitation();
  }, [fetchInvitation]);

  return {
    invitation,
    loading,
    error,
    refresh
  };
}

/**
 * Hook to accept an invitation
 * 
 * Provides mutation function to accept an invitation and handles
 * loading, error, and success states.
 * 
 * @returns {Object} Hook return value
 * @returns {Function} return.acceptInvitation - Function to accept invitation
 * @returns {boolean} return.loading - Whether the request is in progress
 * @returns {string|null} return.error - Error message if request failed
 * @returns {boolean} return.success - Whether the invitation was accepted successfully
 * @returns {Function} return.reset - Function to reset the hook state
 */
export function useAcceptInvitation() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const acceptInvitation = useCallback(async (request: AcceptInvitationRequest) => {
    try {
      setLoading(true);
      setError(null);
      setSuccess(false);

      await InvitationService.acceptInvitation(request);
      
      setSuccess(true);
      return true;
    } catch (err: any) {
      setError(err.message || 'Error al aceptar la invitación');
      setSuccess(false);
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setSuccess(false);
  }, []);

  return {
    acceptInvitation,
    loading,
    error,
    success,
    reset
  };
}

