import { useState } from 'react';
import { Shield, FileUp, Link2, Github, Twitter, Linkedin, AlertTriangle, Sun, Moon } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface ThreatResult {
  riskLevel: 'high' | 'medium' | 'low';
  confidenceScore: number;
  primaryCategory: string;
  provokingFiles: number;
  detections: {
    category: string;
    confidence: number;
    color: string;
  }[];
}

export function ThreatDetectionDashboard() {
  const [activeTab, setActiveTab] = useState<'url' | 'file'>('url');
  const [activeNav, setActiveNav] = useState<'submit' | 'malware' | 'ransomware'>('submit');
  const [inputValue, setInputValue] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<ThreatResult | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(true);

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    
    setTimeout(() => {
      const mockResult: ThreatResult = {
        riskLevel: 'high',
        confidenceScore: 94,
        primaryCategory: 'Phishing',
        provokingFiles: 1245,
        detections: [
          { category: 'Phishing', confidence: 94, color: '#EF4444' },
          { category: 'Malware', confidence: 67, color: '#F97316' },
          { category: 'Ransomware', confidence: 45, color: '#EAB308' }
        ]
      };
      setResult(mockResult);
      setIsAnalyzing(false);
    }, 2000);
  };

  return (
    <div className={`min-h-screen ${isDarkMode ? 'bg-[#0F1729] text-white' : 'bg-gray-50 text-gray-900'}`}>
      {/* Header */}
      <header className={`border-b ${isDarkMode ? 'border-gray-800 bg-[#1a2332]' : 'border-gray-200 bg-white'}`}>
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <img src="./src/styles/logo.png" alt="TruthGuard Logo" className="w-8 h-8" />
              <div>
                <h1 className="font-bold text-lg">TruthGuard</h1>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex items-center gap-6">
              <button
                onClick={() => setActiveNav('submit')}
                className={`text-sm transition-colors ${
                  activeNav === 'submit' ? 'text-indigo-400' : `${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`
                }`}
              >
                Submit & Scan
              </button>
              <button
                onClick={() => setActiveNav('malware')}
                className={`text-sm transition-colors ${
                  activeNav === 'malware' ? 'text-indigo-400' : `${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`
                }`}
              >
                Malware
              </button>
              <button
                onClick={() => setActiveNav('ransomware')}
                className={`text-sm transition-colors ${
                  activeNav === 'ransomware' ? 'text-indigo-400' : `${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`
                }`}
              >
                Ransomware
              </button>
            </nav>

            {/* Icons */}
            <div className="flex items-center gap-3">
              <button 
                onClick={() => setIsDarkMode(!isDarkMode)}
                className={`w-8 h-8 flex items-center justify-center ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'} transition-colors`}
              >
                {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <button className="w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-pink-500 flex items-center justify-center text-xs font-bold text-white">
                U
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Title */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-3">Advanced Threat Detection</h2>
          <p className={isDarkMode ? 'text-gray-400' : 'text-gray-600'}>
            Analyze text, URLs, and files instantly using our AI-powered engine.
          </p>
        </div>

        {/* Two Column Layout */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Left Column - Analysis Input */}
          <div className={`${isDarkMode ? 'bg-[#1a2332] border-gray-800' : 'bg-white border-gray-200'} rounded-xl border p-6`}>
            <div className="flex items-center gap-2 mb-6">
              <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
              <h3 className="font-semibold">Analysis Input</h3>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 mb-6">
              <button
                onClick={() => setActiveTab('url')}
                className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-colors ${
                  activeTab === 'url'
                    ? `${isDarkMode ? 'bg-[#0F1729] text-white' : 'bg-indigo-100 text-indigo-700'}`
                    : `${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`
                }`}
              >
                Text/URL
              </button>
              <button
                onClick={() => setActiveTab('file')}
                className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-colors ${
                  activeTab === 'file'
                    ? `${isDarkMode ? 'bg-[#0F1729] text-white' : 'bg-indigo-100 text-indigo-700'}`
                    : `${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`
                }`}
              >
                File Upload
              </button>
            </div>

            {/* Input Area */}
            {activeTab === 'url' ? (
              <div className="space-y-4">
                <div>
                  <label className={`block text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'} mb-2`}>
                    Enter content to analyze
                  </label>
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Paste suspicious text or URL..."
                    rows={6}
                    className={`w-full ${isDarkMode ? 'bg-[#0F1729] border-gray-700 text-white placeholder-gray-500' : 'bg-white border-gray-300 text-gray-900 placeholder-gray-400'} border rounded-lg px-4 py-3 focus:outline-none focus:border-indigo-500 resize-none`}
                  />
                </div>
              </div>
            ) : (
              <div className={`border-2 border-dashed ${isDarkMode ? 'border-gray-700' : 'border-gray-300'} rounded-lg p-8 text-center`}>
                <FileUp className={`w-12 h-12 ${isDarkMode ? 'text-gray-500' : 'text-gray-400'} mx-auto mb-3`} />
                <p className={isDarkMode ? 'text-gray-400' : 'text-gray-600'}>Drop file here or click to upload</p>
                <p className={`text-sm ${isDarkMode ? 'text-gray-500' : 'text-gray-500'} mb-4`}>Max file size: 50MB</p>
                <button className={`px-4 py-2 ${isDarkMode ? 'bg-[#0F1729] border-gray-700' : 'bg-gray-50 border-gray-300'} border rounded-lg text-sm hover:border-indigo-500 transition-colors`}>
                  Select File
                </button>
              </div>
            )}

            {/* Analyze Button */}
            <button
              onClick={handleAnalyze}
              disabled={!inputValue || isAnalyzing}
              className="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white py-3 rounded-lg font-medium flex items-center justify-center gap-2 transition-colors"
            >
              {isAnalyzing ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Shield className="w-5 h-5" />
                  Analyze Now
                </>
              )}
            </button>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {result ? (
              <>
                {/* Alert Banner */}
                <div className={`${isDarkMode ? 'bg-gradient-to-r from-red-500/10 to-red-500/5 border-red-500/30' : 'bg-red-50 border-red-200'} border rounded-xl p-5`}>
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <h4 className="font-semibold text-red-500 mb-1">High Risk Detected</h4>
                      <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                        This analyzed content shows strong indicators of being a phishing attempt. Exercise extreme caution.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-3 gap-4">
                  {/* Confidence Score */}
                  <div className={`${isDarkMode ? 'bg-[#1a2332] border-gray-800' : 'bg-white border-gray-200'} border rounded-xl p-4`}>
                    <div className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'} mb-2`}>Confidence Score</div>
                    <div className="text-3xl font-bold text-red-500">{result.confidenceScore}%</div>
                    <div className={`text-xs ${isDarkMode ? 'text-gray-500' : 'text-gray-500'} mt-1`}>Very High</div>
                  </div>

                  {/* Primary Category */}
                  <div className={`${isDarkMode ? 'bg-[#1a2332] border-gray-800' : 'bg-white border-gray-200'} border rounded-xl p-4`}>
                    <div className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'} mb-2`}>Primary Category</div>
                    <div className="text-xl font-bold">{result.primaryCategory}</div>
                    <div className={`text-xs ${isDarkMode ? 'text-gray-500' : 'text-gray-500'} mt-1`}>Threat detected</div>
                  </div>

                  {/* Provoking Files */}
                  <div className={`${isDarkMode ? 'bg-[#1a2332] border-gray-800' : 'bg-white border-gray-200'} border rounded-xl p-4`}>
                    <div className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'} mb-2`}>Provoking Files</div>
                    <div className="text-3xl font-bold">{result.provokingFiles.toLocaleString()}</div>
                    <div className={`text-xs ${isDarkMode ? 'text-gray-500' : 'text-gray-500'} mt-1`}>In our database</div>
                  </div>
                </div>

                {/* Additional Info */}
                <div className={`${isDarkMode ? 'bg-[#1a2332] border-gray-800' : 'bg-white border-gray-200'} border rounded-xl p-5`}>
                  <div className="flex gap-4 text-sm mb-4">
                    <button className={`px-4 py-1.5 ${isDarkMode ? 'bg-[#0F1729] border-indigo-500/30' : 'bg-indigo-100 border-indigo-200'} rounded-lg text-indigo-400 border`}>
                      Categories
                    </button>
                    <button className={`px-4 py-1.5 rounded-lg ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'} transition-colors`}>
                      Confusion Matrix
                    </button>
                    <button className={`px-4 py-1.5 rounded-lg ${isDarkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'} transition-colors`}>
                      Extracted Entities
                    </button>
                  </div>

                  {/* Chart */}
                  <div>
                    <h4 className="text-sm font-medium mb-4">Detection Confidence by Category (%)</h4>
                    <ResponsiveContainer width="100%" height={200}>
                      <BarChart data={result.detections}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDarkMode ? '#374151' : '#E5E7EB'} />
                        <XAxis 
                          dataKey="category" 
                          stroke={isDarkMode ? '#9CA3AF' : '#6B7280'}
                          tick={{ fill: isDarkMode ? '#9CA3AF' : '#6B7280', fontSize: 12 }}
                        />
                        <YAxis 
                          stroke={isDarkMode ? '#9CA3AF' : '#6B7280'}
                          tick={{ fill: isDarkMode ? '#9CA3AF' : '#6B7280', fontSize: 12 }}
                          domain={[0, 100]}
                        />
                        <Tooltip 
                          contentStyle={{ 
                            backgroundColor: isDarkMode ? '#1a2332' : '#fff', 
                            border: `1px solid ${isDarkMode ? '#374151' : '#E5E7EB'}`,
                            borderRadius: '8px',
                            color: isDarkMode ? '#fff' : '#000'
                          }}
                          formatter={(value) => [`${value}%`, 'Confidence']}
                        />
                        <Bar dataKey="confidence" radius={[8, 8, 0, 0]}>
                          {result.detections.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </>
            ) : (
              <div className={`${isDarkMode ? 'bg-[#1a2332] border-gray-800' : 'bg-white border-gray-200'} border rounded-xl p-12 text-center`}>
                <Shield className={`w-16 h-16 ${isDarkMode ? 'text-gray-600' : 'text-gray-300'} mx-auto mb-4`} />
                <h3 className={`text-xl font-semibold mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Ready to Analyze</h3>
                <p className={isDarkMode ? 'text-gray-500' : 'text-gray-500'}>
                  Enter content in the analysis input and click "Analyze Now" to detect threats.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className={`border-t ${isDarkMode ? 'border-gray-800' : 'border-gray-200'} mt-16`}>
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img src="./src/styles/logo.png" alt="TruthGuard Logo" className="w-6 h-6" />
              <div>
                <div className="font-semibold text-sm">TruthGuard</div>
                <div className={`text-xs ${isDarkMode ? 'text-gray-500' : 'text-gray-500'}`}>
                  © 2026 TruthGuard. All rights reserved. Built for advanced threat analysis.
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <a href="#" className={`w-9 h-9 rounded-lg border ${isDarkMode ? 'border-gray-800 text-gray-400 hover:text-white hover:border-gray-700' : 'border-gray-200 text-gray-600 hover:text-gray-900 hover:border-gray-300'} flex items-center justify-center transition-colors`}>
                <Github className="w-4 h-4" />
              </a>
              <a href="#" className={`w-9 h-9 rounded-lg border ${isDarkMode ? 'border-gray-800 text-gray-400 hover:text-white hover:border-gray-700' : 'border-gray-200 text-gray-600 hover:text-gray-900 hover:border-gray-300'} flex items-center justify-center transition-colors`}>
                <Twitter className="w-4 h-4" />
              </a>
              <a href="#" className={`w-9 h-9 rounded-lg border ${isDarkMode ? 'border-gray-800 text-gray-400 hover:text-white hover:border-gray-700' : 'border-gray-200 text-gray-600 hover:text-gray-900 hover:border-gray-300'} flex items-center justify-center transition-colors`}>
                <Linkedin className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}