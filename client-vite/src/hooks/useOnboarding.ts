import { useState, useCallback, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../lib/api';
import { API_BASE_URL, FRONTEND_URL } from '../config/api';

export interface CandidateFormData {
  // Basic info
  name: string;
  email: string;
  dateOfBirth: string;
  city: string;
  country: string;
  phone: string;
  jobCategory: string;

  // Experience data
  experiences: any[];

  // Education data
  educations: any[];

  // Projects data
  projects: any[];

  // Additional optional fields
  expectedAnnualSalary?: number;
  currentAnnualSalary?: number;
  currency?: string;
  relocation?: boolean;
  workModality?: string[];
  languages?: Record<string, string>;
  otherLanguages?: string;
  linkedinUrl?: string;
  skills?: string[];
  timezone?: string;
  candidateNotes?: string;
}

export const useOnboarding = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  // Extract jobPositionId from URL if present
  const jobPositionId = searchParams.get('jobPositionId');

  // Step definitions
  const steps = [
    { id: 1, title: "Email & CV", path: "/" },
    { id: 2, title: "Perfil Personal", path: "/candidate/onboarding/complete-profile" },
    { id: 3, title: "Experiencia", path: "/candidate/onboarding/experience" },
    { id: 4, title: "Educación", path: "/candidate/onboarding/education" },
    { id: 5, title: "Proyectos", path: "/candidate/onboarding/projects" },
    { id: 6, title: "Revisión CV", path: "/candidate/onboarding/resumes" }
  ];

  // Detect current step based on pathname
  const currentPath = window.location.pathname;
  const currentStepFromPath = steps.find(step => step.path === currentPath)?.id || 1;

  const [currentStep, setCurrentStep] = useState(currentStepFromPath);

  // Initialize candidateData - will be loaded from backend
  const [candidateData, setCandidateData] = useState<Partial<CandidateFormData>>({
    experiences: [],
    educations: [],
    projects: [],
    workModality: [],
    languages: {},
    skills: []
  });

  const [isLoading, setIsLoading] = useState(false);

  // Load candidate data from backend when hook initializes
  const loadCandidateFromBackend = useCallback(async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      console.log('🔍 No auth token found, using default data');
      return;
    }

    setIsLoading(true);
    try {
      console.log('🔄 Loading candidate profile from backend...');
      console.log('🔑 Using token:', token.substring(0, 20) + '...');

      // Test CORS first with a simple endpoint
      try {
        const corsTest = await fetch(`${API_BASE_URL}/cors-test`, {
          method: 'GET',
          headers: {
            'Origin': FRONTEND_URL
          }
        });
        console.log('🌐 CORS test result:', corsTest.ok ? 'SUCCESS' : 'FAILED');
      } catch (corsError) {
        console.error('🌐 CORS test error:', corsError);
      }

      const profile = await api.getMyProfile();

      console.log('✅ Loaded candidate profile:', profile);
      setCandidateData({
        name: profile.name || '',
        email: profile.email || '',
        dateOfBirth: profile.date_of_birth || '',
        city: profile.city || '',
        country: profile.country || '',
        phone: profile.phone || '',
        jobCategory: profile.job_category || '',
        linkedinUrl: profile.linkedin_url || '',
        experiences: [], // Will be loaded separately
        educations: [], // Will be loaded separately
        projects: [], // Will be loaded separately
        workModality: [],
        languages: {},
        skills: []
      });
    } catch (error) {
      console.error('❌ Error loading candidate from backend:', error);
      // This is normal for new users who haven't completed their profile yet
      // Keep default empty state and continue with onboarding flow
      console.log('📝 This is likely a new user - continuing with empty profile state');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Load data when component mounts or when auth token changes
  useEffect(() => {
    loadCandidateFromBackend();
  }, [loadCandidateFromBackend]);

  const updateCandidateData = useCallback(async (data: Partial<CandidateFormData>) => {
    console.log('🔄 Updating candidate data:', data);

    // Update local state immediately for UI responsiveness
    setCandidateData(prev => ({ ...prev, ...data }));

    // Always save to backend if we have auth token - no localStorage fallback
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        console.log('💾 Saving candidate data to backend...');

        // Create updated data by merging with current state
        const updatedCandidateData = { ...candidateData, ...data };

        // Map frontend data to backend format
        const backendData = {
          name: updatedCandidateData.name,
          email: updatedCandidateData.email,
          date_of_birth: updatedCandidateData.dateOfBirth,
          city: updatedCandidateData.city,
          country: updatedCandidateData.country,
          phone: updatedCandidateData.phone,
          job_category: updatedCandidateData.jobCategory,
          linkedin_url: updatedCandidateData.linkedinUrl,
        };

        // Filter out undefined/empty values, but allow empty strings for clearing data
        const filteredData = Object.fromEntries(
          // eslint-disable-next-line @typescript-eslint/no-unused-vars
          Object.entries(backendData).filter(([_, value]) => value !== undefined)
        );

        if (Object.keys(filteredData).length > 0) {
          await api.updateMyProfile(filteredData);
          console.log('✅ Successfully saved to backend');
        }
      } catch (error) {
        console.error('❌ Error saving candidate data to backend:', error);
        // Don't revert local state - let user try again
        throw error; // Re-throw to let calling component handle the error
      }
    } else {
      console.warn('⚠️ No auth token found - data not saved to backend');
    }
  }, [candidateData]);

  const nextStep = useCallback(() => {
    const nextStepNumber = Math.min(currentStep + 1, steps.length);
    setCurrentStep(nextStepNumber);

    const nextStepPath = steps.find(s => s.id === nextStepNumber)?.path;
    if (nextStepPath) {
      // Preserve jobPositionId in navigation if it exists
      const url = jobPositionId ? `${nextStepPath}?jobPositionId=${jobPositionId}` : nextStepPath;
      navigate(url);
    }
  }, [currentStep, steps, navigate, jobPositionId]);

  const prevStep = useCallback(() => {
    const prevStepNumber = Math.max(currentStep - 1, 1);
    setCurrentStep(prevStepNumber);

    const prevStepPath = steps.find(s => s.id === prevStepNumber)?.path;
    if (prevStepPath) {
      // Preserve jobPositionId in navigation if it exists
      const url = jobPositionId ? `${prevStepPath}?jobPositionId=${jobPositionId}` : prevStepPath;
      navigate(url);
    }
  }, [currentStep, steps, navigate, jobPositionId]);

  const goToStep = useCallback((stepId: number) => {
    if (stepId >= 1 && stepId <= steps.length) {
      setCurrentStep(stepId);

      const targetStep = steps.find(s => s.id === stepId);
      if (targetStep) {
        // Preserve jobPositionId in navigation if it exists
        const url = jobPositionId ? `${targetStep.path}?jobPositionId=${jobPositionId}` : targetStep.path;
        navigate(url);
      }
    }
  }, [steps, navigate, jobPositionId]);

  const clearCandidateData = useCallback(() => {
    console.log('🧹 Clearing candidate data - resetting to empty state');
    const defaultData = {
      name: '',
      email: '',
      dateOfBirth: '',
      city: '',
      country: '',
      phone: '',
      jobCategory: '',
      linkedinUrl: '',
      experiences: [],
      educations: [],
      projects: [],
      workModality: [],
      languages: {},
      skills: []
    };
    setCandidateData(defaultData);
    // Backend data will be cleared when user logs out or new session starts
  }, []);

  const isFirstStep = currentStep === 1;
  const isLastStep = currentStep === steps.length;
  const currentStepData = steps.find(s => s.id === currentStep);

  return {
    currentStep,
    steps,
    candidateData,
    jobPositionId,
    updateCandidateData,
    clearCandidateData,
    loadCandidateFromBackend,
    nextStep,
    prevStep,
    goToStep,
    isFirstStep,
    isLastStep,
    currentStepData,
    isLoading
  };
};