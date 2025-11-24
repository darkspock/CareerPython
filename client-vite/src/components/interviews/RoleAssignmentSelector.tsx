import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { X, Plus, Trash2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import type { CompanyRole } from '../../types/company';
import type { CompanyUser } from '../../types/companyUser';

export interface RoleAssignment {
  id: string; // unique ID for this assignment
  roleId: string;
  userIds: string[];
}

interface RoleAssignmentSelectorProps {
  assignment: RoleAssignment;
  availableRoles: CompanyRole[];
  availableUsers: CompanyUser[];
  onChange: (assignment: RoleAssignment) => void;
  onRemove: () => void;
  usedRoleIds: string[]; // Roles already used in other assignments
}

export default function RoleAssignmentSelector({
  assignment,
  availableRoles,
  availableUsers,
  onChange,
  onRemove,
  usedRoleIds,
}: RoleAssignmentSelectorProps) {
  const { t } = useTranslation();
  const [selectedUserId, setSelectedUserId] = useState<string>('');

  const handleRoleChange = (roleId: string) => {
    onChange({
      ...assignment,
      roleId: roleId || '',
      userIds: roleId ? assignment.userIds : [], // Clear users if role is cleared
    });
  };

  const handleAddUser = () => {
    if (!selectedUserId) return;
    
    if (assignment.userIds.includes(selectedUserId)) {
      // Already added
      setSelectedUserId('');
      return;
    }

    onChange({
      ...assignment,
      userIds: [...assignment.userIds, selectedUserId],
    });
    setSelectedUserId('');
  };

  const handleRemoveUser = (userId: string) => {
    onChange({
      ...assignment,
      userIds: assignment.userIds.filter((id) => id !== userId),
    });
  };

  // Filter out roles that are already used (except the current one)
  const availableRolesFiltered = availableRoles.filter(
    (role) => role.id === assignment.roleId || !usedRoleIds.includes(role.id)
  );

  // Filter out users that are already assigned
  const availableUsersFiltered = availableUsers.filter(
    (user) => !assignment.userIds.includes(user.id)
  );

  const selectedRole = availableRoles.find((r) => r.id === assignment.roleId);

  return (
    <div className="border rounded-lg p-4 bg-gray-50 space-y-4">
      <div className="flex items-start gap-3">
        {/* Role Selector */}
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('company.interviews.form.role', { defaultValue: 'Role' })} <span className="text-red-600">*</span>
          </label>
          <Select value={assignment.roleId || undefined} onValueChange={handleRoleChange}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder={t('company.interviews.form.selectRole', { defaultValue: 'Select a role' })} />
            </SelectTrigger>
            <SelectContent>
              {availableRolesFiltered.length === 0 ? (
                <div className="px-2 py-4 text-sm text-gray-500 text-center">
                  {t('company.interviews.form.noRoles', { defaultValue: 'No roles available' })}
                </div>
              ) : (
                availableRolesFiltered.map((role) => (
                  <SelectItem key={role.id} value={role.id}>
                    {role.name}
                  </SelectItem>
                ))
              )}
            </SelectContent>
          </Select>
        </div>

        {/* Remove Assignment Button */}
        <div className="pt-8">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={onRemove}
            className="text-red-600 hover:text-red-700 hover:bg-red-50"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Users Assignment */}
      {assignment.roleId && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('company.interviews.form.assignedPeople', { defaultValue: 'Assigned People' })}
          </label>

          {/* Add User Section */}
          <div className="flex gap-2 mb-3">
            <Select value={selectedUserId || undefined} onValueChange={(value) => setSelectedUserId(value || '')}>
              <SelectTrigger className="flex-1">
                <SelectValue placeholder={t('company.interviews.form.selectPerson', { defaultValue: 'Select a person' })} />
              </SelectTrigger>
              <SelectContent>
                {availableUsersFiltered.length === 0 ? (
                  <div className="px-2 py-4 text-sm text-gray-500 text-center">
                    {assignment.userIds.length > 0
                      ? t('company.interviews.form.allUsersAssigned', { defaultValue: 'All users already assigned' })
                      : t('company.interviews.form.noUsers', { defaultValue: 'No users available' })}
                  </div>
                ) : (
                  availableUsersFiltered.map((user) => (
                    <SelectItem key={user.id} value={user.id}>
                      {user.email || user.id}
                    </SelectItem>
                  ))
                )}
              </SelectContent>
            </Select>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={handleAddUser}
              disabled={!selectedUserId}
            >
              <Plus className="h-4 w-4 mr-1" />
              {t('company.interviews.form.add', { defaultValue: 'Add' })}
            </Button>
          </div>

          {/* Assigned Users List */}
          {assignment.userIds.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {assignment.userIds.map((userId) => {
                const user = availableUsers.find((u) => u.id === userId);
                return user ? (
                  <Badge key={userId} variant="secondary" className="flex items-center gap-1">
                    {user.email || user.id}
                    <button
                      type="button"
                      onClick={() => handleRemoveUser(userId)}
                      className="ml-1 hover:text-red-600 transition-colors"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </Badge>
                ) : null;
              })}
            </div>
          ) : (
            <p className="text-sm text-gray-500 italic">
              {t('company.interviews.form.noPeopleAssigned', { defaultValue: 'No people assigned yet (optional)' })}
            </p>
          )}
        </div>
      )}

      {/* Role info */}
      {selectedRole && (
        <div className="text-xs text-gray-600 pt-2 border-t">
          <strong>{selectedRole.name}:</strong> {assignment.userIds.length} {t('company.interviews.form.peopleAssigned', { defaultValue: 'people assigned' })}
        </div>
      )}
    </div>
  );
}

