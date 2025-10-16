import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';
// import InterviewList from '../components/interview/InterviewList'; // Temporarily disabled
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorAlert from '../components/common/ErrorAlert';
// import { Interview, InterviewFilters, InterviewStatus } from '../types/interview'; // Temporarily disabled

const InterviewPage: React.FC = () => {
  const [activeInterview, setActiveInterview] = useState<any | null>(null); // Temporarily using any
  const [loadingActive, setLoadingActive] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadActiveInterview();
  }, []);

  const loadActiveInterview = async () => {
    try {
      setLoadingActive(true);
      setError(null);
      const interview = await api.getActiveInterview();
      setActiveInterview(interview);
    } catch (err: any) {
      // Active interview not found is not an error
      if (!err.message.includes('404')) {
        setError(err.message || 'Failed to load active interview');
      }
    } finally {
      setLoadingActive(false);
    }
  };

  const handleResumeInterview = async (interviewId: string) => {
    try {
      await api.resumeInterview(interviewId);
      // Redirect to interview interface
      window.location.href = `/interviews/${interviewId}/conduct`;
    } catch (err: any) {
      alert(`Failed to resume interview: ${err.message}`);
    }
  };

  const handleStartNewInterview = () => {
    // Navigate to create interview or template selection
    window.location.href = '/interviews/templates';
  };

  const getActiveInterviewDefaults = (): any => { // Temporarily using any
    if (activeInterview) {
      return {
        status: 'IN_PROGRESS' // Temporarily using string literal
      };
    }
    return {};
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Interview Dashboard</h1>
              <p className="mt-2 text-gray-600">
                Manage your interviews, track progress, and view analytics
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleStartNewInterview}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                New Interview
              </button>

              <button
                onClick={() => window.location.href = '/interviews/templates'}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Browse Templates
              </button>
            </div>
          </div>
        </div>

        {/* Active Interview Alert */}
        {loadingActive ? (
          <div className="mb-6">
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center gap-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                <span className="text-gray-600">Checking for active interviews...</span>
              </div>
            </div>
          </div>
        ) : activeInterview ? (
          <div className="mb-6">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-blue-900">
                      Resume Active Interview
                    </h3>
                    <p className="text-blue-700 mt-1">
                      You have a {activeInterview.interview_type.replace('_', ' ').toLowerCase()} interview in progress
                      {activeInterview.status === 'PAUSED' && ' (currently paused)'}
                    </p>
                    {activeInterview.metadata?.completion_percentage && (
                      <div className="mt-2">
                        <div className="flex items-center gap-2 text-sm text-blue-600">
                          <span>Progress: {Math.round(activeInterview.metadata.completion_percentage)}%</span>
                          <div className="flex-1 max-w-32 bg-blue-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{ width: `${activeInterview.metadata.completion_percentage}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <button
                  onClick={() => handleResumeInterview(activeInterview.id)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  {activeInterview.status === 'PAUSED' ? 'Resume' : 'Continue'}
                </button>
              </div>
            </div>
          </div>
        ) : null}

        {/* Error Alert */}
        {error && (
          <div className="mb-6">
            <ErrorAlert message={error} onRetry={loadActiveInterview} />
          </div>
        )}

        {/* Quick Stats */}
        <div className="mb-8 grid grid-cols-1 md:grid-cols-4 gap-6">
          <QuickStatCard
            title="Total Interviews"
            value="--"
            icon="📋"
            loading={true}
          />
          <QuickStatCard
            title="In Progress"
            value="--"
            icon="⏳"
            loading={true}
          />
          <QuickStatCard
            title="Completed"
            value="--"
            icon="✅"
            loading={true}
          />
          <QuickStatCard
            title="Average Score"
            value="--"
            icon="📊"
            loading={true}
          />
        </div>

        {/* Main Interview List */}
        {/* Temporarily disabled InterviewList component */}
        <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
          <p className="text-gray-600">Interview list component temporarily disabled for admin panel development.</p>
          <p className="text-sm text-gray-500 mt-2">Please use the admin panel at <code>/admin</code> to manage interviews.</p>
        </div>
      </div>
    </div>
  );
};

interface QuickStatCardProps {
  title: string;
  value: string;
  icon: string;
  loading?: boolean;
}

const QuickStatCard: React.FC<QuickStatCardProps> = ({ title, value, icon, loading = false }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">
            {loading ? (
              <div className="animate-pulse bg-gray-200 h-8 w-12 rounded"></div>
            ) : (
              value
            )}
          </p>
        </div>
        <div className="text-2xl">{icon}</div>
      </div>
    </div>
  );
};

export default InterviewPage;