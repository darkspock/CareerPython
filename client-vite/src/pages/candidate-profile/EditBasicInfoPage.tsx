import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CandidateProfileLayout } from '../../components/candidate-profile';
import { ProfileBasicInfoForm } from '../../components/candidate-profile/forms';
import { api } from '../../lib/api';

interface CandidateData {
  name?: string;
  date_of_birth?: string;
  city?: string;
  country?: string;
  phone?: string;
  email?: string;
  job_category?: string;
  languages?: Record<string, string>;
  skills?: string[];
  expected_annual_salary?: number;
  current_annual_salary?: number;
  relocation?: boolean;
  work_modality?: string[];
  current_roles?: string[];
  expected_roles?: string[];
}

const EditBasicInfoPage: React.FC = () => {
  const navigate = useNavigate();
  const [candidate, setCandidate] = useState<CandidateData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCandidateData();
  }, []);

  const loadCandidateData = async () => {
    try {
      setLoading(true);

      // Try to get full profile summary first
      let candidateData: CandidateData;
      try {
        const profileSummary = await api.getMyProfileSummary() as any;
        candidateData = profileSummary.candidate;
        } catch (summaryError) {
        console.log('Profile summary not available, trying basic profile:', summaryError);
        candidateData = await api.getMyProfile() as CandidateData;
      }

      setCandidate(candidateData);
    } catch (error) {
      console.error('Error loading candidate data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (data: CandidateData) => {
    // Show success message and navigate back
    navigate('/candidate/profile', {
      state: {
        showSuccessMessage: true,
        successMessage: 'Perfil actualizado correctamente'
      }
    });
  };

  const handleCancel = () => {
    navigate('/candidate/profile');
  };

  if (loading) {
    return (
      <CandidateProfileLayout
        title="Editar Información Personal"
        subtitle="Cargando información..."
        currentSection="profile"
      >
        <div className="p-8 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando datos del perfil...</p>
        </div>
      </CandidateProfileLayout>
    );
  }

  return (
    <CandidateProfileLayout
      title="Editar Información Personal"
      subtitle="Actualiza tus datos personales y profesionales"
      currentSection="profile"
    >
      <div className="p-6">
        <ProfileBasicInfoForm
          initialData={candidate}
          onSave={handleSave}
          onCancel={handleCancel}
          showActions={true}
        />
      </div>
    </CandidateProfileLayout>
  );
};

export default EditBasicInfoPage;