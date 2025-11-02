/**
 * CTAButton Component
 * 
 * Reusable call-to-action button component with consistent styling.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Button content
 * @param {string} [props.variant] - Button variant (primary, secondary, outline)
 * @param {string} [props.size] - Button size (small, medium, large)
 * @param {boolean} [props.disabled] - Whether button is disabled
 * @param {boolean} [props.loading] - Whether button is in loading state
 * @param {Function} [props.onClick] - Click handler
 * @param {string} [props.href] - Link URL (if button should be a link)
 * @param {string} [props.className] - Additional CSS classes
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

interface CTAButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  href?: string;
  className?: string;
  type?: 'button' | 'submit';
}

export default function CTAButton({
  children,
  variant = 'primary',
  size = 'large',
  disabled = false,
  loading = false,
  onClick,
  href,
  className = '',
  type = 'button'
}: CTAButtonProps) {
  const variantClasses = {
    primary: 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl',
    secondary: 'bg-gray-800 hover:bg-gray-900 text-white',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50'
  };

  const sizeClasses = {
    small: 'px-4 py-2 text-sm',
    medium: 'px-6 py-3 text-base',
    large: 'px-8 py-4 text-lg font-semibold'
  };

  const baseClasses = `inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;

  const content = loading ? (
    <>
      <Loader2 className="w-5 h-5 animate-spin mr-2" />
      <span>Procesando...</span>
    </>
  ) : (
    children
  );

  if (href) {
    return (
      <Link to={href} className={baseClasses}>
        {content}
      </Link>
    );
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={baseClasses}
    >
      {content}
    </button>
  );
}

