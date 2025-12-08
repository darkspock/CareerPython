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
import { useState, useMemo } from 'react';
import {
  UserPlus,
  Search,
  Filter,
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
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Alert, AlertDescription } from '@/components/ui/alert';

export default function UsersManagementPage() {
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState<CompanyUserRole | 'all'>('all');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');

  // Filters object for hook - memoized to prevent infinite loops
  const filters: CompanyUsersFilters | undefined = useMemo(() => {
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
  }, [searchTerm, roleFilter, statusFilter]);

  // Hooks
  const { users, loading, error, refresh, companyId } = useCompanyUsers(filters);
  const { inviteUser: _inviteUser, loading: _inviteLoading, error: _inviteError, invitationLink: _invitationLink, reset: resetInvite } = useInviteUser();
  const { removeUser, loading: removeLoading, error: removeError, reset: resetRemove } = useRemoveUser();
  const { assignRole, loading: _assignLoading, error: _assignError, reset: resetAssign } = useAssignRole();
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
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      const userIdMatch = user.user_id.toLowerCase().includes(searchLower);
      const emailMatch = user.email?.toLowerCase().includes(searchLower);
      if (!userIdMatch && !emailMatch) {
        return false;
      }
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
        <Button onClick={() => setShowInviteModal(true)}>
          <UserPlus className="w-5 h-5 mr-2" />
          Invitar Usuario
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <form onSubmit={handleSearch} className="flex gap-4 items-end">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Buscar Usuarios
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search className="h-5 w-5 text-gray-400" />
                </div>
                <Input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Buscar por email..."
                  className="pl-10"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Rol
              </label>
              <Select value={roleFilter} onValueChange={(value) => setRoleFilter(value as CompanyUserRole | 'all')}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Rol" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos los roles</SelectItem>
                  <SelectItem value="admin">Administrador</SelectItem>
                  <SelectItem value="recruiter">Reclutador</SelectItem>
                  <SelectItem value="viewer">Visualizador</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Estado
              </label>
              <Select value={statusFilter} onValueChange={(value) => setStatusFilter(value as 'all' | 'active' | 'inactive')}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Estado" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos</SelectItem>
                  <SelectItem value="active">Activos</SelectItem>
                  <SelectItem value="inactive">Inactivos</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Button type="submit">
              <Filter className="w-4 h-4 mr-2" />
              Filtrar
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            {error}
          </AlertDescription>
        </Alert>
      )}

      {/* Users Table */}
      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Usuario</TableHead>
                <TableHead>Rol</TableHead>
                <TableHead>Estado</TableHead>
                <TableHead>Fecha de Incorporación</TableHead>
                <TableHead className="text-right">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredUsers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-12">
                    <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">
                      {searchTerm || roleFilter !== 'all' || statusFilter !== 'all'
                        ? 'No se encontraron usuarios con los filtros seleccionados'
                        : 'No hay usuarios en la empresa'}
                    </p>
                  </TableCell>
                </TableRow>
              ) : (
                filteredUsers.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>
                      <div className="text-sm font-medium text-gray-900">{user.email || user.user_id}</div>
                    </TableCell>
                    <TableCell>
                      <UserRoleBadge role={user.role} />
                    </TableCell>
                    <TableCell>
                      <UserStatusBadge status={user.status} />
                    </TableCell>
                    <TableCell className="text-sm text-gray-500">
                      {new Date(user.created_at).toLocaleDateString('es-ES', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleOpenAssignRole(user)}
                          title="Cambiar rol"
                        >
                          <Edit className="w-5 h-5" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleOpenRemove(user)}
                          title="Eliminar usuario"
                          disabled={user.user_id === currentUserId}
                          className="text-red-600 hover:text-red-900"
                        >
                          <Trash2 className="w-5 h-5" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

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
