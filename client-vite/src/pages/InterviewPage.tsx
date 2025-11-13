import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, FileText, Clock, CheckCircle2, BarChart3, Loader2 } from 'lucide-react';
import { api } from '../lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
// Progress component - using simple div for now

const InterviewPage: React.FC = () => {
  const navigate = useNavigate();
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
      navigate(`/interviews/${interviewId}/conduct`);
    } catch (err: any) {
      setError(`Failed to resume interview: ${err.message}`);
    }
  };

  const handleStartNewInterview = () => {
    navigate('/interviews/templates');
  };

  const handleBrowseTemplates = () => {
    navigate('/interviews/templates');
  };

  // const getActiveInterviewDefaults = (): any => { // Temporarily using any
  //   if (activeInterview) {
  //     return {
  //       status: 'IN_PROGRESS' // Temporarily using string literal
  //     };
  //   }
  //   return {};
  // };

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
              <Button onClick={handleStartNewInterview} className="flex items-center gap-2">
                <Plus className="w-5 h-5" />
                New Interview
              </Button>

              <Button onClick={handleBrowseTemplates} variant="outline" className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Browse Templates
              </Button>
            </div>
          </div>
        </div>

        {/* Active Interview Alert */}
        {loadingActive ? (
          <Card className="mb-6">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
                <span className="text-gray-600">Checking for active interviews...</span>
              </div>
            </CardContent>
          </Card>
        ) : activeInterview ? (
          <Alert className="mb-6 border-blue-200 bg-blue-50">
            <Clock className="h-4 w-4 text-blue-600" />
            <AlertTitle className="text-blue-900">Resume Active Interview</AlertTitle>
            <AlertDescription className="text-blue-700">
              <p className="mb-2">
                You have a {activeInterview.interview_type.replace('_', ' ').toLowerCase()} interview in progress
                {activeInterview.status === 'PAUSED' && ' (currently paused)'}
              </p>
              {activeInterview.metadata?.completion_percentage && (
                <div className="mt-3">
                  <div className="flex items-center gap-2 text-sm text-blue-600 mb-2">
                    <span>Progress: {Math.round(activeInterview.metadata.completion_percentage)}%</span>
                  </div>
                  <div className="flex-1 max-w-xs bg-blue-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{ width: `${activeInterview.metadata.completion_percentage}%` }}
                    />
                  </div>
                </div>
              )}
              <div className="mt-4">
                <Button
                  onClick={() => handleResumeInterview(activeInterview.id)}
                  size="sm"
                >
                  {activeInterview.status === 'PAUSED' ? 'Resume' : 'Continue'}
                </Button>
              </div>
            </AlertDescription>
          </Alert>
        ) : null}

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Quick Stats */}
        <div className="mb-8 grid grid-cols-1 md:grid-cols-4 gap-6">
          <QuickStatCard
            title="Total Interviews"
            value="--"
            icon={<FileText className="w-6 h-6" />}
            loading={true}
          />
          <QuickStatCard
            title="In Progress"
            value="--"
            icon={<Clock className="w-6 h-6" />}
            loading={true}
          />
          <QuickStatCard
            title="Completed"
            value="--"
            icon={<CheckCircle2 className="w-6 h-6" />}
            loading={true}
          />
          <QuickStatCard
            title="Average Score"
            value="--"
            icon={<BarChart3 className="w-6 h-6" />}
            loading={true}
          />
        </div>

        {/* Main Interview List */}
        {/* Temporarily disabled InterviewList component */}
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-gray-600">Interview list component temporarily disabled for admin panel development.</p>
              <p className="text-sm text-gray-500 mt-2">Please use the admin panel at <code className="bg-gray-100 px-1 py-0.5 rounded">/admin</code> to manage interviews.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

interface QuickStatCardProps {
  title: string;
  value: string;
  icon: React.ReactNode;
  loading?: boolean;
}

const QuickStatCard: React.FC<QuickStatCardProps> = ({ title, value, icon, loading = false }) => {
  return (
    <Card>
      <CardContent className="pt-6">
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
          <div className="text-gray-400">{icon}</div>
        </div>
      </CardContent>
    </Card>
  );
};

export default InterviewPage;