import React from 'react';
import { useParams } from 'react-router-dom';
import { CompanyProvider, useCompany } from '../../context/CompanyContext';

interface PublicCompanyRouteProps {
  children: React.ReactNode;
}

/**
 * Inner component that handles company loading and error states
 */
const PublicCompanyRouteInner: React.FC<PublicCompanyRouteProps> = ({ children }) => {
  const { companySlug } = useParams<{ companySlug: string }>();
  const { company, isLoading, error } = useCompany();

  // Show loading state while fetching company
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

  // If company not found, show error
  if (error || !company) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-6xl mb-4">404</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Company Not Found</h1>
          <p className="text-gray-600 mb-4">
            The company "{companySlug}" does not exist or is not active.
          </p>
          <a
            href="/positions"
            className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Browse All Jobs
          </a>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};

/**
 * PublicCompanyRoute - Wrapper for public company pages
 *
 * This component:
 * 1. Wraps children with CompanyProvider to fetch company info from slug
 * 2. Shows loading state while fetching
 * 3. Shows 404 if company not found
 * 4. Does NOT require authentication
 *
 * Usage in routes:
 * ```tsx
 * <Route path="/:companySlug/positions" element={
 *   <PublicCompanyRoute>
 *     <CompanyPositionsPage />
 *   </PublicCompanyRoute>
 * } />
 * ```
 */
const PublicCompanyRoute: React.FC<PublicCompanyRouteProps> = ({ children }) => {
  return (
    <CompanyProvider>
      <PublicCompanyRouteInner>
        {children}
      </PublicCompanyRouteInner>
    </CompanyProvider>
  );
};

export default PublicCompanyRoute;
