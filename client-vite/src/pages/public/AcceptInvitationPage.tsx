/**
 * AcceptInvitationPage Component
 * 
 * Public page for accepting company user invitations. Supports two flows:
 * 1. New user: Create account and accept invitation
 * 2. Existing user: Accept invitation and link account to company
 * 
 * Features:
 * - Token validation from URL query params
 * - Conditional form rendering based on user login status
 * - Form validation (email, name, password)
 * - Error handling and success states
 * - Automatic redirection after acceptance
 * 
 * @component
 */
// Public page for accepting user invitations
import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useInvitation, useAcceptInvitation } from '../../hooks/useInvitations';
import { decodeJWTPayload } from '../../utils/jwt';
import InvitationDetails from '../../components/invitations/InvitationDetails';
import type {
  AcceptInvitationRequest
} from '../../types/companyUser';
import {
  isInvitationExpired
} from '../../types/companyUser';
import {
  Mail,
  Lock,
  User,
  CheckCircle,
  AlertCircle,
  Loader2,
  ArrowRight
} from 'lucide-react';

export default function AcceptInvitationPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');

  const { invitation, loading, error: invitationError, refresh: _refreshInvitation } = useInvitation(token);
  const { acceptInvitation, loading: submitting, error: acceptError, success, reset: resetAccept } = useAcceptInvitation();
  const [error, setError] = useState<string | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Form state for new user
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    // Check if user is logged in
    const accessToken = localStorage.getItem('access_token');
    setIsLoggedIn(!!accessToken);

    if (!token) {
      setError('Token de invitación no proporcionado');
    }
  }, [token]);

  useEffect(() => {
    if (invitation) {
      setEmail(invitation.email); // Pre-fill email from invitation
      
      // Check if invitation is valid for acceptance
      if (invitation.status !== 'pending') {
        setError(`Esta invitación está en estado: ${invitation.status}`);
      } else if (isInvitationExpired(invitation.expires_at)) {
        setError('Esta invitación ha expirado');
      }
    }
  }, [invitation]);

  useEffect(() => {
    if (invitationError) {
      setError(invitationError);
    }
  }, [invitationError]);

  useEffect(() => {
    if (acceptError) {
      setError(acceptError);
    }
  }, [acceptError]);

  useEffect(() => {
    if (success) {
      // Redirect after 2 seconds
      setTimeout(() => {
        navigate('/company/auth/login');
      }, 2000);
    }
  }, [success, navigate]);

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    if (!email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = 'El email no es válido';
    }

    if (!name.trim()) {
      errors.name = 'El nombre es requerido';
    }

    if (!password) {
      errors.password = 'La contraseña es requerida';
    } else if (password.length < 8) {
      errors.password = 'La contraseña debe tener al menos 8 caracteres';
    }

    if (password !== confirmPassword) {
      errors.confirmPassword = 'Las contraseñas no coinciden';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleAcceptAsNewUser = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm() || !token) return;

    setError(null);
    resetAccept();

    const request: AcceptInvitationRequest = {
      token,
      email,
      name,
      password
    };

    const result = await acceptInvitation(request);
    if (!result) {
      // Error is already set by the hook
      return;
    }
  };

  const handleAcceptAsExistingUser = async () => {
    if (!token) return;

    setError(null);
    resetAccept();

    // Get user_id from JWT token
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      setError('Debes iniciar sesión primero');
      return;
    }

    // Decode JWT to get user_id
    let userId: string | undefined;
    try {
      const payload = decodeJWTPayload(accessToken);
      userId = payload?.sub || payload?.user_id || payload?.id;
    } catch (err) {
      console.error('Error decoding JWT:', err);
      setError('Error al obtener información del usuario. Por favor, inicia sesión nuevamente.');
      return;
    }

    if (!userId) {
      setError('No se pudo obtener el ID del usuario. Por favor, inicia sesión nuevamente.');
      return;
    }

    const request: AcceptInvitationRequest = {
      token,
      user_id: userId
    };

    const result = await acceptInvitation(request);
    if (result) {
      // Redirect after 2 seconds
      setTimeout(() => {
        navigate('/company/dashboard');
      }, 2000);
    }
  };

  if (loading && !invitation) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Cargando invitación...</p>
        </div>
      </div>
    );
  }

  if (error && !invitation) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
          <div className="text-center">
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Error</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <button
              onClick={() => navigate('/')}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Volver al inicio
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">¡Invitación Aceptada!</h2>
          <p className="text-gray-600 mb-6">
            Tu cuenta ha sido creada y vinculada a la empresa. Serás redirigido al login.
          </p>
          <Loader2 className="w-6 h-6 text-blue-600 animate-spin mx-auto" />
        </div>
      </div>
    );
  }

  if (!invitation) {
    return null;
  }

  const canAccept = invitation.status === 'pending' && !isInvitationExpired(invitation.expires_at);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Aceptar Invitación
          </h1>
          <p className="text-gray-600">
            Únete a la empresa como nuevo miembro del equipo
          </p>
        </div>

        {/* Invitation Details */}
        <InvitationDetails invitation={invitation} />

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-red-600" />
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        {/* Acceptance Form */}
        {canAccept && (
          <div className="bg-white rounded-lg shadow-md p-6">
            {isLoggedIn ? (
              // Case B: Existing User
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Aceptar como Usuario Existente
                </h3>
                <p className="text-gray-600 mb-6">
                  Ya tienes una cuenta. Haz clic en el botón para vincular tu cuenta a esta empresa.
                </p>
                <button
                  onClick={handleAcceptAsExistingUser}
                  disabled={submitting}
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {submitting ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Procesando...</span>
                    </>
                  ) : (
                    <>
                      <span>Aceptar Invitación</span>
                      <ArrowRight className="w-5 h-5" />
                    </>
                  )}
                </button>
              </div>
            ) : (
              // Case A: New User
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Crear Cuenta y Aceptar Invitación
                </h3>
                <p className="text-gray-600 mb-6">
                  Completa el formulario para crear tu cuenta y unirte a la empresa.
                </p>

                <form onSubmit={handleAcceptAsNewUser} className="space-y-4">
                  {/* Email Field */}
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                      Email
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Mail className="h-5 w-5 text-gray-400" />
                      </div>
                      <input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className={`w-full pl-10 pr-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                          formErrors.email
                            ? 'border-red-300 focus:ring-red-500'
                            : 'border-gray-300 focus:ring-blue-500'
                        }`}
                        placeholder="tu@email.com"
                        readOnly
                      />
                    </div>
                    {formErrors.email && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.email}</p>
                    )}
                  </div>

                  {/* Name Field */}
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                      Nombre Completo
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <User className="h-5 w-5 text-gray-400" />
                      </div>
                      <input
                        id="name"
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className={`w-full pl-10 pr-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                          formErrors.name
                            ? 'border-red-300 focus:ring-red-500'
                            : 'border-gray-300 focus:ring-blue-500'
                        }`}
                        placeholder="Tu nombre completo"
                        required
                      />
                    </div>
                    {formErrors.name && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.name}</p>
                    )}
                  </div>

                  {/* Password Field */}
                  <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                      Contraseña
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Lock className="h-5 w-5 text-gray-400" />
                      </div>
                      <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className={`w-full pl-10 pr-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                          formErrors.password
                            ? 'border-red-300 focus:ring-red-500'
                            : 'border-gray-300 focus:ring-blue-500'
                        }`}
                        placeholder="Mínimo 8 caracteres"
                        required
                      />
                    </div>
                    {formErrors.password && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.password}</p>
                    )}
                  </div>

                  {/* Confirm Password Field */}
                  <div>
                    <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                      Confirmar Contraseña
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Lock className="h-5 w-5 text-gray-400" />
                      </div>
                      <input
                        id="confirmPassword"
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className={`w-full pl-10 pr-3 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                          formErrors.confirmPassword
                            ? 'border-red-300 focus:ring-red-500'
                            : 'border-gray-300 focus:ring-blue-500'
                        }`}
                        placeholder="Repite tu contraseña"
                        required
                      />
                    </div>
                    {formErrors.confirmPassword && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.confirmPassword}</p>
                    )}
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={submitting}
                    className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                  >
                    {submitting ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        <span>Procesando...</span>
                      </>
                    ) : (
                      <>
                        <span>Aceptar y Crear Cuenta</span>
                        <ArrowRight className="w-5 h-5" />
                      </>
                    )}
                  </button>
                </form>

                {/* Alternative: Login Link */}
                <div className="mt-6 text-center">
                  <p className="text-sm text-gray-600">
                    ¿Ya tienes una cuenta?{' '}
                    <button
                      onClick={() => navigate('/company/auth/login')}
                      className="text-blue-600 hover:text-blue-700 font-medium"
                    >
                      Inicia sesión
                    </button>
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {!canAccept && invitation && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-yellow-600" />
              <p className="text-yellow-800">
                Esta invitación no puede ser aceptada en este momento.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

