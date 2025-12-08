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
import React, { useState, useEffect } from 'react';
import { UserCog, AlertTriangle, Loader2 } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Card, CardContent } from '@/components/ui/card';
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
    if (user.role === 'admin' && role !== 'admin') {
      setWarning('Estas cambiando un usuario administrador a otro rol. Asegurate de que haya otros administradores.');
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

  const handleCompanyRoleToggle = (roleId: string, checked: boolean) => {
    if (checked) {
      setSelectedCompanyRoles([...selectedCompanyRoles, roleId]);
    } else {
      setSelectedCompanyRoles(selectedCompanyRoles.filter(id => id !== roleId));
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && handleClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <UserCog className="w-6 h-6 text-blue-600" />
            Asignar Rol
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4 py-4">
          {warning && (
            <Alert className="border-yellow-200 bg-yellow-50">
              <AlertTriangle className="w-4 h-4 text-yellow-600" />
              <AlertDescription className="text-yellow-800">{warning}</AlertDescription>
            </Alert>
          )}

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Current Role Info */}
          <Card className="bg-gray-50">
            <CardContent className="pt-4 space-y-2">
              <div>
                <p className="text-sm text-muted-foreground">Usuario:</p>
                <p className="font-medium">{user.user_id}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Rol actual:</p>
                <p className="font-medium capitalize">{user.role}</p>
              </div>
            </CardContent>
          </Card>

          {/* System Role Select */}
          <div className="space-y-2">
            <Label htmlFor="role">Rol del Sistema</Label>
            <Select
              value={role}
              onValueChange={(value) => {
                const newRole = value as CompanyUserRole;
                setRole(newRole);
                if (user.role === 'admin' && newRole !== 'admin') {
                  setWarning('Estas cambiando un usuario administrador a otro rol. Asegurate de que haya otros administradores.');
                } else {
                  setWarning(null);
                }
              }}
            >
              <SelectTrigger>
                <SelectValue placeholder="Seleccionar rol" />
              </SelectTrigger>
              <SelectContent>
                {COMPANY_USER_ROLE_OPTIONS.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <p className="text-xs text-muted-foreground">
              Define los permisos del usuario en la aplicacion
            </p>
          </div>

          {/* Company Roles (Personalizados) */}
          <div className="space-y-2">
            <Label>Roles de la Empresa</Label>
            {loadingCompanyRoles ? (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Cargando roles...</span>
              </div>
            ) : companyRoles.length === 0 ? (
              <Card className="bg-gray-50">
                <CardContent className="pt-4">
                  <p className="text-sm text-muted-foreground">
                    No hay roles personalizados creados.{' '}
                    <a href="/company/settings/roles" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                      Crear roles
                    </a>
                  </p>
                </CardContent>
              </Card>
            ) : (
              <Card className="bg-gray-50 max-h-48 overflow-y-auto">
                <CardContent className="pt-4 space-y-2">
                  {companyRoles.map((companyRole) => (
                    <div
                      key={companyRole.id}
                      className="flex items-start gap-3 p-2 rounded hover:bg-gray-100"
                    >
                      <Checkbox
                        id={`role-${companyRole.id}`}
                        checked={selectedCompanyRoles.includes(companyRole.id)}
                        onCheckedChange={(checked) =>
                          handleCompanyRoleToggle(companyRole.id, checked as boolean)
                        }
                      />
                      <div className="flex-1">
                        <Label
                          htmlFor={`role-${companyRole.id}`}
                          className="text-sm font-medium cursor-pointer"
                        >
                          {companyRole.name}
                        </Label>
                        {companyRole.description && (
                          <p className="text-xs text-muted-foreground">{companyRole.description}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}
            <p className="text-xs text-muted-foreground">
              Roles personalizados para asignar en workflows
            </p>
          </div>

          {/* Submit Buttons */}
          <DialogFooter className="gap-2 sm:gap-0">
            <Button type="button" variant="outline" onClick={handleClose}>
              Cancelar
            </Button>
            <Button type="submit" disabled={loading || role === user.role}>
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Asignando...
                </>
              ) : (
                'Asignar Rol'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
