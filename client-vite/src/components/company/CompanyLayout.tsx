import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import {
  Building2,
  Users,
  Briefcase,
  Settings,
  LogOut,
  Menu,
  X,
  LayoutDashboard,
  Layers,
  ChevronDown,
  ChevronRight,
  Search
} from 'lucide-react';
import { useState, useEffect } from 'react';
import { recruiterCompanyService } from '../../services/recruiterCompanyService';
import { phaseService } from '../../services/phaseService';
import type { Phase } from '../../types/phase';
import UserSettingsMenu from './UserSettingsMenu';

export default function CompanyLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [companyName, setCompanyName] = useState<string>('Company');
  const [phases, setPhases] = useState<Phase[]>([]);
  const [candidatesMenuOpen, setCandidatesMenuOpen] = useState(false);

  useEffect(() => {
    loadCompanyName();
    loadPhases();
  }, []);

  const getCompanyId = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  };

  const loadCompanyName = async () => {
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      const company = await recruiterCompanyService.getCompany(companyId);
      setCompanyName(company.name);
    } catch (error) {
      console.error('Error loading company name:', error);
    }
  };

  const loadPhases = async () => {
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      const phasesData = await phaseService.listPhases(companyId);
      setPhases(phasesData.sort((a, b) => a.sort_order - b.sort_order));
    } catch (error) {
      console.error('Error loading phases:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/company/login');
  };

  const getPhaseUrl = (phase: Phase) => {
    // Determine the correct view based on phase configuration
    if (phase.default_view === 'KANBAN') {
      return `/company/workflow-board?phase=${phase.id}`;
    } else {
      return `/company/candidates?phase=${phase.id}`;
    }
  };

  const menuItems = [
    { path: '/company/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/company/positions', icon: Briefcase, label: 'Job Positions' },
    { path: '/company/settings', icon: Settings, label: 'Settings' },
  ];

  const isActive = (path: string) => location.pathname === path;
  const isCandidatesActive = location.pathname.startsWith('/company/candidates') || location.pathname.startsWith('/company/workflow-board');

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Mobile Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 z-50 h-screen w-64 bg-white border-r border-gray-200
          transform transition-transform duration-300 ease-in-out lg:hidden
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Logo/Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div className="flex items-center gap-2">
              <Building2 className="w-8 h-8 text-blue-600" />
              <span className="font-bold text-xl text-gray-900">{companyName}</span>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
            {menuItems.slice(0, 1).map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-lg transition-colors
                    ${
                      active
                        ? 'bg-blue-50 text-blue-700 font-medium'
                        : 'text-gray-700 hover:bg-gray-100'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}

            {/* Candidates Menu with Phases */}
            <div>
              <button
                onClick={() => setCandidatesMenuOpen(!candidatesMenuOpen)}
                className={`
                  flex items-center justify-between w-full gap-3 px-4 py-3 rounded-lg transition-colors
                  ${
                    isCandidatesActive
                      ? 'bg-blue-50 text-blue-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-100'
                  }
                `}
              >
                <div className="flex items-center gap-3">
                  <Users className="w-5 h-5" />
                  <span>Candidates</span>
                </div>
                {candidatesMenuOpen ? (
                  <ChevronDown className="w-4 h-4" />
                ) : (
                  <ChevronRight className="w-4 h-4" />
                )}
              </button>

              {/* Phase Submenu */}
              {candidatesMenuOpen && (
                <div className="ml-4 mt-1 space-y-1">
                  {/* Search All Candidates Button */}
                  <Link
                    to="/company/candidates"
                    onClick={() => setSidebarOpen(false)}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm
                      ${
                        location.pathname === '/company/candidates' && !location.search.includes('phase=')
                          ? 'bg-blue-50 text-blue-700 font-medium'
                          : 'text-gray-600 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Search className="w-4 h-4" />
                    <span>Search All Candidates</span>
                  </Link>
                  
                  {/* Phase-specific views */}
                  {phases.map((phase) => (
                    <Link
                      key={phase.id}
                      to={getPhaseUrl(phase)}
                      onClick={() => setSidebarOpen(false)}
                      className={`
                        flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm
                        ${
                          location.search.includes(`phase=${phase.id}`)
                            ? 'bg-blue-50 text-blue-700 font-medium'
                            : 'text-gray-600 hover:bg-gray-100'
                        }
                      `}
                    >
                      <Layers className="w-4 h-4" />
                      <span>{phase.name}</span>
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {menuItems.slice(1).map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-lg transition-colors
                    ${
                      active
                        ? 'bg-blue-50 text-blue-700 font-medium'
                        : 'text-gray-700 hover:bg-gray-100'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </aside>

      {/* Desktop Sidebar */}
      <aside className="sticky top-0 left-0 z-50 h-screen w-64 bg-white border-r border-gray-200 hidden lg:block">
        <div className="flex flex-col h-full">
          {/* Logo/Header */}
          <div className="flex items-center p-6 border-b border-gray-200">
            <div className="flex items-center gap-2">
              <Building2 className="w-8 h-8 text-blue-600" />
              <span className="font-bold text-xl text-gray-900">{companyName}</span>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
            {menuItems.slice(0, 1).map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-lg transition-colors
                    ${
                      active
                        ? 'bg-blue-50 text-blue-700 font-medium'
                        : 'text-gray-700 hover:bg-gray-100'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}

            {/* Candidates Menu with Phases */}
            <div>
              <button
                onClick={() => setCandidatesMenuOpen(!candidatesMenuOpen)}
                className={`
                  flex items-center justify-between w-full gap-3 px-4 py-3 rounded-lg transition-colors
                  ${
                    isCandidatesActive
                      ? 'bg-blue-50 text-blue-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-100'
                  }
                `}
              >
                <div className="flex items-center gap-3">
                  <Users className="w-5 h-5" />
                  <span>Candidates</span>
                </div>
                {candidatesMenuOpen ? (
                  <ChevronDown className="w-4 h-4" />
                ) : (
                  <ChevronRight className="w-4 h-4" />
                )}
              </button>

              {/* Phase Submenu */}
              {candidatesMenuOpen && (
                <div className="ml-4 mt-1 space-y-1">
                  {/* Search All Candidates Button */}
                  <Link
                    to="/company/candidates"
                    onClick={() => setSidebarOpen(false)}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm
                      ${
                        location.pathname === '/company/candidates' && !location.search.includes('phase=')
                          ? 'bg-blue-50 text-blue-700 font-medium'
                          : 'text-gray-600 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Search className="w-4 h-4" />
                    <span>Search All Candidates</span>
                  </Link>
                  
                  {/* Phase-specific views */}
                  {phases.map((phase) => (
                    <Link
                      key={phase.id}
                      to={getPhaseUrl(phase)}
                      onClick={() => setSidebarOpen(false)}
                      className={`
                        flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm
                        ${
                          location.search.includes(`phase=${phase.id}`)
                            ? 'bg-blue-50 text-blue-700 font-medium'
                            : 'text-gray-600 hover:bg-gray-100'
                        }
                      `}
                    >
                      <Layers className="w-4 h-4" />
                      <span>{phase.name}</span>
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {menuItems.slice(1).map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-lg transition-colors
                    ${
                      active
                        ? 'bg-blue-50 text-blue-700 font-medium'
                        : 'text-gray-700 hover:bg-gray-100'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Top Bar (Desktop & Mobile) */}
        <header className="bg-white border-b border-gray-200 relative z-10 overflow-visible">
          <div className="flex items-center justify-between px-4 py-3 overflow-visible">
            {/* Mobile Menu Button */}
            <button
              onClick={() => setSidebarOpen(true)}
              className="text-gray-500 hover:text-gray-700 lg:hidden"
            >
              <Menu className="w-6 h-6" />
            </button>
            
            {/* Title - Only on mobile */}
            <div className="flex items-center gap-2 lg:hidden">
              <Building2 className="w-6 h-6 text-blue-600" />
              <span className="font-semibold text-gray-900">Company Dashboard</span>
            </div>
            
            {/* Navigation Menu (Desktop) */}
            <nav className="hidden lg:flex items-center gap-1 flex-1 relative">
              {menuItems.map((item) => {
                const Icon = item.icon;
                const active = isActive(item.path);
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-lg transition-colors
                      ${
                        active
                          ? 'bg-blue-50 text-blue-700 font-medium'
                          : 'text-gray-700 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
              
              {/* Separator */}
              <div className="flex-1" />
              <div className="h-6 w-px bg-gray-300 mx-2" />
              
              {/* User Settings Menu */}
              <UserSettingsMenu onLogout={handleLogout} />
            </nav>
            
            {/* Mobile: User Menu */}
            <div className="lg:hidden">
              <UserSettingsMenu onLogout={handleLogout} />
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}