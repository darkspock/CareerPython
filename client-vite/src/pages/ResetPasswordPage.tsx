import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { toast } from 'react-toastify';
import { api } from '../lib/api';

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [tokenValid, setTokenValid] = useState(true);

  useEffect(() => {
    // Validate token on mount
    if (!token) {
      setTokenValid(false);
      toast.error('Token de restablecimiento de contraseña no encontrado');
    }
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!token) {
      toast.error('Token de restablecimiento inválido');
      return;
    }

    // Validate passwords
    if (password.length < 8) {
      toast.error('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    if (password !== confirmPassword) {
      toast.error('Las contraseñas no coinciden');
      return;
    }

    setIsLoading(true);

    try {
      await api.resetPasswordWithToken(token, password);

      toast.success('¡Contraseña establecida correctamente! Ahora puedes iniciar sesión.', {
        position: 'top-center',
        autoClose: 5000,
      });

      // Redirect to login after 2 seconds
      setTimeout(() => {
        navigate('/candidate/auth/login');
      }, 2000);
    } catch (error: any) {
      console.error('Error resetting password:', error);

      let errorMessage = 'Error al establecer la contraseña. Por favor intenta de nuevo.';

      if (error?.message) {
        if (error.message.includes('expired') || error.message.includes('invalid')) {
          errorMessage = 'El enlace de restablecimiento ha expirado o es inválido. Por favor solicita uno nuevo.';
          setTokenValid(false);
        } else {
          errorMessage = error.message;
        }
      }

      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (!tokenValid) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center">
          <div className="text-6xl mb-4">❌</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Enlace Inválido</h1>
          <p className="text-gray-600 mb-6">
            El enlace de restablecimiento ha expirado o es inválido.
          </p>
          <button
            onClick={() => navigate('/candidate/auth/login')}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 px-4 rounded-lg font-medium transition-all"
          >
            Ir al Inicio de Sesión
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
        <div className="text-center mb-8">
          <div className="text-5xl mb-4">🔐</div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Establece tu Contraseña</h1>
          <p className="text-gray-600">Crea una contraseña segura para tu cuenta</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              Nueva Contraseña
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              placeholder="Mínimo 8 caracteres"
              required
              minLength={8}
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
              Confirmar Contraseña
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              placeholder="Repite tu contraseña"
              required
              minLength={8}
            />
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="text-sm text-blue-800">
              <p className="font-semibold mb-2">Requisitos de contraseña:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Mínimo 8 caracteres</li>
                <li>Recomendado: incluir mayúsculas, minúsculas y números</li>
              </ul>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-all ${
              isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-105'
            }`}
          >
            {isLoading ? 'Estableciendo contraseña...' : 'Establecer Contraseña'}
          </button>

          <div className="text-center">
            <button
              type="button"
              onClick={() => navigate('/candidate/auth/login')}
              className="text-blue-600 hover:text-blue-700 text-sm font-medium"
            >
              ← Volver al inicio de sesión
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
