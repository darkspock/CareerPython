// Badge component for displaying user roles
import React from 'react';
import type { CompanyUserRole } from '../../types/companyUser';
import {
  getCompanyUserRoleColor,
  getCompanyUserRoleLabel
} from '../../types/companyUser';

interface UserRoleBadgeProps {
  role: CompanyUserRole;
  className?: string;
}

export default function UserRoleBadge({ role, className = '' }: UserRoleBadgeProps) {
  return (
    <span
      className={`px-2 py-1 rounded-full text-xs font-medium ${getCompanyUserRoleColor(
        role
      )} ${className}`}
    >
      {getCompanyUserRoleLabel(role)}
    </span>
  );
}

