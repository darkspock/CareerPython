import React from 'react';
import { Trash2 } from 'lucide-react';
import { usePositionEnums } from '../../hooks/useEnums';

export interface Role {
  role: string;
}

interface RoleSelectorProps {
  roles: Role[];
  onChange: (roles: Role[]) => void;
  title: string;
  placeholder?: string;
  className?: string;
}

const RoleSelector: React.FC<RoleSelectorProps> = ({
  roles,
  onChange,
  title,
  placeholder = "Selecciona un rol",
  className = ""
}) => {
  const { desiredRoles: roleOptions, loading } = usePositionEnums();

  const addRole = () => {
    onChange([...roles, { role: '' }]);
  };

  const removeRole = (index: number) => {
    onChange(roles.filter((_, i) => i !== index));
  };

  const updateRole = (index: number, value: string) => {
    const updated = [...roles];
    updated[index] = { role: value };
    onChange(updated);
  };

  if (loading) {
    return (
      <div className={className}>
        <label className="block text-sm font-medium text-gray-700 mb-2">{title}</label>
        <div className="animate-pulse bg-gray-200 rounded-lg p-4">
          <p className="text-sm text-gray-500">Cargando roles...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700 mb-2">{title}</label>
      <div className="space-y-3">
        {roles.map((roleItem, index) => (
          <div key={index} className="flex items-center gap-3">
            <div className="flex-1">
              <select
                value={roleItem.role}
                onChange={(e) => updateRole(index, e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">{placeholder}</option>
                {roleOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            <button
              type="button"
              onClick={() => removeRole(index)}
              className="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
              title="Eliminar rol"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        ))}

        <button
          type="button"
          onClick={addRole}
          className="w-full py-3 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-500 hover:text-blue-600 transition duration-200"
        >
          + Agregar rol
        </button>
      </div>
    </div>
  );
};

export default RoleSelector;

// Export utility functions for data conversion
export const convertRolesFromBackend = (roles: string[] | undefined): Role[] => {
  if (!roles || !Array.isArray(roles)) return [];
  return roles.map(role => ({ role }));
};

export const convertRolesToBackend = (roles: Role[]): string[] => {
  return roles
    .filter(roleItem => roleItem.role && roleItem.role.trim() !== '')
    .map(roleItem => roleItem.role);
};