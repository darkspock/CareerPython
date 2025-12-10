/**
 * ExperienceLevelBadge Component
 * Displays experience level with appropriate styling
 */
import React from 'react';
import { GraduationCap } from 'lucide-react';
import {
  ExperienceLevel,
  getExperienceLevelLabel
} from '../../../types/position';

interface ExperienceLevelBadgeProps {
  level: ExperienceLevel | string;
  showIcon?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const getLevelColor = (level: ExperienceLevel | string): string => {
  switch (level) {
    case ExperienceLevel.INTERNSHIP:
    case 'internship':
      return 'bg-purple-50 text-purple-700';
    case ExperienceLevel.ENTRY:
    case 'entry':
      return 'bg-green-50 text-green-700';
    case ExperienceLevel.MID:
    case 'mid':
      return 'bg-blue-50 text-blue-700';
    case ExperienceLevel.SENIOR:
    case 'senior':
      return 'bg-indigo-50 text-indigo-700';
    case ExperienceLevel.LEAD:
    case 'lead':
      return 'bg-orange-50 text-orange-700';
    case ExperienceLevel.EXECUTIVE:
    case 'executive':
      return 'bg-red-50 text-red-700';
    default:
      return 'bg-gray-50 text-gray-700';
  }
};

export const ExperienceLevelBadge: React.FC<ExperienceLevelBadgeProps> = ({
  level,
  showIcon = true,
  size = 'md',
  className = ''
}) => {
  const label = getExperienceLevelLabel(level);
  const colorClasses = getLevelColor(level);

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base'
  };

  const iconSizes = {
    sm: 12,
    md: 14,
    lg: 16
  };

  return (
    <span
      className={`inline-flex items-center gap-1 font-medium rounded-full ${colorClasses} ${sizeClasses[size]} ${className}`}
    >
      {showIcon && <GraduationCap size={iconSizes[size]} />}
      {label}
    </span>
  );
};

export default ExperienceLevelBadge;
