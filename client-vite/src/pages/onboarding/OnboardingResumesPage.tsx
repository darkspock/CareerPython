import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, CheckCircle } from 'lucide-react';
import { OnboardingLayout } from '../../components/onboarding';
import { api } from '../../lib/api';

interface CreateResumeFormData {
  name: string;
  include_ai_enhancement: boolean;
  general_data: {
    target_role?: string;
    experience?: string;
  };
}

const OnboardingResumesPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<CreateResumeFormData>({
    name: '',
    include_ai_enhancement: false,
    general_data: {
      target_role: '',
      experience: ''
    }
  });
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Generate default name based on current date
  const generateDefaultName = () => {
    const today = new Date();
    const dateStr = today.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long'
    });
    return `Mi Primer CV - ${dateStr}`;
  };

  // Set default name if empty
  React.useEffect(() => {
    if (!formData.name) {
      setFormData(prev => ({
        ...prev,
        name: generateDefaultName()
      }));
    }
  }, []);

  const handleSubmit = async () => {
    setError(null);
    setIsCreating(true);

    try {
      // Create the resume using the existing API
      await api.createResume({
        name: formData.name,
        include_ai_enhancement: formData.include_ai_enhancement,
        general_data: formData.general_data
      });

      // Onboarding complete! Navigate to resumes page to show the newly created resume
      navigate('/candidate/profile/resumes', {
        state: {
          showSuccessMessage: true,
          successMessage: '¡Felicidades! Has completado tu perfil y creado tu primer CV. ¡Bienvenido a tu dashboard!'
        }
      });
    } catch (error) {
      console.error('Error creating resume:', error);
      setError('Error al crear el CV. Por favor, inténtalo de nuevo.');
    } finally {
      setIsCreating(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;

    if (name.startsWith('general_data.')) {
      const fieldName = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        general_data: {
          ...prev.general_data,
          [fieldName]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const canSkip = true; // Allow users to skip creating CV for now

  const handleSkip = () => {
    navigate('/candidate/profile', {
      state: {
        showSuccessMessage: true,
        successMessage: '¡Perfil completado! Puedes crear tu CV más tarde desde tu dashboard.'
      }
    });
  };

  return (
    <OnboardingLayout
      title="Crea tu Primer CV"
      subtitle="Genera un currículum profesional con la información que has proporcionado"
      onNext={handleSubmit}
      nextButtonText={isCreating ? "Creando CV..." : "Crear CV y Finalizar"}
      nextButtonDisabled={isCreating || !formData.name.trim()}
      canSkip={canSkip}
      onSkip={handleSkip}
    >
      <div className="space-y-6">
        {/* Success Preview */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
            <div>
              <h4 className="text-sm font-medium text-green-900">¡Casi terminamos!</h4>
              <p className="text-sm text-green-800 mt-1">
                Has completado tu perfil con experiencia, educación y proyectos.
                Ahora solo falta generar tu CV profesional.
              </p>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {/* Form */}
        <div className="space-y-6">
          {/* Resume Name */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Nombre del CV *
            </label>
            <input
              type="text"
              id="name"
              name="name"
              required
              value={formData.name}
              onChange={handleInputChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="ej. Mi CV Profesional"
            />
            <p className="text-xs text-gray-500 mt-1">
              Dale un nombre descriptivo para identificarlo fácilmente
            </p>
          </div>

          {/* Target Role */}
          <div>
            <label htmlFor="general_data.target_role" className="block text-sm font-medium text-gray-700 mb-2">
              Rol Objetivo (Opcional)
            </label>
            <input
              type="text"
              id="general_data.target_role"
              name="general_data.target_role"
              value={formData.general_data.target_role}
              onChange={handleInputChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="ej. Desarrollador Full Stack Senior"
            />
            <p className="text-xs text-gray-500 mt-1">
              El tipo de posición que buscas
            </p>
          </div>

          {/* Experience to Highlight */}
          <div>
            <label htmlFor="general_data.experience" className="block text-sm font-medium text-gray-700 mb-2">
              Experiencia a Destacar (Opcional)
            </label>
            <textarea
              id="general_data.experience"
              name="general_data.experience"
              rows={3}
              value={formData.general_data.experience}
              onChange={handleInputChange}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="ej. Desarrollo de aplicaciones web, gestión de equipos, metodologías ágiles..."
            />
            <p className="text-xs text-gray-500 mt-1">
              Aspectos específicos de tu experiencia que quieres resaltar
            </p>
          </div>
        </div>

        {/* What's included preview */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <FileText className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <h4 className="text-sm font-medium text-blue-900">¿Qué incluirá tu CV?</h4>
              <ul className="text-sm text-blue-800 mt-2 space-y-1">
                <li>• Tu información personal y de contacto</li>
                <li>• Experiencia laboral que has añadido</li>
                <li>• Formación académica y certificaciones</li>
                <li>• Proyectos y logros destacados</li>
                <li>• Habilidades técnicas que has especificado</li>
              </ul>
              <p className="text-sm text-blue-700 mt-3 font-medium">
                Podrás editar y crear más versiones desde tu dashboard.
              </p>
            </div>
          </div>
        </div>
      </div>
    </OnboardingLayout>
  );
};

export default OnboardingResumesPage;