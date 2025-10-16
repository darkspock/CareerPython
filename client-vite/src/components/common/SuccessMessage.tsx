import React, { useEffect, useState } from 'react';
import { CheckCircle, X } from 'lucide-react';

interface SuccessMessageProps {
  message: string;
  isVisible: boolean;
  onClose: () => void;
  autoHideDelay?: number; // in milliseconds, default 5000 (5 seconds)
}

export const SuccessMessage: React.FC<SuccessMessageProps> = ({
  message,
  isVisible,
  onClose,
  autoHideDelay = 5000
}) => {
  const [shouldShow, setShouldShow] = useState(false);

  useEffect(() => {
    if (isVisible) {
      setShouldShow(true);

      // Auto-hide after specified delay
      const timer = setTimeout(() => {
        setShouldShow(false);
        setTimeout(onClose, 300); // Wait for animation to complete
      }, autoHideDelay);

      return () => clearTimeout(timer);
    } else {
      setShouldShow(false);
    }
  }, [isVisible, autoHideDelay, onClose]);

  if (!isVisible && !shouldShow) return null;

  return (
    <div className="fixed top-4 right-4 z-50">
      <div
        className={`
          bg-green-50 border border-green-200 rounded-xl p-4 shadow-lg
          transform transition-all duration-300 ease-in-out
          ${shouldShow ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
          max-w-md
        `}
      >
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <CheckCircle className="h-5 w-5 text-green-600" />
          </div>

          <div className="flex-1">
            <p className="text-green-800 text-sm font-medium">
              {message}
            </p>
          </div>

          <button
            onClick={() => {
              setShouldShow(false);
              setTimeout(onClose, 300);
            }}
            className="flex-shrink-0 text-green-600 hover:text-green-800 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Progress bar showing remaining time */}
        <div className="mt-3 bg-green-200 rounded-full h-1 overflow-hidden">
          <div
            className="bg-green-600 h-full rounded-full transition-all ease-linear"
            style={{
              animation: shouldShow ? `successMessageShrink ${autoHideDelay}ms linear` : 'none',
              width: shouldShow ? '0%' : '100%'
            }}
          />
        </div>
      </div>

      <style>{`
        @keyframes successMessageShrink {
          from { width: 100%; }
          to { width: 0%; }
        }
      `}</style>
    </div>
  );
};