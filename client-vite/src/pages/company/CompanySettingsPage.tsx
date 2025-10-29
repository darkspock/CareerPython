import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Workflow, Users, Settings, Layers, RotateCcw, AlertTriangle, Building2, FileText } from 'lucide-react';
import { phaseService } from '../../services/phaseService';

export default function CompanySettingsPage() {
  const navigate = useNavigate();
  const [showResetModal, setShowResetModal] = useState(false);
  const [resetting, setResetting] = useState(false);

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

  const handleResetConfiguration = async () => {
    const companyId = getCompanyId();
    if (!companyId) {
      alert('Company ID not found');
      return;
    }

    try {
      setResetting(true);
      const result = await phaseService.initializeDefaultPhases(companyId);
      setShowResetModal(false);

      if (result && result.length > 0) {
        alert('Configuration initialized successfully! 4 default phases have been created.');
        navigate('/company/settings/phases');
      } else {
        alert('Phases already exist for this company. To reset, please delete existing phases first from the Phase Management page.');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Unknown error occurred';
      alert('Failed to initialize configuration: ' + errorMessage);
    } finally {
      setResetting(false);
    }
  };
  const settingsCards = [
    {
      title: 'Content Pages',
      description: 'Manage company pages and content',
      icon: FileText,
      path: '/company/pages',
      color: 'indigo',
    },
    {
      title: 'Phase Management',
      description: 'Organize recruitment into high-level phases',
      icon: Layers,
      path: '/company/settings/phases',
      color: 'purple',
    },
    {
      title: 'Workflow Settings',
      description: 'Manage recruitment workflows and stages',
      icon: Workflow,
      path: '/company/settings/workflows',
      color: 'blue',
    },
    {
      title: 'Company Roles',
      description: 'Define roles that can be assigned to workflow stages',
      icon: Users,
      path: '/company/settings/roles',
      color: 'green',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Settings className="w-8 h-8 text-gray-700" />
          <h1 className="text-3xl font-bold text-gray-900">Company Settings</h1>
        </div>
        <p className="text-gray-600">
          Configure your company's workflows, roles, and recruitment process
        </p>
      </div>

      {/* Settings Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Company Profile Card */}
        <Link
          to="/company/settings/edit"
          className="group bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-200 hover:border-gray-300"
        >
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-indigo-50 text-indigo-600 group-hover:bg-indigo-100 transition-colors">
              <Building2 className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                Company Profile
              </h2>
              <p className="text-gray-600 text-sm">
                Edit your company name, domain, and public URL slug
              </p>
            </div>
          </div>
        </Link>

        {/* Other Settings Cards */}
        {settingsCards.map((card) => {
          const Icon = card.icon;
          const colorClasses = {
            blue: 'bg-blue-50 text-blue-600 group-hover:bg-blue-100',
            green: 'bg-green-50 text-green-600 group-hover:bg-green-100',
            purple: 'bg-purple-50 text-purple-600 group-hover:bg-purple-100',
          };

          return (
            <Link
              key={card.path}
              to={card.path}
              className="group bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-200 hover:border-gray-300"
            >
              <div className="flex items-start gap-4">
                <div
                  className={`p-3 rounded-lg transition-colors ${
                    colorClasses[card.color as keyof typeof colorClasses]
                  }`}
                >
                  <Icon className="w-6 h-6" />
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                    {card.title}
                  </h2>
                  <p className="text-gray-600 text-sm">{card.description}</p>
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Quick Access Section */}
      <div className="mt-12 bg-gray-50 rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Access</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            to="/company/settings/workflows/create"
            className="flex items-center gap-3 p-4 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-colors"
          >
            <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-semibold">
              +
            </div>
            <div>
              <div className="font-medium text-gray-900">Create New Workflow</div>
              <div className="text-sm text-gray-500">Set up a new recruitment workflow</div>
            </div>
          </Link>
          <Link
            to="/company/settings/roles"
            className="flex items-center gap-3 p-4 bg-white rounded-lg border border-gray-200 hover:border-green-300 hover:bg-green-50 transition-colors"
          >
            <div className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-semibold">
              +
            </div>
            <div>
              <div className="font-medium text-gray-900">Add Company Role</div>
              <div className="text-sm text-gray-500">Define a new role for your team</div>
            </div>
          </Link>
        </div>
      </div>

      {/* Initialize Configuration Section */}
      <div className="mt-8 bg-blue-50 rounded-lg border border-blue-200 p-6">
        <div className="flex items-start gap-3">
          <RotateCcw className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
          <div className="flex-1">
            <h2 className="text-lg font-semibold text-blue-900 mb-2">Initialize Default Phases</h2>
            <p className="text-blue-800 text-sm mb-4">
              Initialize your company's phase configuration with the default setup. This will create 4
              standard phases (Sourcing, Evaluation, Offer & Pre-Onboarding, and Talent Pool) with
              their default workflows. Only works if you don't have existing phases.
            </p>
            <button
              onClick={() => setShowResetModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
              Initialize Default Phases
            </button>
          </div>
        </div>
      </div>

      {/* Reset Confirmation Modal */}
      {showResetModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            {/* Background overlay */}
            <div
              className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
              onClick={() => !resetting && setShowResetModal(false)}
            ></div>

            {/* Modal panel */}
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-6 py-6">
                {/* Header */}
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
                    <RotateCcw className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Initialize Default Phases?
                    </h3>
                  </div>
                </div>

                {/* Content */}
                <div className="mt-4">
                  <p className="text-sm text-gray-600 mb-4">
                    This action will initialize 4 default phases with their workflows:
                  </p>
                  <ul className="list-disc list-inside text-sm text-gray-600 space-y-2 mb-4 ml-4">
                    <li><strong>Sourcing</strong> (Kanban) - Screening and filtering process</li>
                    <li><strong>Evaluation</strong> (Kanban) - Interview and assessment</li>
                    <li><strong>Offer and Pre-Onboarding</strong> (List) - Offer negotiation and documents</li>
                    <li><strong>Talent Pool</strong> (List) - Long-term candidate tracking</li>
                  </ul>
                  <p className="text-sm text-blue-700 font-medium">
                    Note: This will only work if you don't have existing phases. If phases already exist,
                    you'll need to delete them first from the Phase Management page.
                  </p>
                </div>
              </div>

              {/* Footer Actions */}
              <div className="bg-gray-50 px-6 py-4 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowResetModal(false)}
                  disabled={resetting}
                  className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleResetConfiguration}
                  disabled={resetting}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                  {resetting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      Initializing...
                    </>
                  ) : (
                    <>
                      <RotateCcw className="w-4 h-4" />
                      Yes, Initialize Phases
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
