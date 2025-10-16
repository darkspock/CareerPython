import React from 'react';

interface RealTimeProviderProps {
  children: React.ReactNode;
  userId?: string;
}

export const RealTimeProvider: React.FC<RealTimeProviderProps> = ({ children }) => {
  // Simplified RealTime provider for now
  return <>{children}</>;
};