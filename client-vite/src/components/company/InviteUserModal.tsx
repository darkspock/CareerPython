/**
 * InviteUserModal Component
 *
 * Modal component for inviting new users to a company. Allows administrators
 * to send invitations with a specific role (admin, recruiter, viewer).
 *
 * Features:
 * - Email validation
 * - Role selection
 * - Success state with invitation link to copy
 * - Error handling with user-friendly messages
 *
 * @component
 * @param {Object} props - Component props
 * @param {string} props.companyId - The company ID to invite the user to
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onClose - Callback when modal is closed
 * @param {Function} [props.onSuccess] - Callback when invitation is sent successfully
 */
import React, { useState, useEffect } from 'react';
import { Mail, UserPlus, Copy, Check, AlertCircle } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import type {
  InviteCompanyUserRequest,
  CompanyUserRole
} from '../../types/companyUser';
import { COMPANY_USER_ROLE_OPTIONS } from '../../types/companyUser';
import { useInviteUser } from '../../hooks/useCompanyUsers';

interface InviteUserModalProps {
  companyId: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export default function InviteUserModal({
  companyId: _companyId,
  isOpen,
  onClose,
  onSuccess
}: InviteUserModalProps) {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState<CompanyUserRole>('recruiter');
  const [copied, setCopied] = useState(false);

  const { inviteUser, loading, error, invitationLink, reset } = useInviteUser();

  useEffect(() => {
    if (!isOpen) {
      setEmail('');
      setRole('recruiter');
      setCopied(false);
      reset();
    }
  }, [isOpen, reset]);

  useEffect(() => {
    if (invitationLink && onSuccess) {
      onSuccess();
    }
  }, [invitationLink, onSuccess]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const request: InviteCompanyUserRequest = {
      email: email.trim().toLowerCase(),
      role
    };

    await inviteUser(request);
  };

  const handleCopyLink = () => {
    if (invitationLink?.invitation_link) {
      navigator.clipboard.writeText(invitationLink.invitation_link);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClose = () => {
    setEmail('');
    setRole('recruiter');
    setCopied(false);
    reset();
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && handleClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <UserPlus className="w-6 h-6 text-blue-600" />
            {invitationLink ? 'Invitacion Enviada' : 'Invitar Usuario'}
          </DialogTitle>
        </DialogHeader>

        <div className="py-4">
          {invitationLink ? (
            // Success State
            <div className="space-y-4">
              <Alert className="border-green-200 bg-green-50">
                <Check className="w-5 h-5 text-green-600" />
                <AlertDescription className="text-green-800">
                  Invitacion enviada exitosamente a <strong>{invitationLink.email}</strong>
                </AlertDescription>
              </Alert>

              <div className="space-y-2">
                <Label>Link de Invitacion</Label>
                <div className="flex items-center gap-2">
                  <Input
                    value={invitationLink.invitation_link}
                    readOnly
                    className="flex-1 bg-gray-50"
                  />
                  <Button
                    onClick={handleCopyLink}
                    variant={copied ? 'secondary' : 'default'}
                    size="icon"
                  >
                    {copied ? (
                      <Check className="w-4 h-4" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground">
                  Comparte este link manualmente si es necesario
                </p>
              </div>

              <div className="text-sm text-muted-foreground">
                <p>
                  <strong>Expira:</strong>{' '}
                  {new Date(invitationLink.expires_at).toLocaleDateString('es-ES', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>

              <DialogFooter>
                <Button onClick={handleClose} className="w-full">
                  Cerrar
                </Button>
              </DialogFooter>
            </div>
          ) : (
            // Form State
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="w-4 h-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {/* Email Field */}
              <div className="space-y-2">
                <Label htmlFor="email">Email del Usuario</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-10"
                    placeholder="usuario@ejemplo.com"
                  />
                </div>
              </div>

              {/* Role Field */}
              <div className="space-y-2">
                <Label htmlFor="role">Rol</Label>
                <Select value={role} onValueChange={(value) => setRole(value as CompanyUserRole)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Seleccionar rol" />
                  </SelectTrigger>
                  <SelectContent>
                    {COMPANY_USER_ROLE_OPTIONS.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">
                  El usuario recibira permisos segun su rol
                </p>
              </div>

              {/* Submit Buttons */}
              <DialogFooter className="gap-2 sm:gap-0">
                <Button type="button" variant="outline" onClick={handleClose}>
                  Cancelar
                </Button>
                <Button type="submit" disabled={loading || !email.trim()}>
                  {loading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Enviando...
                    </>
                  ) : (
                    <>
                      <UserPlus className="w-4 h-4" />
                      Enviar Invitacion
                    </>
                  )}
                </Button>
              </DialogFooter>
            </form>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
