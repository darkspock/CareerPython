import React from 'react';

interface ProviderProps {
  children: React.ReactNode;
  onErrorReport?: (report: any) => Promise<void>;
}

export const ErrorProvider: React.FC<ProviderProps> = ({ children }) => {
  return <>{children}</>;
};

export const ConnectionProvider: React.FC<ProviderProps> = ({ children }) => {
  return <>{children}</>;
};

export const MonitoringProvider: React.FC<ProviderProps> = ({ children }) => {
  return <>{children}</>;
};