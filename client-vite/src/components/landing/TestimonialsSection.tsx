/**
 * TestimonialsSection Component
 * 
 * Displays customer testimonials in a carousel or grid layout.
 * 
 * @component
 */
import React from 'react';
import SectionContainer from './SectionContainer';
import { Star, Quote } from 'lucide-react';

interface Testimonial {
  name: string;
  role: string;
  company?: string;
  content: string;
  rating: number;
  avatar?: string;
}

const testimonials: Testimonial[] = [
  {
    name: 'María González',
    role: 'Directora de Recursos Humanos',
    company: 'TechStart Solutions',
    content: 'La plataforma ha reducido nuestro tiempo de contratación en un 60%. La asistencia de IA es increíble y nos ayuda a encontrar los mejores candidatos.',
    rating: 5
  },
  {
    name: 'Carlos Martínez',
    role: 'CEO',
    company: 'InnovateCorp',
    content: 'La personalización de workflows nos permite adaptar el proceso exactamente a nuestras necesidades. El ROI ha sido excelente desde el primer mes.',
    rating: 5
  },
  {
    name: 'Ana Rodríguez',
    role: 'Gerente de Talento',
    company: 'Digital Ventures',
    content: 'La integración fue sencilla y el soporte siempre está disponible. Nuestro equipo de reclutamiento está muy satisfecho con las herramientas.',
    rating: 5
  }
];

export default function TestimonialsSection() {
  return (
    <SectionContainer backgroundColor="white" id="testimonials">
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Lo que dicen nuestros clientes
        </h2>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Miles de empresas confían en nosotros para su proceso de reclutamiento
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {testimonials.map((testimonial, index) => (
          <div
            key={index}
            className="p-6 rounded-xl bg-white border border-gray-200 hover:shadow-lg transition-all duration-200"
          >
            <div className="flex items-center mb-4">
              {[...Array(testimonial.rating)].map((_, i) => (
                <Star
                  key={i}
                  className="w-5 h-5 text-yellow-400 fill-current"
                />
              ))}
            </div>

            <div className="mb-4">
              <Quote className="w-8 h-8 text-blue-500 opacity-50 mb-2" />
              <p className="text-gray-700 italic">"{testimonial.content}"</p>
            </div>

            <div className="flex items-center">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-semibold text-lg mr-4">
                {testimonial.name.charAt(0)}
              </div>
              <div>
                <div className="font-semibold text-gray-900">
                  {testimonial.name}
                </div>
                <div className="text-sm text-gray-600">
                  {testimonial.role}
                  {testimonial.company && ` • ${testimonial.company}`}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </SectionContainer>
  );
}

