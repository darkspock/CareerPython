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
import React, { useRef } from 'react';
import { Building, Globe, Phone, MapPin, Upload, X, AlertCircle } from 'lucide-react';

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
}

export default function CompanyDataForm({
  formData,
  onChange,
  errors,
  onLogoUpload
}: CompanyDataFormProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [logoPreview, setLogoPreview] = React.useState<string | null>(null);
  const [uploadingLogo, setUploadingLogo] = React.useState(false);

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
            className={`w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
              errors.domain
                ? 'border-red-300 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
            }`}
            placeholder="miempresa.com"
            required
          />
        </div>
        {errors.domain && (
          <p className="mt-1 text-sm text-red-600 flex items-center">
            <AlertCircle className="w-4 h-4 mr-1" />
            {errors.domain}
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

