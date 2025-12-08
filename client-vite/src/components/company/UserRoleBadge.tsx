// Badge component for displaying user roles
import type { CompanyUserRole } from '../../types/companyUser';
import {
  getCompanyUserRoleColor,
  getCompanyUserRoleLabel
} from '../../types/companyUser';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface UserRoleBadgeProps {
  role: CompanyUserRole;
  className?: string;
}

export default function UserRoleBadge({ role, className = '' }: UserRoleBadgeProps) {
  // Map the color classes to badge variants or keep custom colors
  const colorClass = getCompanyUserRoleColor(role);

  return (
    <Badge
      className={cn(colorClass, className)}
    >
      {getCompanyUserRoleLabel(role)}
    </Badge>
  );
}
