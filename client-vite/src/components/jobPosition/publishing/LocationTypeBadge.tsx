/**
 * LocationTypeBadge Component
 * Displays work location type with icon
 */
import React from 'react';
import { MapPin, Home, Building2 } from 'lucide-react';
import {
  WorkLocationType,
  getWorkLocationTypeLabel
} from '../../../types/position';

interface LocationTypeBadgeProps {
  type: WorkLocationType | string;
  showIcon?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const getLocationIcon = (type: WorkLocationType | string, size: number) => {
  const iconProps = { size, className: 'flex-shrink-0' };

  switch (type) {
    case WorkLocationType.REMOTE:
    case 'remote':
      return <Home {...iconProps} />;
    case WorkLocationType.HYBRID:
    case 'hybrid':
      return <Building2 {...iconProps} />;
    case WorkLocationType.ON_SITE:
    case 'on_site':
    default:
      return <MapPin {...iconProps} />;
  }
};

const getLocationColor = (type: WorkLocationType | string): string => {
  switch (type) {
    case WorkLocationType.REMOTE:
    case 'remote':
      return 'bg-green-50 text-green-700';
    case WorkLocationType.HYBRID:
    case 'hybrid':
      return 'bg-purple-50 text-purple-700';
    case WorkLocationType.ON_SITE:
    case 'on_site':
    default:
      return 'bg-gray-50 text-gray-700';
  }
};

export const LocationTypeBadge: React.FC<LocationTypeBadgeProps> = ({
  type,
  showIcon = true,
  size = 'md',
  className = ''
}) => {
  const label = getWorkLocationTypeLabel(type);
  const colorClasses = getLocationColor(type);

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
      {showIcon && getLocationIcon(type, iconSizes[size])}
      {label}
    </span>
  );
};

export default LocationTypeBadge;
