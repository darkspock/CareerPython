import React, { useState, useEffect, useRef } from 'react';
import { api } from '../../lib/api';

interface Company {
  id: string;
  name: string;
  sector?: string;
  location?: string;
  website?: string;
}

interface CompanySelectorProps {
  value?: string;
  onChange: (companyId: string | null, company?: Company) => void;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  className?: string;
  label?: string;
  error?: string;
  allowClear?: boolean;
}

export const CompanySelector: React.FC<CompanySelectorProps> = ({
  value,
  onChange,
  placeholder = "Search companies...",
  disabled = false,
  required = false,
  className = "",
  label,
  error,
  allowClear = true
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);

  const wrapperRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout>();

  // Fetch company by ID when value changes
  useEffect(() => {
    if (value && (!selectedCompany || selectedCompany.id !== value)) {
      fetchCompanyById(value);
    } else if (!value && selectedCompany) {
      setSelectedCompany(null);
      setSearchTerm('');
    }
  }, [value]);

  // Handle clicks outside component
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        if (selectedCompany) {
          setSearchTerm(selectedCompany.name);
        } else {
          setSearchTerm('');
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [selectedCompany]);

  const fetchCompanyById = async (companyId: string) => {
    try {
      setLoading(true);
      setSearchError(null);

      // Try searching in the list first (more likely to work)
      const response = await api.authenticatedRequest(`/admin/companies?page_size=100`);
      const foundCompany = response.companies?.find((c: Company) => c.id === companyId);
      if (foundCompany) {
        setSelectedCompany(foundCompany);
        setSearchTerm(foundCompany.name);
      } else {
        // Company not found, but don't show error immediately
        setSelectedCompany(null);
        setSearchTerm('');
      }
    } catch (err: any) {
      console.error('Failed to fetch company:', err);
      setSelectedCompany(null);
      setSearchTerm('');
    } finally {
      setLoading(false);
    }
  };

  const searchCompanies = async (term: string) => {
    if (!term.trim()) {
      setCompanies([]);
      return;
    }

    try {
      setLoading(true);
      setSearchError(null);

      const response = await api.authenticatedRequest(
        `/admin/companies?search_term=${encodeURIComponent(term)}&page_size=20`
      );

      setCompanies(response.companies || []);
    } catch (err: any) {
      console.error('Search companies error:', err);
      setSearchError(`Search failed: ${err.message || 'Unknown error'}`);
      setCompanies([]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const term = e.target.value;
    setSearchTerm(term);
    setIsOpen(true);

    // Clear previous timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Debounce search
    timeoutRef.current = setTimeout(() => {
      searchCompanies(term);
    }, 300);
  };

  const handleCompanySelect = (company: Company) => {
    setSelectedCompany(company);
    setSearchTerm(company.name);
    setIsOpen(false);
    onChange(company.id, company);
  };

  const handleClear = () => {
    setSelectedCompany(null);
    setSearchTerm('');
    setCompanies([]);
    setIsOpen(false);
    onChange(null);
    inputRef.current?.focus();
  };

  const handleInputFocus = () => {
    setIsOpen(true);
    if (searchTerm && !selectedCompany) {
      searchCompanies(searchTerm);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setIsOpen(false);
      if (selectedCompany) {
        setSearchTerm(selectedCompany.name);
      }
    }
  };

  return (
    <div className={`relative ${className}`} ref={wrapperRef}>
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}

      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={searchTerm}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          className={`w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed ${
            error ? 'border-red-500' : ''
          }`}
        />

        {/* Loading spinner */}
        {loading && (
          <div className="absolute right-8 top-1/2 transform -translate-y-1/2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          </div>
        )}

        {/* Clear button */}
        {allowClear && (selectedCompany || searchTerm) && !disabled && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}

        {/* Dropdown arrow */}
        <div className="absolute right-2 top-1/2 transform -translate-y-1/2 pointer-events-none">
          <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
          {loading && companies.length === 0 && (
            <div className="px-4 py-2 text-gray-500 text-center">
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                Searching...
              </div>
            </div>
          )}

          {searchError && (
            <div className="px-4 py-2 text-red-500 text-center">
              {searchError}
            </div>
          )}

          {!loading && companies.length === 0 && searchTerm && !searchError && (
            <div className="px-4 py-2 text-gray-500 text-center">
              No companies found for "{searchTerm}"
            </div>
          )}

          {companies.map((company) => (
            <div
              key={company.id}
              onClick={() => handleCompanySelect(company)}
              className="px-4 py-2 hover:bg-blue-50 cursor-pointer border-b border-gray-100 last:border-b-0"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{company.name}</div>
                  <div className="text-sm text-gray-500 flex items-center space-x-2">
                    {company.sector && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                        {company.sector}
                      </span>
                    )}
                    {company.location && <span>📍 {company.location}</span>}
                  </div>
                </div>
                {company.website && (
                  <div className="text-xs text-gray-400">
                    🌐
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Error message */}
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}

      {/* Selected company info */}
      {selectedCompany && !isOpen && !error && (
        <div className="mt-1 text-xs text-gray-500">
          Selected: {selectedCompany.name}
          {selectedCompany.sector && ` • ${selectedCompany.sector}`}
          {selectedCompany.location && ` • ${selectedCompany.location}`}
        </div>
      )}
    </div>
  );
};

export default CompanySelector;