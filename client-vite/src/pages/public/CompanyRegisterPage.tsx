/**
 * CompanyRegisterPage Component
 * 
 * Multi-step registration page for companies.
 * 
 * @component
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CompanyRegistrationService } from '../../services/companyRegistrationService';
import UserDataForm from '../../components/registration/UserDataForm';
import CompanyDataForm from '../../components/registration/CompanyDataForm';
import AdditionalOptionsForm from '../../components/registration/AdditionalOptionsForm';
import { 
  CheckCircle, 
  Loader2, 
  AlertCircle, 
  ArrowRight, 
  ArrowLeft,
  Building,
  User,
  Settings,
  Check
} from 'lucide-react';

type Step = 1 | 2 | 3;

export default function CompanyRegisterPage() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState<Step>(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [emailExists, setEmailExists] = useState(false);
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    // User data
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    
    // Company data
    company_name: '',
    domain: '',
    logo_url: '',
    contact_phone: '',
    address: '',
    
    // Options
    initialize_workflows: true,        // NEW: Default to true
    include_example_data: false,       // Keep default false
    accept_terms: false,
    accept_privacy: false
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleFieldChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const validateStep = (step: Step): boolean => {
    const newErrors: Record<string, string> = {};

    if (step === 1) {
      // Validate user data
      if (!formData.email.trim()) {
        newErrors.email = 'El email es requerido';
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        newErrors.email = 'El email no es válido';
      } else if (emailExists) {
        // Prevent continuing if email already exists
        newErrors.email = 'Este email ya está registrado. Por favor, usa otro email o inicia sesión.';
      }

      if (!formData.full_name.trim()) {
        newErrors.full_name = 'El nombre es requerido';
      } else if (formData.full_name.trim().length < 2) {
        newErrors.full_name = 'El nombre debe tener al menos 2 caracteres';
      }

      if (!formData.password) {
        newErrors.password = 'La contraseña es requerida';
      } else if (formData.password.length < 8) {
        newErrors.password = 'La contraseña debe tener al menos 8 caracteres';
      }

      if (!formData.confirmPassword) {
        newErrors.confirmPassword = 'Confirma tu contraseña';
      } else if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Las contraseñas no coinciden';
      }
    } else if (step === 2) {
      // Validate company data
      if (!formData.company_name.trim()) {
        newErrors.company_name = 'El nombre de la empresa es requerido';
      } else if (formData.company_name.trim().length < 3) {
        newErrors.company_name = 'El nombre debe tener al menos 3 caracteres';
      }

      if (!formData.domain.trim()) {
        newErrors.domain = 'El dominio es requerido';
      } else if (!/^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}$/.test(formData.domain)) {
        newErrors.domain = 'El dominio no es válido (ejemplo: miempresa.com)';
      }
    } else if (step === 3) {
      // Validate options
      if (!formData.accept_terms) {
        newErrors.accept_terms = 'Debes aceptar los términos y condiciones';
      }
      if (!formData.accept_privacy) {
        newErrors.accept_privacy = 'Debes aceptar la política de privacidad';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      if (currentStep < 3) {
        setCurrentStep((currentStep + 1) as Step);
      } else {
        handleSubmit();
      }
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep((currentStep - 1) as Step);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    if (!validateStep(3)) return;

    setLoading(true);
    setError(null);

    try {
      const registrationData = {
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name,
        company_name: formData.company_name,
        domain: formData.domain,
        logo_url: formData.logo_url || undefined,
        contact_phone: formData.contact_phone || undefined,
        address: formData.address || undefined,
        initialize_workflows: formData.initialize_workflows,  // NEW
        include_example_data: formData.include_example_data,
        accept_terms: formData.accept_terms,
        accept_privacy: formData.accept_privacy
      };

      let response;
      
      if (emailExists) {
        // Link existing user
        response = await CompanyRegistrationService.linkExistingUserToCompany({
          ...registrationData,
          password: formData.password // For authentication
        });
      } else {
        // Register new company and user
        response = await CompanyRegistrationService.registerCompanyWithUser(registrationData);
      }

      setSuccess(true);
      
      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        if (response.redirect_url) {
          window.location.href = response.redirect_url;
        } else {
          // Use company slug from localStorage (set during registration)
          const companySlug = localStorage.getItem('company_slug');
          if (companySlug) {
            navigate(`/${companySlug}/admin/dashboard`);
          } else {
            navigate('/company/auth/login');
          }
        }
      }, 2000);
    } catch (err: any) {
      setError(err.message || 'Error al registrar la empresa. Intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  const steps = [
    { number: 1, title: 'Datos de Usuario', icon: User },
    { number: 2, title: 'Datos de Empresa', icon: Building },
    { number: 3, title: 'Opciones', icon: Settings }
  ];

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center">
          <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100 mb-4">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">¡Registro Exitoso!</h2>
          <p className="text-gray-600 mb-4">
            Tu empresa ha sido registrada correctamente. Estamos configurando tu cuenta...
          </p>
          <Loader2 className="w-6 h-6 text-blue-600 animate-spin mx-auto" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Registra tu Empresa
          </h1>
          <p className="text-gray-600">
            Crea tu cuenta y comienza a transformar tu proceso de reclutamiento
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => {
              const Icon = step.icon;
              const isActive = currentStep === step.number;
              const isCompleted = currentStep > step.number;

              return (
                <React.Fragment key={step.number}>
                  <div className="flex flex-col items-center flex-1">
                    <div
                      className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${
                        isCompleted
                          ? 'bg-green-500 text-white'
                          : isActive
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-600'
                      }`}
                    >
                      {isCompleted ? (
                        <Check className="w-6 h-6" />
                      ) : (
                        <Icon className="w-6 h-6" />
                      )}
                    </div>
                    <span
                      className={`mt-2 text-sm font-medium ${
                        isActive ? 'text-blue-600' : 'text-gray-600'
                      }`}
                    >
                      {step.title}
                    </span>
                  </div>
                  {index < steps.length - 1 && (
                    <div
                      className={`flex-1 h-1 mx-4 transition-all ${
                        isCompleted ? 'bg-green-500' : 'bg-gray-200'
                      }`}
                    />
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="text-red-800 font-medium">Error</h3>
                <p className="text-red-700 text-sm mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* Step Content */}
          {currentStep === 1 && (
            <UserDataForm
              formData={formData}
              onChange={handleFieldChange}
              errors={errors}
              onEmailCheck={setEmailExists}
            />
          )}

          {currentStep === 2 && (
            <CompanyDataForm
              formData={formData}
              onChange={handleFieldChange}
              errors={errors}
              onDomainValidation={(_isValid, error) => {
                if (error) {
                  setErrors(prev => ({ ...prev, domain: error }));
                } else {
                  setErrors(prev => {
                    const newErrors = { ...prev };
                    delete newErrors.domain;
                    return newErrors;
                  });
                }
              }}
            />
          )}

          {currentStep === 3 && (
            <AdditionalOptionsForm
              formData={formData}
              onChange={handleFieldChange}
              errors={errors}
            />
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={handleBack}
              disabled={currentStep === 1 || loading}
              className="flex items-center px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Anterior
            </button>

            <button
              type="button"
              onClick={handleNext}
              disabled={loading}
              className="flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Procesando...
                </>
              ) : currentStep === 3 ? (
                <>
                  Completar Registro
                  <CheckCircle className="w-5 h-5 ml-2" />
                </>
              ) : (
                <>
                  Siguiente
                  <ArrowRight className="w-5 h-5 ml-2" />
                </>
              )}
            </button>
          </div>
        </div>

        {/* Login Link */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            ¿Ya tienes una cuenta?{' '}
            <a
              href="/company/auth/login"
              className="font-medium text-blue-600 hover:text-blue-700"
            >
              Inicia sesión
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

