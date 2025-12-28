import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { useTranslation } from 'react-i18next';
import { Plus, Search, Edit, Trash2, Power, PowerOff } from 'lucide-react';
import { companyInterviewTemplateService } from '../../services/companyInterviewTemplateService';
import type { InterviewTemplate, TemplateFilters } from '../../services/companyInterviewTemplateService';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Badge } from '@/components/ui/badge';
import { toast } from 'react-toastify';

const CompanyInterviewTemplatesPage: React.FC = () => {
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const { t } = useTranslation();
  const [templates, setTemplates] = useState<InterviewTemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<TemplateFilters>({
    page: 1,
    page_size: 10
  });

  const templateTypes = [
    { value: 'EXTENDED_PROFILE', label: t('company.interviewTemplateEditor.templateTypes.EXTENDED_PROFILE') },
    { value: 'POSITION_INTERVIEW', label: t('company.interviewTemplateEditor.templateTypes.POSITION_INTERVIEW') },
    { value: 'SCREENING', label: t('company.interviewTemplateEditor.templateTypes.SCREENING', { defaultValue: 'Screening' }) },
    { value: 'CUSTOM', label: t('company.interviewTemplateEditor.templateTypes.CUSTOM', { defaultValue: 'Custom' }) }
  ];
  
  // Helper function to get label for template type
  const getTemplateTypeLabel = (type: string) => {
    const templateType = templateTypes.find(t => t.value === type);
    return templateType ? templateType.label : type;
  };

  const statusOptions = [
    { value: 'ENABLED', label: 'Enabled' },
    { value: 'DRAFT', label: 'Draft' },
    { value: 'DISABLED', label: 'Disabled' }
  ];

  useEffect(() => {
    fetchTemplates();
  }, [filters]);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await companyInterviewTemplateService.listTemplates(filters);
      setTemplates(data);
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to fetch interview templates';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTemplate = () => {
    navigate(getPath('interview-templates/create'));
  };

  const handleEditTemplate = (template: InterviewTemplate) => {
    navigate(getPath(`interview-templates/edit/${template.id}`));
  };

  const handleDeleteTemplate = async (templateId: string) => {
    if (!confirm('¿Estás seguro de que quieres eliminar este interview template?')) return;

    try {
      await companyInterviewTemplateService.deleteTemplate(templateId);
      toast.success('Interview template eliminado correctamente');
      fetchTemplates();
    } catch (err: any) {
      toast.error(err.message || 'Error al eliminar el interview template');
    }
  };

  const handleEnableTemplate = async (templateId: string) => {
    try {
      await companyInterviewTemplateService.enableTemplate(templateId);
      toast.success('Interview template habilitado correctamente');
      fetchTemplates();
    } catch (err: any) {
      toast.error(err.message || 'Error al habilitar el interview template');
    }
  };

  const handleDisableTemplate = async (templateId: string) => {
    try {
      await companyInterviewTemplateService.disableTemplate(templateId);
      toast.success('Interview template deshabilitado correctamente');
      fetchTemplates();
    } catch (err: any) {
      toast.error(err.message || 'Error al deshabilitar el interview template');
    }
  };

  return (
    <TooltipProvider>
      <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Interview Templates</h1>
          <p className="text-gray-600 mt-1">Gestiona los interview templates para candidatos</p>
        </div>
        <Button onClick={handleCreateTemplate}>
          <Plus className="w-5 h-5 mr-2" />
          Crear Interview Template
        </Button>
      </div>

      {/* Filters */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Filtros</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                type="text"
                placeholder="Buscar por nombre..."
                value={filters.search_term || ''}
                onChange={(e) => setFilters({ ...filters, search_term: e.target.value || undefined })}
                className="pl-10"
              />
            </div>
            <Select
              value={filters.type || 'all'}
              onValueChange={(value) => setFilters({ ...filters, type: value === 'all' ? undefined : value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Tipo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos los tipos</SelectItem>
                {templateTypes.map((type) => (
                  <SelectItem key={type.value} value={type.value}>
                    {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select
              value={filters.status || 'all'}
              onValueChange={(value) => setFilters({ ...filters, status: value === 'all' ? undefined : value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Estado" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos los estados</SelectItem>
                {statusOptions.map((status) => (
                  <SelectItem key={status.value} value={status.value}>
                    {status.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button
              variant="outline"
              onClick={() => setFilters({ page: 1, page_size: 10 })}
            >
              Limpiar Filtros
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Error Message */}
      {error && (
        <Card className="mb-6 border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-800">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Templates Table */}
      <Card>
        {loading ? (
          <CardContent className="pt-6">
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          </CardContent>
        ) : templates.length === 0 ? (
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <p className="text-gray-600 mb-4">No se encontraron interview templates</p>
              <Button onClick={handleCreateTemplate}>
                <Plus className="w-5 h-5 mr-2" />
                Crear Primer Interview Template
              </Button>
            </div>
          </CardContent>
        ) : (
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nombre</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Estado</TableHead>
                  <TableHead>Categoría</TableHead>
                  <TableHead className="text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {templates.map((template) => (
                  <TableRow key={template.id}>
                    <TableCell>
                      <div>
                        <div className="text-sm font-medium text-gray-900">{template.name}</div>
                        <div className="text-sm text-gray-500">ID: {String(template.id).substring(0, 8)}...</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">
                        {getTemplateTypeLabel(template.type)}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant={
                        template.status === 'ENABLED' ? 'default' :
                        template.status === 'DRAFT' ? 'secondary' : 'destructive'
                      }>
                        {template.status.charAt(0).toUpperCase() + template.status.slice(1).toLowerCase()}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-gray-500">
                      {template.job_category || 'N/A'}
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => handleEditTemplate(template)}
                            >
                              <Edit className="w-4 h-4" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>Editar template</TooltipContent>
                        </Tooltip>
                        {template.status === 'ENABLED' ? (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => handleDisableTemplate(template.id)}
                              >
                                <PowerOff className="w-4 h-4 text-yellow-600" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Deshabilitar template</TooltipContent>
                          </Tooltip>
                        ) : (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => handleEnableTemplate(template.id)}
                              >
                                <Power className="w-4 h-4 text-green-600" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Habilitar template</TooltipContent>
                          </Tooltip>
                        )}
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => handleDeleteTemplate(template.id)}
                              className="text-red-600 hover:text-red-900"
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>Eliminar template</TooltipContent>
                        </Tooltip>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        )}
      </Card>
      </div>
    </TooltipProvider>
  );
};

export default CompanyInterviewTemplatesPage;

