/**
 * ContactSection Component
 * 
 * Section container for the contact form.
 * 
 * @component
 */
import React from 'react';
import SectionContainer from './SectionContainer';
import ContactForm from './ContactForm';
import { Mail, Phone, MapPin } from 'lucide-react';

export default function ContactSection() {
  return (
    <SectionContainer backgroundColor="gray" id="contact">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            ¿Tienes preguntas?
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Estamos aquí para ayudarte. Contáctanos y te responderemos pronto.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 text-blue-600 mb-4">
              <Mail className="w-8 h-8" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Email</h3>
            <p className="text-gray-600">contacto@careerpython.com</p>
          </div>

          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 text-blue-600 mb-4">
              <Phone className="w-8 h-8" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Teléfono</h3>
            <p className="text-gray-600">+34 900 000 000</p>
          </div>

          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 text-blue-600 mb-4">
              <MapPin className="w-8 h-8" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Ubicación</h3>
            <p className="text-gray-600">España</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-8">
          <ContactForm />
        </div>
      </div>
    </SectionContainer>
  );
}

