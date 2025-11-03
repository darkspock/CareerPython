/**
 * CompanyLandingPage Component
 * 
 * Main landing page for companies to learn about and register for the platform.
 * 
 * @component
 */
// import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import HeroSection from '../../components/landing/HeroSection';
import BenefitsSection from '../../components/landing/BenefitsSection';
import PricingSection from '../../components/landing/PricingSection';
import TestimonialsSection from '../../components/landing/TestimonialsSection';
import ContactSection from '../../components/landing/ContactSection';
import LanguageSelector from '../../components/landing/LanguageSelector';

export default function CompanyLandingPage() {
  const { t } = useTranslation();

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation (optional - simple sticky nav) */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <img 
                src="/logoATS.png" 
                alt="ATSMonkey Logo" 
                className="h-10 w-auto"
              />
              <div className="text-2xl font-bold">
                <span className="text-yellow-600">ats</span>
                <span className="text-[#0073e6]">monkey</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => scrollToSection('benefits')}
                className="text-gray-600 hover:text-gray-900 transition bg-transparent border-none cursor-pointer"
              >
                {t('landing.nav.benefits')}
              </button>
              <button
                onClick={() => scrollToSection('pricing')}
                className="text-gray-600 hover:text-gray-900 transition bg-transparent border-none cursor-pointer"
              >
                {t('landing.nav.pricing')}
              </button>
              <button
                onClick={() => scrollToSection('testimonials')}
                className="text-gray-600 hover:text-gray-900 transition bg-transparent border-none cursor-pointer"
              >
                {t('landing.nav.testimonials')}
              </button>
              <button
                onClick={() => scrollToSection('contact')}
                className="text-gray-600 hover:text-gray-900 transition bg-transparent border-none cursor-pointer"
              >
                {t('landing.nav.contact')}
              </button>
              <LanguageSelector />
              <Link
                to="/company/register"
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition"
              >
                {t('landing.nav.register')}
              </Link>
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
              <h3 className="text-white font-semibold text-lg mb-4">
                <span className="text-yellow-400">ats</span><span className="text-[#0073e6]">monkey</span>
              </h3>
              <p className="text-sm">
                {t('landing.footer.description')}
              </p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">{t('landing.footer.product')}</h4>
              <ul className="space-y-2 text-sm">
                <li><button onClick={() => scrollToSection('benefits')} className="hover:text-white transition text-left">{t('landing.footer.features')}</button></li>
                <li><button onClick={() => scrollToSection('pricing')} className="hover:text-white transition text-left">{t('landing.footer.pricing')}</button></li>
                <li><a href="#" className="hover:text-white transition">{t('landing.footer.api')}</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">{t('landing.footer.company')}</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition">{t('landing.footer.about')}</a></li>
                <li><a href="#" className="hover:text-white transition">{t('landing.footer.blog')}</a></li>
                <li><button onClick={() => scrollToSection('contact')} className="hover:text-white transition text-left">{t('landing.footer.contact')}</button></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">{t('landing.footer.legal')}</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition">{t('landing.footer.terms')}</a></li>
                <li><a href="#" className="hover:text-white transition">{t('landing.footer.privacy')}</a></li>
                <li><a href="#" className="hover:text-white transition">{t('landing.footer.cookies')}</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
            <p>&copy; {new Date().getFullYear()} ATSMonkey. {t('landing.footer.rights')}</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

