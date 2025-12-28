import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { ArrowLeft, Calendar, User, Briefcase, FileText, Users, X } from 'lucide-react';
import { companyInterviewService, type CreateInterviewRequest } from '../../services/companyInterviewService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import { toast } from 'react-toastify';
import { useInterviewFormData } from '../../hooks/useInterviewFormData';
import { useInterviewForm } from '../../hooks/useInterviewForm';

export default function CreateInterviewPage() {
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  
  // Load form data
  const {
    candidates,
    positions,
    templates,
    roles,
    companyUsers,
    loading: loadingData,
    error: dataError,
  } = useInterviewFormData();
  
  // Form management
  const {
    formData: formDataRaw,
    selectedInterviewerIds,
    selectedRoleIds,
    loading: formLoading,
    error: formError,
    setFormData,
    handleToggleRole,
    handleToggleInterviewer,
    getAvailableUsers,
    validate,
    clearError,
  } = useInterviewForm({
    roles,
    companyUsers,
  });
  
  // Type assertion for create mode
  const formData = formDataRaw as CreateInterviewRequest;
  const loading = formLoading;
  const error = formError || dataError;

  const interviewTypes = [
    { value: 'CUSTOM', label: 'Personalizada' },
    { value: 'TECHNICAL', label: 'Técnica' },
    { value: 'BEHAVIORAL', label: 'Conductual' },
    { value: 'CULTURAL_FIT', label: 'Ajuste Cultural' },
    { value: 'KNOWLEDGE_CHECK', label: 'Verificación de Conocimientos' },
    { value: 'EXPERIENCE_CHECK', label: 'Verificación de Experiencia' },
  ];

  const processTypes = [
    { value: 'CANDIDATE_SIGN_UP', label: 'Registro de Candidato' },
    { value: 'CANDIDATE_APPLICATION', label: 'Aplicación de Candidato' },
    { value: 'SCREENING', label: 'Screening' },
    { value: 'INTERVIEW', label: 'Entrevista' },
    { value: 'FEEDBACK', label: 'Feedback' },
  ];

  const interviewModes = [
    { value: 'AUTOMATIC', label: 'Automático' },
    { value: 'AI', label: 'IA' },
    { value: 'MANUAL', label: 'Manual' },
  ];

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    if (!validate()) {
      return;
    }

    try {
      const createData = formData as CreateInterviewRequest;
      const response = await companyInterviewService.createInterview(createData);
      toast.success('Entrevista creada correctamente');
      const interviewId = response.interview_id || (response as any).interview?.id;
      if (interviewId) {
        navigate(getPath(`interviews/${interviewId}`));
      } else {
        navigate(getPath('interviews'));
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Error al crear la entrevista';
      toast.error(errorMessage);
      console.error('Error creating interview:', err);
    }
  }, [formData, validate, clearError, navigate]);

  if (loadingData) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Cargando datos...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate(getPath('interviews'))}
          className="mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Volver a Entrevistas
        </Button>
        <h1 className="text-3xl font-bold text-gray-900">Crear Nueva Entrevista</h1>
        <p className="text-gray-600 mt-1">Programa una nueva entrevista para un candidato</p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle>Información Básica</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="candidate_id" className="flex items-center gap-2 mb-2">
                <User className="w-4 h-4" />
                Candidato *
              </Label>
              <Select
                value={formData.candidate_id}
                onValueChange={(value) => setFormData({ ...formData, candidate_id: value })}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona un candidato" />
                </SelectTrigger>
                <SelectContent>
                  {candidates.map((candidate) => (
                    <SelectItem key={candidate.candidate_id} value={candidate.candidate_id}>
                      {candidate.candidate_name} ({candidate.candidate_email})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="required_roles" className="flex items-center gap-2 mb-2">
                <Users className="w-4 h-4" />
                Roles Requeridos *
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
              <Label htmlFor="interview_type" className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4" />
                Tipo de Entrevista *
              </Label>
              <Select
                value={formData.interview_type}
                onValueChange={(value) => setFormData({ ...formData, interview_type: value as any })}
                required
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {interviewTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
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
              <Label htmlFor="interview_mode" className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4" />
                Modo de Entrevista *
              </Label>
              <Select
                value={formData.interview_mode}
                onValueChange={(value) => setFormData({ ...formData, interview_mode: value as 'AUTOMATIC' | 'AI' | 'MANUAL' })}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona un modo" />
                </SelectTrigger>
                <SelectContent>
                  {interviewModes.map((mode) => (
                    <SelectItem key={mode.value} value={mode.value}>
                      {mode.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="job_position_id" className="flex items-center gap-2 mb-2">
                <Briefcase className="w-4 h-4" />
                Posición de Trabajo (Opcional)
              </Label>
              <Select
                value={formData.job_position_id || 'none'}
                onValueChange={(value) => setFormData({ ...formData, job_position_id: value === 'none' ? undefined : value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona una posición" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Ninguna</SelectItem>
                  {positions.map((position) => (
                    <SelectItem key={position.id} value={position.id}>
                      {position.title}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="interview_template_id" className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4" />
                Plantilla de Entrevista (Opcional)
              </Label>
              <Select
                value={formData.interview_template_id || 'none'}
                onValueChange={(value) => setFormData({ ...formData, interview_template_id: value === 'none' ? undefined : value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona una plantilla" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Ninguna</SelectItem>
                  {templates.map((template) => (
                    <SelectItem key={template.id} value={template.id}>
                      {template.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

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
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate(getPath('interviews'))}
          >
            Cancelar
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? 'Creando...' : 'Crear Entrevista'}
          </Button>
        </div>
      </form>
    </div>
  );
}

