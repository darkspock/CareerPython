import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Shield, Lock, Mail, ArrowRight, Settings } from "lucide-react";
import { useTranslation } from "react-i18next";
import { api } from "../lib/api";

export default function AdminLoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { t } = useTranslation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const response = await api.login({
        username: email,
        password: password,
      }) as { access_token: string };

      localStorage.setItem("access_token", response.access_token);

      // Verify admin access
      try {
        await api.authenticatedRequest('/admin/health');
        // If admin health check succeeds, redirect to admin panel
        navigate("/admin/dashboard");
      } catch (adminError) {
        // If admin check fails, show error
        setError(t('adminLogin.errors.noPermissions'));
        localStorage.removeItem("access_token");
      }
    } catch (error: any) {
      console.error("Login error:", error);
      setError(error.message || t('adminLogin.errors.invalidCredentials'));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto w-16 h-16 bg-red-600 rounded-full flex items-center justify-center mb-4">
            <Shield className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">
            {t('adminLogin.title')}
          </h2>
          <p className="text-gray-300">
            {t('adminLogin.subtitle')}
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-4 w-4 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-red-800">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                {t('adminLogin.form.adminEmail')}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
                  placeholder={t('adminLogin.form.emailPlaceholder')}
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                {t('adminLogin.form.password')}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
                  placeholder="••••••••"
                />
              </div>
            </div>

            {/* Security Notice */}
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <Shield className="h-4 w-4 text-amber-400 mt-0.5" />
                </div>
                <div className="ml-2">
                  <p className="text-xs text-amber-800">
                    {t('adminLogin.form.securityNotice')}
                  </p>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 px-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  {t('adminLogin.form.verifyingAccess')}
                </>
              ) : (
                <>
                  <Settings className="w-4 h-4" />
                  {t('adminLogin.form.accessPanel')}
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Footer Links */}
          <div className="text-center mt-6 space-y-3">
            <div className="text-xs text-gray-500">
              {t('adminLogin.footer.candidateQuestion')}{" "}
              <Link
                to="/candidate/login"
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                {t('adminLogin.footer.candidateAccess')}
              </Link>
            </div>
          </div>
        </div>

        {/* Admin Features */}
        <div className="text-center">
          <p className="text-sm text-gray-300 mb-4">{t('adminLogin.features.title')}</p>
          <div className="grid grid-cols-2 gap-4 text-xs">
            <div className="flex items-center justify-center gap-2 text-gray-300">
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
              {t('adminLogin.features.userManagement')}
            </div>
            <div className="flex items-center justify-center gap-2 text-gray-300">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              {t('adminLogin.features.candidateManagement')}
            </div>
            <div className="flex items-center justify-center gap-2 text-gray-300">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              {t('adminLogin.features.companyManagement')}
            </div>
            <div className="flex items-center justify-center gap-2 text-gray-300">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              {t('adminLogin.features.interviewTemplates')}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}