import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Eye, EyeOff } from 'lucide-react';

interface AnalysisResult {
  success: boolean;
  filename: string;
  text_length: number;
  text_preview: string;
  analysis_result: {
    candidate_info: any;
    experiences: any[];
    educations: any[];
    projects: any[];
    skills: string[];
    confidence_score: number;
  };
  raw_ai_response: string;
  error_message?: string;
}

interface AIConfig {
  model: string;
  max_tokens: number;
  timeout: number;
  api_url: string;
  has_api_key: boolean;
  api_key_preview?: string;
}

export default function AITestPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [aiConfig, setAIConfig] = useState<AIConfig | null>(null);
  const [showRawResponse, setShowRawResponse] = useState(false);
  const [showTextPreview, setShowTextPreview] = useState(false);

  const loadAIConfig = async () => {
    try {
      const response = await fetch('http://localhost:8000/test/ai-config');
      const config = await response.json();
      setAIConfig(config);
    } catch (error) {
      console.error('Failed to load AI config:', error);
    }
  };

  React.useEffect(() => {
    loadAIConfig();
  }, []);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setResult(null);
    } else {
      alert('Please select a PDF file');
    }
  };

  const analyzeFile = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/test/analyze-pdf-direct', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Analysis failed:', error);
      setResult({
        success: false,
        filename: selectedFile.name,
        text_length: 0,
        text_preview: '',
        analysis_result: {
          candidate_info: {},
          experiences: [],
          educations: [],
          projects: [],
          skills: [],
          confidence_score: 0,
        },
        raw_ai_response: '',
        error_message: `Network error: ${error}`
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              🤖 AI Resume Analysis Test
            </h1>
            <p className="text-gray-600">
              Test the xAI resume analysis directly without queues. Upload a PDF to see immediate results.
            </p>
          </div>

          {/* AI Configuration */}
          {aiConfig && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-blue-900 mb-2">AI Configuration</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><strong>Model:</strong> {aiConfig.model}</div>
                <div><strong>Max Tokens:</strong> {aiConfig.max_tokens}</div>
                <div><strong>Timeout:</strong> {aiConfig.timeout}s</div>
                <div><strong>API Key:</strong> {aiConfig.has_api_key ? '✅ Configured' : '❌ Missing'}</div>
              </div>
              {aiConfig.api_key_preview && (
                <div className="text-xs text-gray-600 mt-2">
                  Key Preview: {aiConfig.api_key_preview}
                </div>
              )}
            </div>
          )}

          {/* File Upload */}
          <div className="mb-8">
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Select PDF Resume
            </label>

            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-all">
              {selectedFile ? (
                <div className="flex items-center justify-center gap-3 text-green-700">
                  <CheckCircle className="w-8 h-8" />
                  <div>
                    <p className="font-medium">{selectedFile.name}</p>
                    <p className="text-sm text-gray-500">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
              ) : (
                <div>
                  <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600 mb-2">Choose a PDF file to analyze</p>
                </div>
              )}

              <input
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="mt-4 inline-block bg-blue-600 text-white px-6 py-2 rounded-lg cursor-pointer hover:bg-blue-700 transition-colors"
              >
                {selectedFile ? 'Change File' : 'Select PDF'}
              </label>
            </div>
          </div>

          {/* Analyze Button */}
          {selectedFile && (
            <div className="mb-8 text-center">
              <button
                onClick={analyzeFile}
                disabled={isAnalyzing}
                className={`px-8 py-3 rounded-lg font-medium transition-all ${
                  isAnalyzing
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {isAnalyzing ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                    Analyzing with AI...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    Analyze with xAI
                  </div>
                )}
              </button>
            </div>
          )}

          {/* Results */}
          {result && (
            <div className="space-y-6">
              {/* Status */}
              <div className={`rounded-lg p-4 ${
                result.success
                  ? 'bg-green-50 border border-green-200'
                  : 'bg-red-50 border border-red-200'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  {result.success ? (
                    <CheckCircle className="w-5 h-5 text-green-600" />
                  ) : (
                    <AlertCircle className="w-5 h-5 text-red-600" />
                  )}
                  <h3 className={`font-semibold ${
                    result.success ? 'text-green-900' : 'text-red-900'
                  }`}>
                    {result.success ? 'Analysis Successful!' : 'Analysis Failed'}
                  </h3>
                </div>

                <div className="text-sm space-y-1">
                  <p><strong>File:</strong> {result.filename}</p>
                  <p><strong>Text Length:</strong> {result.text_length} characters</p>
                  {result.success && (
                    <p><strong>Confidence:</strong> {(result.analysis_result.confidence_score * 100).toFixed(1)}%</p>
                  )}
                  {result.error_message && (
                    <p className="text-red-700"><strong>Error:</strong> {result.error_message}</p>
                  )}
                </div>
              </div>

              {/* Extracted Text Preview */}
              {result.text_preview && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <button
                    onClick={() => setShowTextPreview(!showTextPreview)}
                    className="flex items-center gap-2 text-gray-700 hover:text-gray-900 mb-2"
                  >
                    {showTextPreview ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    <span className="font-medium">Extracted Text Preview</span>
                  </button>

                  {showTextPreview && (
                    <pre className="text-xs text-gray-600 whitespace-pre-wrap bg-white p-3 rounded border max-h-40 overflow-y-auto">
                      {result.text_preview}
                    </pre>
                  )}
                </div>
              )}

              {/* Analysis Results */}
              {result.success && result.analysis_result && (
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-gray-900">Extracted Information</h3>

                  {/* Candidate Info */}
                  {Object.keys(result.analysis_result.candidate_info).length > 0 && (
                    <div className="bg-blue-50 rounded-lg p-4">
                      <h4 className="font-medium text-blue-900 mb-2">Personal Information</h4>
                      <pre className="text-sm text-blue-800 whitespace-pre-wrap">
                        {JSON.stringify(result.analysis_result.candidate_info, null, 2)}
                      </pre>
                    </div>
                  )}

                  {/* Experience */}
                  {result.analysis_result.experiences.length > 0 && (
                    <div className="bg-green-50 rounded-lg p-4">
                      <h4 className="font-medium text-green-900 mb-2">
                        Experience ({result.analysis_result.experiences.length})
                      </h4>
                      <pre className="text-sm text-green-800 whitespace-pre-wrap">
                        {JSON.stringify(result.analysis_result.experiences, null, 2)}
                      </pre>
                    </div>
                  )}

                  {/* Education */}
                  {result.analysis_result.educations.length > 0 && (
                    <div className="bg-purple-50 rounded-lg p-4">
                      <h4 className="font-medium text-purple-900 mb-2">
                        Education ({result.analysis_result.educations.length})
                      </h4>
                      <pre className="text-sm text-purple-800 whitespace-pre-wrap">
                        {JSON.stringify(result.analysis_result.educations, null, 2)}
                      </pre>
                    </div>
                  )}

                  {/* Skills */}
                  {result.analysis_result.skills.length > 0 && (
                    <div className="bg-orange-50 rounded-lg p-4">
                      <h4 className="font-medium text-orange-900 mb-2">
                        Skills ({result.analysis_result.skills.length})
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {result.analysis_result.skills.map((skill, index) => (
                          <span
                            key={index}
                            className="bg-orange-200 text-orange-800 px-2 py-1 rounded text-sm"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Raw AI Response */}
              {result.raw_ai_response && (
                <div className="bg-gray-100 rounded-lg p-4">
                  <button
                    onClick={() => setShowRawResponse(!showRawResponse)}
                    className="flex items-center gap-2 text-gray-700 hover:text-gray-900 mb-2"
                  >
                    {showRawResponse ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    <span className="font-medium">Raw AI Response</span>
                  </button>

                  {showRawResponse && (
                    <pre className="text-xs text-gray-600 whitespace-pre-wrap bg-white p-3 rounded border max-h-60 overflow-y-auto">
                      {result.raw_ai_response}
                    </pre>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};