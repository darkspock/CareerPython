import React, { useEffect, useState } from 'react';
import { Navigate, useParams } from 'react-router-dom';
import { CompanyProvider, useCompany } from '../../context/CompanyContext';

interface ProtectedCompanyScopedRouteProps {
  children: React.ReactNode;
}

/**
 * Inner component that handles authentication and company validation
 */
const ProtectedCompanyScopedRouteInner: React.FC<ProtectedCompanyScopedRouteProps> = ({ children }) => {
  const { companySlug } = useParams<{ companySlug: string }>();
  const { company, isLoading: companyLoading, error: companyError } = useCompany();

  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userCompanyIdFromToken, setUserCompanyIdFromToken] = useState<string | null>(null);

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
          setUserCompanyIdFromToken(payload.company_id);
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

  // Show loading state while checking auth and company
  if (isLoading || companyLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    // Try to get company slug from localStorage if not in URL
    const storedSlug = localStorage.getItem('company_slug');
    const loginPath = companySlug
      ? `/${companySlug}/admin/login`
      : storedSlug
        ? `/${storedSlug}/admin/login`
        : '/company/auth/login';

    return <Navigate to={loginPath} replace state={{
      message: 'Please login to access the company dashboard',
      returnTo: window.location.pathname,
    }} />;
  }

  // If company not found, show error
  if (companyError || !company) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-6xl mb-4">404</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Company Not Found</h1>
          <p className="text-gray-600 mb-4">
            The company "{companySlug}" does not exist or is not active.
          </p>
          <a
            href="/"
            className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Go Home
          </a>
        </div>
      </div>
    );
  }

  // Verify user has access to this specific company
  if (userCompanyIdFromToken && company.id !== userCompanyIdFromToken) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-yellow-500 text-6xl mb-4">403</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h1>
          <p className="text-gray-600 mb-4">
            You don't have permission to access {company.name}'s admin panel.
          </p>
          <a
            href="/company/dashboard"
            className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Go to Your Dashboard
          </a>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};

/**
 * ProtectedCompanyScopedRoute - Protects company admin routes with slug validation
 *
 * This component:
 * 1. Wraps children with CompanyProvider to fetch company info from slug
 * 2. Verifies the user is authenticated as a company user
 * 3. Verifies the user belongs to the company in the URL
 *
 * Usage in routes:
 * ```tsx
 * <Route path="/:companySlug/admin/*" element={
 *   <ProtectedCompanyScopedRoute>
 *     <CompanyLayout />
 *   </ProtectedCompanyScopedRoute>
 * }>
 *   <Route path="dashboard" element={<CompanyDashboardPage />} />
 * </Route>
 * ```
 */
const ProtectedCompanyScopedRoute: React.FC<ProtectedCompanyScopedRouteProps> = ({ children }) => {
  return (
    <CompanyProvider>
      <ProtectedCompanyScopedRouteInner>
        {children}
      </ProtectedCompanyScopedRouteInner>
    </CompanyProvider>
  );
};

export default ProtectedCompanyScopedRoute;
