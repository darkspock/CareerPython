/**
 * RemoveUserConfirmModal Component
 *
 * Confirmation modal for removing a user from a company. Displays warnings
 * and validation messages to prevent destructive actions.
 *
 * Features:
 * - User information display
 * - Warning messages
 * - Validation notes (cannot remove self, cannot remove last admin)
 * - Loading and error states
 *
 * @component
 * @param {Object} props - Component props
 * @param {CompanyUser} props.user - The user to be removed
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onClose - Callback when modal is closed
 * @param {Function} props.onConfirm - Callback when removal is confirmed
 * @param {boolean} props.loading - Whether the removal is in progress
 * @param {string|null} props.error - Error message if removal failed
 */
import { AlertTriangle, Trash2 } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Card, CardContent } from '@/components/ui/card';
import type { CompanyUser } from '../../types/companyUser';

interface RemoveUserConfirmModalProps {
  user: CompanyUser;
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  loading?: boolean;
  error?: string | null;
}

export default function RemoveUserConfirmModal({
  user,
  isOpen,
  onClose,
  onConfirm,
  loading = false,
  error = null
}: RemoveUserConfirmModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
              <Trash2 className="w-5 h-5 text-red-600" />
            </div>
            Eliminar Usuario
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <Alert className="border-yellow-200 bg-yellow-50">
            <AlertTriangle className="w-4 h-4 text-yellow-600" />
            <AlertDescription className="text-yellow-800">
              <strong className="block mb-1">Confirmar Eliminacion</strong>
              Esta accion eliminara el usuario de la empresa. El usuario no podra acceder a los recursos de la empresa.
            </AlertDescription>
          </Alert>

          <Card className="bg-gray-50">
            <CardContent className="pt-4 space-y-2">
              <div>
                <p className="text-sm text-muted-foreground">Usuario a eliminar:</p>
                <p className="font-medium">{user.user_id}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Rol actual:</p>
                <p className="font-medium capitalize">{user.role}</p>
              </div>
            </CardContent>
          </Card>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Alert className="border-blue-200 bg-blue-50">
            <AlertDescription className="text-blue-800 text-xs">
              <strong>Nota:</strong> No se puede eliminar el ultimo administrador de la empresa ni eliminarte a ti mismo.
            </AlertDescription>
          </Alert>
        </div>

        <DialogFooter className="gap-2 sm:gap-0">
          <Button variant="outline" onClick={onClose} disabled={loading}>
            Cancelar
          </Button>
          <Button variant="destructive" onClick={onConfirm} disabled={loading}>
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Eliminando...
              </>
            ) : (
              <>
                <Trash2 className="w-4 h-4" />
                Eliminar Usuario
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
