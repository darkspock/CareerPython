/**
 * InviteUserModal Component
 * 
 * Modal component for inviting new users to a company. Allows administrators
 * to send invitations with a specific role (admin, recruiter, viewer).
 * 
 * Features:
 * - Email validation
 * - Role selection
 * - Success state with invitation link to copy
 * - Error handling with user-friendly messages
 * 
 * @component
 * @param {Object} props - Component props
 * @param {string} props.companyId - The company ID to invite the user to
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onClose - Callback when modal is closed
 * @param {Function} [props.onSuccess] - Callback when invitation is sent successfully
 */
// Modal for inviting a new user to the company
import React, { useState, useEffect } from 'react';
import { X, Mail, UserPlus, Copy, Check, AlertCircle } from 'lucide-react';
import type {
  InviteCompanyUserRequest,
  CompanyUserRole
} from '../../types/companyUser';
import { COMPANY_USER_ROLE_OPTIONS } from '../../types/companyUser';
import { useInviteUser } from '../../hooks/useCompanyUsers';

interface InviteUserModalProps {
  companyId: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export default function InviteUserModal({
  companyId,
  isOpen,
  onClose,
  onSuccess
}: InviteUserModalProps) {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState<CompanyUserRole>('recruiter');
  const [copied, setCopied] = useState(false);

  const { inviteUser, loading, error, invitationLink, reset } = useInviteUser();

  useEffect(() => {
    if (!isOpen) {
      setEmail('');
      setRole('recruiter');
      setCopied(false);
      reset();
    }
  }, [isOpen, reset]);

  useEffect(() => {
    if (invitationLink && onSuccess) {
      onSuccess();
    }
  }, [invitationLink, onSuccess]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const request: InviteCompanyUserRequest = {
      email: email.trim().toLowerCase(),
      role
    };

    await inviteUser(request);
  };

  const handleCopyLink = () => {
    if (invitationLink?.invitation_link) {
      navigator.clipboard.writeText(invitationLink.invitation_link);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClose = () => {
    setEmail('');
    setRole('recruiter');
    setCopied(false);
    reset();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <UserPlus className="w-6 h-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              {invitationLink ? 'Invitación Enviada' : 'Invitar Usuario'}
            </h2>
          </div>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {invitationLink ? (
            // Success State
            <div className="space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Check className="w-5 h-5 text-green-600" />
                  <p className="text-green-800 font-medium">¡Invitación enviada exitosamente!</p>
                </div>
                <p className="text-green-700 text-sm">
                  Se ha enviado un email a <strong>{invitationLink.email}</strong>
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Link de Invitación
                </label>
                <div className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={invitationLink.invitation_link}
                    readOnly
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-sm"
                  />
                  <button
                    onClick={handleCopyLink}
                    className={`px-4 py-2 rounded-lg transition ${
                      copied
                        ? 'bg-green-100 text-green-700'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                  >
                    {copied ? (
                      <Check className="w-5 h-5" />
                    ) : (
                      <Copy className="w-5 h-5" />
                    )}
                  </button>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Comparte este link manualmente si es necesario
                </p>
              </div>

              <div className="text-sm text-gray-600">
                <p>
                  <strong>Expira:</strong>{' '}
                  {new Date(invitationLink.expires_at).toLocaleDateString('es-ES', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>

              <button
                onClick={handleClose}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition"
              >
                Cerrar
              </button>
            </div>
          ) : (
            // Form State
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <p className="text-red-800 text-sm">{error}</p>
                </div>
              )}

              {/* Email Field */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email del Usuario
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="usuario@ejemplo.com"
                  />
                </div>
              </div>

              {/* Role Field */}
              <div>
                <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                  Rol
                </label>
                <select
                  id="role"
                  value={role}
                  onChange={(e) => setRole(e.target.value as CompanyUserRole)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {COMPANY_USER_ROLE_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  El usuario recibirá permisos según su rol
                </p>
              </div>

              {/* Submit Button */}
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={handleClose}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={loading || !email.trim()}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {loading || inviteLoading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Enviando...</span>
                    </>
                  ) : (
                    <>
                      <UserPlus className="w-4 h-4" />
                      <span>Enviar Invitación</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

