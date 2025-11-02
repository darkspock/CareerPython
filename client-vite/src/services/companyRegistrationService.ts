// Company registration API service
import { ApiClient } from '../lib/api';
import type {
  CompanyRegistrationRequest,
  CompanyRegistrationResponse,
  LinkUserRequest,
  LinkUserResponse,
  CheckEmailResponse
} from '../types/companyRegistration';

export class CompanyRegistrationService {
  /**
   * Register a new company with a new user
   */
  static async registerCompanyWithUser(
    data: CompanyRegistrationRequest
  ): Promise<CompanyRegistrationResponse> {
    try {
      const response = await ApiClient.post<CompanyRegistrationResponse>(
        '/company/register',
        data
      );
      return response;
    } catch (error: any) {
      console.error('Error registering company:', error);
      
      // Translate error messages for better UX
      if (error.message.includes('domain') || error.message.includes('dominio')) {
        if (error.message.includes('already') || error.message.includes('ya existe')) {
          throw new Error('Este dominio ya está en uso. Por favor, elige otro.');
        }
        throw new Error('El dominio ingresado no es válido.');
      }
      if (error.message.includes('email') || error.message.includes('correo')) {
        if (error.message.includes('already') || error.message.includes('ya está')) {
          throw new Error('Este email ya está registrado. ¿Ya tienes una cuenta?');
        }
        throw new Error('El email ingresado no es válido.');
      }
      if (error.message.includes('password') || error.message.includes('contraseña')) {
        throw new Error('La contraseña no cumple con los requisitos mínimos.');
      }
      
      throw new Error(error.message || 'Error al registrar la empresa. Intenta nuevamente.');
    }
  }

  /**
   * Link an existing user to a new company
   */
  static async linkExistingUserToCompany(
    data: LinkUserRequest
  ): Promise<LinkUserResponse> {
    try {
      const response = await ApiClient.post<LinkUserResponse>(
        '/company/register/link-user',
        data
      );
      return response;
    } catch (error: any) {
      console.error('Error linking user to company:', error);
      
      // Translate error messages
      if (error.message.includes('invalid') || error.message.includes('incorrect')) {
        throw new Error('Email o contraseña incorrectos.');
      }
      if (error.message.includes('domain') || error.message.includes('dominio')) {
        if (error.message.includes('already') || error.message.includes('ya existe')) {
          throw new Error('Este dominio ya está en uso.');
        }
        throw new Error('El dominio ingresado no es válido.');
      }
      
      throw new Error(error.message || 'Error al vincular la cuenta. Intenta nuevamente.');
    }
  }

  /**
   * Check if an email already exists
   * Optional: For checking before registration
   */
  static async checkEmailExists(email: string): Promise<CheckEmailResponse> {
    try {
      const response = await ApiClient.get<CheckEmailResponse>(
        `/users/check-email?email=${encodeURIComponent(email)}`
      );
      return response;
    } catch (error: any) {
      console.error('Error checking email:', error);
      // If endpoint doesn't exist, return default response
      return { exists: false, can_link: false };
    }
  }
}

