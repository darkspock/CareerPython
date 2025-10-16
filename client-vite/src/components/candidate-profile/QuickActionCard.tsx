import React from 'react';
import { ArrowRight } from 'lucide-react';

interface QuickActionCardProps {
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  action: () => void;
  buttonText: string;
  color?: 'blue' | 'green' | 'purple' | 'orange';
  badge?: string;
}

const QuickActionCard: React.FC<QuickActionCardProps> = ({
  title,
  description,
  icon: Icon,
  action,
  buttonText,
  color = 'blue',
  badge
}) => {
  const colorClasses = {
    blue: {
      bg: 'bg-blue-50',
      icon: 'text-blue-600',
      button: 'bg-blue-600 hover:bg-blue-700',
      border: 'border-blue-200'
    },
    green: {
      bg: 'bg-green-50',
      icon: 'text-green-600',
      button: 'bg-green-600 hover:bg-green-700',
      border: 'border-green-200'
    },
    purple: {
      bg: 'bg-purple-50',
      icon: 'text-purple-600',
      button: 'bg-purple-600 hover:bg-purple-700',
      border: 'border-purple-200'
    },
    orange: {
      bg: 'bg-orange-50',
      icon: 'text-orange-600',
      button: 'bg-orange-600 hover:bg-orange-700',
      border: 'border-orange-200'
    }
  };

  const colors = colorClasses[color];

  return (
    <div className={`${colors.bg} ${colors.border} border rounded-lg p-6 transition-all hover:shadow-md group`}>
      <div className="flex items-start gap-4">
        {/* Icon */}
        <div className={`${colors.bg} p-3 rounded-lg`}>
          <Icon className={`w-6 h-6 ${colors.icon}`} />
        </div>

        {/* Content */}
        <div className="flex-1">
          <div className="flex items-start justify-between mb-2">
            <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
            {badge && (
              <span className="px-2 py-1 text-xs font-medium text-blue-600 bg-blue-100 rounded-full">
                {badge}
              </span>
            )}
          </div>

          <p className="text-gray-600 mb-4">{description}</p>

          {/* Action Button */}
          <button
            onClick={action}
            className={`${colors.button} text-white px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 group-hover:gap-3`}
          >
            {buttonText}
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuickActionCard;