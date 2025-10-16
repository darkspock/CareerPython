/**
 * Loading Spinner Component
 *
 * Reusable loading spinner with customizable size and color.
 */

import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'blue' | 'gray' | 'white' | 'green' | 'red';
  className?: string;
  text?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  color = 'blue',
  className = '',
  text
}) => {
  const getSizeClasses = (size: string) => {
    switch (size) {
      case 'sm':
        return 'w-4 h-4';
      case 'md':
        return 'w-6 h-6';
      case 'lg':
        return 'w-8 h-8';
      case 'xl':
        return 'w-12 h-12';
      default:
        return 'w-6 h-6';
    }
  };

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'blue':
        return 'text-blue-600';
      case 'gray':
        return 'text-gray-600';
      case 'white':
        return 'text-white';
      case 'green':
        return 'text-green-600';
      case 'red':
        return 'text-red-600';
      default:
        return 'text-blue-600';
    }
  };

  const getTextSizeClasses = (size: string) => {
    switch (size) {
      case 'sm':
        return 'text-sm';
      case 'md':
        return 'text-base';
      case 'lg':
        return 'text-lg';
      case 'xl':
        return 'text-xl';
      default:
        return 'text-base';
    }
  };

  if (text) {
    return (
      <div className={`flex flex-col items-center justify-center space-y-2 ${className}`}>
        <Loader2 className={`animate-spin ${getSizeClasses(size)} ${getColorClasses(color)}`} />
        <p className={`${getTextSizeClasses(size)} ${getColorClasses(color)} font-medium`}>
          {text}
        </p>
      </div>
    );
  }

  return (
    <div className={`flex items-center justify-center ${className}`}>
      <Loader2 className={`animate-spin ${getSizeClasses(size)} ${getColorClasses(color)}`} />
    </div>
  );
};

export default LoadingSpinner;