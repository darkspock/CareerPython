import { useState, useEffect, useCallback } from 'react';
import type { 
  CreateInterviewRequest, 
  UpdateInterviewRequest,
  Interview 
} from '../services/companyInterviewService';
import type { CompanyRole } from '../types/company';
import type { CompanyUser } from '../types/companyUser';
import { toast } from 'react-toastify';

export interface UseInterviewFormOptions {
  initialData?: Interview | null;
  roles: CompanyRole[];
  companyUsers: CompanyUser[];
  onSuccess?: () => void;
}

export interface UseInterviewFormReturn {
  // Form data
  formData: CreateInterviewRequest | UpdateInterviewRequest;
  
  // State
  selectedInterviewerIds: string[];
  selectedRoleIds: string[];
  loading: boolean;
  error: string | null;
  
  // Actions
  setFormData: (data: Partial<CreateInterviewRequest | UpdateInterviewRequest>) => void;
  handleToggleRole: (roleId: string) => void;
  handleToggleInterviewer: (userId: string) => void;
  getAvailableUsers: () => CompanyUser[];
  validate: () => boolean;
  clearError: () => void;
  reset: () => void;
}

export function useInterviewForm(options: UseInterviewFormOptions): UseInterviewFormReturn {
  const { initialData, roles, companyUsers, onSuccess: _onSuccess } = options;
  
  const isEditMode = !!initialData;
  
  // Form state
  const [formData, setFormDataState] = useState<CreateInterviewRequest | UpdateInterviewRequest>(() => {
    if (isEditMode && initialData) {
      return {
        title: initialData.title || undefined,
        description: initialData.description || undefined,
        scheduled_at: initialData.scheduled_at ? formatDateForInput(initialData.scheduled_at) : undefined,
        deadline_date: initialData.deadline_date ? formatDateForInput(initialData.deadline_date) : undefined,
        process_type: initialData.process_type,
        required_roles: initialData.required_roles || undefined,
        interviewers: initialData.interviewers || [],
        interviewer_notes: initialData.interviewer_notes || undefined,
        feedback: initialData.feedback || undefined,
        score: initialData.score || undefined,
      } as UpdateInterviewRequest;
    }
    
    return {
      candidate_id: '',
      required_roles: [],
      interview_type: 'CUSTOM',
      interview_mode: 'MANUAL',
      process_type: undefined,
      job_position_id: undefined,
      interview_template_id: undefined,
      title: '',
      description: '',
      scheduled_at: '',
      deadline_date: undefined,
      interviewers: [],
    } as CreateInterviewRequest;
  });
  
  const [selectedInterviewerIds, setSelectedInterviewerIds] = useState<string[]>(() => {
    if (isEditMode && initialData?.interviewers) {
      // Match interviewers by email or ID
      const matchedIds: string[] = [];
      initialData.interviewers.forEach((interviewer) => {
        const user = companyUsers.find(u => u.email === interviewer || u.id === interviewer);
        if (user) {
          matchedIds.push(user.id);
        }
      });
      return matchedIds;
    }
    return [];
  });
  
  const [selectedRoleIds, setSelectedRoleIds] = useState<string[]>(() => {
    if (isEditMode && initialData?.required_roles) {
      return initialData.required_roles;
    }
    return [];
  });
  
  const [loading, _setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Update selectedInterviewerIds when companyUsers are loaded in edit mode
  useEffect(() => {
    if (isEditMode && initialData && companyUsers.length > 0 && initialData.interviewers) {
      const matchedIds: string[] = [];
      initialData.interviewers.forEach((interviewer) => {
        const user = companyUsers.find(u => u.email === interviewer || u.id === interviewer);
        if (user) {
          matchedIds.push(user.id);
        }
      });
      if (matchedIds.length > 0) {
        setSelectedInterviewerIds(matchedIds);
      }
    }
  }, [isEditMode, initialData, companyUsers]);
  
  // Format date for datetime-local input
  const formatDateForInput = useCallback((dateString: string): string => {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  }, []);
  
  // Set form data
  const setFormData = useCallback((data: Partial<CreateInterviewRequest | UpdateInterviewRequest>) => {
    setFormDataState(prev => ({ ...prev, ...data }));
  }, []);
  
  // Toggle role selection
  const handleToggleRole = useCallback((roleId: string) => {
    const currentIds = selectedRoleIds || [];
    let newIds: string[];
    
    if (currentIds.includes(roleId)) {
      newIds = currentIds.filter(id => id !== roleId);
    } else {
      newIds = [...currentIds, roleId];
    }
    
    setSelectedRoleIds(newIds);
    
    // Remove interviewers that no longer have any of the required roles
    const validInterviewerIds = selectedInterviewerIds.filter(userId => {
      const user = companyUsers.find(u => u.id === userId);
      if (!user) return false;
      
      // If no roles selected, keep all interviewers
      if (newIds.length === 0) return true;
      
      const userRoleIds = user.company_roles || [];
      return newIds.some(roleId => userRoleIds.includes(roleId));
    });
    
    setFormData({
      required_roles: newIds.length > 0 ? newIds : (isEditMode ? undefined : []),
      interviewers: validInterviewerIds,
    });
    setSelectedInterviewerIds(validInterviewerIds);
    
    // Show warning if interviewers were removed
    if (validInterviewerIds.length < selectedInterviewerIds.length) {
      const removedCount = selectedInterviewerIds.length - validInterviewerIds.length;
      toast.warning(
        `${removedCount} entrevistador(es) fueron removidos porque no tienen los roles requeridos`
      );
    }
  }, [selectedRoleIds, selectedInterviewerIds, companyUsers, isEditMode, setFormData]);
  
  // Toggle interviewer selection
  const handleToggleInterviewer = useCallback((userId: string) => {
    const currentIds = selectedInterviewerIds || [];
    if (currentIds.includes(userId)) {
      const newIds = currentIds.filter(id => id !== userId);
      setSelectedInterviewerIds(newIds);
      setFormData({
        interviewers: newIds.length > 0 ? newIds : [],
      });
    } else {
      // Validate that user has at least one of the required roles
      const user = companyUsers.find(u => u.id === userId);
      const requiredRoleIds = formData.required_roles || [];
      
      if (requiredRoleIds.length > 0 && user) {
        const userRoleIds = user.company_roles || [];
        const hasRequiredRole = requiredRoleIds.some(roleId => userRoleIds.includes(roleId));
        
        if (!hasRequiredRole) {
          const requiredRoleNames = requiredRoleIds
            .map(roleId => roles.find(r => r.id === roleId)?.name)
            .filter(Boolean)
            .join(', ');
          
          toast.warning(
            `El usuario ${user.email || user.id} no tiene ninguno de los roles requeridos: ${requiredRoleNames}`
          );
          return;
        }
      }
      
      const newIds = [...currentIds, userId];
      setSelectedInterviewerIds(newIds);
      setFormData({
        interviewers: newIds,
      });
    }
  }, [selectedInterviewerIds, companyUsers, formData.required_roles, roles, setFormData]);
  
  // Get available users based on selected roles
  const getAvailableUsers = useCallback((): CompanyUser[] => {
    const requiredRoleIds = formData.required_roles || [];
    
    // If no roles selected, show all users
    if (requiredRoleIds.length === 0) {
      return companyUsers;
    }
    
    // Filter users that have at least one of the required roles
    return companyUsers.filter(user => {
      const userRoleIds = user.company_roles || [];
      return requiredRoleIds.some(roleId => userRoleIds.includes(roleId));
    });
  }, [formData.required_roles, companyUsers]);
  
  // Validate form
  const validate = useCallback((): boolean => {
    if (!isEditMode) {
      const createData = formData as CreateInterviewRequest;
      if (!createData.candidate_id) {
        setError('El candidato es requerido');
        return false;
      }
      if (!createData.interview_type) {
        setError('El tipo de entrevista es requerido');
        return false;
      }
      if (!createData.interview_mode) {
        setError('El modo de entrevista es requerido');
        return false;
      }
      if (!createData.required_roles || createData.required_roles.length === 0) {
        setError('Debe seleccionar al menos un rol requerido');
        return false;
      }
    }
    return true;
  }, [formData, isEditMode]);
  
  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);
  
  // Reset form
  const reset = useCallback(() => {
    if (isEditMode && initialData) {
      setFormDataState({
        title: initialData.title || undefined,
        description: initialData.description || undefined,
        scheduled_at: initialData.scheduled_at ? formatDateForInput(initialData.scheduled_at) : undefined,
        deadline_date: initialData.deadline_date ? formatDateForInput(initialData.deadline_date) : undefined,
        process_type: initialData.process_type,
        required_roles: initialData.required_roles || undefined,
        interviewers: initialData.interviewers || [],
        interviewer_notes: initialData.interviewer_notes || undefined,
        feedback: initialData.feedback || undefined,
        score: initialData.score || undefined,
      } as UpdateInterviewRequest);
      setSelectedRoleIds(initialData.required_roles || []);
      setSelectedInterviewerIds([]);
    } else {
      setFormDataState({
        candidate_id: '',
        required_roles: [],
        interview_type: 'CUSTOM',
        interview_mode: 'MANUAL',
        process_type: undefined,
        job_position_id: undefined,
        interview_template_id: undefined,
        title: '',
        description: '',
        scheduled_at: '',
        deadline_date: undefined,
        interviewers: [],
      } as CreateInterviewRequest);
      setSelectedRoleIds([]);
      setSelectedInterviewerIds([]);
    }
    setError(null);
  }, [isEditMode, initialData, formatDateForInput]);
  
  return {
    formData,
    selectedInterviewerIds,
    selectedRoleIds,
    loading,
    error,
    setFormData,
    handleToggleRole,
    handleToggleInterviewer,
    getAvailableUsers,
    validate,
    clearError,
    reset,
  };
}

