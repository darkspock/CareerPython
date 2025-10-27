import { Link } from 'react-router-dom';
import { Workflow, Users, Settings, Layers } from 'lucide-react';

export default function CompanySettingsPage() {
  const settingsCards = [
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
    </div>
  );
}
