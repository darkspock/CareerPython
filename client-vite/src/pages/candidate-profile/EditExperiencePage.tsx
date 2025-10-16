import React from 'react';
import { CandidateProfileLayout } from '../../components/candidate-profile';
import { ProfileExperienceForm } from '../../components/candidate-profile/forms';

const EditExperiencePage: React.FC = () => {
  return (
    <CandidateProfileLayout
      title="Gestionar Experiencia Laboral"
      subtitle="Añade, edita o elimina tu experiencia profesional"
      currentSection="experience"
    >
      <div className="p-6">
        <ProfileExperienceForm />
      </div>
    </CandidateProfileLayout>
  );
};

export default EditExperiencePage;