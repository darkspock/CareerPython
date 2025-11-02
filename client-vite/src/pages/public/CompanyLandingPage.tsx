/**
 * CompanyLandingPage Component
 * 
 * Main landing page for companies to learn about and register for the platform.
 * 
 * @component
 */
import React from 'react';
import HeroSection from '../../components/landing/HeroSection';
import BenefitsSection from '../../components/landing/BenefitsSection';
import PricingSection from '../../components/landing/PricingSection';
import TestimonialsSection from '../../components/landing/TestimonialsSection';
import ContactSection from '../../components/landing/ContactSection';

export default function CompanyLandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation (optional - simple sticky nav) */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              CareerPython
            </div>
            <div className="flex items-center space-x-4">
              <a
                href="#benefits"
                className="text-gray-600 hover:text-gray-900 transition"
              >
                Beneficios
              </a>
              <a
                href="#pricing"
                className="text-gray-600 hover:text-gray-900 transition"
              >
                Precios
              </a>
              <a
                href="#testimonials"
                className="text-gray-600 hover:text-gray-900 transition"
              >
                Testimonios
              </a>
              <a
                href="#contact"
                className="text-gray-600 hover:text-gray-900 transition"
              >
                Contacto
              </a>
              <a
                href="/company/register"
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition"
              >
                Registrarse
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main>
        <HeroSection />
        <BenefitsSection />
        <PricingSection />
        <TestimonialsSection />
        <ContactSection />
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-white font-semibold text-lg mb-4">CareerPython</h3>
              <p className="text-sm">
                Transformando el proceso de reclutamiento con inteligencia artificial.
              </p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Producto</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#benefits" className="hover:text-white transition">Características</a></li>
                <li><a href="#pricing" className="hover:text-white transition">Precios</a></li>
                <li><a href="#" className="hover:text-white transition">API</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Empresa</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition">Sobre Nosotros</a></li>
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                <li><a href="#contact" className="hover:text-white transition">Contacto</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition">Términos</a></li>
                <li><a href="#" className="hover:text-white transition">Privacidad</a></li>
                <li><a href="#" className="hover:text-white transition">Cookies</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
            <p>&copy; {new Date().getFullYear()} CareerPython. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

