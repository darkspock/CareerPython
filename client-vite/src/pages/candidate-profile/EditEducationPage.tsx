import React from 'react';
import { CandidateProfileLayout } from '../../components/candidate-profile';
import { ProfileEducationForm } from '../../components/candidate-profile/forms';

const EditEducationPage: React.FC = () => {
  return (
    <CandidateProfileLayout
      title="Gestionar Educación"
      subtitle="Añade, edita o elimina tu formación académica"
      currentSection="education"
    >
      <div className="p-6">
        <ProfileEducationForm />
      </div>
    </CandidateProfileLayout>
  );
};

export default EditEducationPage;