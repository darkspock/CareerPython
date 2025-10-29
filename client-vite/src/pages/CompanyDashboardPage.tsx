import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Building2, Users, Briefcase, TrendingUp } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function CompanyDashboardPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [companyName] = useState("My Company"); // TODO: Get from API

  return (
    <div>
      {/* Main Content */}
      <div className="max-w-7xl mx-auto">
        {/* Welcome Message */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-xl shadow-lg p-8 mb-8 text-white">
          <h2 className="text-3xl font-bold mb-2">Company Recruitment Dashboard</h2>
          <p className="text-blue-100">Manage your recruitment process efficiently</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Candidates */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Total Candidates</p>
                <p className="text-3xl font-bold text-gray-900">0</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Active Positions */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Active Positions</p>
                <p className="text-3xl font-bold text-gray-900">0</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Briefcase className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          {/* Pending Interviews */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Pending Interviews</p>
                <p className="text-3xl font-bold text-gray-900">0</p>
              </div>
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>

          {/* Total Workflows */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Active Workflows</p>
                <p className="text-3xl font-bold text-gray-900">0</p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Building2 className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button
              onClick={() => navigate('/company/candidates')}
              className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-all text-left"
            >
              <Users className="w-6 h-6 text-blue-600 mb-2" />
              <p className="font-medium text-gray-900">Manage Candidates</p>
              <p className="text-sm text-gray-500">View and manage applicants</p>
            </button>

            <button
              onClick={() => navigate('/company/positions')}
              className="p-4 border-2 border-gray-200 rounded-lg hover:border-green-500 hover:bg-green-50 transition-all text-left"
            >
              <Briefcase className="w-6 h-6 text-green-600 mb-2" />
              <p className="font-medium text-gray-900">Job Positions</p>
              <p className="text-sm text-gray-500">Create and manage positions</p>
            </button>

            <button
              onClick={() => navigate('/company/phases')}
              className="p-4 border-2 border-gray-200 rounded-lg hover:border-yellow-500 hover:bg-yellow-50 transition-all text-left"
            >
              <TrendingUp className="w-6 h-6 text-yellow-600 mb-2" />
              <p className="font-medium text-gray-900">Workflow Board</p>
              <p className="text-sm text-gray-500">Track candidates through stages</p>
            </button>

            <button
              onClick={() => navigate('/company/settings')}
              className="p-4 border-2 border-gray-200 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-all text-left"
            >
              <Building2 className="w-6 h-6 text-purple-600 mb-2" />
              <p className="font-medium text-gray-900">Workflows</p>
              <p className="text-sm text-gray-500">Manage recruitment workflows</p>
            </button>
          </div>
        </div>

        {/* Coming Soon Notice */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-6">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-bold">!</span>
              </div>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-blue-900 mb-1">Dashboard Under Development</h4>
              <p className="text-blue-800">
                The company dashboard is currently under active development.
                More features including candidate management, job positions, interviews, and workflows will be available soon.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
