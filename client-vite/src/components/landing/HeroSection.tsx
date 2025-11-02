/**
 * HeroSection Component
 * 
 * Main hero section of the landing page with title, subtitle, and CTA.
 * 
 * @component
 */
import React from 'react';
import CTAButton from './CTAButton';
import SectionContainer from './SectionContainer';
import { ArrowRight, Sparkles } from 'lucide-react';

export default function HeroSection() {
  return (
    <SectionContainer backgroundColor="gradient" fullWidth>
      <div className="text-center">
        <div className="max-w-4xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-blue-100 text-blue-800 text-sm font-medium mb-6">
            <Sparkles className="w-4 h-4 mr-2" />
            Transforma tu proceso de reclutamiento
          </div>

          {/* Main Title */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Recluta con{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Inteligencia
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Reduce costos y tiempo en tu proceso de selección con nuestra plataforma 
            personalizable, flujo completo y asistencia de IA.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <CTAButton
              href="/company/register"
              variant="primary"
              size="large"
            >
              Empezar Gratis
              <ArrowRight className="w-5 h-5 ml-2" />
            </CTAButton>
            <CTAButton
              href="#benefits"
              variant="outline"
              size="large"
            >
              Conocer Más
            </CTAButton>
          </div>

          {/* Trust Indicators */}
          <div className="mt-12 pt-8 border-t border-gray-200">
            <p className="text-sm text-gray-500 mb-4">Confían en nosotros:</p>
            <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
              <div className="text-gray-400 font-semibold">+100 Empresas</div>
              <div className="text-gray-400 font-semibold">+10,000 Candidatos</div>
              <div className="text-gray-400 font-semibold">98% Satisfacción</div>
            </div>
          </div>
        </div>
      </div>
    </SectionContainer>
  );
}

