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
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

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
    {
      id: 'applications',
      labelKey: 'candidateProfile.nav.applications',
      icon: Send,
      path: '/candidate/profile/applications',
      descriptionKey: 'candidateProfile.nav.applicationsDesc'
    },
    // Phase B items (grayed out for MVP)
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
    <aside className="w-64 bg-card shadow-sm border-r border-border min-h-screen">
      {/* Logo/Brand */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-sm">CP</span>
          </div>
          <div>
            <h2 className="font-bold text-foreground">{t('candidateProfile.header.title')}</h2>
            <p className="text-xs text-muted-foreground">{t('candidateProfile.header.subtitle')}</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4">
        <div className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item);
            const disabled = item.disabled;

            return (
              <Button
                key={item.id}
                variant="ghost"
                onClick={() => !disabled && navigate(item.path)}
                disabled={disabled}
                className={cn(
                  "w-full justify-start h-auto py-3 px-3",
                  active && "bg-primary/10 text-primary border border-primary/20",
                  disabled && "opacity-50"
                )}
              >
                <Icon className={cn(
                  "w-5 h-5 mr-3 flex-shrink-0",
                  active ? "text-primary" : "text-muted-foreground"
                )} />
                <div className="flex-1 text-left">
                  <div className={cn(
                    "font-medium",
                    active ? "text-primary" : "text-foreground"
                  )}>
                    {t(item.labelKey)}
                  </div>
                  <div className="text-xs text-muted-foreground font-normal">
                    {t(item.descriptionKey)}
                  </div>
                </div>
              </Button>
            );
          })}
        </div>
      </nav>

      {/* Footer */}
      <div className="absolute bottom-0 w-64 p-4 border-t border-border">
        <div className="text-center">
          <p className="text-xs text-muted-foreground">{t('candidateProfile.footer.brandName')}</p>
          <p className="text-xs text-muted-foreground/70">{t('candidateProfile.footer.version')}</p>
        </div>
      </div>
    </aside>
  );
};

export default ProfileSidebar;