import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Calendar, FileText, Users, X } from 'lucide-react';
import { companyInterviewService, type UpdateInterviewRequest } from '../../services/companyInterviewService';
import type { Interview } from '../../services/companyInterviewService';
import { CompanyUserService } from '../../services/companyUserService';
import { api } from '../../lib/api';
import type { CompanyRole } from '../../types/company';
import type { CompanyUser } from '../../types/companyUser';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import { toast } from 'react-toastify';

export default function EditInterviewPage() {
  const { interviewId } = useParams<{ interviewId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [interview, setInterview] = useState<Interview | null>(null);

  const [formData, setFormData] = useState<UpdateInterviewRequest>({
    title: undefined,
    description: undefined,
    scheduled_at: undefined,
    deadline_date: undefined,
    process_type: undefined,
    required_roles: undefined,
    interviewers: [],
    interviewer_notes: undefined,
    feedback: undefined,
    score: undefined,
  });

  const [roles, setRoles] = useState<CompanyRole[]>([]);
  const [companyUsers, setCompanyUsers] = useState<CompanyUser[]>([]);
  const [selectedInterviewerIds, setSelectedInterviewerIds] = useState<string[]>([]);
  const [selectedRoleIds, setSelectedRoleIds] = useState<string[]>([]);

  const processTypes = [
    { value: 'CANDIDATE_SIGN_UP', label: 'Registro de Candidato' },
    { value: 'CANDIDATE_APPLICATION', label: 'Aplicación de Candidato' },
    { value: 'SCREENING', label: 'Screening' },
    { value: 'INTERVIEW', label: 'Entrevista' },
    { value: 'FEEDBACK', label: 'Feedback' },
  ];

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
    if (interviewId) {
      loadInterview();
      loadRolesAndUsers();
    }
  }, [interviewId]);

  // Effect to match interviewers after both interview and companyUsers are loaded
  useEffect(() => {
    if (interview && companyUsers.length > 0 && interview.interviewers) {
      const matchedIds: string[] = [];
      interview.interviewers.forEach((interviewer) => {
        // Try to find by email first, then by ID
        const user = companyUsers.find(u => u.email === interviewer || u.id === interviewer);
        if (user) {
          matchedIds.push(user.id);
        }
      });
      if (matchedIds.length > 0) {
        setSelectedInterviewerIds(matchedIds);
      }
    }
  }, [interview, companyUsers]);

  const loadRolesAndUsers = async () => {
    const companyId = getCompanyId();
    if (!companyId) return;

    try {
      // Load company roles (only active)
      const rolesData = await api.listCompanyRoles(companyId, true);
      setRoles(rolesData as CompanyRole[]);

      // Load company users (only active)
      const usersData = await CompanyUserService.getCompanyUsers(companyId, { active_only: true });
      setCompanyUsers(usersData);
    } catch (err: any) {
      console.error('Error loading roles/users:', err);
    }
  };

  const loadInterview = async () => {
    if (!interviewId) return;

    try {
      setLoadingData(true);
      setError(null);
      const data = await companyInterviewService.getInterview(interviewId);
      setInterview(data);
      
      // Populate form with existing data
      setFormData({
        title: data.title || undefined,
        description: data.description || undefined,
        scheduled_at: data.scheduled_at ? formatDateForInput(data.scheduled_at) : undefined,
        deadline_date: data.deadline_date ? formatDateForInput(data.deadline_date) : undefined,
        process_type: data.process_type,
        required_roles: data.required_roles || undefined,
        interviewers: data.interviewers || [],
        interviewer_notes: data.interviewer_notes || undefined,
        feedback: data.feedback || undefined,
        score: data.score || undefined,
      });

      // Set selected role IDs
      if (data.required_roles && data.required_roles.length > 0) {
        setSelectedRoleIds(data.required_roles);
      }

      // Set selected interviewer IDs after companyUsers are loaded
      // This will be handled in a separate effect
    } catch (err: any) {
      setError(err.message || 'Error al cargar la entrevista');
      console.error('Error loading interview:', err);
      toast.error(err.message || 'Error al cargar la entrevista');
    } finally {
      setLoadingData(false);
    }
  };

  const formatDateForInput = (dateString: string): string => {
    // Convert ISO date string to datetime-local format (YYYY-MM-DDTHH:mm)
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  };

  const handleToggleRole = (roleId: string) => {
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
      ...formData,
      required_roles: newIds.length > 0 ? newIds : undefined,
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
  };

  const handleToggleInterviewer = (userId: string) => {
    const currentIds = selectedInterviewerIds || [];
    if (currentIds.includes(userId)) {
      const newIds = currentIds.filter(id => id !== userId);
      setSelectedInterviewerIds(newIds);
      setFormData({
        ...formData,
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
        ...formData,
        interviewers: newIds,
      });
    }
  };

  // Filter users based on selected required roles
  const getAvailableUsers = (): CompanyUser[] => {
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
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!interviewId) {
      setError('ID de entrevista no encontrado');
      return;
    }

    try {
      setLoading(true);
      await companyInterviewService.updateInterview(interviewId, formData);
      toast.success('Entrevista actualizada correctamente');
      navigate(`/company/interviews/${interviewId}`);
    } catch (err: any) {
      const errorMessage = err.message || 'Error al actualizar la entrevista';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error('Error updating interview:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Cargando entrevista...</span>
        </div>
      </div>
    );
  }

  if (!interview) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>No se pudo cargar la entrevista</AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate(`/company/interviews/${interviewId}`)}
          className="mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Volver a Detalle de Entrevista
        </Button>
        <h1 className="text-3xl font-bold text-gray-900">Editar Entrevista</h1>
        <p className="text-gray-600 mt-1">Actualiza la información de la entrevista</p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Read-only Information */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Información de Solo Lectura</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-gray-600">
          <div>
            <span className="font-medium">Candidato:</span> {interview.candidate_id}
          </div>
          <div>
            <span className="font-medium">Tipo:</span> {interview.interview_type}
          </div>
          {interview.process_type && (
            <div>
              <span className="font-medium">Tipo de Proceso:</span> {interview.process_type}
            </div>
          )}
          {interview.required_roles && interview.required_roles.length > 0 && (
            <div>
              <span className="font-medium">Roles Requeridos:</span> {interview.required_roles.join(', ')}
            </div>
          )}
          {interview.job_position_id && (
            <div>
              <span className="font-medium">Posición:</span> {interview.job_position_id}
            </div>
          )}
          {interview.interview_template_id && (
            <div>
              <span className="font-medium">Plantilla:</span> {interview.interview_template_id}
            </div>
          )}
        </CardContent>
      </Card>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Interview Details */}
        <Card>
          <CardHeader>
            <CardTitle>Detalles de la Entrevista</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="title">Título (Opcional)</Label>
              <Input
                id="title"
                type="text"
                value={formData.title || ''}
                onChange={(e) => setFormData({ ...formData, title: e.target.value || undefined })}
                placeholder="Título de la entrevista"
              />
            </div>

            <div>
              <Label htmlFor="description">Descripción (Opcional)</Label>
              <Textarea
                id="description"
                value={formData.description || ''}
                onChange={(e) => setFormData({ ...formData, description: e.target.value || undefined })}
                rows={4}
                placeholder="Descripción o notas sobre la entrevista"
              />
            </div>

            <div>
              <Label htmlFor="scheduled_at" className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4" />
                Fecha y Hora Programada (Opcional)
              </Label>
              <Input
                id="scheduled_at"
                type="datetime-local"
                value={formData.scheduled_at || ''}
                onChange={(e) => setFormData({ ...formData, scheduled_at: e.target.value || undefined })}
              />
            </div>

            <div>
              <Label htmlFor="deadline_date" className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4" />
                Fecha Límite (Opcional)
              </Label>
              <Input
                id="deadline_date"
                type="datetime-local"
                value={formData.deadline_date || ''}
                onChange={(e) => setFormData({ ...formData, deadline_date: e.target.value || undefined })}
              />
            </div>

            <div>
              <Label htmlFor="process_type" className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4" />
                Tipo de Proceso (Opcional)
              </Label>
              <Select
                value={formData.process_type || 'none'}
                onValueChange={(value) => setFormData({ ...formData, process_type: value === 'none' ? undefined : value as any })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona un tipo de proceso" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Ninguno</SelectItem>
                  {processTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="required_roles" className="flex items-center gap-2 mb-2">
                <Users className="w-4 h-4" />
                Roles Requeridos (Opcional)
              </Label>
              <div className="border rounded-md p-3 min-h-[100px] max-h-[200px] overflow-y-auto">
                {roles.length === 0 ? (
                  <p className="text-sm text-gray-500">No hay roles disponibles</p>
                ) : (
                  <div className="space-y-2">
                    {roles.map((role) => (
                      <label
                        key={role.id}
                        className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded"
                      >
                        <input
                          type="checkbox"
                          checked={selectedRoleIds.includes(role.id)}
                          onChange={() => handleToggleRole(role.id)}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span className="text-sm">{role.name}</span>
                        {role.description && (
                          <span className="text-xs text-gray-500">- {role.description}</span>
                        )}
                      </label>
                    ))}
                  </div>
                )}
              </div>
              {selectedRoleIds.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {selectedRoleIds.map((roleId) => {
                    const role = roles.find(r => r.id === roleId);
                    return role ? (
                      <div
                        key={roleId}
                        className="flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                      >
                        <span>{role.name}</span>
                        <button
                          type="button"
                          onClick={() => handleToggleRole(roleId)}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </div>
                    ) : null;
                  })}
                </div>
              )}
            </div>

            <div>
              <Label className="flex items-center gap-2 mb-2">
                <Users className="w-4 h-4" />
                Entrevistadores (Opcional)
              </Label>
              {formData.required_roles && formData.required_roles.length > 0 && (
                <p className="text-xs text-gray-500 mb-2">
                  Solo se muestran usuarios que tienen al menos uno de los roles requeridos seleccionados
                </p>
              )}
              <div className="border rounded-md p-3 min-h-[100px] max-h-[200px] overflow-y-auto">
                {companyUsers.length === 0 ? (
                  <p className="text-sm text-gray-500">No hay usuarios disponibles</p>
                ) : getAvailableUsers().length === 0 ? (
                  <div className="text-sm text-gray-500">
                    {formData.required_roles && formData.required_roles.length > 0 ? (
                      <p>No hay usuarios con los roles requeridos seleccionados</p>
                    ) : (
                      <p>No hay usuarios disponibles</p>
                    )}
                  </div>
                ) : (
                  <div className="space-y-2">
                    {getAvailableUsers().map((user) => {
                      const userRoleIds = user.company_roles || [];
                      const requiredRoleIds = formData.required_roles || [];
                      const hasRequiredRole = requiredRoleIds.length === 0 || 
                        requiredRoleIds.some(roleId => userRoleIds.includes(roleId));
                      
                      return (
                        <label
                          key={user.id}
                          className={`flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded ${
                            !hasRequiredRole ? 'opacity-50' : ''
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={selectedInterviewerIds.includes(user.id)}
                            onChange={() => handleToggleInterviewer(user.id)}
                            disabled={!hasRequiredRole}
                            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 disabled:opacity-50"
                          />
                          <span className="text-sm">
                            {user.email || user.id}
                            {user.role && <span className="text-xs text-gray-500 ml-2">({user.role})</span>}
                            {user.company_roles && user.company_roles.length > 0 && (
                              <span className="text-xs text-blue-600 ml-2">
                                [{user.company_roles.map(roleId => {
                                  const role = roles.find(r => r.id === roleId);
                                  return role?.name || roleId;
                                }).join(', ')}]
                              </span>
                            )}
                          </span>
                        </label>
                      );
                    })}
                  </div>
                )}
              </div>
              {selectedInterviewerIds.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {selectedInterviewerIds.map((userId) => {
                    const user = companyUsers.find(u => u.id === userId);
                    return user ? (
                      <div
                        key={userId}
                        className="flex items-center gap-1 px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs"
                      >
                        <span>{user.email || user.id}</span>
                        <button
                          type="button"
                          onClick={() => handleToggleInterviewer(userId)}
                          className="text-green-600 hover:text-green-800"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </div>
                    ) : null;
                  })}
                </div>
              )}
            </div>

            <div>
              <Label htmlFor="interviewer_notes">Notas del Entrevistador (Opcional)</Label>
              <Textarea
                id="interviewer_notes"
                value={formData.interviewer_notes || ''}
                onChange={(e) => setFormData({ ...formData, interviewer_notes: e.target.value || undefined })}
                rows={3}
                placeholder="Notas internas del entrevistador"
              />
            </div>

            <div>
              <Label htmlFor="feedback">Feedback (Opcional)</Label>
              <Textarea
                id="feedback"
                value={formData.feedback || ''}
                onChange={(e) => setFormData({ ...formData, feedback: e.target.value || undefined })}
                rows={4}
                placeholder="Feedback sobre la entrevista"
              />
            </div>

            <div>
              <Label htmlFor="score">Puntuación (Opcional)</Label>
              <Input
                id="score"
                type="number"
                min="0"
                max="100"
                step="0.1"
                value={formData.score || ''}
                onChange={(e) => setFormData({ ...formData, score: e.target.value ? parseFloat(e.target.value) : undefined })}
                placeholder="0-100"
              />
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate(`/company/interviews/${interviewId}`)}
          >
            Cancelar
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? 'Guardando...' : 'Guardar Cambios'}
          </Button>
        </div>
      </form>
    </div>
  );
}

