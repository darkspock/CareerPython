import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config/api';

export interface EnumOption {
  value: string;
  label: string;
}

export interface EnumMetadata {
  languages: EnumOption[];
  language_levels: EnumOption[];
  desired_roles: EnumOption[];
  work_location_types: EnumOption[];
  employment_types: EnumOption[];
  contract_types: EnumOption[];
  experience_levels: EnumOption[];
  job_categories: EnumOption[];
}

export const useEnums = () => {
  const [enums, setEnums] = useState<EnumMetadata | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEnums = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/admin/enums/metadata`);
        if (!response.ok) {
          throw new Error(`Failed to fetch enums: ${response.status}`);
        }
        const data = await response.json();
        setEnums(data);
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch enum metadata');
        console.error('Error fetching enums:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchEnums();
  }, []);

  return { enums, loading, error };
};

// Convenience hooks for specific enum types
export const useLanguageEnums = () => {
  const { enums, loading, error } = useEnums();
  return {
    languages: enums?.languages || [],
    languageLevels: enums?.language_levels || [],
    loading,
    error
  };
};

export const usePositionEnums = () => {
  const { enums, loading, error } = useEnums();
  return {
    desiredRoles: enums?.desired_roles || [],
    workLocationTypes: enums?.work_location_types || [],
    employmentTypes: enums?.employment_types || [],
    experienceLevels: enums?.experience_levels || [],
    jobCategories: enums?.job_categories || [],
    loading,
    error
  };
};