// Badge component for displaying user status
import type { CompanyUserStatus } from '../../types/companyUser';
import { getCompanyUserStatusColor } from '../../types/companyUser';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface UserStatusBadgeProps {
  status: CompanyUserStatus;
  className?: string;
}

export default function UserStatusBadge({ status, className = '' }: UserStatusBadgeProps) {
  const labels: Record<CompanyUserStatus, string> = {
    active: 'Activo',
    inactive: 'Inactivo'
  };

  const colorClass = getCompanyUserStatusColor(status);

  return (
    <Badge
      className={cn(colorClass, className)}
    >
      {labels[status]}
    </Badge>
  );
}
