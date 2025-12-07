/**
 * Public Position Detail Page
 * Phase 10: Public job detail with application form
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
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
  HelpCircle
} from 'lucide-react';
import { publicPositionService } from '../../services/publicPositionService';
import { publicQuestionService, type PublicApplicationQuestion } from '../../services/publicQuestionService';
import type { Position } from '../../types/position';
import { getLocation, getIsRemote, getEmploymentType, getSalaryRange, getExperienceLevel, getDepartment, getRequirements } from '../../types/position';
import '../../components/common/WysiwygEditor.css';

export default function PublicPositionDetailPage() {
  const { slugOrId } = useParams<{ slugOrId: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [position, setPosition] = useState<Position | null>(null);
  const [questions, setQuestions] = useState<PublicApplicationQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [applicationSuccess, _setApplicationSuccess] = useState(false);

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

  const handleApply = () => {
    // Phase 10: Redirect to landing page with job position ID for full onboarding flow
    if (position?.id) {
      navigate(`/?jobPositionId=${position.id}`);
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
              {/* Success Message */}
              {applicationSuccess && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                  <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-green-900 mb-2 text-center">
                    Application Submitted!
                  </h3>
                  <p className="text-green-800 text-sm text-center mb-4">
                    Your application has been successfully submitted. We'll review it and get back to you soon.
                  </p>
                  <button
                    onClick={() => navigate('/positions')}
                    className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    Browse More Positions
                  </button>
                </div>
              )}

              {/* Application Section */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Apply for this Position</h3>
                <p className="text-gray-600 text-sm mb-6">
                  Ready to take the next step in your career? Start your application process and we'll guide you through creating your profile.
                </p>
                <button
                  onClick={handleApply}
                  className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium flex items-center justify-center gap-2"
                >
                  <Send className="w-5 h-5" />
                  Start Application
                </button>
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
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-800">
                  <strong>What's next?</strong> You'll be guided through a simple onboarding process where you can upload your resume and complete your profile.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
