import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { FileText, Send, Calendar, User, Plus, Edit } from 'lucide-react';
import { CandidateProfileLayout } from '../components/candidate-profile';
import StatCard from '../components/candidate-profile/StatCard';
import QuickActionCard from '../components/candidate-profile/QuickActionCard';
import RecentActivitySection from '../components/candidate-profile/RecentActivitySection';
import { api } from '../lib/api';

interface DashboardStats {
  resumesCount: number;
  applicationsCount: number;
  interviewsCount: number;
  profileCompleteness: number;
}

const CandidateProfilePage: React.FC = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [stats, setStats] = useState<DashboardStats>({
    resumesCount: 0,
    applicationsCount: 0,
    interviewsCount: 0,
    profileCompleteness: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);

      // Load resumes count
      try {
        const resumes = await api.getResumes() as Array<{ id: string }> | { resumes?: Array<{ id: string }> };
        const resumesArray = Array.isArray(resumes) ? resumes : (resumes.resumes || []);
        setStats(prev => ({ ...prev, resumesCount: resumesArray.length }));
      } catch (error) {
        console.log('Could not load resumes:', error);
      }

      // Calculate profile completeness
      try {
        const profile = await api.getMyProfile();
        const completeness = calculateProfileCompleteness(profile);
        setStats(prev => ({ ...prev, profileCompleteness: completeness }));
      } catch (error) {
        console.log('Could not load profile:', error);
      }

      // Mock data for Phase B features (applications and interviews)
      setStats(prev => ({
        ...prev,
        applicationsCount: 0, // Will be implemented in Phase B
        interviewsCount: 0     // Will be implemented in Phase B
      }));

    } catch (error) {
      console.error('Error loading dashboard stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateProfileCompleteness = (profile: any): number => {
    if (!profile) return 0;

    const fields = [
      profile.name,
      profile.email,
      profile.phone,
      profile.city,
      profile.country,
      profile.date_of_birth,
      profile.job_category
    ];

    const completedFields = fields.filter(field => field && field.toString().trim() !== '').length;
    return Math.round((completedFields / fields.length) * 100);
  };

  const handleCreateResume = () => {
    navigate('/candidate/profile/resumes/create');
  };

  const handleEditProfile = () => {
    navigate('/candidate/profile/edit');
  };

  const handleViewResumes = () => {
    navigate('/candidate/profile/resumes');
  };

  const handleViewExperience = () => {
    navigate('/candidate/profile/experience');
  };

  if (loading) {
    return (
      <CandidateProfileLayout
        title={t("candidateProfile.dashboard.title")}
        subtitle={t("candidateProfile.dashboard.loading")}
        currentSection="dashboard"
      >
        <div className="p-8 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{t("candidateProfile.dashboard.loadingStats")}</p>
        </div>
      </CandidateProfileLayout>
    );
  }

  return (
    <CandidateProfileLayout
      title={t("candidateProfile.dashboard.title")}
      subtitle={t("candidateProfile.dashboard.subtitle")}
      currentSection="dashboard"
    >
      <div className="p-6 space-y-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title={t("candidateProfile.stats.resumesCreated")}
            value={stats.resumesCount}
            icon={FileText}
            color="blue"
            subtitle={t("candidateProfile.stats.resumes")}
          />
          <StatCard
            title={t("candidateProfile.stats.applications")}
            value={stats.applicationsCount}
            icon={Send}
            color="green"
            subtitle={t("candidateProfile.stats.comingSoon")}
          />
          <StatCard
            title={t("candidateProfile.stats.interviews")}
            value={stats.interviewsCount}
            icon={Calendar}
            color="orange"
            subtitle={t("candidateProfile.stats.comingSoon")}
          />
          <StatCard
            title={t("candidateProfile.stats.profileComplete")}
            value={`${stats.profileCompleteness}%`}
            icon={User}
            color="purple"
          />
        </div>

        {/* Profile Completion Banner */}
        {stats.profileCompleteness < 100 && (
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">
                  {t("candidateProfile.completionBanner.title")}
                </h3>
                <p className="text-blue-700 mb-4">
                  {t("candidateProfile.completionBanner.description", { percent: stats.profileCompleteness })}
                </p>
                <div className="w-full bg-blue-200 rounded-full h-2 mb-4">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${stats.profileCompleteness}%` }}
                  ></div>
                </div>
              </div>
              <button
                onClick={handleEditProfile}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <Edit className="w-4 h-4" />
                {t("candidateProfile.completionBanner.button")}
              </button>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">{t("candidateProfile.quickActions.title")}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <QuickActionCard
              title={t("candidateProfile.quickActions.generateResume.title")}
              description={t("candidateProfile.quickActions.generateResume.description")}
              icon={Plus}
              action={handleCreateResume}
              buttonText={t("candidateProfile.quickActions.generateResume.button")}
              color="blue"
              badge={stats.resumesCount === 0 ? t("candidateProfile.quickActions.generateResume.badge") : undefined}
            />
            <QuickActionCard
              title={t("candidateProfile.quickActions.manageResumes.title")}
              description={t("candidateProfile.quickActions.manageResumes.description")}
              icon={FileText}
              action={handleViewResumes}
              buttonText={t("candidateProfile.quickActions.manageResumes.button")}
              color="green"
            />
            <QuickActionCard
              title={t("candidateProfile.quickActions.updateExperience.title")}
              description={t("candidateProfile.quickActions.updateExperience.description")}
              icon={User}
              action={handleViewExperience}
              buttonText={t("candidateProfile.quickActions.updateExperience.button")}
              color="purple"
            />
            <QuickActionCard
              title={t("candidateProfile.quickActions.completeProfile.title")}
              description={t("candidateProfile.quickActions.completeProfile.description")}
              icon={Edit}
              action={handleEditProfile}
              buttonText={t("candidateProfile.quickActions.completeProfile.button")}
              color="orange"
            />
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <RecentActivitySection />
        </div>

        {/* Getting Started Guide (for new users) */}
        {stats.resumesCount === 0 && stats.profileCompleteness < 50 && (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">🚀 {t("candidateProfile.gettingStarted.title")}</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  1
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">{t("candidateProfile.gettingStarted.step1.title")}</h3>
                  <p className="text-sm text-gray-600">{t("candidateProfile.gettingStarted.step1.description")}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  2
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">{t("candidateProfile.gettingStarted.step2.title")}</h3>
                  <p className="text-sm text-gray-600">{t("candidateProfile.gettingStarted.step2.description")}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  3
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">{t("candidateProfile.gettingStarted.step3.title")}</h3>
                  <p className="text-sm text-gray-600">{t("candidateProfile.gettingStarted.step3.description")}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </CandidateProfileLayout>
  );
};

export default CandidateProfilePage;