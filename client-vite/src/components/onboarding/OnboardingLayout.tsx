import React from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { ProgressIndicator } from './ProgressIndicator';
import { useOnboarding } from '../../hooks/useOnboarding';

interface OnboardingLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  showNavigation?: boolean;
  showProgress?: boolean;
  onNext?: () => void;
  onPrevious?: () => void;
  nextButtonText?: string;
  previousButtonText?: string;
  nextButtonDisabled?: boolean;
  canSkip?: boolean;
  onSkip?: () => void;
}

export const OnboardingLayout: React.FC<OnboardingLayoutProps> = ({
  children,
  title,
  subtitle,
  showNavigation = true,
  showProgress = true,
  onNext,
  onPrevious,
  nextButtonText = "Siguiente",
  previousButtonText = "Anterior",
  nextButtonDisabled = false,
  canSkip = false,
  onSkip
}) => {
  const {
    steps,
    currentStep,
    goToStep,
    nextStep,
    prevStep,
    isFirstStep,
    isLastStep
  } = useOnboarding();

  const handleNext = () => {
    if (onNext) {
      onNext();
    } else {
      nextStep();
    }
  };

  const handlePrevious = () => {
    if (onPrevious) {
      onPrevious();
    } else {
      prevStep();
    }
  };

  const handleSkip = () => {
    if (onSkip) {
      onSkip();
    } else {
      nextStep();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Progress Indicator */}
      {showProgress && (
        <div className="bg-white border-b border-gray-200">
          <ProgressIndicator
            steps={steps}
            currentStep={currentStep}
            onStepClick={goToStep}
          />
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 px-4 py-8">
          <div className="max-w-2xl mx-auto">
            {/* Header */}
            {(title || subtitle) && (
              <div className="text-center mb-8">
                {title && (
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    {title}
                  </h1>
                )}
                {subtitle && (
                  <p className="text-lg text-gray-600">
                    {subtitle}
                  </p>
                )}
              </div>
            )}

            {/* Page Content */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              {children}
            </div>
          </div>
        </div>

        {/* Navigation */}
        {showNavigation && (
          <div className="bg-white border-t border-gray-200 px-4 py-4">
            <div className="max-w-2xl mx-auto flex items-center justify-between">
              {/* Previous Button */}
              <button
                onClick={handlePrevious}
                disabled={isFirstStep}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                  isFirstStep
                    ? 'text-gray-400 cursor-not-allowed'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <ArrowLeft className="w-4 h-4" />
                {previousButtonText}
              </button>

              {/* Skip Button */}
              {canSkip && (
                <button
                  onClick={handleSkip}
                  className="text-gray-500 hover:text-gray-700 font-medium"
                >
                  Omitir sección
                </button>
              )}

              {/* Next Button */}
              <button
                onClick={handleNext}
                disabled={nextButtonDisabled}
                className={`flex items-center gap-2 px-6 py-2 rounded-lg font-medium transition-all ${
                  nextButtonDisabled
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : isLastStep
                    ? 'bg-green-600 hover:bg-green-700 text-white'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {isLastStep ? 'Finalizar' : nextButtonText}
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};