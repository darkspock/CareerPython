/**
 * LanguagesList Component
 * Displays language requirements with proficiency levels
 */
import React from 'react';
import { Globe } from 'lucide-react';
import type { LanguageRequirement } from '../../../types/position';

interface LanguagesListProps {
  languages: LanguageRequirement[] | null | undefined;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
  layout?: 'inline' | 'list';
  className?: string;
}

const getLevelColor = (level: string): string => {
  switch (level) {
    case 'Native':
      return 'bg-green-100 text-green-800';
    case 'C2':
    case 'C1':
      return 'bg-blue-100 text-blue-800';
    case 'B2':
    case 'B1':
      return 'bg-yellow-100 text-yellow-800';
    case 'A2':
    case 'A1':
      return 'bg-gray-100 text-gray-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export const LanguagesList: React.FC<LanguagesListProps> = ({
  languages,
  size = 'md',
  showIcon = true,
  layout = 'inline',
  className = ''
}) => {
  if (!languages || languages.length === 0) {
    return null;
  }

  const sizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  };

  const levelSizeClasses = {
    sm: 'px-1.5 py-0.5 text-xs',
    md: 'px-2 py-0.5 text-xs',
    lg: 'px-2.5 py-1 text-sm'
  };

  const iconSizes = {
    sm: 12,
    md: 14,
    lg: 16
  };

  if (layout === 'list') {
    return (
      <ul className={`space-y-1 ${className}`}>
        {languages.map((lang, index) => (
          <li
            key={`${lang.language}-${index}`}
            className={`flex items-center gap-2 ${sizeClasses[size]}`}
          >
            {showIcon && <Globe size={iconSizes[size]} className="text-gray-400" />}
            <span className="font-medium">{lang.language}</span>
            <span className={`rounded-full ${getLevelColor(lang.level)} ${levelSizeClasses[size]}`}>
              {lang.level}
            </span>
          </li>
        ))}
      </ul>
    );
  }

  return (
    <div className={`flex flex-wrap items-center gap-2 ${className}`}>
      {showIcon && <Globe size={iconSizes[size]} className="text-gray-400" />}
      {languages.map((lang, index) => (
        <span
          key={`${lang.language}-${index}`}
          className={`inline-flex items-center gap-1 ${sizeClasses[size]}`}
        >
          <span className="font-medium">{lang.language}</span>
          <span className={`rounded-full ${getLevelColor(lang.level)} ${levelSizeClasses[size]}`}>
            {lang.level}
          </span>
          {index < languages.length - 1 && <span className="text-gray-300 mx-1">|</span>}
        </span>
      ))}
    </div>
  );
};

export default LanguagesList;
