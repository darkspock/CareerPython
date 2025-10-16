import React from 'react';
import { CandidateProfileLayout } from '../../components/candidate-profile';
import { ProfileProjectsForm } from '../../components/candidate-profile/forms';

const EditProjectsPage: React.FC = () => {
  return (
    <CandidateProfileLayout
      title="Gestionar Proyectos"
      subtitle="Añade, edita o elimina tus proyectos personales y profesionales"
      currentSection="projects"
    >
      <div className="p-6">
        <ProfileProjectsForm />
      </div>
    </CandidateProfileLayout>
  );
};

export default EditProjectsPage;