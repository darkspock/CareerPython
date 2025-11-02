// Invitation API service (public endpoints)
import { ApiClient } from '../lib/api';
import type {
  CompanyUserInvitation,
  AcceptInvitationRequest
} from '../types/companyUser';

export class InvitationService {
  private static readonly BASE_PATH = '/invitations';

  /**
   * Get invitation details by token (public endpoint)
   * @param token - Invitation token from URL
   * @returns CompanyUserInvitation details
   */
  static async getInvitationByToken(token: string): Promise<CompanyUserInvitation> {
    try {
      const response = await ApiClient.get<CompanyUserInvitation>(
        `${this.BASE_PATH}/${token}`
      );
      return response;
    } catch (error: any) {
      console.error('Error fetching invitation:', error);
      
      // Translate error messages for better UX
      if (error.message.includes('not found') || error.message.includes('404')) {
        throw new Error('La invitación no existe o el token es inválido');
      }
      if (error.message.includes('expired') || error.message.includes('expirada')) {
        throw new Error('La invitación ha expirado. Por favor, solicita una nueva invitación.');
      }
      
      throw error;
    }
  }

  /**
   * Accept a user invitation (public endpoint)
   * @param request - Accept invitation request data
   * @returns Success message
   */
  static async acceptInvitation(
    request: AcceptInvitationRequest
  ): Promise<{ message: string }> {
    try {
      const response = await ApiClient.post<{ message: string }>(
        `${this.BASE_PATH}/accept`,
        request
      );
      return response;
    } catch (error: any) {
      console.error('Error accepting invitation:', error);
      
      // Translate error messages for better UX
      if (error.message.includes('invalid') || error.message.includes('inválido')) {
        throw new Error('El token de invitación es inválido');
      }
      if (error.message.includes('expired') || error.message.includes('expirada')) {
        throw new Error('La invitación ha expirado. Por favor, solicita una nueva invitación.');
      }
      if (error.message.includes('already') || error.message.includes('ya está')) {
        throw new Error('Este email ya está vinculado a la empresa');
      }
      if (error.message.includes('password') || error.message.includes('contraseña')) {
        throw new Error('La contraseña no cumple con los requisitos mínimos');
      }
      
      throw error;
    }
  }
}

