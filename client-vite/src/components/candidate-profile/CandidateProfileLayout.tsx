import React, { useState, useEffect } from 'react';
import ProfileHeader from './ProfileHeader';
import ProfileSidebar from './ProfileSidebar';
import { api } from '../../lib/api';

interface CandidateData {
  name?: string;
  email?: string;
  city?: string;
  country?: string;
  job_category?: string;
  phone?: string;
  date_of_birth?: string;
}

interface CandidateProfileLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  currentSection?: string;
}

const CandidateProfileLayout: React.FC<CandidateProfileLayoutProps> = ({
  children,
  title,
  subtitle,
  currentSection
}) => {
  const [candidate, setCandidate] = useState<CandidateData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCandidateData();
  }, []);

  const loadCandidateData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Try to get full profile summary first
      let candidateData: CandidateData;
      try {
        const profileSummary = await api.getMyProfileSummary() as any;
        candidateData = profileSummary.candidate;
        console.log('Loaded profile summary:', profileSummary);
      } catch (summaryError) {
        console.log('Profile summary not available, trying basic profile:', summaryError);
        candidateData = await api.getMyProfile() as CandidateData;
      }

      setCandidate(candidateData);
    } catch (error) {
      console.error('Error loading candidate data:', error);
      setError('Error al cargar la información del perfil');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando perfil...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Error de Carga</h1>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <ProfileHeader candidate={candidate} />

      <div className="flex">
        {/* Sidebar */}
        <ProfileSidebar currentSection={currentSection} />

        {/* Main Content */}
        <main className="flex-1 p-6">
          {/* Page Title */}
          {title && (
            <div className="mb-6">
              <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
              {subtitle && <p className="text-gray-600 mt-1">{subtitle}</p>}
            </div>
          )}

          {/* Content Container */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default CandidateProfileLayout;