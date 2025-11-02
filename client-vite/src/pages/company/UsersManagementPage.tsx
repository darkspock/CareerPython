/**
 * UsersManagementPage Component
 * 
 * Protected page for managing company users. Allows administrators to:
 * - View list of company users with their roles and status
 * - Invite new users
 * - Assign/change user roles
 * - Remove users from the company
 * 
 * Features:
 * - Filtering by role, status, and search term
 * - Table view with user information
 * - Modals for invitation, role assignment, and user removal
 * - Real-time data refresh
 * 
 * @component
 */
// Company Users Management Page
import { useState, useEffect } from 'react';
import {
  UserPlus,
  Search,
  Filter,
  MoreVertical,
  Edit,
  Trash2,
  Users,
  Loader2,
  AlertCircle
} from 'lucide-react';
import { useCompanyUsers, useInviteUser, useRemoveUser, useAssignRole } from '../../hooks/useCompanyUsers';
import { getUserId } from '../../utils/companyAuth';
import type {
  CompanyUser,
  CompanyUsersFilters,
  CompanyUserRole,
  AssignRoleRequest
} from '../../types/companyUser';
import InviteUserModal from '../../components/company/InviteUserModal';
import AssignRoleModal from '../../components/company/AssignRoleModal';
import RemoveUserConfirmModal from '../../components/company/RemoveUserConfirmModal';
import UserRoleBadge from '../../components/company/UserRoleBadge';
import UserStatusBadge from '../../components/company/UserStatusBadge';

export default function UsersManagementPage() {
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState<CompanyUserRole | 'all'>('all');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');
  
  // Filters object for hook
  const filters: CompanyUsersFilters | undefined = (() => {
    const f: CompanyUsersFilters = {
      active_only: statusFilter === 'active'
    };
    if (roleFilter !== 'all') {
      f.role = roleFilter;
    }
    if (searchTerm.trim()) {
      f.search = searchTerm.trim();
    }
    return Object.keys(f).length > 0 ? f : undefined;
  })();

  // Hooks
  const { users, loading, error, refresh, companyId } = useCompanyUsers(filters);
  const { inviteUser, loading: inviteLoading, error: inviteError, invitationLink, reset: resetInvite } = useInviteUser();
  const { removeUser, loading: removeLoading, error: removeError, reset: resetRemove } = useRemoveUser();
  const { assignRole, loading: assignLoading, error: assignError, reset: resetAssign } = useAssignRole();
  const currentUserId = getUserId();
  
  // Modals
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [showAssignRoleModal, setShowAssignRoleModal] = useState(false);
  const [showRemoveModal, setShowRemoveModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState<CompanyUser | null>(null);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    refresh();
  };

  const handleInviteSuccess = () => {
    refresh();
    setShowInviteModal(false);
    resetInvite();
  };

  const handleAssignRoleSuccess = async (user: CompanyUser, role: CompanyUserRole) => {
    const request: AssignRoleRequest = { role };
    const result = await assignRole(user.user_id, request);
    
    if (result) {
      refresh();
      setShowAssignRoleModal(false);
      setSelectedUser(null);
      resetAssign();
    }
  };

  const handleRemoveUserConfirm = async () => {
    if (!selectedUser) return;

    const result = await removeUser(selectedUser.user_id);
    
    if (result) {
      setShowRemoveModal(false);
      setSelectedUser(null);
      refresh();
      resetRemove();
    }
  };

  const handleOpenAssignRole = (user: CompanyUser) => {
    setSelectedUser(user);
    setShowAssignRoleModal(true);
    resetAssign();
  };

  const handleOpenRemove = (user: CompanyUser) => {
    setSelectedUser(user);
    setShowRemoveModal(true);
    resetRemove();
  };

  // Filter users client-side for additional filtering (the API already filters, but we can add more)
  const filteredUsers = users.filter((user) => {
    if (searchTerm && !user.user_id.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false;
    }
    return true;
  });

  if (loading && users.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Cargando usuarios...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestión de Usuarios</h1>
          <p className="text-gray-600 mt-1">Administra los usuarios de tu empresa</p>
        </div>
        <button
          onClick={() => setShowInviteModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center space-x-2"
        >
          <UserPlus className="w-5 h-5" />
          <span>Invitar Usuario</span>
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <form onSubmit={handleSearch} className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Buscar Usuarios
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Buscar por email o ID..."
                className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Rol
            </label>
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value as CompanyUserRole | 'all')}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Todos los roles</option>
              <option value="admin">Administrador</option>
              <option value="recruiter">Reclutador</option>
              <option value="viewer">Visualizador</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Estado
            </label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as 'all' | 'active' | 'inactive')}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Todos</option>
              <option value="active">Activos</option>
              <option value="inactive">Inactivos</option>
            </select>
          </div>

          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition flex items-center space-x-2"
          >
            <Filter className="w-4 h-4" />
            <span>Filtrar</span>
          </button>
        </form>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="text-red-800 font-medium">Error</h3>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Users Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuario
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rol
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Fecha de Incorporación
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredUsers.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-12 text-center">
                    <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">
                      {searchTerm || roleFilter !== 'all' || statusFilter !== 'all'
                        ? 'No se encontraron usuarios con los filtros seleccionados'
                        : 'No hay usuarios en la empresa'}
                    </p>
                  </td>
                </tr>
              ) : (
                filteredUsers.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{user.user_id}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <UserRoleBadge role={user.role} />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <UserStatusBadge status={user.status} />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(user.created_at).toLocaleDateString('es-ES', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end space-x-2">
                        <button
                          onClick={() => handleOpenAssignRole(user)}
                          className="text-blue-600 hover:text-blue-900 transition"
                          title="Cambiar rol"
                        >
                          <Edit className="w-5 h-5" />
                        </button>
                        <button
                          onClick={() => handleOpenRemove(user)}
                          className="text-red-600 hover:text-red-900 transition"
                          title="Eliminar usuario"
                          disabled={user.user_id === currentUserId}
                        >
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modals */}
      {companyId && (
        <>
          <InviteUserModal
            companyId={companyId}
            isOpen={showInviteModal}
            onClose={() => setShowInviteModal(false)}
            onSuccess={handleInviteSuccess}
          />

          {selectedUser && (
            <>
              <AssignRoleModal
                companyId={companyId}
                user={selectedUser}
                isOpen={showAssignRoleModal}
                onClose={() => {
                  setShowAssignRoleModal(false);
                  setSelectedUser(null);
                }}
                onSuccess={handleAssignRoleSuccess}
              />

              <RemoveUserConfirmModal
                user={selectedUser}
                isOpen={showRemoveModal}
                onClose={() => {
                  setShowRemoveModal(false);
                  setSelectedUser(null);
                  resetRemove();
                }}
                onConfirm={handleRemoveUserConfirm}
                loading={removeLoading}
                error={removeError}
              />
            </>
          )}
        </>
      )}
    </div>
  );
}

