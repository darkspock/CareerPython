/**
 * Public Position Detail Page
 * Phase 10: Public job detail with application form
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import {
  ArrowLeft,
  MapPin,
  DollarSign,
  Clock,
  Briefcase,
  Building2,
  Send,
  AlertCircle,
  CheckCircle,
  HelpCircle,
  Upload,
  Mail,
  Sparkles
} from 'lucide-react';
import { publicPositionService } from '../../services/publicPositionService';
import { publicQuestionService, type PublicApplicationQuestion } from '../../services/publicQuestionService';
import { api } from '../../lib/api';
import type { Position } from '../../types/position';
import { getLocation, getIsRemote, getEmploymentType, getSalaryRange, getExperienceLevel, getDepartment, getRequirements } from '../../types/position';
import { Checkbox } from '../../components/ui/checkbox';
import { Label } from '../../components/ui/label';
import '../../components/common/WysiwygEditor.css';

export default function PublicPositionDetailPage() {
  const { slugOrId } = useParams<{ slugOrId: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [position, setPosition] = useState<Position | null>(null);
  const [questions, setQuestions] = useState<PublicApplicationQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Application form state
  const [email, setEmail] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [gdprConsent, setGdprConsent] = useState(false);
  const [wantsCVHelp, setWantsCVHelp] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [registrationSuccess, setRegistrationSuccess] = useState(false);

  useEffect(() => {
    if (slugOrId) {
      loadPosition();
    }
  }, [slugOrId]);

  useEffect(() => {
    if (position?.id) {
      loadQuestions(position.id);
    }
  }, [position?.id]);

  const loadQuestions = async (positionId: string) => {
    try {
      const data = await publicQuestionService.getQuestionsForPosition(positionId);
      setQuestions(data.sort((a, b) => a.sort_order - b.sort_order));
    } catch (err) {
      // Silently fail - questions are optional
      console.log('No questions configured for this position');
    }
  };

  const loadPosition = async () => {
    if (!slugOrId) return;

    try {
      setLoading(true);
      setError(null);
      const data = await publicPositionService.getPublicPosition(slugOrId);
      setPosition(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load position');
      console.error('Error loading position:', err);
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = email.trim() !== '' && gdprConsent;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isFormValid || !position?.id) return;

    setIsSubmitting(true);
    try {
      const formData = new FormData();
      formData.append('email', email);
      formData.append('gdpr_consent', 'true');
      formData.append('job_position_id', position.id);

      if (position.company_id) {
        formData.append('company_id', position.company_id);
      }

      if (selectedFile) {
        formData.append('resume_file', selectedFile);
      }

      if (wantsCVHelp) {
        formData.append('wants_cv_help', 'true');
      }

      const data = await api.initiateRegistration(formData);

      if (data.success) {
        setRegistrationSuccess(true);
        toast.success('¡Revisa tu correo para verificar tu email!', {
          position: "top-center",
          autoClose: 7000,
        });
      }
    } catch (error: any) {
      console.error('Error:', error);

      let errorMessage = 'Error de conexión. Por favor intenta de nuevo.';
      if (error?.message) {
        errorMessage = error.message;
      }

      if (errorMessage.includes('ya está registrado') || errorMessage.includes('already exists')) {
        const shouldLogin = confirm(`${errorMessage}\n\n¿Quieres ir a la página de login?`);
        if (shouldLogin) {
          navigate('/candidate/auth/login');
          return;
        }
      } else {
        toast.error(errorMessage);
      }
    } finally {
      setIsSubmitting(false);
    }
  };


  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error && !position) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 max-w-md">
          <AlertCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2 text-center">Position Not Found</h2>
          <p className="text-gray-600 mb-6 text-center">{error}</p>
          <button
            onClick={() => navigate('/positions')}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center justify-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Positions
          </button>
        </div>
      </div>
    );
  }

  if (!position) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <button
            onClick={() => navigate('/positions')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Positions
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Position Details */}
          <div className="lg:col-span-2 space-y-6">
            {/* Position Header */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Building2 className="w-8 h-8 text-blue-600" />
                </div>
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">{position.title}</h1>
                  <p className="text-lg text-gray-600">Company Name</p>
                </div>
              </div>

              {/* Quick Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {getLocation(position) && (
                  <div className="flex items-center gap-2 text-gray-700">
                    <MapPin className="w-5 h-5 text-gray-400" />
                    <span>{getLocation(position)}</span>
                    {getIsRemote(position) && <span className="text-blue-600">(Remote)</span>}
                  </div>
                )}
                {getEmploymentType(position) && (
                  <div className="flex items-center gap-2 text-gray-700">
                    <Clock className="w-5 h-5 text-gray-400" />
                    <span>{getEmploymentType(position)}</span>
                  </div>
                )}
                {getExperienceLevel(position) && (
                  <div className="flex items-center gap-2 text-gray-700">
                    <Briefcase className="w-5 h-5 text-gray-400" />
                    <span>{getExperienceLevel(position)}</span>
                  </div>
                )}
                {getSalaryRange(position) && (
                  <div className="flex items-center gap-2 text-gray-700">
                    <DollarSign className="w-5 h-5 text-gray-400" />
                    <span>{String(getSalaryRange(position))}</span>
                  </div>
                )}
              </div>

              {/* Tags */}
              {getDepartment(position) && (
                <div className="mt-4 flex flex-wrap gap-2">
                  <span className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full">
                    {getDepartment(position)}
                  </span>
                </div>
              )}
            </div>

            {/* Description */}
            {position.description && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">About the Position</h2>
                <div 
                  className="prose max-w-none text-gray-700"
                  dangerouslySetInnerHTML={{ __html: position.description }}
                />
              </div>
            )}

            {/* Requirements */}
            {getRequirements(position) && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Requirements</h2>
                <div 
                  className="prose max-w-none text-gray-700"
                  dangerouslySetInnerHTML={{ __html: getRequirements(position) || '' }}
                />
              </div>
            )}

            {/* Responsibilities */}
            {(position as any).responsibilities && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Responsibilities</h2>
                <div 
                  className="prose max-w-none text-gray-700"
                  dangerouslySetInnerHTML={{ __html: (position as any).responsibilities || '' }}
                />
              </div>
            )}
          </div>

          {/* Right Column - Application */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-6">
              {/* Application Section */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                {registrationSuccess ? (
                  /* Success message after registration */
                  <div className="text-center py-4">
                    <div className="h-14 w-14 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Mail className="h-7 w-7 text-green-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">¡Revisa tu correo!</h3>
                    <p className="text-gray-600 text-sm mb-4">
                      Te hemos enviado un enlace de verificación a <strong>{email}</strong>
                    </p>
                    <p className="text-xs text-gray-500">
                      Haz clic en el enlace del correo para completar tu candidatura.
                      Si no lo encuentras, revisa tu carpeta de spam.
                    </p>
                  </div>
                ) : (
                  /* Registration form */
                  <>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Aplicar a esta oferta</h3>
                    <p className="text-gray-600 text-sm mb-4">
                      Completa tu información para enviar tu candidatura
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Email *
                        </label>
                        <input
                          type="email"
                          placeholder="tu@email.com"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          className="w-full px-3 py-2 rounded-lg border border-gray-300 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Currículum (PDF)
                        </label>
                        <label className={`w-full flex items-center justify-center gap-2 rounded-lg h-20 px-3 text-sm font-medium transition-all cursor-pointer border-2 border-dashed ${selectedFile
                          ? "bg-green-50 text-green-700 border-green-300"
                          : "bg-gray-50 border-gray-300 text-gray-600 hover:border-blue-400 hover:bg-blue-50"
                          }`}>
                          {selectedFile ? (
                            <div className="text-center">
                              <CheckCircle className="w-5 h-5 mx-auto mb-1" />
                              <span className="truncate block max-w-[180px] text-xs">{selectedFile.name}</span>
                            </div>
                          ) : (
                            <div className="text-center">
                              <Upload className="w-5 h-5 mx-auto mb-1" />
                              <span className="text-xs">Arrastra o haz clic para subir</span>
                            </div>
                          )}
                          <input
                            type="file"
                            accept=".pdf"
                            className="hidden"
                            onChange={(e) => {
                              const file = e.target.files?.[0];
                              if (file) {
                                setSelectedFile(file);
                              }
                            }}
                          />
                        </label>
                        <p className="text-xs text-gray-500 mt-1">Opcional - Formato PDF</p>

                        {/* CV Builder checkbox */}
                        <div className="flex items-start space-x-2 mt-3 p-2.5 bg-purple-50 rounded-lg border border-purple-100">
                          <Checkbox
                            id="cv-help"
                            checked={wantsCVHelp}
                            onCheckedChange={(checked) => setWantsCVHelp(checked === true)}
                            className="mt-0.5"
                          />
                          <Label htmlFor="cv-help" className="text-xs text-purple-700 leading-relaxed cursor-pointer flex items-center gap-1">
                            <Sparkles className="w-3 h-3" />
                            <strong>Ayúdame a crear un CV profesional</strong>
                          </Label>
                        </div>
                      </div>

                      {/* GDPR Consent Checkbox */}
                      <div className="flex items-start space-x-2 p-3 bg-gray-50 rounded-lg">
                        <Checkbox
                          id="gdpr-consent"
                          checked={gdprConsent}
                          onCheckedChange={(checked) => setGdprConsent(checked === true)}
                          className="mt-0.5"
                        />
                        <Label htmlFor="gdpr-consent" className="text-xs text-gray-600 leading-relaxed cursor-pointer">
                          Acepto el tratamiento de mis datos personales según la{' '}
                          <a href="#" className="text-blue-600 hover:underline">política de privacidad</a>
                          {' '}y autorizo el uso de mi información para este proceso de selección. *
                        </Label>
                      </div>

                      <button
                        type="submit"
                        disabled={!isFormValid || isSubmitting}
                        className={`w-full py-3 rounded-lg text-sm font-semibold transition-all flex items-center justify-center gap-2 ${isFormValid && !isSubmitting
                          ? "bg-blue-600 hover:bg-blue-700 text-white"
                          : "bg-gray-200 text-gray-500 cursor-not-allowed"
                          }`}
                      >
                        <Send className="w-4 h-4" />
                        {isSubmitting ? "Enviando..." : "Enviar candidatura"}
                      </button>

                      <p className="text-xs text-gray-500 text-center">
                        Te enviaremos un correo para verificar tu email
                      </p>
                    </form>
                  </>
                )}
              </div>

              {/* Questions Preview */}
              {questions.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <HelpCircle className="w-5 h-5 text-purple-600" />
                    <h3 className="text-sm font-semibold text-gray-900">{t('publicQuestions.previewTitle')}</h3>
                  </div>
                  <p className="text-xs text-gray-500 mb-4">{t('publicQuestions.previewDescription')}</p>
                  <ul className="space-y-2">
                    {questions.map((question) => (
                      <li key={question.id} className="flex items-start gap-2 text-sm">
                        <span className="w-1.5 h-1.5 rounded-full bg-purple-600 mt-1.5 flex-shrink-0" />
                        <span className="text-gray-700">
                          {question.label}
                          {question.is_required && <span className="text-red-500 ml-1">*</span>}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Info Box */}
              {!registrationSuccess && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-800">
                    <strong>¿Qué sigue?</strong> Te enviaremos un email de verificación. Al confirmarlo, podrás completar tu perfil y responder las preguntas de la aplicación.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
