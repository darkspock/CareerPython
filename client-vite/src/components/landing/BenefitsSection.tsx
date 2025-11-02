/**
 * BenefitsSection Component
 * 
 * Displays the main benefits of the platform in a grid layout.
 * 
 * @component
 */
import React from 'react';
import { useTranslation } from 'react-i18next';
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
  titleKey: string;
  descriptionKey: string;
}

const benefitIcons = [
  <TrendingDown className="w-8 h-8" />,
  <Settings className="w-8 h-8" />,
  <Workflow className="w-8 h-8" />,
  <Sparkles className="w-8 h-8" />,
];

const benefitKeys = [
  { titleKey: 'landing.benefits.reduceCosts.title', descriptionKey: 'landing.benefits.reduceCosts.description' },
  { titleKey: 'landing.benefits.customizable.title', descriptionKey: 'landing.benefits.customizable.description' },
  { titleKey: 'landing.benefits.completeFlow.title', descriptionKey: 'landing.benefits.completeFlow.description' },
  { titleKey: 'landing.benefits.aiAssistance.title', descriptionKey: 'landing.benefits.aiAssistance.description' },
];

export default function BenefitsSection() {
  const { t } = useTranslation();

  return (
    <SectionContainer backgroundColor="white" id="benefits">
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          {t('landing.benefits.title')}
        </h2>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          {t('landing.benefits.subtitle')}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {benefitKeys.map((benefit, index) => (
          <div
            key={index}
            className="p-6 rounded-xl bg-white border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all duration-200"
          >
            <div className="flex items-center justify-center w-16 h-16 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 text-white mb-4">
              {benefitIcons[index]}
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {t(benefit.titleKey)}
            </h3>
            <p className="text-gray-600">
              {t(benefit.descriptionKey)}
            </p>
          </div>
        ))}
      </div>
    </SectionContainer>
  );
}

