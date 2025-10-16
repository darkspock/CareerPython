import React from 'react';
import { OnboardingLayout } from '../../components/onboarding';
import { ProfileProjectsForm } from '../../components/candidate-profile/forms';

const OnboardingProjectsPage: React.FC = () => {
  return (
    <OnboardingLayout
      title="Proyectos"
      subtitle="Añade proyectos relevantes que muestren tus habilidades"
    >
      <ProfileProjectsForm />
    </OnboardingLayout>
  );
};

export default OnboardingProjectsPage;