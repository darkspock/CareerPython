/**
 * SectionContainer Component
 * 
 * Wrapper component for landing page sections with consistent spacing and styling.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Content to render
 * @param {string} [props.className] - Additional CSS classes
 * @param {string} [props.backgroundColor] - Background color variant
 * @param {boolean} [props.fullWidth] - Whether to use full width
 */
import React from 'react';

interface SectionContainerProps {
  children: React.ReactNode;
  className?: string;
  backgroundColor?: 'white' | 'gray' | 'blue' | 'gradient';
  fullWidth?: boolean;
  id?: string;
}

export default function SectionContainer({
  children,
  className = '',
  backgroundColor = 'white',
  fullWidth = false,
  id
}: SectionContainerProps) {
  const bgClasses = {
    white: 'bg-white',
    gray: 'bg-gray-50',
    blue: 'bg-blue-50',
    gradient: 'bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50'
  };

  const containerClass = fullWidth ? 'w-full' : 'max-w-7xl mx-auto';

  return (
    <section id={id} className={`${bgClasses[backgroundColor]} py-16 px-4 sm:px-6 lg:px-8 ${className}`}>
      <div className={containerClass}>
        {children}
      </div>
    </section>
  );
}

