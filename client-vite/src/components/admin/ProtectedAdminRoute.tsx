import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { api } from '../../lib/api';


interface AdminRouteProps {
  children: React.ReactNode;
}

const ProtectedAdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const verifyAdminAccess = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          setIsAdmin(false);
          setIsLoading(false);
          return;
        }

        // Check admin access by calling the admin health endpoint
        await api.authenticatedRequest('/admin/health');
        setIsAdmin(true);
      } catch (error: any) {
        console.log('Admin access denied:', error.message);
        setIsAdmin(false);
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    verifyAdminAccess();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAdmin) {
    return <Navigate to="/admin/login" replace state={{
      message: 'Admin access required',
      error: error
    }} />;
  }

  return <>{children}</>;
};

export default ProtectedAdminRoute;