/**
 * CompanyDataForm Component
 * 
 * Form component for collecting company registration data.
 * 
 * @component
 * @param {Object} props - Component props
 * @param {Object} props.formData - Form data object
 * @param {Function} props.onChange - Handler for form field changes
 * @param {Object} props.errors - Validation errors
 * @param {Function} [props.onLogoUpload] - Handler for logo upload
 */
import React, { useRef, useState, useEffect } from 'react';
import { Building, Globe, Phone, MapPin, Upload, X, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { CompanyRegistrationService } from '../../services/companyRegistrationService';

interface CompanyDataFormProps {
  formData: {
    company_name: string;
    domain: string;
    logo_url?: string;
    contact_phone?: string;
    address?: string;
  };
  onChange: (field: string, value: string) => void;
  errors: Record<string, string>;
  onLogoUpload?: (file: File) => Promise<void>;
  onDomainValidation?: (isValid: boolean, error?: string) => void;
}

export default function CompanyDataForm({
  formData,
  onChange,
  errors,
  onLogoUpload,
  onDomainValidation
}: CompanyDataFormProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [logoPreview, setLogoPreview] = React.useState<string | null>(null);
  const [uploadingLogo, setUploadingLogo] = React.useState(false);
  const [domainStatus, setDomainStatus] = useState<'idle' | 'checking' | 'available' | 'taken' | 'invalid'>('idle');
  const [domainError, setDomainError] = useState<string | null>(null);
  const domainCheckTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleLogoSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Por favor, selecciona un archivo de imagen');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('El archivo debe ser menor a 5MB');
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setLogoPreview(reader.result as string);
    };
    reader.readAsDataURL(file);

    // Upload if handler provided
    if (onLogoUpload) {
      setUploadingLogo(true);
      try {
        await onLogoUpload(file);
      } catch (error) {
        console.error('Error uploading logo:', error);
        setLogoPreview(null);
      } finally {
        setUploadingLogo(false);
      }
    } else {
      // If no upload handler, just store as data URL
      onChange('logo_url', reader.result as string);
    }
  };

  const removeLogo = () => {
    setLogoPreview(null);
    onChange('logo_url', '');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Validate domain format
  const validateDomainFormat = (domain: string): boolean => {
    if (!domain.trim()) return false;
    // Basic domain validation regex
    const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}$/;
    return domainRegex.test(domain);
  };

  // Check domain availability
  const checkDomainAvailability = async (domain: string) => {
    if (!domain.trim()) {
      setDomainStatus('idle');
      setDomainError(null);
      if (onDomainValidation) onDomainValidation(true);
      return;
    }

    // First validate format
    if (!validateDomainFormat(domain)) {
      setDomainStatus('invalid');
      setDomainError('El dominio no es válido (ejemplo: miempresa.com)');
      if (onDomainValidation) onDomainValidation(false, 'El dominio no es válido (ejemplo: miempresa.com)');
      return;
    }

    // Format is valid, check availability
    setDomainStatus('checking');
    setDomainError(null);

    try {
      const result = await CompanyRegistrationService.checkDomainAvailable(domain);
      // TODO: Re-enable domain availability check when needed
      // For now, only validate format, not availability
      if (result.available) {
        setDomainStatus('available');
        setDomainError(null);
        if (onDomainValidation) onDomainValidation(true);
      } else {
        // Domain is taken, but we allow it for now
        setDomainStatus('available');
        setDomainError(null);
        if (onDomainValidation) onDomainValidation(true);
      }
    } catch (error: any) {
      console.error('Error checking domain:', error);
      // On error, don't block the user, but show as invalid format
      setDomainStatus('invalid');
      setDomainError('Error al verificar el dominio. Verifica el formato.');
      if (onDomainValidation) onDomainValidation(false, 'Error al verificar el dominio. Verifica el formato.');
    }
  };

  // Handle domain change with debounce
  useEffect(() => {
    // Clear previous timeout
    if (domainCheckTimeoutRef.current) {
      clearTimeout(domainCheckTimeoutRef.current);
    }

    // Reset status when domain is cleared
    if (!formData.domain.trim()) {
      setDomainStatus('idle');
      setDomainError(null);
      if (onDomainValidation) onDomainValidation(true);
      return;
    }

    // Set debounce timeout (500ms)
    domainCheckTimeoutRef.current = setTimeout(() => {
      checkDomainAvailability(formData.domain);
    }, 500);

    // Cleanup
    return () => {
      if (domainCheckTimeoutRef.current) {
        clearTimeout(domainCheckTimeoutRef.current);
      }
    };
  }, [formData.domain]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (domainCheckTimeoutRef.current) {
        clearTimeout(domainCheckTimeoutRef.current);
      }
    };
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <label htmlFor="company_name" className="block text-sm font-medium text-gray-700 mb-2">
          Nombre de la Empresa *
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Building className="h-5 w-5 text-gray-400" />
          </div>
          <input
            id="company_name"
            type="text"
            value={formData.company_name}
            onChange={(e) => onChange('company_name', e.target.value)}
            className={`w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
              errors.company_name
                ? 'border-red-300 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
            }`}
            placeholder="Mi Empresa S.L."
            required
            minLength={3}
          />
        </div>
        {errors.company_name && (
          <p className="mt-1 text-sm text-red-600 flex items-center">
            <AlertCircle className="w-4 h-4 mr-1" />
            {errors.company_name}
          </p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          Mínimo 3 caracteres
        </p>
      </div>

      <div>
        <label htmlFor="domain" className="block text-sm font-medium text-gray-700 mb-2">
          Dominio Corporativo *
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Globe className="h-5 w-5 text-gray-400" />
          </div>
          <input
            id="domain"
            type="text"
            value={formData.domain}
            onChange={(e) => onChange('domain', e.target.value.toLowerCase())}
            onBlur={() => {
              if (formData.domain.trim()) {
                checkDomainAvailability(formData.domain);
              }
            }}
            className={`w-full pl-10 pr-10 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
              errors.domain || domainError
                ? 'border-red-300 focus:ring-red-500'
                : domainStatus === 'available'
                ? 'border-green-300 focus:ring-green-500'
                : 'border-gray-300 focus:ring-blue-500'
            }`}
            placeholder="miempresa.com"
            required
          />
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            {domainStatus === 'checking' && (
              <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
            )}
            {domainStatus === 'available' && (
              <CheckCircle className="h-5 w-5 text-green-500" />
            )}
            {domainStatus === 'taken' && (
              <AlertCircle className="h-5 w-5 text-red-500" />
            )}
            {domainStatus === 'invalid' && formData.domain.trim() && (
              <AlertCircle className="h-5 w-5 text-red-500" />
            )}
          </div>
        </div>
        {(errors.domain || domainError) && (
          <p className="mt-1 text-sm text-red-600 flex items-center">
            <AlertCircle className="w-4 h-4 mr-1" />
            {errors.domain || domainError}
          </p>
        )}
        {domainStatus === 'available' && !errors.domain && !domainError && (
          <p className="mt-1 text-sm text-green-600 flex items-center">
            <CheckCircle className="w-4 h-4 mr-1" />
            Dominio disponible
          </p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          Sin http:// o www.
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Logo de la Empresa (Opcional)
        </label>
        <div className="flex items-center space-x-4">
          {logoPreview || formData.logo_url ? (
            <div className="relative">
              <img
                src={logoPreview || formData.logo_url || ''}
                alt="Logo preview"
                className="w-20 h-20 object-contain border border-gray-300 rounded-lg"
              />
              <button
                type="button"
                onClick={removeLogo}
                className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="w-20 h-20 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
              <Upload className="w-8 h-8 text-gray-400" />
            </div>
          )}
          <div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleLogoSelect}
              className="hidden"
              id="logo-upload"
            />
            <label
              htmlFor="logo-upload"
              className="cursor-pointer inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition"
            >
              {uploadingLogo ? 'Subiendo...' : logoPreview || formData.logo_url ? 'Cambiar Logo' : 'Subir Logo'}
            </label>
            <p className="mt-1 text-xs text-gray-500">
              PNG, JPG o GIF (máx. 5MB)
            </p>
          </div>
        </div>
      </div>

      <div>
        <label htmlFor="contact_phone" className="block text-sm font-medium text-gray-700 mb-2">
          Teléfono de Contacto
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Phone className="h-5 w-5 text-gray-400" />
          </div>
          <input
            id="contact_phone"
            type="tel"
            value={formData.contact_phone || ''}
            onChange={(e) => onChange('contact_phone', e.target.value)}
            className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="+34 600 000 000"
          />
        </div>
      </div>

      <div>
        <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-2">
          Dirección
        </label>
        <div className="relative">
          <div className="absolute top-3 left-3 pointer-events-none">
            <MapPin className="h-5 w-5 text-gray-400" />
          </div>
          <input
            id="address"
            type="text"
            value={formData.address || ''}
            onChange={(e) => onChange('address', e.target.value)}
            className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Calle, Ciudad, País"
          />
        </div>
      </div>
    </div>
  );
}

