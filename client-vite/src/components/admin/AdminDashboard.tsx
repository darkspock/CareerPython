import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../lib/api';

interface DashboardStats {
  users_count: number;
  candidates_count: number;
  companies_count: number;
  job_positions_count: number;
  recent_activity: any[];
}

const AdminDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const response = await api.authenticatedRequest('/admin/dashboard') as DashboardStats;
        setStats(response);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="text-red-800">
          <strong>Error:</strong> {error}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Admin Dashboard</h2>
        <p className="text-gray-600 mt-2">
          Welcome to the CareerPython administration panel
        </p>
      </div>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <span className="text-2xl text-blue-600">👥</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Users</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.users_count || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <span className="text-2xl text-green-600">🎯</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Candidates</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.candidates_count || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <span className="text-2xl text-purple-600">🏢</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Companies</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.companies_count || 0}
              </p>
            </div>
          </div>
        </div>

        <div
          className="bg-white p-6 rounded-lg shadow-sm border cursor-pointer hover:shadow-lg transition-shadow duration-200"
          onClick={() => navigate('/admin/positions')}
        >
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <span className="text-2xl text-orange-600">💼</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Job Positions</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.job_positions_count || 0}
              </p>
              <p className="text-xs text-blue-600 mt-1">Click to manage →</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <button className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <span className="text-xl mr-3">👤</span>
            <div className="text-left">
              <p className="font-medium text-gray-900">Create New User</p>
              <p className="text-sm text-gray-600">Add a new user to the system</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/admin/companies')}
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <span className="text-xl mr-3">🏢</span>
            <div className="text-left">
              <p className="font-medium text-gray-900">Manage Companies</p>
              <p className="text-sm text-gray-600">View and manage companies</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/admin/positions')}
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <span className="text-xl mr-3">💼</span>
            <div className="text-left">
              <p className="font-medium text-gray-900">Manage Positions</p>
              <p className="text-sm text-gray-600">View and manage job positions</p>
            </div>
          </button>

          <button className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <span className="text-xl mr-3">📝</span>
            <div className="text-left">
              <p className="font-medium text-gray-900">Create Template</p>
              <p className="text-sm text-gray-600">Add interview template</p>
            </div>
          </button>
        </div>
      </div>

      {/* System Status */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Database Connection</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              Connected
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">API Status</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              Operational
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Background Tasks</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              Running
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;