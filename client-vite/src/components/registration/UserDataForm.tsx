/**
 * UserDataForm Component
 * 
 * Form component for collecting user registration data (email, password, name).
 * 
 * @component
 * @param {Object} props - Component props
 * @param {Object} props.formData - Form data object
 * @param {Function} props.onChange - Handler for form field changes
 * @param {Object} props.errors - Validation errors
 * @param {boolean} props.checkEmailExists - Whether to check if email exists
 */
import { useState, useEffect } from 'react';
import { Mail, Lock, User, AlertCircle } from 'lucide-react';
import { CompanyRegistrationService } from '../../services/companyRegistrationService';

interface UserDataFormProps {
  formData: {
    email: string;
    password: string;
    confirmPassword: string;
    full_name: string;
  };
  onChange: (field: string, value: string) => void;
  errors: Record<string, string>;
  onEmailCheck?: (exists: boolean) => void;
}

export default function UserDataForm({
  formData,
  onChange,
  errors,
  onEmailCheck
}: UserDataFormProps) {
  const [checkingEmail, setCheckingEmail] = useState(false);

  useEffect(() => {
    const checkEmail = async () => {
      if (!formData.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        return;
      }

      setCheckingEmail(true);
      try {
        const result = await CompanyRegistrationService.checkEmailExists(formData.email);
        if (onEmailCheck) {
          onEmailCheck(result.exists);
        }
      } catch (error) {
        // Silently fail - optional check
      } finally {
        setCheckingEmail(false);
      }
    };

    // Debounce email check
    const timeoutId = setTimeout(checkEmail, 500);
    return () => clearTimeout(timeoutId);
  }, [formData.email, onEmailCheck]);

  return (
    <div className="space-y-6">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
          Email *
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Mail className="h-5 w-5 text-gray-400" />
          </div>
          <input
            id="email"
            type="email"
            value={formData.email}
            onChange={(e) => onChange('email', e.target.value)}
            className={`w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
              errors.email
                ? 'border-red-300 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
            }`}
            placeholder="tu@email.com"
            required
          />
          {checkingEmail && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
          )}
        </div>
        {errors.email && (
          <p className="mt-1 text-sm text-red-600 flex items-center">
            <AlertCircle className="w-4 h-4 mr-1" />
            {errors.email}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-2">
          Nombre Completo *
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <User className="h-5 w-5 text-gray-400" />
          </div>
          <input
            id="full_name"
            type="text"
            value={formData.full_name}
            onChange={(e) => onChange('full_name', e.target.value)}
            className={`w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
              errors.full_name
                ? 'border-red-300 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
            }`}
            placeholder="Juan Pérez"
            required
          />
        </div>
        {errors.full_name && (
          <p className="mt-1 text-sm text-red-600 flex items-center">
            <AlertCircle className="w-4 h-4 mr-1" />
            {errors.full_name}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
          Contraseña *
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Lock className="h-5 w-5 text-gray-400" />
          </div>
          <input
            id="password"
            type="password"
            value={formData.password}
            onChange={(e) => onChange('password', e.target.value)}
            className={`w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
              errors.password
                ? 'border-red-300 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
            }`}
            placeholder="Mínimo 8 caracteres"
            required
            minLength={8}
          />
        </div>
        {errors.password && (
          <p className="mt-1 text-sm text-red-600 flex items-center">
            <AlertCircle className="w-4 h-4 mr-1" />
            {errors.password}
          </p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          Mínimo 8 caracteres
        </p>
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
          Confirmar Contraseña *
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Lock className="h-5 w-5 text-gray-400" />
          </div>
          <input
            id="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={(e) => onChange('confirmPassword', e.target.value)}
            className={`w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
              errors.confirmPassword
                ? 'border-red-300 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
            }`}
            placeholder="Repite tu contraseña"
            required
            minLength={8}
          />
        </div>
        {errors.confirmPassword && (
          <p className="mt-1 text-sm text-red-600 flex items-center">
            <AlertCircle className="w-4 h-4 mr-1" />
            {errors.confirmPassword}
          </p>
        )}
      </div>
    </div>
  );
}

