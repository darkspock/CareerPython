import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import { useOnboarding } from "../hooks/useOnboarding";

const EducationLevel = {
  HIGH_SCHOOL: "Bachillerato",
  TECHNICAL: "Técnico",
  UNDERGRADUATE: "Universitario",
  GRADUATE: "Postgrado",
  MASTER: "Maestría",
  DOCTORATE: "Doctorado",
  OTHER: "Otro",
};

interface Education {
  institution: string;
  degree: string;
  fieldOfStudy: string;
  level: string;
  startDate: string;
  endDate: string;
  isCurrentStudy: boolean;
  description: string;
}

export default function EducationPage() {
  const [educations, setEducations] = useState<Education[]>([
    {
      institution: "",
      degree: "",
      fieldOfStudy: "",
      level: "",
      startDate: "",
      endDate: "",
      isCurrentStudy: false,
      description: "",
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { jobPositionId } = useOnboarding();

  useEffect(() => {
    // Verificar que el usuario tenga un token de autenticación
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/");
      return;
    }

    // Cargar educaciones existentes
    loadExistingEducations();
  }, [navigate]);

  const loadExistingEducations = async () => {
    try {
      const existingEducations = await api.getEducations();
      
      if (existingEducations && existingEducations.length > 0) {
        // Mapear las educaciones del backend al formato del frontend
        const mappedEducations = existingEducations.map((edu: any) => ({
          institution: edu.institution || "",
          degree: edu.degree || "",
          fieldOfStudy: edu.field_of_study || "",
          level: edu.level || "",
          startDate: edu.start_date || "",
          endDate: edu.end_date || "",
          isCurrentStudy: !edu.end_date,
          description: edu.description || "",
        }));
        
        setEducations(mappedEducations);
      }
    } catch (error) {
      console.error("Error loading existing educations:", error);
      // Si hay error, mantener el estado inicial con una educación vacía
    }
  };

  const addEducation = () => {
    setEducations([
      ...educations,
      {
        institution: "",
        degree: "",
        fieldOfStudy: "",
        level: "",
        startDate: "",
        endDate: "",
        isCurrentStudy: false,
        description: "",
      }
    ]);
  };

  const removeEducation = (index: number) => {
    if (educations.length > 1) {
      setEducations(educations.filter((_, i) => i !== index));
    }
  };

  const updateEducation = (index: number, field: keyof Education, value: string | boolean) => {
    const updated = [...educations];
    updated[index] = { ...updated[index], [field]: value };
    
    // Si marca como estudio actual, limpiar fecha de fin
    if (field === 'isCurrentStudy' && value === true) {
      updated[index].endDate = '';
    }
    
    setEducations(updated);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("No autorizado. Por favor, inicia sesión.");
      setIsLoading(false);
      navigate("/");
      return;
    }

    try {
      // Filtrar educaciones vacías
      const validEducations = educations.filter(edu => 
        edu.institution.trim() && edu.degree.trim()
      );

      if (validEducations.length === 0) {
        setError("Debes agregar al menos una formación académica.");
        setIsLoading(false);
        return;
      }

      // Guardar educaciones en el backend
      for (const education of validEducations) {
        const educationToSave = {
          degree: education.degree,
          institution: education.institution,
          description: education.description || "",
          start_date: education.startDate,
          end_date: education.isCurrentStudy ? null : education.endDate,
        };
        
        await api.createEducation(educationToSave);
      }
      
      // Navegar al siguiente paso (proyectos), preservando jobPositionId
      const nextUrl = jobPositionId
        ? `/candidate/profile/projects?jobPositionId=${jobPositionId}`
        : '/candidate/profile/projects';
      navigate(nextUrl);
    } catch (error) {
      setError("Error al guardar la información educativa. Inténtalo de nuevo.");
    } finally {
      setIsLoading(false);
    }
  };

  const goBack = () => {
    const backUrl = jobPositionId
      ? `/candidate/profile/experience?jobPositionId=${jobPositionId}`
      : '/candidate/profile/experience';
    navigate(backUrl);
  };

  const skipStep = () => {
    const nextUrl = jobPositionId
      ? `/candidate/profile/projects?jobPositionId=${jobPositionId}`
      : '/candidate/profile/projects';
    navigate(nextUrl);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Formación Académica
          </h2>
          <p className="text-gray-600">
            Comparte tu formación académica para completar tu perfil profesional.
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-8">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}

            {educations.map((education, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-6 space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-medium text-gray-900">
                    Formación {index + 1}
                  </h3>
                  {educations.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeEducation(index)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Eliminar
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Institución
                    </label>
                    <input
                      type="text"
                      value={education.institution}
                      onChange={(e) => updateEducation(index, 'institution', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Universidad, colegio, instituto..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nivel Educativo
                    </label>
                    <select
                      value={education.level}
                      onChange={(e) => updateEducation(index, 'level', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Selecciona un nivel</option>
                      {Object.entries(EducationLevel).map(([key, value]) => (
                        <option key={key} value={key}>{value}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Título/Grado
                    </label>
                    <input
                      type="text"
                      value={education.degree}
                      onChange={(e) => updateEducation(index, 'degree', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Ingeniería, Licenciatura, Técnico..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Campo de Estudio
                    </label>
                    <input
                      type="text"
                      value={education.fieldOfStudy}
                      onChange={(e) => updateEducation(index, 'fieldOfStudy', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Sistemas, Administración, Marketing..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Fecha de Inicio
                    </label>
                    <input
                      type="date"
                      value={education.startDate}
                      onChange={(e) => updateEducation(index, 'startDate', e.target.value)}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Fecha de Graduación
                    </label>
                    <input
                      type="date"
                      value={education.endDate}
                      onChange={(e) => updateEducation(index, 'endDate', e.target.value)}
                      disabled={education.isCurrentStudy}
                      className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                    />
                  </div>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id={`current-study-${index}`}
                    checked={education.isCurrentStudy}
                    onChange={(e) => updateEducation(index, 'isCurrentStudy', e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor={`current-study-${index}`} className="ml-2 block text-sm text-gray-900">
                    Estudio actual
                  </label>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Descripción (Opcional)
                  </label>
                  <textarea
                    value={education.description}
                    onChange={(e) => updateEducation(index, 'description', e.target.value)}
                    rows={3}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Menciona logros académicos, proyectos destacados, especialización..."
                  />
                </div>
              </div>
            ))}

            <button
              type="button"
              onClick={addEducation}
              className="w-full py-3 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-500 hover:text-blue-600 transition duration-200"
            >
              + Agregar otra formación
            </button>

            <div className="flex gap-4">
              <button
                type="button"
                onClick={goBack}
                className="flex-1 py-3 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition duration-200"
              >
                ← Atrás
              </button>
              <button
                type="button"
                onClick={skipStep}
                className="flex-1 py-3 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition duration-200"
              >
                Omitir por ahora
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
              >
                {isLoading ? "Guardando..." : "Continuar"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}