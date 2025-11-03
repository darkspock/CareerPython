import { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, Save, X } from 'lucide-react';
import { api } from '../../lib/api';
import type { CompanyRole, CreateRoleRequest, UpdateRoleRequest } from '../../types/company';

export default function CompanyRolesPage() {
  const [roles, setRoles] = useState<CompanyRole[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingRole, setEditingRole] = useState<CompanyRole | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });

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

  useEffect(() => {
    loadRoles();
  }, []);

  const loadRoles = async () => {
    const companyId = getCompanyId();
    if (!companyId) {
      setError('No se pudo obtener el ID de la empresa');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      console.log('Loading roles for company:', companyId);
      const response = await api.listCompanyRoles(companyId, false);
      console.log('Roles response:', response);
      setRoles(response as CompanyRole[]);
    } catch (err: any) {
      console.error('Error loading roles:', err);
      setError(err.message || 'Failed to load roles');
      setRoles([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      const data: CreateRoleRequest = {
        name: formData.name,
        description: formData.description || undefined,
      };
      await api.createCompanyRole(companyId, data);
      setFormData({ name: '', description: '' });
      setIsCreating(false);
      loadRoles();
    } catch (err: any) {
      alert(err.message || 'Failed to create role');
    }
  };

  const handleUpdate = async () => {
    const companyId = getCompanyId();
    if (!companyId || !editingRole) return;

    try {
      const data: UpdateRoleRequest = {
        name: formData.name,
        description: formData.description || undefined,
      };
      await api.updateCompanyRole(companyId, editingRole.id, data);
      setEditingRole(null);
      setFormData({ name: '', description: '' });
      loadRoles();
    } catch (err: any) {
      alert(err.message || 'Failed to update role');
    }
  };

  const handleDelete = async (roleId: string) => {
    const companyId = getCompanyId();
    if (!companyId) return;

    if (!confirm('Are you sure you want to delete this role?')) return;

    try {
      await api.deleteCompanyRole(companyId, roleId);
      loadRoles();
    } catch (err: any) {
      alert(err.message || 'Failed to delete role');
    }
  };

  const startEdit = (role: CompanyRole) => {
    setEditingRole(role);
    setFormData({ name: role.name, description: role.description || '' });
    setIsCreating(false);
  };

  const startCreate = () => {
    setIsCreating(true);
    setEditingRole(null);
    setFormData({ name: '', description: '' });
  };

  const cancelEdit = () => {
    setEditingRole(null);
    setIsCreating(false);
    setFormData({ name: '', description: '' });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading roles...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {/* Header */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Company Roles</h2>
              <p className="mt-1 text-sm text-gray-500">
                Manage roles that can be assigned to workflow stages
              </p>
            </div>
            {!isCreating && !editingRole && (
              <button
                onClick={startCreate}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                Add Role
              </button>
            )}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 bg-red-50 border-l-4 border-red-500">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Create/Edit Form */}
        {(isCreating || editingRole) && (
          <div className="p-6 bg-gray-50 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {isCreating ? 'Create New Role' : 'Edit Role'}
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Role Name *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g., Senior Backend Engineer"
                  maxLength={100}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Optional description"
                  rows={3}
                />
              </div>
              <div className="flex gap-3">
                <button
                  onClick={isCreating ? handleCreate : handleUpdate}
                  disabled={!formData.name.trim()}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  <Save className="w-4 h-4" />
                  {isCreating ? 'Create' : 'Update'}
                </button>
                <button
                  onClick={cancelEdit}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  <X className="w-4 h-4" />
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Roles List */}
        <div className="divide-y divide-gray-200">
          {!error && roles.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-500 mb-4">No roles created yet</p>
              {!isCreating && (
                <button
                  onClick={startCreate}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Create Your First Role
                </button>
              )}
            </div>
          ) : error && roles.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-red-600 mb-4">Error: {error}</p>
              <button
                onClick={loadRoles}
                className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Retry
              </button>
            </div>
          ) : (
            roles.map((role) => (
              <div
                key={role.id}
                className={`p-6 hover:bg-gray-50 transition-colors ${
                  editingRole?.id === role.id ? 'bg-blue-50' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-semibold text-gray-900">{role.name}</h3>
                      {role.is_active ? (
                        <span className="px-2 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-full">
                          Active
                        </span>
                      ) : (
                        <span className="px-2 py-1 text-xs font-medium text-gray-600 bg-gray-200 rounded-full">
                          Inactive
                        </span>
                      )}
                    </div>
                    {role.description && (
                      <p className="mt-2 text-sm text-gray-600">{role.description}</p>
                    )}
                    <p className="mt-2 text-xs text-gray-400">
                      Created: {new Date(role.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-2 ml-4">
                    <button
                      onClick={() => startEdit(role)}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      title="Edit role"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(role.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete role"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
