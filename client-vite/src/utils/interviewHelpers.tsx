import type { ReactElement } from 'react';
import { Badge } from '@/components/ui/badge';

/**
 * Format date string to localized format
 * Memoized helper function
 */
export function formatDate(dateString?: string): string {
  if (!dateString) return 'N/A';
  try {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return dateString;
  }
}

/**
 * Format date string to detailed localized format
 */
export function formatDateDetailed(dateString?: string): string {
  if (!dateString) return 'N/A';
  try {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return dateString;
  }
}

/**
 * Get status badge configuration
 */
export function getStatusBadgeConfig(status: string): {
  label: string;
  variant: 'default' | 'secondary' | 'destructive' | 'outline';
} {
  const statusConfig: Record<string, {
    label: string;
    variant: 'default' | 'secondary' | 'destructive' | 'outline'
  }> = {
    SCHEDULED: { label: 'Programada', variant: 'default' },
    IN_PROGRESS: { label: 'En Progreso', variant: 'secondary' },
    COMPLETED: { label: 'Completada', variant: 'default' },
    CANCELLED: { label: 'Cancelada', variant: 'destructive' },
    PENDING: { label: 'Pendiente', variant: 'outline' },
  };

  return statusConfig[status] || { 
    label: status.replace('_', ' '), 
    variant: 'outline' as const 
  };
}

/**
 * Get status badge JSX element
 */
export function getStatusBadge(status: string): ReactElement {
  const config = getStatusBadgeConfig(status);
  return (
    <Badge variant={config.variant}>
      {config.label}
    </Badge>
  );
}

/**
 * Get interview type label (InterviewTypeEnum)
 */
export function getTypeLabel(type: string): string {
  const typeLabels: Record<string, string> = {
    CUSTOM: 'Personalizada',
    TECHNICAL: 'Técnica',
    BEHAVIORAL: 'Conductual',
    CULTURAL_FIT: 'Ajuste Cultural',
    KNOWLEDGE_CHECK: 'Verificación de Conocimientos',
    EXPERIENCE_CHECK: 'Verificación de Experiencia',
  };

  return typeLabels[type] || type.replace('_', ' ');
}

/**
 * Get interview template type label (InterviewTemplateTypeEnum)
 */
export function getTemplateTypeLabel(type: string): string {
  const typeLabels: Record<string, string> = {
    EXTENDED_PROFILE: 'Perfil Extendido',
    POSITION_INTERVIEW: 'Entrevista de Posición',
    SCREENING: 'Screening',
    CUSTOM: 'Personalizada',
  };

  return typeLabels[type] || type.replace('_', ' ');
}

