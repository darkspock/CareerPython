/**
 * Public Position Detail Page
 * Phase 10: Public job detail with application form
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  MapPin,
  DollarSign,
  Clock,
  Briefcase,
  Building2,
  Home,
  AlertCircle,
  CheckCircle,
  Send
} from 'lucide-react';
import { publicPositionService } from '../../services/publicPositionService';
import type { Position } from '../../types/position';

export default function PublicPositionDetailPage() {
  const { slugOrId } = useParams<{ slugOrId: string }>();
  const navigate = useNavigate();
  const [position, setPosition] = useState<Position | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showApplicationForm, setShowApplicationForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [applicationSuccess, setApplicationSuccess] = useState(false);
  const [applicationData, setApplicationData] = useState({
    cover_letter: '',
    referral_source: ''
  });

  useEffect(() => {
    if (slugOrId) {
      loadPosition();
    }
  }, [slugOrId]);

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

  const handleSubmitApplication = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!slugOrId) return;

    try {
      setSubmitting(true);
      setError(null);
      await publicPositionService.submitApplication(slugOrId, applicationData);
      setApplicationSuccess(true);
      setShowApplicationForm(false);
    } catch (err: any) {
      setError(err.message || 'Failed to submit application');
      console.error('Error submitting application:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const getEmploymentTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      FULL_TIME: 'Full-time',
      PART_TIME: 'Part-time',
      CONTRACT: 'Contract',
      TEMPORARY: 'Temporary',
      INTERNSHIP: 'Internship'
    };
    return labels[type] || type;
  };

  const getExperienceLevelLabel = (level: string) => {
    const labels: Record<string, string> = {
      ENTRY: 'Entry Level',
      INTERMEDIATE: 'Intermediate',
      SENIOR: 'Senior',
      LEAD: 'Lead',
      EXECUTIVE: 'Executive'
    };
    return labels[level] || level;
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
                {position.location && (
                  <div className="flex items-center gap-2 text-gray-700">
                    <MapPin className="w-5 h-5 text-gray-400" />
                    <span>{position.location}</span>
                    {position.is_remote && <span className="text-blue-600">(Remote)</span>}
                  </div>
                )}
                {position.employment_type && (
                  <div className="flex items-center gap-2 text-gray-700">
                    <Clock className="w-5 h-5 text-gray-400" />
                    <span>{getEmploymentTypeLabel(position.employment_type)}</span>
                  </div>
                )}
                {position.experience_level && (
                  <div className="flex items-center gap-2 text-gray-700">
                    <Briefcase className="w-5 h-5 text-gray-400" />
                    <span>{getExperienceLevelLabel(position.experience_level)}</span>
                  </div>
                )}
                {position.salary_range_max && (
                  <div className="flex items-center gap-2 text-gray-700">
                    <DollarSign className="w-5 h-5 text-gray-400" />
                    <span>
                      {position.salary_range_min && `$${position.salary_range_min.toLocaleString()} - `}
                      ${position.salary_range_max.toLocaleString()}
                    </span>
                  </div>
                )}
              </div>

              {/* Tags */}
              {position.department && (
                <div className="mt-4 flex flex-wrap gap-2">
                  <span className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full">
                    {position.department}
                  </span>
                </div>
              )}
            </div>

            {/* Description */}
            {position.description && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">About the Position</h2>
                <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                  {position.description}
                </div>
              </div>
            )}

            {/* Requirements */}
            {position.requirements && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Requirements</h2>
                <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                  {position.requirements}
                </div>
              </div>
            )}

            {/* Responsibilities */}
            {position.responsibilities && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Responsibilities</h2>
                <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                  {position.responsibilities}
                </div>
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

              {/* Application Form */}
              {!applicationSuccess && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  {!showApplicationForm ? (
                    <>
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Apply for this Position</h3>
                      <p className="text-gray-600 text-sm mb-6">
                        Ready to take the next step in your career? Click below to submit your application.
                      </p>
                      <button
                        onClick={() => setShowApplicationForm(true)}
                        className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium flex items-center justify-center gap-2"
                      >
                        <Send className="w-5 h-5" />
                        Apply Now
                      </button>
                    </>
                  ) : (
                    <form onSubmit={handleSubmitApplication}>
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Application Form</h3>

                      {error && (
                        <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
                          <p className="text-red-800 text-sm">{error}</p>
                        </div>
                      )}

                      <div className="space-y-4">
                        {/* Cover Letter */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Cover Letter (Optional)
                          </label>
                          <textarea
                            value={applicationData.cover_letter}
                            onChange={(e) => setApplicationData({ ...applicationData, cover_letter: e.target.value })}
                            rows={6}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="Tell us why you're a great fit for this position..."
                          />
                        </div>

                        {/* Referral Source */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            How did you hear about us? (Optional)
                          </label>
                          <input
                            type="text"
                            value={applicationData.referral_source}
                            onChange={(e) => setApplicationData({ ...applicationData, referral_source: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="e.g. LinkedIn, Friend referral, Job board"
                          />
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="mt-6 flex gap-3">
                        <button
                          type="button"
                          onClick={() => setShowApplicationForm(false)}
                          className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                        >
                          Cancel
                        </button>
                        <button
                          type="submit"
                          disabled={submitting}
                          className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                          {submitting ? (
                            <>
                              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                              Submitting...
                            </>
                          ) : (
                            <>
                              <Send className="w-4 h-4" />
                              Submit
                            </>
                          )}
                        </button>
                      </div>
                    </form>
                  )}
                </div>
              )}

              {/* Info Box */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-800">
                  <strong>Note:</strong> You need to be logged in as a candidate to submit an application.
                  If you don't have an account, you'll be prompted to create one.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
