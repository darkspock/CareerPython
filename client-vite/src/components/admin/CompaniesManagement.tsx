import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCompanies } from '../../hooks/useCompanies';
import type {
  Company,
  CompanyFormData
} from '../../types/company';
import {
  COMPANY_STATUS_OPTIONS,
  COMPANY_INDUSTRY_OPTIONS,
  COMPANY_SIZE_OPTIONS,
  getCompanyStatusColor,
  getCompanyStatusIcon
} from '../../types/company';

const CompaniesManagement: React.FC = () => {
  const navigate = useNavigate();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingCompany, setEditingCompany] = useState<Company | null>(null);

  // Use custom hook for company management
  const {
    companies,
    stats,
    loading,
    error,
    filters,
    setFilters,
    createCompany,
    updateCompany,
    deleteCompany,
    approveCompany,
    rejectCompany,
    activateCompany,
    deactivateCompany,
    clearError,
    refresh
  } = useCompanies();

  // Form state for create/edit
  const [formData, setFormData] = useState<CompanyFormData>({
    name: '',
    description: '',
    website: '',
    industry: '',
    size: 'medium',
    location: '',
    logo_url: '',
    founded_year: '',
    employee_count: '',
    contact_email: '',
    contact_phone: ''
  });



  const handleCreateCompany = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate required fields
    if (!formData.name || formData.name.trim() === '') {
      alert('Company name is required');
      return;
    }

    try {
      // Map frontend data to backend schema format
      const companyData = {
        // user_id is now optional and not sent
        name: formData.name.trim(),
        sector: formData.industry || null, // Map industry to sector
        size: formData.employee_count ? parseInt(formData.employee_count) : null, // Use employee_count as size
        location: formData.location || null,
        website: formData.website || null,
        culture: { values: [] }, // Basic culture object
        external_data: { source: "admin_panel" }
      };

      await createCompany(companyData);
      setShowCreateModal(false);
      resetForm();
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleUpdateCompany = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingCompany) return;

    // Validate required fields
    if (!formData.name || formData.name.trim() === '') {
      alert('Company name is required');
      return;
    }

    try {
      // Map frontend data to backend schema format for update
      const companyData = {
        name: formData.name.trim(),
        sector: formData.industry || null, // Map industry to sector
        size: formData.employee_count ? parseInt(formData.employee_count) : null, // Use employee_count as size
        location: formData.location || null,
        website: formData.website || null,
        culture: { values: [] }, // Basic culture object
        external_data: { source: "admin_panel" }
      };

      await updateCompany(editingCompany.id, companyData);
      setEditingCompany(null);
      resetForm();
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleDeleteCompany = async (companyId: string) => {
    if (!confirm('Are you sure you want to delete this company?')) return;

    try {
      await deleteCompany(companyId);
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleApproveCompany = async (companyId: string) => {
    try {
      await approveCompany(companyId);
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleRejectCompany = async (companyId: string) => {
    const reason = prompt('Please provide a reason for rejection:');
    if (!reason) return;

    try {
      await rejectCompany(companyId, reason);
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleActivateCompany = async (companyId: string) => {
    try {
      await activateCompany(companyId);
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleDeactivateCompany = async (companyId: string) => {
    try {
      await deactivateCompany(companyId);
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleOpenPositions = (companyId: string) => {
    // Navigate to positions page with company filter
    navigate(`/admin/positions?companyId=${companyId}`);
  };

  const handleEditCompany = (company: Company) => {
    setEditingCompany(company);
    setFormData({
      name: company.name || '',
      description: '', // Backend doesn't have description
      website: company.website || '',
      industry: (company as any).sector || '', // Map sector to industry
      size: company.size || '',
      location: company.location || '',
      logo_url: company.logo_url || '',
      founded_year: company.founded_year?.toString() || '',
      employee_count: ((company as any).size || company.employee_count)?.toString() || '', // Map size to employee_count
      contact_email: company.contact_email || '',
      contact_phone: company.contact_phone || ''
    });
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      website: '',
      industry: '',
      size: 'medium',
      location: '',
      logo_url: '',
      founded_year: '',
      employee_count: '',
      contact_email: '',
      contact_phone: ''
    });
    setEditingCompany(null);
    setShowCreateModal(false);
  };


  const getActionButtons = (company: Company) => {
    const buttons = [];

    // Approve button - only for pending companies
    buttons.push(
      <div key="approve" className="relative group">
        <button
          onClick={() => handleApproveCompany(company.id)}
          disabled={company.status !== 'pending'}
          className={`p-1 rounded ${
            company.status === 'pending'
              ? 'text-green-600 hover:text-green-900 hover:bg-green-50 cursor-pointer'
              : 'text-gray-300 cursor-not-allowed'
          }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          {company.status === 'pending' ? 'Aprobar empresa' : 'Solo empresas pendientes pueden ser aprobadas'}
        </div>
      </div>
    );

    // Reject button - only for pending companies
    buttons.push(
      <div key="reject" className="relative group">
        <button
          onClick={() => handleRejectCompany(company.id)}
          disabled={company.status !== 'pending'}
          className={`p-1 rounded ${
            company.status === 'pending'
              ? 'text-red-600 hover:text-red-900 hover:bg-red-50 cursor-pointer'
              : 'text-gray-300 cursor-not-allowed'
          }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          {company.status === 'pending' ? 'Rechazar empresa' : 'Solo empresas pendientes pueden ser rechazadas'}
        </div>
      </div>
    );

    // Activate button - only for inactive companies
    buttons.push(
      <div key="activate" className="relative group">
        <button
          onClick={() => handleActivateCompany(company.id)}
          disabled={company.status !== 'inactive'}
          className={`p-1 rounded ${
            company.status === 'inactive'
              ? 'text-green-600 hover:text-green-900 hover:bg-green-50 cursor-pointer'
              : 'text-gray-300 cursor-not-allowed'
          }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          {company.status === 'inactive'
            ? 'Activar empresa'
            : 'Solo empresas inactivas pueden ser activadas'}
        </div>
      </div>
    );

    // Deactivate button - only for active companies
    buttons.push(
      <div key="deactivate" className="relative group">
        <button
          onClick={() => handleDeactivateCompany(company.id)}
          disabled={company.status !== 'active'}
          className={`p-1 rounded ${
            company.status === 'active'
              ? 'text-orange-600 hover:text-orange-900 hover:bg-orange-50 cursor-pointer'
              : 'text-gray-300 cursor-not-allowed'
          }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          {company.status === 'active' ? 'Desactivar empresa' : 'Solo empresas activas pueden ser desactivadas'}
        </div>
      </div>
    );

    // Open Positions button - only for active companies
    buttons.push(
      <div key="positions" className="relative group">
        <button
          onClick={() => handleOpenPositions(company.id)}
          disabled={company.status !== 'active'}
          className={`p-1 rounded ${
            company.status === 'active'
              ? 'text-purple-600 hover:text-purple-900 hover:bg-purple-50 cursor-pointer'
              : 'text-gray-300 cursor-not-allowed'
          }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6.5M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m-8 0h8m0 0V8a2 2 0 012 2v4.5M12 15l.01 0M12 12l.01 0M12 9l.01.01M21 12c0 .796-.343 1.536-.886 2.032m-5.228.968L12 15l-2.886 0M3 12c0 .796.343 1.536.886 2.032m5.228.968L12 15l2.886 0" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          {company.status === 'active' ? 'Abrir posiciones' : 'Solo empresas activas pueden abrir posiciones'}
        </div>
      </div>
    );

    // Edit button - always enabled
    buttons.push(
      <div key="edit" className="relative group">
        <button
          onClick={() => handleEditCompany(company)}
          className="text-blue-600 hover:text-blue-900 hover:bg-blue-50 p-1 rounded cursor-pointer"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          Editar empresa
        </div>
      </div>
    );

    // Delete button - disabled for active companies (business rule)
    buttons.push(
      <div key="delete" className="relative group">
        <button
          onClick={() => handleDeleteCompany(company.id)}
          disabled={!['rejected', 'inactive'].includes(company.status)}
          className={`p-1 rounded ${
            ['rejected', 'inactive'].includes(company.status)
              ? 'text-red-600 hover:text-red-900 hover:bg-red-50 cursor-pointer'
              : 'text-gray-300 cursor-not-allowed'
          }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          {['rejected', 'inactive'].includes(company.status)
            ? 'Eliminar empresa'
            : 'Solo empresas rechazadas o inactivas pueden ser eliminadas'}
        </div>
      </div>
    );

    return buttons;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Companies Management</h1>
          <p className="text-gray-600">Manage company registrations and approvals</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Company
        </button>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <StatsCard title="Total Companies" value={stats.total_companies} icon="🏢" />
          <StatsCard title="Pending Approval" value={stats.pending_approval} icon="⏳" color="yellow" />
          <StatsCard title="Approved" value={stats.approved_companies} icon="✅" color="blue" />
          <StatsCard title="Active" value={stats.active_companies} icon="🟢" color="green" />
          <StatsCard title="Rejected" value={stats.rejected_companies} icon="❌" color="red" />
        </div>
      )}

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow-sm border">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input
              type="text"
              placeholder="Search companies..."
              value={filters.search_term || ''}
              onChange={(e) => setFilters({ ...filters, search_term: e.target.value, page: 1 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              value={filters.status || ''}
              onChange={(e) => setFilters({ ...filters, status: (e.target.value as any) || undefined, page: 1 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {COMPANY_STATUS_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
            <select
              value={filters.industry || ''}
              onChange={(e) => setFilters({ ...filters, industry: (e.target.value as any) || undefined, page: 1 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {COMPANY_INDUSTRY_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Size</label>
            <select
              value={filters.size || ''}
              onChange={(e) => setFilters({ ...filters, size: (e.target.value as any) || undefined, page: 1 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {COMPANY_SIZE_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={refresh}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="text-red-800">
            <strong>Error:</strong> {error}
            <button
              onClick={clearError}
              className="ml-2 text-red-600 hover:text-red-800"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Companies Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Company
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Industry
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Size
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {companies.map((company) => (
                  <tr key={company.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <button
                          onClick={() => handleEditCompany(company)}
                          className="text-sm font-medium text-blue-600 hover:text-blue-800 hover:underline text-left"
                        >
                          {company.name}
                        </button>
                        <div className="text-sm text-gray-500">{company.description}</div>
                        {company.website && (
                          <a
                            href={company.website.startsWith('http') ? company.website : `https://${company.website}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-blue-600 hover:text-blue-800"
                          >
                            🌐 {company.website}
                          </a>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {company.industry}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {company.size}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getCompanyStatusColor(company.status)}`}>
                        {getCompanyStatusIcon(company.status)} {company.status.charAt(0).toUpperCase() + company.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {company.location}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center space-x-1">
                        {getActionButtons(company)}
                      </div>
                    </td>
                  </tr>
                ))}
                {companies.length === 0 && !loading && (
                  <tr>
                    <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                      No companies found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Create/Edit Modal */}
      {(showCreateModal || editingCompany) && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-[600px] max-w-2xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingCompany ? 'Edit Company' : 'Create New Company'}
              </h3>
              <form onSubmit={editingCompany ? handleUpdateCompany : handleCreateCompany}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea
                      required
                      rows={3}
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Website</label>
                    <input
                      type="text"
                      placeholder="example.com"
                      value={formData.website}
                      onChange={(e) => setFormData({ ...formData, website: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                    <p className="text-xs text-gray-500 mt-1">No es necesario incluir http:// o https://</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
                    <select
                      value={formData.industry}
                      onChange={(e) => setFormData({ ...formData, industry: e.target.value as any })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Select industry...</option>
                      {COMPANY_INDUSTRY_OPTIONS.slice(1).map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Size</label>
                    <select
                      value={formData.size}
                      onChange={(e) => setFormData({ ...formData, size: e.target.value as any })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Select size...</option>
                      {COMPANY_SIZE_OPTIONS.slice(1).map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                    <input
                      type="text"
                      value={formData.location}
                      onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    type="button"
                    onClick={resetForm}
                    className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                  >
                    {loading ? 'Saving...' : (editingCompany ? 'Update' : 'Create')}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

interface StatsCardProps {
  title: string;
  value: number;
  icon: string;
  color?: 'yellow' | 'blue' | 'green' | 'red' | 'gray';
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, icon, color = 'gray' }) => {
  const colorClasses = {
    yellow: 'bg-yellow-50 border-yellow-200',
    blue: 'bg-blue-50 border-blue-200',
    green: 'bg-green-50 border-green-200',
    red: 'bg-red-50 border-red-200',
    gray: 'bg-gray-50 border-gray-200'
  };

  return (
    <div className={`p-4 border rounded-lg ${colorClasses[color]}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <div className="text-2xl">{icon}</div>
      </div>
    </div>
  );
};

export default CompaniesManagement;