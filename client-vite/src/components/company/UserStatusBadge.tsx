// Badge component for displaying user status
import type { CompanyUserStatus } from '../../types/companyUser';
import { getCompanyUserStatusColor } from '../../types/companyUser';

interface UserStatusBadgeProps {
  status: CompanyUserStatus;
  className?: string;
}

export default function UserStatusBadge({ status, className = '' }: UserStatusBadgeProps) {
  const labels: Record<CompanyUserStatus, string> = {
    active: 'Activo',
    inactive: 'Inactivo'
  };

  return (
    <span
      className={`px-2 py-1 rounded-full text-xs font-medium ${getCompanyUserStatusColor(
        status
      )} ${className}`}
    >
      {labels[status]}
    </span>
  );
}

