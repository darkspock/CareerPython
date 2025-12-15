import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Briefcase, Building2, Calendar, Clock, CheckCircle, XCircle, Eye } from 'lucide-react';
import { CandidateProfileLayout } from '../../components/candidate-profile';
import { api } from '../../lib/api';
import { Card, CardContent } from '../../components/ui/card';

interface Application {
  id: string;
  job_title: string;
  company_name: string;
  status: string;
  created_at: string;
  updated_at: string | null;
  applied_at: string | null;
  has_customized_content: boolean;
}

const getStatusConfig = (status: string, t: (key: string) => string) => {
  const configs: Record<string, { label: string; color: string; icon: React.ElementType }> = {
    applied: {
      label: t('candidateProfile.applications.statuses.applied'),
      color: 'bg-blue-100 text-blue-800',
      icon: Clock
    },
    reviewing: {
      label: t('candidateProfile.applications.statuses.reviewing'),
      color: 'bg-yellow-100 text-yellow-800',
      icon: Eye
    },
    interviewed: {
      label: t('candidateProfile.applications.statuses.interviewed'),
      color: 'bg-purple-100 text-purple-800',
      icon: Calendar
    },
    accepted: {
      label: t('candidateProfile.applications.statuses.accepted'),
      color: 'bg-green-100 text-green-800',
      icon: CheckCircle
    },
    rejected: {
      label: t('candidateProfile.applications.statuses.rejected'),
      color: 'bg-red-100 text-red-800',
      icon: XCircle
    },
    withdrawn: {
      label: t('candidateProfile.applications.statuses.withdrawn'),
      color: 'bg-gray-100 text-gray-800',
      icon: XCircle
    }
  };
  return configs[status] || { label: status, color: 'bg-gray-100 text-gray-800', icon: Clock };
};

const formatDate = (dateString: string | null) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
};

const ApplicationsPage: React.FC = () => {
  const { t } = useTranslation();
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');

  useEffect(() => {
    loadApplications();
  }, [statusFilter]);

  const loadApplications = async () => {
    try {
      setLoading(true);
      setError('');
      const params: { status?: string } = {};
      if (statusFilter) {
        params.status = statusFilter;
      }
      const data = await api.getMyApplications(params);
      setApplications(data);
    } catch (err) {
      console.error('Error loading applications:', err);
      setError(t('candidateProfile.applications.errorLoading'));
    } finally {
      setLoading(false);
    }
  };

  const statusOptions = [
    { value: '', label: t('candidateProfile.applications.allStatuses') },
    { value: 'applied', label: t('candidateProfile.applications.statuses.applied') },
    { value: 'reviewing', label: t('candidateProfile.applications.statuses.reviewing') },
    { value: 'interviewed', label: t('candidateProfile.applications.statuses.interviewed') },
    { value: 'accepted', label: t('candidateProfile.applications.statuses.accepted') },
    { value: 'rejected', label: t('candidateProfile.applications.statuses.rejected') },
  ];

  if (loading) {
    return (
      <CandidateProfileLayout
        title={t('candidateProfile.applications.title')}
        subtitle={t('candidateProfile.applications.loading')}
        currentSection="applications"
      >
        <div className="p-8 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{t('candidateProfile.applications.loading')}</p>
        </div>
      </CandidateProfileLayout>
    );
  }

  return (
    <CandidateProfileLayout
      title={t('candidateProfile.applications.title')}
      subtitle={t('candidateProfile.applications.subtitle')}
      currentSection="applications"
    >
      <div className="p-6 space-y-6">
        {/* Stats Summary */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-blue-600">{applications.length}</div>
              <p className="text-sm text-gray-500">{t('candidateProfile.applications.stats.total')}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-yellow-600">
                {applications.filter(a => a.status === 'reviewing').length}
              </div>
              <p className="text-sm text-gray-500">{t('candidateProfile.applications.stats.inReview')}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-green-600">
                {applications.filter(a => a.status === 'accepted').length}
              </div>
              <p className="text-sm text-gray-500">{t('candidateProfile.applications.stats.accepted')}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-purple-600">
                {applications.filter(a => a.status === 'interviewed').length}
              </div>
              <p className="text-sm text-gray-500">{t('candidateProfile.applications.stats.interviewed')}</p>
            </CardContent>
          </Card>
        </div>

        {/* Filter */}
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">
            {t('candidateProfile.applications.filterByStatus')}:
          </label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {statusOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Applications List */}
        {applications.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {t('candidateProfile.applications.noApplications.title')}
              </h3>
              <p className="text-gray-500">
                {t('candidateProfile.applications.noApplications.description')}
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {applications.map((application) => {
              const statusConfig = getStatusConfig(application.status, t);
              const StatusIcon = statusConfig.icon;

              return (
                <Card key={application.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <Briefcase className="w-5 h-5 text-gray-400" />
                          <h3 className="text-lg font-semibold text-gray-900">
                            {application.job_title}
                          </h3>
                        </div>
                        <div className="flex items-center gap-2 text-gray-600 mb-3">
                          <Building2 className="w-4 h-4" />
                          <span>{application.company_name}</span>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>{t('candidateProfile.applications.appliedOn')}: {formatDate(application.applied_at)}</span>
                          </div>
                          {application.updated_at && (
                            <div className="flex items-center gap-1">
                              <Clock className="w-4 h-4" />
                              <span>{t('candidateProfile.applications.updatedOn')}: {formatDate(application.updated_at)}</span>
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center">
                        <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${statusConfig.color}`}>
                          <StatusIcon className="w-4 h-4" />
                          {statusConfig.label}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </CandidateProfileLayout>
  );
};

export default ApplicationsPage;
