import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';

interface CompanyRouteProps {
  children: React.ReactNode;
}

const ProtectedCompanyRoute: React.FC<CompanyRouteProps> = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const verifyCompanyAccess = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          setIsAuthenticated(false);
          setIsLoading(false);
          return;
        }

        // Decode JWT to check if it's a company user
        const payload = JSON.parse(atob(token.split('.')[1]));

        // Check if token has company_id (indicates company user)
        if (payload.company_id) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error: any) {
        console.log('Company access verification failed:', error.message);
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    verifyCompanyAccess();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/company/login" replace state={{
      message: 'Please login to access the company dashboard',
    }} />;
  }

  return <>{children}</>;
};

export default ProtectedCompanyRoute;
