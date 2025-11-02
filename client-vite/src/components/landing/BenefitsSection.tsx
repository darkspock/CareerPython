/**
 * BenefitsSection Component
 * 
 * Displays the main benefits of the platform in a grid layout.
 * 
 * @component
 */
import React from 'react';
import SectionContainer from './SectionContainer';
import { 
  DollarSign, 
  Settings, 
  Workflow, 
  Sparkles,
  TrendingDown,
  Clock
} from 'lucide-react';

interface Benefit {
  icon: React.ReactNode;
  title: string;
  description: string;
}

const benefits: Benefit[] = [
  {
    icon: <TrendingDown className="w-8 h-8" />,
    title: 'Reduce Costos y Tiempo',
    description: 'Automatiza procesos repetitivos y reduce significativamente el tiempo y costos de contratación.'
  },
  {
    icon: <Settings className="w-8 h-8" />,
    title: 'Completamente Personalizable',
    description: 'Adapta la plataforma a las necesidades específicas de tu empresa con workflows y configuraciones personalizadas.'
  },
  {
    icon: <Workflow className="w-8 h-8" />,
    title: 'Flujo Completo',
    description: 'Gestiona todo el proceso de reclutamiento desde la captación hasta la contratación en una sola plataforma.'
  },
  {
    icon: <Sparkles className="w-8 h-8" />,
    title: 'Asistencia de IA',
    description: 'Utiliza inteligencia artificial para mejorar la selección de candidatos y optimizar tu proceso de contratación.'
  }
];

export default function BenefitsSection() {
  return (
    <SectionContainer backgroundColor="white" id="benefits">
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          ¿Por qué elegirnos?
        </h2>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Todo lo que necesitas para transformar tu proceso de reclutamiento
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {benefits.map((benefit, index) => (
          <div
            key={index}
            className="p-6 rounded-xl bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all duration-200"
          >
            <div className="flex items-center justify-center w-16 h-16 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 text-white mb-4">
              {benefit.icon}
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {benefit.title}
            </h3>
            <p className="text-gray-600">
              {benefit.description}
            </p>
          </div>
        ))}
      </div>
    </SectionContainer>
  );
}

