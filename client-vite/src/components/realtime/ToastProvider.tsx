import React from 'react';

interface ToastProviderProps {
  children: React.ReactNode;
}

export const ToastProvider: React.FC<ToastProviderProps> = ({ children }) => {
  // Simplified Toast provider for now
  return <>{children}</>;
};