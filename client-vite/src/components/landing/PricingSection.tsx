/**
 * PricingSection Component
 * 
 * Displays pricing plans: Startup (Free) and Enterprise (9.99€ per user).
 * 
 * @component
 */
import React from 'react';
import SectionContainer from './SectionContainer';
import CTAButton from './CTAButton';
import { Check, Zap } from 'lucide-react';

interface PricingPlan {
  name: string;
  price: string;
  priceSubtext?: string;
  description: string;
  features: string[];
  ctaText: string;
  highlight?: boolean;
}

const plans: PricingPlan[] = [
  {
    name: 'Startup',
    price: 'Gratis',
    description: 'Perfecto para startups y equipos pequeños',
    features: [
      'Hasta 5 usuarios',
      'Flujos de trabajo personalizados',
      'Asistencia de IA básica',
      'Gestión de candidatos',
      'Soporte por email'
    ],
    ctaText: 'Empezar Gratis',
    highlight: false
  },
  {
    name: 'Empresa',
    price: '9,99€',
    priceSubtext: 'por usuario/mes',
    description: 'Para empresas que necesitan más',
    features: [
      'Usuarios ilimitados',
      'Todas las funciones de Startup',
      'Asistencia de IA avanzada',
      'Analytics y reportes',
      'Soporte prioritario',
      'Integraciones avanzadas',
      'Personalización completa'
    ],
    ctaText: 'Empezar Ahora',
    highlight: true
  }
];

export default function PricingSection() {
  return (
    <SectionContainer backgroundColor="gray" id="pricing">
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Precios simples y transparentes
        </h2>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Elige el plan que mejor se adapte a tu empresa
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        {plans.map((plan, index) => (
          <div
            key={index}
            className={`relative p-8 rounded-2xl bg-white border-2 transition-all duration-200 ${
              plan.highlight
                ? 'border-blue-500 shadow-xl scale-105'
                : 'border-gray-200 hover:border-gray-300 hover:shadow-lg'
            }`}
          >
            {plan.highlight && (
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                  Más Popular
                </span>
              </div>
            )}

            <div className="text-center mb-6">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 mb-4">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {plan.name}
              </h3>
              <div className="mb-2">
                <span className="text-4xl font-bold text-gray-900">
                  {plan.price}
                </span>
                {plan.priceSubtext && (
                  <span className="text-gray-600 text-lg ml-2">
                    {plan.priceSubtext}
                  </span>
                )}
              </div>
              <p className="text-gray-600">{plan.description}</p>
            </div>

            <ul className="space-y-4 mb-8">
              {plan.features.map((feature, featureIndex) => (
                <li key={featureIndex} className="flex items-start">
                  <Check className="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700">{feature}</span>
                </li>
              ))}
            </ul>

            <CTAButton
              href="/company/register"
              variant={plan.highlight ? 'primary' : 'outline'}
              size="large"
              className="w-full"
            >
              {plan.ctaText}
            </CTAButton>
          </div>
        ))}
      </div>

      <div className="text-center mt-8">
        <p className="text-sm text-gray-500">
          Todos los planes incluyen prueba gratuita. Sin tarjetas de crédito requeridas.
        </p>
      </div>
    </SectionContainer>
  );
}

