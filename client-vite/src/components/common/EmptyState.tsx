/**
 * Empty State Component
 *
 * Reusable empty state component for displaying when no data is available.
 */

import React from 'react';
import { type LucideIcon, Inbox } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  actionIcon?: LucideIcon;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon = Inbox,
  title,
  description,
  actionLabel,
  onAction,
  actionIcon: ActionIcon,
  className = '',
  size = 'md'
}) => {
  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return {
          container: 'py-6',
          icon: 'w-10 h-10',
          title: 'text-base',
          description: 'text-sm'
        };
      case 'md':
        return {
          container: 'py-8',
          icon: 'w-12 h-12',
          title: 'text-lg',
          description: 'text-sm'
        };
      case 'lg':
        return {
          container: 'py-12',
          icon: 'w-16 h-16',
          title: 'text-xl',
          description: 'text-base'
        };
      default:
        return {
          container: 'py-8',
          icon: 'w-12 h-12',
          title: 'text-lg',
          description: 'text-sm'
        };
    }
  };

  const sizeClasses = getSizeClasses();

  return (
    <div className={`text-center ${sizeClasses.container} ${className}`}>
      <Icon className={`${sizeClasses.icon} mx-auto mb-3 text-muted-foreground`} />
      <h3 className={`${sizeClasses.title} font-medium text-foreground mb-2`}>
        {title}
      </h3>
      {description && (
        <p className={`${sizeClasses.description} text-muted-foreground mb-4`}>
          {description}
        </p>
      )}
      {actionLabel && onAction && (
        <Button onClick={onAction} variant="default">
          {ActionIcon && <ActionIcon className="w-4 h-4 mr-2" />}
          {actionLabel}
        </Button>
      )}
    </div>
  );
};

export default EmptyState;
