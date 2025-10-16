import React from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

interface AdminLayoutProps {
  children?: React.ReactNode;
}

const AdminLayout: React.FC<AdminLayoutProps> = () => {
  const location = useLocation();
  const { t } = useTranslation();

  const navigationItems = [
    { path: '/admin/dashboard', labelKey: 'admin.nav.dashboard', icon: '📊' },
    { path: '/admin/users', labelKey: 'admin.nav.users', icon: '👥' },
    { path: '/admin/candidates', labelKey: 'admin.nav.candidates', icon: '🎯' },
    { path: '/admin/companies', labelKey: 'admin.nav.companies', icon: '🏢' },
    { path: '/admin/job-positions', labelKey: 'admin.nav.jobPositions', icon: '💼' },
    { path: '/admin/interview-templates', labelKey: 'admin.nav.interviewTemplates', icon: '📝' },
  ];

  const isCurrentPath = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">{t('admin.header.title')}</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">{t('admin.header.subtitle')}</span>
              <button className="text-sm text-blue-600 hover:text-blue-800">
                {t('admin.header.logout')}
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <nav className="w-64 bg-white shadow-sm min-h-screen">
          <div className="p-4">
            <ul className="space-y-2">
              {navigationItems.map((item) => (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isCurrentPath(item.path)
                        ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                    }`}
                  >
                    <span className="text-lg">{item.icon}</span>
                    <span>{t(item.labelKey)}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </nav>

        {/* Main content */}
        <main className="flex-1 p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;