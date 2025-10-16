import React from 'react';
import { CheckCircle } from 'lucide-react';

interface Step {
  id: number;
  title: string;
  path: string;
}

interface ProgressIndicatorProps {
  steps: Step[];
  currentStep: number;
  onStepClick?: (stepId: number) => void;
}

export const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({
  steps,
  currentStep,
  onStepClick
}) => {
  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const isCompleted = step.id < currentStep;
          const isCurrent = step.id === currentStep;
          const isClickable = onStepClick && step.id <= currentStep;

          return (
            <React.Fragment key={step.id}>
              {/* Step Circle */}
              <div className="flex flex-col items-center">
                <button
                  className={`relative flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all duration-200 ${
                    isCompleted
                      ? 'bg-green-500 border-green-500 text-white'
                      : isCurrent
                      ? 'bg-blue-500 border-blue-500 text-white'
                      : 'bg-white border-gray-300 text-gray-400'
                  } ${
                    isClickable ? 'cursor-pointer hover:scale-105' : 'cursor-default'
                  }`}
                  onClick={() => isClickable && onStepClick(step.id)}
                  disabled={!isClickable}
                >
                  {isCompleted ? (
                    <CheckCircle className="w-6 h-6" />
                  ) : (
                    <span className="text-sm font-semibold">{step.id}</span>
                  )}
                </button>

                {/* Step Title */}
                <span
                  className={`mt-2 text-xs font-medium text-center max-w-20 ${
                    isCurrent || isCompleted
                      ? 'text-gray-900'
                      : 'text-gray-500'
                  }`}
                >
                  {step.title}
                </span>
              </div>

              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-2 transition-colors duration-200 ${
                    step.id < currentStep
                      ? 'bg-green-500'
                      : 'bg-gray-200'
                  }`}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};