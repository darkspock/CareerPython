// Component to display a visual list of user permissions
import { Check, X } from 'lucide-react';
import type { CompanyUserPermissions } from '../../types/companyUser';

interface UserPermissionsListProps {
  permissions: CompanyUserPermissions;
  showLabels?: boolean;
}

/**
 * UserPermissionsList Component
 * 
 * Displays a visual list of user permissions with checkmarks for enabled permissions
 * and X icons for disabled permissions.
 * 
 * @param {UserPermissionsListProps} props - Component props
 * @param {CompanyUserPermissions} props.permissions - Object containing permission flags
 * @param {boolean} [props.showLabels=true] - Whether to show permission labels
 */
export default function UserPermissionsList({ 
  permissions, 
  showLabels = true 
}: UserPermissionsListProps) {
  const permissionList = [
    { key: 'can_manage_users' as keyof CompanyUserPermissions, label: 'Gestionar Usuarios' },
    { key: 'can_manage_positions' as keyof CompanyUserPermissions, label: 'Gestionar Posiciones' },
    { key: 'can_view_resumes' as keyof CompanyUserPermissions, label: 'Ver CVs' },
    { key: 'can_manage_resumes' as keyof CompanyUserPermissions, label: 'Gestionar CVs' },
    { key: 'can_invite_users' as keyof CompanyUserPermissions, label: 'Invitar Usuarios' },
    { key: 'can_assign_roles' as keyof CompanyUserPermissions, label: 'Asignar Roles' },
  ];

  return (
    <div className="space-y-2">
      {permissionList.map(({ key, label }) => {
        const hasPermission = permissions[key];
        return (
          <div 
            key={key} 
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-50 transition"
          >
            {hasPermission ? (
              <Check className="w-5 h-5 text-green-600 flex-shrink-0" />
            ) : (
              <X className="w-5 h-5 text-gray-400 flex-shrink-0" />
            )}
            {showLabels && (
              <span className={`text-sm ${hasPermission ? 'text-gray-900' : 'text-gray-500'}`}>
                {label}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}

