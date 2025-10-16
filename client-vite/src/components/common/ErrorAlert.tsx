/**
 * Error Alert Component
 *
 * Reusable error alert component with dismissible functionality
 * and expandable details section.
 */

import React, { useState } from 'react';
import { AlertCircle, X, ChevronDown, ChevronUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ErrorAlertProps {
  message: string;
  onDismiss?: () => void;
  details?: Record<string, any>;
  variant?: 'error' | 'warning' | 'info';
  className?: string;
}

const ErrorAlert: React.FC<ErrorAlertProps> = ({
  message,
  onDismiss,
  details,
  variant = 'error',
  className = ''
}) => {
  const [showDetails, setShowDetails] = useState(false);

  const getVariantClasses = (variant: string) => {
    switch (variant) {
      case 'error':
        return {
          container: 'bg-red-50 border-red-200',
          icon: 'text-red-500',
          text: 'text-red-800',
          button: 'text-red-500 hover:text-red-700'
        };
      case 'warning':
        return {
          container: 'bg-yellow-50 border-yellow-200',
          icon: 'text-yellow-500',
          text: 'text-yellow-800',
          button: 'text-yellow-500 hover:text-yellow-700'
        };
      case 'info':
        return {
          container: 'bg-blue-50 border-blue-200',
          icon: 'text-blue-500',
          text: 'text-blue-800',
          button: 'text-blue-500 hover:text-blue-700'
        };
      default:
        return {
          container: 'bg-red-50 border-red-200',
          icon: 'text-red-500',
          text: 'text-red-800',
          button: 'text-red-500 hover:text-red-700'
        };
    }
  };

  const classes = getVariantClasses(variant);
  const hasDetails = details && Object.keys(details).length > 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className={`border rounded-lg p-4 ${classes.container} ${className}`}
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <AlertCircle className={`w-5 h-5 ${classes.icon}`} />
        </div>

        <div className="ml-3 flex-1">
          <p className={`text-sm font-medium ${classes.text}`}>
            {message}
          </p>

          {hasDetails && (
            <button
              onClick={() => setShowDetails(!showDetails)}
              className={`mt-2 text-sm ${classes.button} flex items-center hover:underline focus:outline-none`}
            >
              {showDetails ? (
                <>
                  <ChevronUp className="w-4 h-4 mr-1" />
                  Hide details
                </>
              ) : (
                <>
                  <ChevronDown className="w-4 h-4 mr-1" />
                  Show details
                </>
              )}
            </button>
          )}

          <AnimatePresence>
            {showDetails && hasDetails && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-3 overflow-hidden"
              >
                <div className={`text-xs ${classes.text} bg-white bg-opacity-50 rounded p-2 border`}>
                  <pre className="whitespace-pre-wrap font-mono">
                    {JSON.stringify(details, null, 2)}
                  </pre>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {onDismiss && (
          <button
            onClick={onDismiss}
            className={`flex-shrink-0 ml-4 ${classes.button} hover:bg-white hover:bg-opacity-20 rounded-full p-1 transition-colors`}
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </motion.div>
  );
};

export default ErrorAlert;