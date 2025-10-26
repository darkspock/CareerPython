import React from 'react';
import { X, AlertTriangle, XCircle, CheckCircle } from 'lucide-react';
import type { ValidationResult, ValidationIssue } from '../../types/workflow';

interface ValidationResultModalProps {
  isOpen: boolean;
  result: ValidationResult | null;
  onClose: () => void;
  onProceedAnyway?: () => void;
  showProceedButton?: boolean;
}

export const ValidationResultModal: React.FC<ValidationResultModalProps> = ({
  isOpen,
  result,
  onClose,
  onProceedAnyway,
  showProceedButton = false
}) => {
  if (!isOpen || !result) return null;

  const renderIssue = (issue: ValidationIssue, index: number) => {
    const isError = issue.severity === 'error';
    const Icon = isError ? XCircle : AlertTriangle;
    const bgColor = isError ? 'bg-red-50' : 'bg-yellow-50';
    const textColor = isError ? 'text-red-800' : 'text-yellow-800';
    const iconColor = isError ? 'text-red-400' : 'text-yellow-400';

    return (
      <div key={index} className={`rounded-lg p-4 ${bgColor}`}>
        <div className="flex">
          <div className="flex-shrink-0">
            <Icon className={`h-5 w-5 ${iconColor}`} />
          </div>
          <div className="ml-3 flex-1">
            <h3 className={`text-sm font-medium ${textColor}`}>
              {issue.field_name}
            </h3>
            <div className={`mt-2 text-sm ${textColor}`}>
              <p>{issue.message}</p>
            </div>
            {issue.should_auto_reject && issue.rejection_reason && (
              <div className="mt-2 text-xs text-red-600 font-semibold">
                ⚠️ Auto-Reject: {issue.rejection_reason}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          onClick={onClose}
        />

        {/* Modal */}
        <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl">
          {/* Header */}
          <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                {result.is_valid ? (
                  <CheckCircle className="h-6 w-6 text-green-500 mr-3" />
                ) : (
                  <XCircle className="h-6 w-6 text-red-500 mr-3" />
                )}
                <h3 className="text-lg font-medium text-gray-900">
                  Validation Result
                </h3>
              </div>
              <button
                onClick={onClose}
                className="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* Success State */}
            {result.is_valid && (
              <div className="rounded-lg bg-green-50 p-4">
                <div className="flex">
                  <CheckCircle className="h-5 w-5 text-green-400" />
                  <div className="ml-3">
                    <p className="text-sm font-medium text-green-800">
                      All validations passed successfully!
                    </p>
                    <p className="mt-1 text-sm text-green-700">
                      The candidate meets all requirements for this stage.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Auto-Reject Warning */}
            {result.should_auto_reject && (
              <div className="mb-4 rounded-lg bg-red-100 p-4 border-2 border-red-300">
                <div className="flex">
                  <XCircle className="h-6 w-6 text-red-600 flex-shrink-0" />
                  <div className="ml-3">
                    <h4 className="text-sm font-bold text-red-800 uppercase">
                      Application Will Be Auto-Rejected
                    </h4>
                    {result.auto_reject_reason && (
                      <p className="mt-1 text-sm text-red-700">
                        Reason: {result.auto_reject_reason}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Errors */}
            {result.has_errors && (
              <div className="mb-4">
                <h4 className="text-sm font-semibold text-red-800 mb-2 flex items-center">
                  <XCircle className="h-4 w-4 mr-1" />
                  Errors ({result.errors.length})
                </h4>
                <div className="space-y-2">
                  {result.errors.map((error, idx) => renderIssue(error, idx))}
                </div>
                {!result.should_auto_reject && (
                  <p className="mt-2 text-xs text-red-600">
                    ⚠️ These errors will block the stage transition
                  </p>
                )}
              </div>
            )}

            {/* Warnings */}
            {result.has_warnings && (
              <div>
                <h4 className="text-sm font-semibold text-yellow-800 mb-2 flex items-center">
                  <AlertTriangle className="h-4 w-4 mr-1" />
                  Warnings ({result.warnings.length})
                </h4>
                <div className="space-y-2">
                  {result.warnings.map((warning, idx) => renderIssue(warning, idx))}
                </div>
                {showProceedButton && !result.has_errors && (
                  <p className="mt-2 text-xs text-yellow-600">
                    ℹ️ These are warnings only. You can proceed if you choose.
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6 gap-2">
            {/* Proceed Anyway Button (only for warnings without errors) */}
            {showProceedButton &&
             result.has_warnings &&
             !result.has_errors &&
             !result.should_auto_reject &&
             onProceedAnyway && (
              <button
                onClick={() => {
                  onProceedAnyway();
                  onClose();
                }}
                className="inline-flex w-full justify-center rounded-md bg-yellow-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-yellow-500 sm:w-auto"
              >
                Proceed Anyway
              </button>
            )}

            {/* Close Button */}
            <button
              onClick={onClose}
              className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
            >
              {result.is_valid ? 'Close' : 'Go Back'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
