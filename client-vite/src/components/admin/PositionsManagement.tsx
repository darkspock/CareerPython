import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { usePositions } from '../../hooks/usePositions';
import { useLanguageEnums, usePositionEnums } from '../../hooks/useEnums';
import type { Position, PositionFormData } from '../../types/position';
import CompanySelector from '../common/CompanySelector';

// StatsCard component for displaying statistics
const StatsCard: React.FC<{ title: string; value: number; icon: string; color?: 'blue' | 'green' | 'yellow' | 'red' | 'purple' }> = ({
  title,
  value,
  icon,
  color = 'blue'
}) => {
  const colorClasses = {
    blue: 'text-blue-600 bg-blue-50',
    green: 'text-green-600 bg-green-50',
    yellow: 'text-yellow-600 bg-yellow-50',
    red: 'text-red-600 bg-red-50',
    purple: 'text-purple-600 bg-purple-50'
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <span className="text-2xl">{icon}</span>
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  );
};

export const PositionsManagement: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const companyIdFilter = searchParams.get('companyId');

  // Fetch dynamic enums
  const { languages, languageLevels, loading: enumsLoading } = useLanguageEnums();
  const { desiredRoles, workLocationTypes } = usePositionEnums();

  // Initialize hook with company filter if present
  const {
    positions,
    stats,
    loading,
    error,
    filters,
    pagination,
    createPosition,
    updatePosition,
    deletePosition,
    activatePosition,
    deactivatePosition,
    setFilters,
    clearError
  } = usePositions({
    initialFilters: companyIdFilter ? { company_id: companyIdFilter } : {},
    autoFetch: true
  });

  // Modal and form state
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingPosition, setEditingPosition] = useState<Position | null>(null);
  const [formData, setFormData] = useState<PositionFormData>({
    company_id: companyIdFilter || '',
    title: '',
    description: '',
    department: '',
    location: '',
    work_location_type: 'on_site',
    employment_type: 'full_time',
    experience_level: 'mid',
    salary_min: '',
    salary_max: '',
    salary_currency: 'USD',
    requirements: '',
    benefits: '',
    skills: '',
    application_deadline: '',
    application_url: '',
    application_email: '',
    contact_person: '',
    // Updated fields
    working_hours: '',
    travel_required: 0,
    visa_sponsorship: false,
    reports_to: '',
    number_of_openings: '1',
    job_category: 'other',
    languages_required: [],
    desired_roles: []
  });

  // Search and filter state
  const [searchTerm, setSearchTerm] = useState('');
  const [companyFilter, setCompanyFilter] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState('');
  const [locationFilter, setLocationFilter] = useState('');
  const [employmentTypeFilter, setEmploymentTypeFilter] = useState('');
  const [experienceLevelFilter, setExperienceLevelFilter] = useState('');
  const [isRemoteFilter, setIsRemoteFilter] = useState<boolean | undefined>(undefined);
  const [isActiveFilter, setIsActiveFilter] = useState<boolean | undefined>(undefined);

  // Apply filters when they change
  useEffect(() => {
    const newFilters = {
      ...filters,
      search_term: searchTerm || undefined,
      company_id: companyFilter || undefined,
      department: departmentFilter || undefined,
      location: locationFilter || undefined,
      employment_type: employmentTypeFilter || undefined,
      experience_level: experienceLevelFilter || undefined,
      is_remote: isRemoteFilter,
      is_active: isActiveFilter,
      page: 1 // Reset to first page when filters change
    };
    setFilters(newFilters);
  }, [searchTerm, companyFilter, departmentFilter, locationFilter, employmentTypeFilter, experienceLevelFilter, isRemoteFilter, isActiveFilter]);

  // Clear company filter function
  const clearCompanyFilter = () => {
    const newParams = new URLSearchParams(searchParams);
    newParams.delete('companyId');
    setSearchParams(newParams);
    setFilters({ ...filters, company_id: undefined });
    setCompanyFilter(''); // Clear local company filter state
  };

  // Form handlers
  const handleCreatePosition = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const positionData = {
        company_id: formData.company_id,
        title: formData.title,
        description: formData.description,
        department: formData.department || undefined,
        location: formData.location,
        employment_type: formData.employment_type,
        experience_level: formData.experience_level,
        salary_min: formData.salary_min ? parseInt(formData.salary_min) : undefined,
        salary_max: formData.salary_max ? parseInt(formData.salary_max) : undefined,
        salary_currency: formData.salary_currency || undefined,
        requirements: formData.requirements ? formData.requirements.split('\n').filter(r => r.trim()) : [],
        benefits: formData.benefits ? formData.benefits.split('\n').filter(b => b.trim()) : [],
        skills: formData.skills ? formData.skills.split('\n').filter(s => s.trim()) : [],
        work_location_type: formData.work_location_type,
        application_deadline: formData.application_deadline || undefined,
        application_url: formData.application_url || undefined,
        application_email: formData.application_email || undefined,
        // New fields
        working_hours: formData.working_hours || undefined,
        travel_required: typeof formData.travel_required === 'number' ? formData.travel_required : (formData.travel_required ? 1 : 0),
        visa_sponsorship: formData.visa_sponsorship,
        contact_person: formData.contact_person || undefined,
        reports_to: formData.reports_to || undefined,
        number_of_openings: formData.number_of_openings ? parseInt(formData.number_of_openings) : 1,
        job_category: formData.job_category,
        languages_required: formData.languages_required && formData.languages_required.length > 0
          ? formData.languages_required.reduce((acc, langReq) => {
              if (langReq.language && langReq.level) {
                acc[langReq.language] = langReq.level;
              }
              return acc;
            }, {} as Record<string, string>)
          : undefined,
        desired_roles: formData.desired_roles
      };

      await createPosition(positionData);
      resetForm();
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleUpdatePosition = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingPosition) return;
    try {
      const positionData = {
        title: formData.title,
        description: formData.description,
        department: formData.department || undefined,
        location: formData.location,
        employment_type: formData.employment_type,
        experience_level: formData.experience_level,
        salary_min: formData.salary_min ? parseInt(formData.salary_min) : undefined,
        salary_max: formData.salary_max ? parseInt(formData.salary_max) : undefined,
        salary_currency: formData.salary_currency || undefined,
        requirements: formData.requirements ? formData.requirements.split('\n').filter(r => r.trim()) : [],
        benefits: formData.benefits ? formData.benefits.split('\n').filter(b => b.trim()) : [],
        skills: formData.skills ? formData.skills.split('\n').filter(s => s.trim()) : [],
        work_location_type: formData.work_location_type,
        application_deadline: formData.application_deadline || undefined,
        application_url: formData.application_url || undefined,
        application_email: formData.application_email || undefined,
        // New fields
        working_hours: formData.working_hours || undefined,
        travel_required: typeof formData.travel_required === 'number' ? formData.travel_required : (formData.travel_required ? 1 : 0),
        visa_sponsorship: formData.visa_sponsorship,
        contact_person: formData.contact_person || undefined,
        reports_to: formData.reports_to || undefined,
        number_of_openings: formData.number_of_openings ? parseInt(formData.number_of_openings) : undefined,
        job_category: formData.job_category,
        languages_required: formData.languages_required && formData.languages_required.length > 0
          ? formData.languages_required.reduce((acc, langReq) => {
              if (langReq.language && langReq.level) {
                acc[langReq.language] = langReq.level;
              }
              return acc;
            }, {} as Record<string, string>)
          : undefined,
        desired_roles: formData.desired_roles
      };

      await updatePosition(editingPosition.id, positionData);
      resetForm();
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleDeletePosition = async (positionId: string) => {
    if (!confirm('Are you sure you want to delete this position?')) return;
    try {
      await deletePosition(positionId);
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleActivatePosition = async (positionId: string) => {
    try {
      await activatePosition(positionId);
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleDeactivatePosition = async (positionId: string) => {
    try {
      await deactivatePosition(positionId);
    } catch (err: any) {
      // Error is already handled by the hook
    }
  };

  const handleEditPosition = (position: Position) => {
    // Debug: Let's see what data we're getting
    console.log('Editing position data:', {
      languages_required: position.languages_required,
      desired_roles: position.desired_roles,
      languages_type: typeof position.languages_required,
      roles_type: typeof position.desired_roles
    });

    setEditingPosition(position);

    // Helper function to safely handle legacy and new fields
    const getSalaryMin = () => {
      if (position.salary_range?.min_amount) return position.salary_range.min_amount.toString();
      if (position.salary_min) return position.salary_min.toString();
      return '';
    };

    const getSalaryMax = () => {
      if (position.salary_range?.max_amount) return position.salary_range.max_amount.toString();
      if (position.salary_max) return position.salary_max.toString();
      return '';
    };

    const getSalaryCurrency = () => {
      if (position.salary_range?.currency) return position.salary_range.currency;
      if (position.salary_currency) return position.salary_currency;
      return 'USD';
    };

    const newFormData: PositionFormData = {
      company_id: position.company_id,
      workflow_id: position.workflow_id || null,
      title: position.title,
      description: position.description || '',
      department: position.department || '',
      location: position.location || '',
      work_location_type: position.work_location_type || 'on_site',
      employment_type: position.employment_type || position.contract_type || 'full_time',
      experience_level: (() => {
        if (position.experience_level && ['entry', 'mid', 'senior', 'executive'].includes(position.experience_level)) {
          return position.experience_level as 'entry' | 'mid' | 'senior' | 'executive';
        }
        if (position.position_level === 'junior') return 'entry';
        if (position.position_level === 'lead') return 'senior';
        if (position.position_level && ['entry', 'mid', 'senior', 'executive'].includes(position.position_level)) {
          return position.position_level as 'entry' | 'mid' | 'senior' | 'executive';
        }
        return 'mid';
      })(),
      salary_min: getSalaryMin(),
      salary_max: getSalaryMax(),
      salary_currency: getSalaryCurrency(),
      requirements: Array.isArray(position.requirements) ? position.requirements.join('\n') :
                   (typeof position.requirements === 'object' && position.requirements?.requirements) ?
                   position.requirements.requirements.join('\n') : '',
      benefits: position.benefits?.join('\n') || '',
      skills: position.skills?.join('\n') || '',
      application_deadline: position.application_deadline || '',
      application_url: position.application_url || '',
      application_email: position.application_email || '',
      // New fields
      working_hours: position.working_hours || '',
      travel_required: typeof position.travel_required === 'number' ? position.travel_required : (position.travel_required ? 1 : 0),
      visa_sponsorship: position.visa_sponsorship || false,
      contact_person: position.contact_person || '',
      reports_to: position.reports_to || '',
      number_of_openings: position.number_of_openings?.toString() || '1',
      job_category: position.job_category || 'other',
      languages_required: (() => {
        if (!position.languages_required) return [];

        // If it's already an array of objects with language/level, use it
        if (Array.isArray(position.languages_required)) {
          return position.languages_required.map(item =>
            typeof item === 'object' && item.language && item.level
              ? item
              : { language: '', level: '' }
          );
        }

        // If it's an object like {"english": "fluent", "spanish": "basic"}
        if (typeof position.languages_required === 'object') {
          return Object.entries(position.languages_required).map(([language, level]) => ({
            language,
            level: typeof level === 'string' ? level : ''
          }));
        }

        return [];
      })(),
      desired_roles: (() => {
        if (!position.desired_roles) return [];

        // If it's already an array, use it
        if (Array.isArray(position.desired_roles)) {
          return position.desired_roles.filter(role => typeof role === 'string' && role.length > 0);
        }

        return [];
      })()
    };

    console.log('Converted form data:', {
      languages_required: newFormData.languages_required,
      desired_roles: newFormData.desired_roles
    });

    setFormData(newFormData);
    setShowCreateModal(true);
  };

  const resetForm = () => {
    setFormData({
      company_id: companyIdFilter || '',
      title: '',
      description: '',
      department: '',
      location: '',
      employment_type: 'full_time',
      experience_level: 'mid',
      salary_min: '',
      salary_max: '',
      salary_currency: 'USD',
      requirements: '',
      benefits: '',
      skills: '',
      work_location_type: 'on_site',
      application_deadline: '',
      application_url: '',
      application_email: '',
      // New fields
      working_hours: '',
      travel_required: 0,
      visa_sponsorship: false,
      contact_person: '',
      reports_to: '',
      number_of_openings: '1',
      job_category: 'other',
      languages_required: [],
      desired_roles: []
    });
    setEditingPosition(null);
    setShowCreateModal(false);
  };

  const formatSalary = (position: Position) => {
    // Handle new salary_range format
    if (position.salary_range) {
      const { min_amount, max_amount, currency } = position.salary_range;
      if (min_amount && max_amount) {
        return `${currency} ${min_amount.toLocaleString()} - ${max_amount.toLocaleString()}`;
      }
      if (min_amount) return `${currency} ${min_amount.toLocaleString()}+`;
      if (max_amount) return `Up to ${currency} ${max_amount.toLocaleString()}`;
    }

    // Handle legacy format
    const min = position.salary_min;
    const max = position.salary_max;
    const currency = position.salary_currency || 'USD';

    if (!min && !max) return 'Not specified';
    if (min && max) return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}`;
    if (min) return `${currency} ${min.toLocaleString()}+`;
    if (max) return `Up to ${currency} ${max.toLocaleString()}`;
    return 'Not specified';
  };

  const getActionButtons = (position: Position) => {
    const buttons = [];

    // Activate/Deactivate button
    if (position.is_active) {
      buttons.push(
        <div key="deactivate" className="relative group">
          <button
            onClick={() => handleDeactivatePosition(position.id)}
            className="text-orange-600 hover:text-orange-900 hover:bg-orange-50 p-1 rounded cursor-pointer"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
            Desactivar posición
          </div>
        </div>
      );
    } else {
      buttons.push(
        <div key="activate" className="relative group">
          <button
            onClick={() => handleActivatePosition(position.id)}
            className="text-green-600 hover:text-green-900 hover:bg-green-50 p-1 rounded cursor-pointer"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
            Activar posición
          </div>
        </div>
      );
    }

    // Edit button
    buttons.push(
      <div key="edit" className="relative group">
        <button
          onClick={() => handleEditPosition(position)}
          className="text-blue-600 hover:text-blue-900 hover:bg-blue-50 p-1 rounded cursor-pointer"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          Editar posición
        </div>
      </div>
    );

    // Delete button
    buttons.push(
      <div key="delete" className="relative group">
        <button
          onClick={() => handleDeletePosition(position.id)}
          className="text-red-600 hover:text-red-900 hover:bg-red-50 p-1 rounded cursor-pointer"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
          Eliminar posición
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
          <h1 className="text-2xl font-bold text-gray-900">Open Positions Management</h1>
          <p className="text-gray-600">
            {companyIdFilter
              ? `Manage job positions for company ${companyIdFilter}`
              : 'Manage all job positions across companies'}
          </p>
        </div>
        <div className="flex gap-2">
          {companyIdFilter && (
            <button
              onClick={clearCompanyFilter}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Clear Filter
            </button>
          )}
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Position
          </button>
        </div>
      </div>

      {/* Company Filter Alert */}
      {companyIdFilter && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-blue-800">
              Filtered by Company ID: <strong>{companyIdFilter}</strong>
            </span>
          </div>
        </div>
      )}

      {/* Stats Cards */}
      {stats && !companyIdFilter && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <StatsCard title="Total Positions" value={stats.total_positions} icon="💼" />
          <StatsCard title="Active Positions" value={stats.active_positions} icon="✅" color="green" />
          <StatsCard title="Inactive Positions" value={stats.inactive_positions} icon="⏸️" color="yellow" />
          <StatsCard title="Full Time" value={stats.positions_by_type.full_time || 0} icon="⏰" color="blue" />
          <StatsCard title="Remote" value={Object.values(stats.positions_by_company).reduce((a, b) => a + b, 0)} icon="🏠" color="purple" />
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search positions..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Company filter - only show when not filtering by URL parameter */}
          {!companyIdFilter && (
            <div>
              <CompanySelector
                label="Company"
                value={companyFilter}
                onChange={(companyId) => {
                  setCompanyFilter(companyId || '');
                }}
                placeholder="Filter by company..."
                allowClear={true}
              />
            </div>
          )}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Department</label>
            <input
              type="text"
              value={departmentFilter}
              onChange={(e) => setDepartmentFilter(e.target.value)}
              placeholder="Filter by department..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
            <input
              type="text"
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
              placeholder="Filter by location..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Employment Type</label>
            <select
              value={employmentTypeFilter}
              onChange={(e) => setEmploymentTypeFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="full_time">Full Time</option>
              <option value="part_time">Part Time</option>
              <option value="contract">Contract</option>
              <option value="internship">Internship</option>
              <option value="freelance">Freelance</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Experience Level</label>
            <select
              value={experienceLevelFilter}
              onChange={(e) => setExperienceLevelFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Levels</option>
              <option value="entry">Entry</option>
              <option value="mid">Mid</option>
              <option value="senior">Senior</option>
              <option value="executive">Executive</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Remote</label>
            <select
              value={isRemoteFilter === undefined ? '' : isRemoteFilter.toString()}
              onChange={(e) => setIsRemoteFilter(e.target.value === '' ? undefined : e.target.value === 'true')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All</option>
              <option value="true">Remote</option>
              <option value="false">On-site</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              value={isActiveFilter === undefined ? '' : isActiveFilter.toString()}
              onChange={(e) => setIsActiveFilter(e.target.value === '' ? undefined : e.target.value === 'true')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All</option>
              <option value="true">Active</option>
              <option value="false">Inactive</option>
            </select>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-red-800">{error}</span>
            </div>
            <button
              onClick={clearError}
              className="text-red-600 hover:text-red-800"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Loading State */}
      {(loading || enumsLoading) && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">
            {enumsLoading ? 'Loading enum options...' : 'Loading positions...'}
          </span>
        </div>
      )}

      {/* Positions Table */}
      {!loading && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Position
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Company
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type & Level
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Salary
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {positions.map((position) => (
                  <tr key={position.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{position.title}</div>
                        <div className="text-sm text-gray-500">{position.department}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {position.company_name || position.company_id}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{position.location || 'Not specified'}</div>
                      {(position.is_remote || position.work_location_type === 'remote') && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          Remote
                        </span>
                      )}
                      {position.work_location_type === 'hybrid' && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          Hybrid
                        </span>
                      )}
                      {position.work_location_type && position.work_location_type !== 'on_site' && position.work_location_type !== 'remote' && position.work_location_type !== 'hybrid' && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          {position.work_location_type.replace('_', ' ').toUpperCase()}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {position.employment_type ? position.employment_type.replace('_', ' ').toUpperCase() : 'Not specified'}
                      </div>
                      <div className="text-sm text-gray-500">
                        {position.experience_level ? position.experience_level.charAt(0).toUpperCase() + position.experience_level.slice(1) : 'Not specified'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {formatSalary(position)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        position.status === 'open' || (position.is_active === true && !position.status)
                          ? 'bg-green-100 text-green-800'
                          : position.status === 'pending'
                          ? 'bg-yellow-100 text-yellow-800'
                          : position.status === 'approved'
                          ? 'bg-blue-100 text-blue-800'
                          : position.status === 'rejected'
                          ? 'bg-red-100 text-red-800'
                          : position.status === 'paused'
                          ? 'bg-orange-100 text-orange-800'
                          : position.status === 'closed'
                          ? 'bg-gray-100 text-gray-800'
                          : position.is_active === false
                          ? 'bg-gray-100 text-gray-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {position.status
                          ? position.status.charAt(0).toUpperCase() + position.status.slice(1)
                          : position.is_active
                          ? 'Active'
                          : 'Inactive'
                        }
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-1">
                        {getActionButtons(position)}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {pagination.totalPages > 1 && (
            <div className="bg-gray-50 px-6 py-3 flex items-center justify-between border-t border-gray-200">
              <div className="flex-1 flex justify-between sm:hidden">
                <button
                  onClick={() => setFilters({ ...filters, page: Math.max(1, pagination.page - 1) })}
                  disabled={pagination.page <= 1}
                  className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <button
                  onClick={() => setFilters({ ...filters, page: Math.min(pagination.totalPages, pagination.page + 1) })}
                  disabled={pagination.page >= pagination.totalPages}
                  className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
              <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-gray-700">
                    Showing <span className="font-medium">{((pagination.page - 1) * pagination.pageSize) + 1}</span> to{' '}
                    <span className="font-medium">
                      {Math.min(pagination.page * pagination.pageSize, pagination.total)}
                    </span>{' '}
                    of <span className="font-medium">{pagination.total}</span> results
                  </p>
                </div>
                <div>
                  <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                    <button
                      onClick={() => setFilters({ ...filters, page: Math.max(1, pagination.page - 1) })}
                      disabled={pagination.page <= 1}
                      className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Previous
                    </button>
                    <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                      Page {pagination.page} of {pagination.totalPages}
                    </span>
                    <button
                      onClick={() => setFilters({ ...filters, page: Math.min(pagination.totalPages, pagination.page + 1) })}
                      disabled={pagination.page >= pagination.totalPages}
                      className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Next
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Create/Edit Position Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-10 mx-auto p-5 border w-[800px] max-w-4xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  {editingPosition ? 'Edit Position' : 'Create New Position'}
                </h3>
                <button
                  onClick={resetForm}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <form onSubmit={editingPosition ? handleUpdatePosition : handleCreatePosition} className="space-y-6">
                {/* Company and Basic Info */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Company *
                    </label>
                    <CompanySelector
                      value={formData.company_id}
                      onChange={(companyId) => {
                        setFormData({ ...formData, company_id: companyId || '' });
                      }}
                      placeholder="Search and select company..."
                      disabled={!!editingPosition}
                      error={error && !formData.company_id ? 'Company is required' : undefined}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Position Title *
                    </label>
                    <input
                      type="text"
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Senior Software Engineer"
                    />
                  </div>
                </div>

                {/* Department and Location */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Department
                    </label>
                    <input
                      type="text"
                      value={formData.department}
                      onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Engineering"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Location *
                    </label>
                    <input
                      type="text"
                      value={formData.location}
                      onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Madrid, Spain"
                    />
                  </div>
                </div>

                {/* Employment Type and Experience Level */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Employment Type *
                    </label>
                    <select
                      value={formData.employment_type}
                      onChange={(e) => setFormData({ ...formData, employment_type: e.target.value as any })}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="full_time">Full Time</option>
                      <option value="part_time">Part Time</option>
                      <option value="contract">Contract</option>
                      <option value="internship">Internship</option>
                      <option value="freelance">Freelance</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Experience Level *
                    </label>
                    <select
                      value={formData.experience_level}
                      onChange={(e) => setFormData({ ...formData, experience_level: e.target.value as any })}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="entry">Entry Level</option>
                      <option value="mid">Mid Level</option>
                      <option value="senior">Senior Level</option>
                      <option value="executive">Executive</option>
                    </select>
                  </div>
                </div>

                {/* Salary Information */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Salary Min
                    </label>
                    <input
                      type="number"
                      value={formData.salary_min}
                      onChange={(e) => setFormData({ ...formData, salary_min: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="50000"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Salary Max
                    </label>
                    <input
                      type="number"
                      value={formData.salary_max}
                      onChange={(e) => setFormData({ ...formData, salary_max: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="80000"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Currency
                    </label>
                    <select
                      value={formData.salary_currency}
                      onChange={(e) => setFormData({ ...formData, salary_currency: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                      <option value="GBP">GBP</option>
                      <option value="CAD">CAD</option>
                    </select>
                  </div>
                </div>

                {/* Work Location Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Work Location Type *
                  </label>
                  <select
                    value={formData.work_location_type}
                    onChange={(e) => setFormData({ ...formData, work_location_type: e.target.value as any })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    {workLocationTypes.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Job Description */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Job Description *
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    required
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Describe the job role, responsibilities, and expectations..."
                  />
                </div>

                {/* Requirements */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Requirements (one per line)
                  </label>
                  <textarea
                    value={formData.requirements}
                    onChange={(e) => setFormData({ ...formData, requirements: e.target.value })}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder={`Bachelor's degree in Computer Science
3+ years of experience with React
Strong knowledge of TypeScript
Experience with REST APIs`}
                  />
                </div>

                {/* Skills */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Required Skills (one per line)
                  </label>
                  <textarea
                    value={formData.skills}
                    onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder={`JavaScript
React
TypeScript
Node.js`}
                  />
                </div>

                {/* Benefits */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Benefits (one per line)
                  </label>
                  <textarea
                    value={formData.benefits}
                    onChange={(e) => setFormData({ ...formData, benefits: e.target.value })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder={`Health insurance
Remote work options
Professional development budget
Flexible working hours`}
                  />
                </div>

                {/* Application Details */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Application Email
                    </label>
                    <input
                      type="email"
                      value={formData.application_email}
                      onChange={(e) => setFormData({ ...formData, application_email: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="jobs@company.com"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Application URL
                    </label>
                    <input
                      type="url"
                      value={formData.application_url}
                      onChange={(e) => setFormData({ ...formData, application_url: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="https://company.com/careers/apply"
                    />
                  </div>
                </div>

                {/* Application Deadline */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Application Deadline
                  </label>
                  <input
                    type="date"
                    value={formData.application_deadline}
                    onChange={(e) => setFormData({ ...formData, application_deadline: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                {/* Additional Details Section */}
                <div className="border-t pt-6">
                  <h4 className="text-lg font-medium text-gray-900 mb-4">Additional Details</h4>

                  {/* Number of Openings and Job Category */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Number of Openings
                      </label>
                      <input
                        type="number"
                        min="1"
                        value={formData.number_of_openings}
                        onChange={(e) => setFormData({ ...formData, number_of_openings: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="1"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Job Category
                      </label>
                      <select
                        value={formData.job_category}
                        onChange={(e) => setFormData({ ...formData, job_category: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="other">Other</option>
                        <option value="technology">Technology</option>
                        <option value="marketing">Marketing</option>
                        <option value="sales">Sales</option>
                        <option value="design">Design</option>
                        <option value="operations">Operations</option>
                        <option value="finance">Finance</option>
                        <option value="hr">Human Resources</option>
                        <option value="customer_service">Customer Service</option>
                      </select>
                    </div>
                  </div>

                  {/* Working Hours and Travel */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Working Hours
                      </label>
                      <input
                        type="text"
                        value={formData.working_hours}
                        onChange={(e) => setFormData({ ...formData, working_hours: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="40h/week, flexible hours"
                      />
                    </div>

                    <div>
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id="travel_required"
                          checked={!!formData.travel_required}
                          onChange={(e) => setFormData({ ...formData, travel_required: e.target.checked ? 1 : 0 })}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <label htmlFor="travel_required" className="ml-2 block text-sm text-gray-700">
                          Travel Required
                        </label>
                      </div>
                    </div>
                  </div>

                  {/* Reports To */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Reports To
                    </label>
                    <input
                      type="text"
                      value={formData.reports_to}
                      onChange={(e) => setFormData({ ...formData, reports_to: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Team Lead, Manager"
                    />
                  </div>

                  {/* Languages and Roles */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Languages Required
                      </label>
                      <div className="space-y-2">
                        {formData.languages_required.map((langReq, index) => (
                          <div key={index} className="flex gap-2 items-center">
                            <select
                              value={langReq.language}
                              onChange={(e) => {
                                const newLanguages = [...formData.languages_required];
                                newLanguages[index] = { ...newLanguages[index], language: e.target.value };
                                setFormData({ ...formData, languages_required: newLanguages });
                              }}
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                              <option value="">Select Language</option>
                              {languages.map(option => (
                                <option key={option.value} value={option.value}>
                                  {option.label}
                                </option>
                              ))}
                            </select>
                            <select
                              value={langReq.level}
                              onChange={(e) => {
                                const newLanguages = [...formData.languages_required];
                                newLanguages[index] = { ...newLanguages[index], level: e.target.value };
                                setFormData({ ...formData, languages_required: newLanguages });
                              }}
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                              <option value="">Select Level</option>
                              {languageLevels.map(option => (
                                <option key={option.value} value={option.value}>
                                  {option.label}
                                </option>
                              ))}
                            </select>
                            <button
                              type="button"
                              onClick={() => {
                                const newLanguages = formData.languages_required.filter((_, i) => i !== index);
                                setFormData({ ...formData, languages_required: newLanguages });
                              }}
                              className="px-3 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        ))}
                        <button
                          type="button"
                          onClick={() => {
                            setFormData({
                              ...formData,
                              languages_required: [...formData.languages_required, { language: '', level: '' }]
                            });
                          }}
                          className="w-full px-3 py-2 border-2 border-dashed border-gray-300 rounded-md text-gray-600 hover:border-blue-500 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <svg className="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                          </svg>
                          Add Language Requirement
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Desired Roles
                      </label>
                      <div className="space-y-2">
                        {formData.desired_roles.map((role, index) => (
                          <div key={index} className="flex gap-2 items-center">
                            <select
                              value={role}
                              onChange={(e) => {
                                const newRoles = [...formData.desired_roles];
                                newRoles[index] = e.target.value;
                                setFormData({ ...formData, desired_roles: newRoles });
                              }}
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                              <option value="">Select Role</option>
                              {desiredRoles.map(option => (
                                <option key={option.value} value={option.value}>
                                  {option.label}
                                </option>
                              ))}
                            </select>
                            <button
                              type="button"
                              onClick={() => {
                                const newRoles = formData.desired_roles.filter((_, i) => i !== index);
                                setFormData({ ...formData, desired_roles: newRoles });
                              }}
                              className="px-3 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        ))}
                        <button
                          type="button"
                          onClick={() => {
                            setFormData({
                              ...formData,
                              desired_roles: [...formData.desired_roles, '']
                            });
                          }}
                          className="w-full px-3 py-2 border-2 border-dashed border-gray-300 rounded-md text-gray-600 hover:border-blue-500 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <svg className="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                          </svg>
                          Add Desired Role
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Visa Sponsorship */}
                  <div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="visa_sponsorship"
                        checked={formData.visa_sponsorship}
                        onChange={(e) => setFormData({ ...formData, visa_sponsorship: e.target.checked })}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label htmlFor="visa_sponsorship" className="ml-2 block text-sm text-gray-700">
                        Visa Sponsorship Available
                      </label>
                    </div>
                  </div>
                </div>

                {/* Error Display */}
                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-md p-3">
                    <div className="text-red-800 text-sm">{error}</div>
                  </div>
                )}

                {/* Form Actions */}
                <div className="flex justify-end space-x-3 pt-4 border-t">
                  <button
                    type="button"
                    onClick={resetForm}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Saving...' : (editingPosition ? 'Update Position' : 'Create Position')}
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

export default PositionsManagement;