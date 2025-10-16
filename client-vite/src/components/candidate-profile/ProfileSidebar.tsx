import React from 'react';
import {
  User,
  Briefcase,
  GraduationCap,
  FolderOpen,
  FileText,
  Send,
  Calendar,
  Settings,
  Home
} from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

interface ProfileSidebarProps {
  currentSection?: string;
}

const ProfileSidebar: React.FC<ProfileSidebarProps> = ({ currentSection }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();

  const menuItems = [
    {
      id: 'dashboard',
      labelKey: 'candidateProfile.nav.dashboard',
      icon: Home,
      path: '/candidate/profile',
      descriptionKey: 'candidateProfile.nav.dashboardDesc'
    },
    {
      id: 'profile',
      labelKey: 'candidateProfile.nav.profile',
      icon: User,
      path: '/candidate/profile/edit',
      descriptionKey: 'candidateProfile.nav.profileDesc'
    },
    {
      id: 'experience',
      labelKey: 'candidateProfile.nav.experience',
      icon: Briefcase,
      path: '/candidate/profile/experience',
      descriptionKey: 'candidateProfile.nav.experienceDesc'
    },
    {
      id: 'education',
      labelKey: 'candidateProfile.nav.education',
      icon: GraduationCap,
      path: '/candidate/profile/education',
      descriptionKey: 'candidateProfile.nav.educationDesc'
    },
    {
      id: 'projects',
      labelKey: 'candidateProfile.nav.projects',
      icon: FolderOpen,
      path: '/candidate/profile/projects',
      descriptionKey: 'candidateProfile.nav.projectsDesc'
    },
    {
      id: 'resumes',
      labelKey: 'candidateProfile.nav.resumes',
      icon: FileText,
      path: '/candidate/profile/resumes',
      descriptionKey: 'candidateProfile.nav.resumesDesc'
    },
    // Phase B items (grayed out for MVP)
    {
      id: 'applications',
      labelKey: 'candidateProfile.nav.applications',
      icon: Send,
      path: '/candidate/profile/applications',
      descriptionKey: 'candidateProfile.nav.comingSoon',
      disabled: true
    },
    {
      id: 'interviews',
      labelKey: 'candidateProfile.nav.interviews',
      icon: Calendar,
      path: '/candidate/profile/interviews',
      descriptionKey: 'candidateProfile.nav.comingSoon',
      disabled: true
    },
    {
      id: 'settings',
      labelKey: 'candidateProfile.nav.settings',
      icon: Settings,
      path: '/candidate/profile/settings',
      descriptionKey: 'candidateProfile.nav.comingSoon',
      disabled: true
    }
  ];

  const isActive = (item: any) => {
    if (currentSection) {
      return currentSection === item.id;
    }
    return location.pathname === item.path;
  };

  return (
    <aside className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
      {/* Logo/Brand */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">CP</span>
          </div>
          <div>
            <h2 className="font-bold text-gray-900">{t('candidateProfile.header.title')}</h2>
            <p className="text-xs text-gray-500">{t('candidateProfile.header.subtitle')}</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4">
        <div className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item);
            const disabled = item.disabled;

            return (
              <button
                key={item.id}
                onClick={() => !disabled && navigate(item.path)}
                disabled={disabled}
                className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg text-left transition-colors ${
                  disabled
                    ? 'text-gray-400 cursor-not-allowed'
                    : active
                    ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Icon className={`w-5 h-5 ${
                  disabled
                    ? 'text-gray-300'
                    : active
                    ? 'text-blue-600'
                    : 'text-gray-500'
                }`} />
                <div className="flex-1">
                  <div className={`font-medium ${disabled ? 'text-gray-400' : ''}`}>
                    {t(item.labelKey)}
                  </div>
                  <div className="text-xs text-gray-500">
                    {t(item.descriptionKey)}
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Footer */}
      <div className="absolute bottom-0 w-64 p-4 border-t border-gray-200">
        <div className="text-center">
          <p className="text-xs text-gray-500">{t('candidateProfile.footer.brandName')}</p>
          <p className="text-xs text-gray-400">{t('candidateProfile.footer.version')}</p>
        </div>
      </div>
    </aside>
  );
};

export default ProfileSidebar;