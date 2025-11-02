/**
 * InvitationDetails Component
 * 
 * Displays detailed information about a company user invitation including:
 * - Company information
 * - Invited email address
 * - Invitation status with visual badge
 * - Expiration date and countdown
 * 
 * @component
 * @param {Object} props - Component props
 * @param {CompanyUserInvitation} props.invitation - The invitation object to display
 */
// Invitation details component
import React from 'react';
import type { CompanyUserInvitation } from '../../types/companyUser';
import {
  getInvitationStatusColor,
  getInvitationStatusLabel,
  isInvitationExpired,
  getDaysUntilExpiration
} from '../../types/companyUser';
import { AlertCircle, Clock, CheckCircle, XCircle, Building2, Mail } from 'lucide-react';

interface InvitationDetailsProps {
  invitation: CompanyUserInvitation;
}

export default function InvitationDetails({ invitation }: InvitationDetailsProps) {
  const daysUntilExpiration = getDaysUntilExpiration(invitation.expires_at);
  const expired = isInvitationExpired(invitation.expires_at);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-900">Invitación de Empresa</h2>
        <span
          className={`px-3 py-1 rounded-full text-sm font-medium ${getInvitationStatusColor(
            invitation.status
          )}`}
        >
          {getInvitationStatusLabel(invitation.status)}
        </span>
      </div>

      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <Building2 className="w-5 h-5 text-gray-500" />
          <span className="text-gray-700">
            <strong>Empresa:</strong> {invitation.company_id}
          </span>
        </div>

        <div className="flex items-center space-x-2">
          <Mail className="w-5 h-5 text-gray-500" />
          <span className="text-gray-700">
            <strong>Email invitado:</strong> {invitation.email}
          </span>
        </div>

        {invitation.status === 'pending' && (
          <div className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-gray-500" />
            <span className="text-gray-700">
              {expired ? (
                <span className="text-red-600 font-medium">
                  Esta invitación ha expirado
                </span>
              ) : daysUntilExpiration > 0 ? (
                <span>
                  <strong>Expira en:</strong> {daysUntilExpiration} día
                  {daysUntilExpiration !== 1 ? 's' : ''}
                </span>
              ) : (
                <span className="text-orange-600 font-medium">
                  Expira hoy
                </span>
              )}
            </span>
          </div>
        )}

        {invitation.status === 'accepted' && (
          <div className="flex items-center space-x-2 text-green-600">
            <CheckCircle className="w-5 h-5" />
            <span>Esta invitación ya fue aceptada</span>
          </div>
        )}

        {(invitation.status === 'expired' || expired) && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 flex items-start space-x-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-red-800 font-medium">Invitación Expirada</h3>
              <p className="text-red-700 text-sm mt-1">
                Esta invitación expiró el {new Date(invitation.expires_at).toLocaleDateString()}.
                Por favor, solicita una nueva invitación.
              </p>
            </div>
          </div>
        )}

        {invitation.status === 'rejected' && (
          <div className="bg-gray-50 border border-gray-200 rounded-md p-4 flex items-start space-x-3">
            <XCircle className="w-5 h-5 text-gray-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-gray-800 font-medium">Invitación Rechazada</h3>
              <p className="text-gray-700 text-sm mt-1">
                Esta invitación fue rechazada anteriormente.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

