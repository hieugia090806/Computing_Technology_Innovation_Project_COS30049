import { useState } from 'react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Search, AlertTriangle, CheckCircle, Info, XCircle, TrendingUp } from 'lucide-react';

interface AnalysisResult {
  status: 'safe' | 'suspicious' | 'fake';
  score: number;
  factors: {
    name: string;
    status: 'pass' | 'warning' | 'fail';
    description: string;
  }[];
}

export function FakeNewsDetector() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const analyzeWebsite = () => {
    setLoading(true);
    setResult(null);

    // Simulate analysis
    setTimeout(() => {
      // Mock analysis result
      const mockResult: AnalysisResult = {
        status: Math.random() > 0.5 ? 'safe' : 'suspicious',
        score: Math.floor(Math.random() * 40) + 60,
        factors: [
          {
            name: 'Domain Reputation',
            status: Math.random() > 0.3 ? 'pass' : 'warning',
            description: 'Domain age and registration history checked'
          },
          {
            name: 'Content Verification',
            status: Math.random() > 0.4 ? 'pass' : 'fail',
            description: 'Cross-referenced with trusted sources'
          },
          {
            name: 'Author Credibility',
            status: Math.random() > 0.5 ? 'pass' : 'warning',
            description: 'Author credentials and history verified'
          },
          {
            name: 'Fact-Checking',
            status: Math.random() > 0.3 ? 'pass' : 'warning',
            description: 'Claims verified against fact-checking databases'
          },
          {
            name: 'Language Analysis',
            status: Math.random() > 0.6 ? 'pass' : 'warning',
            description: 'Checked for sensational or manipulative language'
          }
        ]
      };
      setResult(mockResult);
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 p-8 text-white">
        <div className="relative z-10 grid md:grid-cols-2 gap-8 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Detect Fake News & Misinformation
            </h2>
            <p className="text-blue-100 text-lg">
              Verify the credibility of newspaper websites and online articles. Our AI-powered system analyzes multiple factors to help you identify unreliable sources.
            </p>
          </div>
          <div className="hidden md:block">
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1749989882242-77402fb6763e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxuZXdzcGFwZXIlMjB2ZXJpZmljYXRpb258ZW58MXx8fHwxNzY4ODc2ODc5fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
              alt="Newspaper verification"
              className="w-full h-48 object-cover rounded-lg"
            />
          </div>
        </div>
      </div>

      {/* Input Section */}
      <div className="bg-white rounded-xl shadow-lg p-6 md:p-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Enter Website URL</h3>
        <div className="flex gap-3">
          <div className="flex-1">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example-news-website.com"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={analyzeWebsite}
            disabled={!url || loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2 font-medium"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                Analyze
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {result && (
        <div className="bg-white rounded-xl shadow-lg p-6 md:p-8 space-y-6">
          {/* Overall Score */}
          <div className="flex items-start gap-4 p-6 rounded-lg bg-gradient-to-r from-gray-50 to-blue-50 border border-blue-100">
            <div className="flex-shrink-0">
              {result.status === 'safe' ? (
                <CheckCircle className="w-12 h-12 text-green-500" />
              ) : result.status === 'suspicious' ? (
                <AlertTriangle className="w-12 h-12 text-yellow-500" />
              ) : (
                <XCircle className="w-12 h-12 text-red-500" />
              )}
            </div>
            <div className="flex-1">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {result.status === 'safe' ? 'Trustworthy Source' : 'Potentially Unreliable'}
              </h3>
              <p className="text-gray-600 mb-3">
                {result.status === 'safe'
                  ? 'This website appears to be a legitimate news source.'
                  : 'This website shows signs of unreliability. Exercise caution.'}
              </p>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-blue-600" />
                  <span className="font-semibold text-gray-900">Credibility Score:</span>
                  <span className={`text-xl font-bold ${
                    result.score >= 80 ? 'text-green-600' : 
                    result.score >= 60 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {result.score}/100
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Factors */}
          <div>
            <h4 className="text-lg font-semibold text-gray-900 mb-4">Analysis Breakdown</h4>
            <div className="space-y-3">
              {result.factors.map((factor, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors"
                >
                  <div className="flex-shrink-0 mt-0.5">
                    {factor.status === 'pass' ? (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    ) : factor.status === 'warning' ? (
                      <AlertTriangle className="w-5 h-5 text-yellow-500" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-500" />
                    )}
                  </div>
                  <div className="flex-1">
                    <h5 className="font-medium text-gray-900">{factor.name}</h5>
                    <p className="text-sm text-gray-600 mt-1">{factor.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Tips */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex gap-3">
              <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <h5 className="font-medium text-blue-900 mb-2">Tips for Identifying Fake News</h5>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• Check multiple sources before believing a story</li>
                  <li>• Look for author credentials and publication date</li>
                  <li>• Verify images and videos using reverse search tools</li>
                  <li>• Be wary of sensational headlines and emotional language</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
