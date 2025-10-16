import React from 'react';
import { Bell, Search, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface CandidateData {
  name?: string;
  email?: string;
  city?: string;
  country?: string;
  job_category?: string;
}

interface ProfileHeaderProps {
  candidate: CandidateData | null;
}

const ProfileHeader: React.FC<ProfileHeaderProps> = ({ candidate }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/auth/login');
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Left side - Welcome message */}
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              ¡Hola, {candidate?.name || 'Candidato'}! 👋
            </h1>
            <p className="text-gray-600 mt-1">
              {candidate?.job_category && (
                <span>{candidate.job_category}</span>
              )}
              {candidate?.city && candidate?.country && (
                <span className="ml-2">📍 {candidate.city}, {candidate.country}</span>
              )}
            </p>
          </div>

          {/* Right side - Actions */}
          <div className="flex items-center gap-4">
            {/* Search */}
            <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
              <Search className="w-5 h-5" />
            </button>

            {/* Notifications */}
            <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 relative">
              <Bell className="w-5 h-5" />
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
            </button>

            {/* User menu */}
            <div className="flex items-center gap-3">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{candidate?.name || 'Usuario'}</p>
                <p className="text-xs text-gray-500">{candidate?.email}</p>
              </div>

              {/* Avatar */}
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white font-medium text-sm">
                  {candidate?.name?.charAt(0)?.toUpperCase() || 'U'}
                </span>
              </div>

              {/* Logout */}
              <button
                onClick={handleLogout}
                className="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
                title="Cerrar sesión"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default ProfileHeader;