/**
 * Resume Statistics Card Component
 *
 * Displays statistical information about resumes with visual indicators.
 */

import React from 'react';
import { motion } from 'framer-motion';

interface ResumeStatsCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  trend?: string;
  color?: 'blue' | 'green' | 'purple' | 'orange' | 'red';
  className?: string;
}

const ResumeStatsCard: React.FC<ResumeStatsCardProps> = ({
  title,
  value,
  icon,
  trend,
  color = 'blue',
  className = ''
}) => {
  const getColorClasses = (color: string) => {
    switch (color) {
      case 'blue':
        return {
          bg: 'bg-blue-100',
          text: 'text-blue-600',
          border: 'border-blue-200'
        };
      case 'green':
        return {
          bg: 'bg-green-100',
          text: 'text-green-600',
          border: 'border-green-200'
        };
      case 'purple':
        return {
          bg: 'bg-purple-100',
          text: 'text-purple-600',
          border: 'border-purple-200'
        };
      case 'orange':
        return {
          bg: 'bg-orange-100',
          text: 'text-orange-600',
          border: 'border-orange-200'
        };
      case 'red':
        return {
          bg: 'bg-red-100',
          text: 'text-red-600',
          border: 'border-red-200'
        };
      default:
        return {
          bg: 'bg-gray-100',
          text: 'text-gray-600',
          border: 'border-gray-200'
        };
    }
  };

  const colorClasses = getColorClasses(color);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-lg border ${colorClasses.border} p-6 ${className}`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <div className="flex items-baseline mt-2">
            <p className="text-2xl font-semibold text-gray-900">{value}</p>
            {trend && (
              <span className={`ml-2 text-sm font-medium ${
                trend.startsWith('+') ? 'text-green-600' :
                trend.startsWith('-') ? 'text-red-600' :
                'text-gray-600'
              }`}>
                {trend}
              </span>
            )}
          </div>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses.bg}`}>
          <div className={colorClasses.text}>
            {icon}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default ResumeStatsCard;