/**
 * RemoveUserConfirmModal Component
 * 
 * Confirmation modal for removing a user from a company. Displays warnings
 * and validation messages to prevent destructive actions.
 * 
 * Features:
 * - User information display
 * - Warning messages
 * - Validation notes (cannot remove self, cannot remove last admin)
 * - Loading and error states
 * 
 * @component
 * @param {Object} props - Component props
 * @param {CompanyUser} props.user - The user to be removed
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onClose - Callback when modal is closed
 * @param {Function} props.onConfirm - Callback when removal is confirmed
 * @param {boolean} props.loading - Whether the removal is in progress
 * @param {string|null} props.error - Error message if removal failed
 */
// Modal for confirming user removal
import { X, AlertTriangle, Trash2 } from 'lucide-react';
import type { CompanyUser } from '../../types/companyUser';

interface RemoveUserConfirmModalProps {
  user: CompanyUser;
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  loading?: boolean;
  error?: string | null;
}

export default function RemoveUserConfirmModal({
  user,
  isOpen,
  onClose,
  onConfirm,
  loading = false,
  error = null
}: RemoveUserConfirmModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
              <Trash2 className="w-5 h-5 text-red-600" />
            </div>
            <h2 className="text-xl font-semibold text-gray-900">Eliminar Usuario</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition"
            disabled={loading}
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
            <div className="flex items-start space-x-3">
              <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="text-yellow-800 font-medium mb-1">Confirmar Eliminación</h3>
                <p className="text-yellow-700 text-sm">
                  Esta acción eliminará el usuario de la empresa. El usuario no podrá acceder a los recursos de la empresa.
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-gray-600 mb-1">Usuario a eliminar:</p>
            <p className="font-medium text-gray-900">{user.user_id}</p>
            <p className="text-sm text-gray-600 mt-2 mb-1">Rol actual:</p>
            <p className="font-medium text-gray-900 capitalize">{user.role}</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
            <p className="text-blue-800 text-xs">
              <strong>Nota:</strong> No se puede eliminar el último administrador de la empresa ni eliminarte a ti mismo.
            </p>
          </div>

          {/* Actions */}
          <div className="flex space-x-3">
            <button
              onClick={onClose}
              disabled={loading}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              onClick={onConfirm}
              disabled={loading}
              className="flex-1 bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Eliminando...</span>
                </>
              ) : (
                <>
                  <Trash2 className="w-4 h-4" />
                  <span>Eliminar Usuario</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

