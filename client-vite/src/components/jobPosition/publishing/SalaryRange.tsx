/**
 * SalaryRange Component
 * Displays formatted salary range with currency
 */
import React from 'react';
import { DollarSign } from 'lucide-react';
import { SalaryPeriod, getSalaryPeriodLabel } from '../../../types/position';

export interface SalaryRangeProps {
  min?: number | null;
  max?: number | null;
  currency?: string | null;
  period?: SalaryPeriod | string | null;
  showIcon?: boolean;
  showPeriod?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const formatCurrency = (amount: number, currency: string = 'USD'): string => {
  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  } catch {
    return `${currency} ${amount.toLocaleString()}`;
  }
};

export const SalaryRange: React.FC<SalaryRangeProps> = ({
  min,
  max,
  currency = 'USD',
  period,
  showIcon = true,
  showPeriod: _showPeriod,
  size: _size,
  className = ''
}) => {
  if (!min && !max) {
    return null;
  }

  const currencyCode = currency || 'USD';
  const periodLabel = period ? getSalaryPeriodLabel(period) : '';

  let rangeText = '';

  if (min && max) {
    if (min === max) {
      rangeText = formatCurrency(min, currencyCode);
    } else {
      rangeText = `${formatCurrency(min, currencyCode)} - ${formatCurrency(max, currencyCode)}`;
    }
  } else if (min) {
    rangeText = `From ${formatCurrency(min, currencyCode)}`;
  } else if (max) {
    rangeText = `Up to ${formatCurrency(max, currencyCode)}`;
  }

  return (
    <span className={`inline-flex items-center gap-1 text-gray-700 ${className}`}>
      {showIcon && <DollarSign size={16} className="text-green-600" />}
      <span className="font-medium">{rangeText}</span>
      {periodLabel && <span className="text-gray-500">{periodLabel}</span>}
    </span>
  );
};

export default SalaryRange;
