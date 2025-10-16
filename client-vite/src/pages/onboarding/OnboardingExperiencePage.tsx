import React from 'react';
import { OnboardingLayout } from '../../components/onboarding';
import { ProfileExperienceForm } from '../../components/candidate-profile/forms';

const OnboardingExperiencePage: React.FC = () => {
  return (
    <OnboardingLayout
      title="Experiencia Laboral"
      subtitle="Añade tu experiencia profesional para completar tu perfil"
    >
      <ProfileExperienceForm />
    </OnboardingLayout>
  );
};

export default OnboardingExperiencePage;