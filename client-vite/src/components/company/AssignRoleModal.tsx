/**
 * AssignRoleModal Component
 * 
 * Modal component for assigning or changing a user's role within a company.
 * Supports role transitions with warnings for critical changes (e.g., removing admin).
 * 
 * Features:
 * - Role selection dropdown
 * - Warning messages for role changes
 * - Validation to prevent removing the last admin
 * - Success/error handling
 * 
 * @component
 * @param {Object} props - Component props
 * @param {string} props.companyId - The company ID
 * @param {CompanyUser} props.user - The user whose role is being changed
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onClose - Callback when modal is closed
 * @param {Function} [props.onSuccess] - Callback when role is assigned successfully
 */
// Modal for assigning a role to a company user
import React, { useState, useEffect } from 'react';
import { X, UserCog, AlertTriangle, Loader2 } from 'lucide-react';
import type {
  CompanyUser,
  CompanyUserRole,
  AssignRoleRequest
} from '../../types/companyUser';
import { COMPANY_USER_ROLE_OPTIONS } from '../../types/companyUser';
import type { CompanyRole } from '../../types/company';
import { useAssignRole } from '../../hooks/useCompanyUsers';
import { api } from '../../lib/api';

interface AssignRoleModalProps {
  companyId: string;
  user: CompanyUser;
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (user: CompanyUser, role: CompanyUserRole) => void;
}

export default function AssignRoleModal({
  companyId,
  user,
  isOpen,
  onClose,
  onSuccess
}: AssignRoleModalProps) {
  const [role, setRole] = useState<CompanyUserRole>(user.role);
  const [selectedCompanyRoles, setSelectedCompanyRoles] = useState<string[]>(user.company_roles || []);
  const [warning, setWarning] = useState<string | null>(null);
  const [companyRoles, setCompanyRoles] = useState<CompanyRole[]>([]);
  const [loadingCompanyRoles, setLoadingCompanyRoles] = useState(false);

  const { assignRole, loading, error, reset } = useAssignRole();

  useEffect(() => {
    if (isOpen) {
      setRole(user.role);
      setSelectedCompanyRoles(user.company_roles || []);
      setWarning(null);
      reset();
      loadCompanyRoles();
    }
  }, [isOpen, user.role, user.company_roles, reset]);

  const loadCompanyRoles = async () => {
    try {
      setLoadingCompanyRoles(true);
      const roles = await api.listCompanyRoles(companyId, false);
      setCompanyRoles(roles as CompanyRole[]);
    } catch (err) {
      console.error('Error loading company roles:', err);
    } finally {
      setLoadingCompanyRoles(false);
    }
  };

  useEffect(() => {
    // Show warning if changing from admin to non-admin
    if (user.role === 'admin' && role !== 'admin') {
      setWarning('Estás cambiando un usuario administrador a otro rol. Asegúrate de que haya otros administradores.');
    } else {
      setWarning(null);
    }
  }, [user.role, role]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const request: AssignRoleRequest = {
      role,
      company_roles: selectedCompanyRoles
    };

    const result = await assignRole(user.user_id, request);
    
    if (result) {
      if (onSuccess) {
        onSuccess(user, role);
      }
      onClose();
    }
  };

  const handleClose = () => {
    setRole(user.role);
    setWarning(null);
    reset();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <UserCog className="w-6 h-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">Asignar Rol</h2>
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
          <form onSubmit={handleSubmit} className="space-y-4">
            {warning && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                <p className="text-yellow-800 text-sm">{warning}</p>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800 text-sm">{error}</p>
              </div>
            )}

            {/* Current Role Info */}
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Usuario:</p>
              <p className="font-medium text-gray-900">{user.user_id}</p>
              <p className="text-sm text-gray-600 mt-2 mb-1">Rol actual:</p>
              <p className="font-medium text-gray-900 capitalize">{user.role}</p>
            </div>

            {/* System Role Select */}
            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                Rol del Sistema
              </label>
              <select
                id="role"
                value={role}
                onChange={(e) => {
                  const newRole = e.target.value as CompanyUserRole;
                  setRole(newRole);
                  
                  // Update warning
                  if (user.role === 'admin' && newRole !== 'admin') {
                    setWarning('Estás cambiando un usuario administrador a otro rol. Asegúrate de que haya otros administradores.');
                  } else {
                    setWarning(null);
                  }
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {COMPANY_USER_ROLE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <p className="mt-1 text-xs text-gray-500">
                Define los permisos del usuario en la aplicación
              </p>
            </div>

            {/* Company Roles (Personalizados) */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Roles de la Empresa
              </label>
              {loadingCompanyRoles ? (
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Cargando roles...</span>
                </div>
              ) : companyRoles.length === 0 ? (
                <div className="text-sm text-gray-500 p-3 bg-gray-50 rounded-lg">
                  No hay roles personalizados creados.{' '}
                  <a href="/company/settings/roles" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                    Crear roles
                  </a>
                </div>
              ) : (
                <div className="space-y-2 p-4 border border-gray-300 rounded-lg bg-gray-50 max-h-48 overflow-y-auto">
                  {companyRoles.map((companyRole) => (
                    <label
                      key={companyRole.id}
                      className="flex items-center gap-2 cursor-pointer hover:bg-gray-100 p-2 rounded"
                    >
                      <input
                        type="checkbox"
                        checked={selectedCompanyRoles.includes(companyRole.id)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSelectedCompanyRoles([...selectedCompanyRoles, companyRole.id]);
                          } else {
                            setSelectedCompanyRoles(selectedCompanyRoles.filter(id => id !== companyRole.id));
                          }
                        }}
                        className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                      />
                      <div className="flex-1">
                        <span className="text-sm font-medium text-gray-700">{companyRole.name}</span>
                        {companyRole.description && (
                          <p className="text-xs text-gray-500">{companyRole.description}</p>
                        )}
                      </div>
                    </label>
                  ))}
                </div>
              )}
              <p className="mt-1 text-xs text-gray-500">
                Roles personalizados para asignar en workflows
              </p>
            </div>

            {/* Submit Buttons */}
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
                disabled={loading || role === user.role}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Asignando...</span>
                  </>
                ) : (
                  <span>Asignar Rol</span>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

