/**
 * AdditionalOptionsForm Component
 * 
 * Form component for additional registration options (example data, terms acceptance).
 * 
 * @component
 * @param {Object} props - Component props
 * @param {Object} props.formData - Form data object
 * @param {Function} props.onChange - Handler for form field changes
 * @param {Object} props.errors - Validation errors
 */
import { Info, AlertCircle, ExternalLink } from 'lucide-react';

interface AdditionalOptionsFormProps {
  formData: {
    initialize_workflows: boolean;  // NEW
    include_example_data: boolean;
    accept_terms: boolean;
    accept_privacy: boolean;
  };
  onChange: (field: string, value: boolean) => void;
  errors: Record<string, string>;
}

export default function AdditionalOptionsForm({
  formData,
  onChange,
  errors
}: AdditionalOptionsFormProps) {
  return (
    <div className="space-y-6">
      {/* Workflows Option */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <Info className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <label className="flex items-start space-x-3 cursor-pointer group">
              <input
                type="checkbox"
                checked={formData.initialize_workflows}
                onChange={(e) => onChange('initialize_workflows', e.target.checked)}
                className="mt-1 w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500"
              />
              <div>
                <span className="text-gray-900 font-medium group-hover:text-green-600 transition">
                  Inicializar workflows por defecto (Recomendado)
                </span>
                <p className="text-sm text-gray-600 mt-1">
                  Esto creará workflows predefinidos para candidatos y posiciones de trabajo que puedes personalizar después.
                </p>
              </div>
            </label>
          </div>
        </div>
      </div>

      {/* Sample Data Option */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <label className="flex items-start space-x-3 cursor-pointer group">
              <input
                type="checkbox"
                checked={formData.include_example_data}
                onChange={(e) => onChange('include_example_data', e.target.checked)}
                className="mt-1 w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <div>
                <span className="text-gray-900 font-medium group-hover:text-blue-600 transition">
                  Incluir datos de ejemplo (Opcional)
                </span>
                <p className="text-sm text-gray-600 mt-1">
                  Esto incluirá usuarios de ejemplo, candidatos, roles y páginas con contenido para ayudarte a evaluar la plataforma.
                </p>
              </div>
            </label>
          </div>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-6 space-y-4">
        <div>
          <label className="flex items-start space-x-3 cursor-pointer group">
            <input
              type="checkbox"
              checked={formData.accept_terms}
              onChange={(e) => onChange('accept_terms', e.target.checked)}
              className="mt-1 w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              required
            />
            <div>
              <span className={`text-gray-900 font-medium group-hover:text-blue-600 transition ${
                errors.accept_terms ? 'text-red-600' : ''
              }`}>
                Acepto los{' '}
                <a
                  href="/terms"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-700 underline inline-flex items-center"
                >
                  términos y condiciones
                  <ExternalLink className="w-4 h-4 ml-1" />
                </a>
                {' '}*
              </span>
              {errors.accept_terms && (
                <p className="mt-1 text-sm text-red-600 flex items-center">
                  <AlertCircle className="w-4 h-4 mr-1" />
                  {errors.accept_terms}
                </p>
              )}
            </div>
          </label>
        </div>

        <div>
          <label className="flex items-start space-x-3 cursor-pointer group">
            <input
              type="checkbox"
              checked={formData.accept_privacy}
              onChange={(e) => onChange('accept_privacy', e.target.checked)}
              className="mt-1 w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              required
            />
            <div>
              <span className={`text-gray-900 font-medium group-hover:text-blue-600 transition ${
                errors.accept_privacy ? 'text-red-600' : ''
              }`}>
                Acepto la{' '}
                <a
                  href="/privacy"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-700 underline inline-flex items-center"
                >
                  política de privacidad
                  <ExternalLink className="w-4 h-4 ml-1" />
                </a>
                {' '}*
              </span>
              {errors.accept_privacy && (
                <p className="mt-1 text-sm text-red-600 flex items-center">
                  <AlertCircle className="w-4 h-4 mr-1" />
                  {errors.accept_privacy}
                </p>
              )}
            </div>
          </label>
        </div>
      </div>
    </div>
  );
}

