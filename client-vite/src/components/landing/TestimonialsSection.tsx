/**
 * TestimonialsSection Component
 * 
 * Displays customer testimonials in a carousel or grid layout.
 * 
 * @component
 */
import React from 'react';
import { useTranslation } from 'react-i18next';
import SectionContainer from './SectionContainer';
import { Star, Quote } from 'lucide-react';

export default function TestimonialsSection() {
  const { t } = useTranslation();

  const testimonials = [
    {
      name: t('landing.testimonials.testimonial1.name'),
      role: t('landing.testimonials.testimonial1.role'),
      company: t('landing.testimonials.testimonial1.company'),
      content: t('landing.testimonials.testimonial1.content'),
      rating: 5
    },
    {
      name: t('landing.testimonials.testimonial2.name'),
      role: t('landing.testimonials.testimonial2.role'),
      company: t('landing.testimonials.testimonial2.company'),
      content: t('landing.testimonials.testimonial2.content'),
      rating: 5
    },
    {
      name: t('landing.testimonials.testimonial3.name'),
      role: t('landing.testimonials.testimonial3.role'),
      company: t('landing.testimonials.testimonial3.company'),
      content: t('landing.testimonials.testimonial3.content'),
      rating: 5
    }
  ];

  return (
    <SectionContainer backgroundColor="white" id="testimonials">
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          {t('landing.testimonials.title')}
        </h2>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          {t('landing.testimonials.subtitle')}
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

