/**
 * Create Resume Modal Component
 *
 * Modal dialog for creating new resumes with form validation
 * and AI enhancement options.
 */

import React, { useState, useEffect } from 'react';
import { X, FileText, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { api } from '../../lib/api';

interface CreateResumeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: {
    name: string;
    candidate_id: string;
    include_ai_enhancement: boolean;
  }) => void;
  loading?: boolean;
}

interface FormData {
  name: string;
  include_ai_enhancement: boolean;
}

interface Candidate {
  id: string;
  name: string;
  email: string;
}

const CreateResumeModal: React.FC<CreateResumeModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  loading = false
}) => {
  const [userProfile, setUserProfile] = useState<Candidate | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(false);
  const [_profileError, setProfileError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    reset,
    watch
  } = useForm<FormData>({
    defaultValues: {
      name: '',
      include_ai_enhancement: true
    },
    mode: 'onChange'
  });

  const includeAI = watch('include_ai_enhancement');

  // Load user profile when modal opens
  useEffect(() => {
    if (isOpen) {
      loadUserProfile();
    }
  }, [isOpen]);

  const loadUserProfile = async () => {
    setLoadingProfile(true);
    setProfileError(null);
    try {
      // Get current user's profile
      const profile = await api.getMyProfile() as any;
      if (profile && profile.id) {
        setUserProfile({
          id: profile.id,
          name: profile.name || 'My Profile',
          email: profile.email || ''
        });
      } else {
        throw new Error('No profile found');
      }
    } catch (error) {
      console.error('Error loading user profile:', error);
      setProfileError('Failed to load your profile. Please make sure you have completed your profile setup.');
      setUserProfile(null);
    } finally {
      setLoadingProfile(false);
    }
  };

  const handleFormSubmit = (data: FormData) => {
    if (!userProfile) {
      return;
    }
    onSubmit({
      ...data,
      candidate_id: userProfile.id
    });
  };

  const handleClose = () => {
    reset();
    setUserProfile(null);
    setProfileError(null);
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white rounded-lg shadow-xl w-full max-w-md"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg mr-3">
                  <FileText className="w-5 h-5 text-blue-600" />
                </div>
                <h2 className="text-lg font-semibold text-gray-900">Create New Resume</h2>
              </div>
              <button
                onClick={handleClose}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                disabled={loading}
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit(handleFormSubmit)} className="p-6 space-y-4">
              {/* Resume Name */}
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                  Resume Name *
                </label>
                <input
                  id="name"
                  type="text"
                  {...register('name', {
                    required: 'Resume name is required',
                    minLength: {
                      value: 3,
                      message: 'Resume name must be at least 3 characters'
                    },
                    maxLength: {
                      value: 100,
                      message: 'Resume name must be less than 100 characters'
                    }
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Software Engineer Resume"
                  disabled={loading}
                />
                {errors.name && (
                  <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                )}
              </div>


              {/* AI Enhancement Option */}
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4">
                <div className="flex items-start">
                  <input
                    id="include_ai_enhancement"
                    type="checkbox"
                    {...register('include_ai_enhancement')}
                    className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    disabled={loading}
                  />
                  <div className="ml-3">
                    <label htmlFor="include_ai_enhancement" className="flex items-center text-sm font-medium text-gray-900 cursor-pointer">
                      <Sparkles className="w-4 h-4 mr-1 text-purple-600" />
                      AI Enhancement
                    </label>
                    <p className="text-sm text-gray-600 mt-1">
                      {includeAI
                        ? 'AI will analyze your profile and enhance your resume with optimized content, professional summaries, and key highlights.'
                        : 'Create a basic resume using your profile data without AI enhancements.'
                      }
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={handleClose}
                  className="flex-1 px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!isValid || loading || !userProfile || loadingProfile}
                  className="flex-1 flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Creating...
                    </>
                  ) : (
                    <>
                      <FileText className="w-4 h-4 mr-2" />
                      Create Resume
                    </>
                  )}
                </button>
              </div>
            </form>

            {/* Info Footer */}
            <div className="px-6 pb-6">
              <div className="bg-blue-50 rounded-lg p-3">
                <div className="flex items-start">
                  <div className="p-1 bg-blue-100 rounded-full mr-2">
                    <FileText className="w-3 h-3 text-blue-600" />
                  </div>
                  <div className="text-xs text-blue-800">
                    <p className="font-medium">What happens next?</p>
                    <p className="mt-1">
                      Your resume will be generated using your profile data. You can then customize,
                      preview, and export it in multiple formats.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default CreateResumeModal;