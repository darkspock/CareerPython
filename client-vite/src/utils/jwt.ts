/**
 * JWT Token utilities for safe token decoding
 */

export interface JWTPayload {
  sub?: string;
  email?: string;
  exp?: number;
  iat?: number;
  [key: string]: any;
}

/**
 * Safely decode a JWT token payload
 * @param token - The JWT token string
 * @returns The decoded payload or null if invalid
 */
export function decodeJWTPayload(token: string): JWTPayload | null {
  try {
    // Verificar que el token tenga el formato JWT (3 partes separadas por puntos)
    const tokenParts = token.split('.');
    if (tokenParts.length !== 3) {
      console.warn('Token does not have JWT format (3 parts)');
      return null;
    }

    // Decodificar la parte del payload (segunda parte)
    let base64Payload = tokenParts[1];

    // Agregar padding si es necesario para base64
    while (base64Payload.length % 4) {
      base64Payload += '=';
    }

    const payload = JSON.parse(atob(base64Payload));
    return payload;
  } catch (error) {
    console.error('Error decoding JWT token:', error);
    return null;
  }
}

/**
 * Get user email from JWT token
 * @param token - The JWT token string
 * @returns The user email or empty string
 */
export function getUserEmailFromToken(token: string): string {
  const payload = decodeJWTPayload(token);
  return payload?.sub || payload?.email || '';
}

/**
 * Check if a JWT token is expired
 * @param token - The JWT token string
 * @returns true if expired, false otherwise
 */
export function isTokenExpired(token: string): boolean {
  const payload = decodeJWTPayload(token);
  if (!payload || !payload.exp) {
    return true; // Assume expired if no expiration time
  }

  const currentTime = Math.floor(Date.now() / 1000);
  return payload.exp < currentTime;
}

/**
 * All session-related localStorage keys.
 * Add new session keys here - this is the single source of truth.
 */
const SESSION_KEYS = [
  "access_token",
  "candidate_id",
  "job_position_id",
  "application_id",
  "wants_cv_help",
  "has_pdf",
] as const;

/**
 * Clear all authentication/session data from localStorage.
 * This is the single source of truth for session cleanup.
 * When adding new session-related localStorage items, add them to SESSION_KEYS above.
 */
export function clearAuthData(): void {
  SESSION_KEYS.forEach(key => localStorage.removeItem(key));
}