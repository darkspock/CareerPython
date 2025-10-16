import React from 'react';
import { OnboardingLayout } from '../../components/onboarding';
import { ProfileEducationForm } from '../../components/candidate-profile/forms';

const OnboardingEducationPage: React.FC = () => {
  return (
    <OnboardingLayout
      title="Formación Académica"
      subtitle="Añade tu formación académica y certificaciones"
    >
      <ProfileEducationForm />
    </OnboardingLayout>
  );
};

export default OnboardingEducationPage;