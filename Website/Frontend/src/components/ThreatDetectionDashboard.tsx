import { useState } from 'react';
import { Sun, Moon, Upload, Link as LinkIcon, FileText, User } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { analyzeContent } from '../services/api';

type TabType = 'newspaper' | 'malware' | 'spam';
type InputType = 'text' | 'file';
type Theme = 'dark' | 'light';

interface DetectionResult {
  overall: number;
  categories: {
    name: string;
    score: number;
    color: string;
  }[];
  threats: {
    type: string;
    severity: string;
    description: string;
  }[];
  timeline: {
    time: string;
    threats: number;
  }[];
  radarData: {
    category: string;
    value: number;
  }[];
}

export function ThreatDetectionDashboard() {
  const [activeTab, setActiveTab] = useState<TabType>('newspaper');
  const [inputType, setInputType] = useState<InputType>('text');
  const [theme, setTheme] = useState<Theme>('dark');
  const [inputValue, setInputValue] = useState('');
  const [fileName, setFileName] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<DetectionResult | null>(null);

  const isDark = theme === 'dark';

  const handleAnalyze = async() => {
    setIsAnalyzing(true);
    setResult(null)
    try {
      const data = await analyzeContent(inputValue);
      const metrics = data.ui_metrics;
      
      const dashboardResult = {
            overall: metrics.confidence_score,

            categories: [
              {
                name: "Prediction Confidence",
                score: metrics.confidence_score,
                color: metrics.status === "DANGER" ? "#ef4444" : "#16a34a",
              },
              {
                name: "Risk Score",
                score: metrics.risk_score,
                color: "#f97316",
              },
            ],

            threats: [
              {
                type: metrics.prediction,
                severity: metrics.status === "DANGER" ? "High" : "Low",
                description: metrics.recommendation,
              },
            ],

            timeline: [
              { time: "Now", threats: Math.round(metrics.risk_score) },
              { time: "+1h", threats: Math.round(metrics.risk_score * 0.9) },
              { time: "+2h", threats: Math.round(metrics.risk_score * 0.7) },
            ],

            radarData: [
              { category: "Confidence", value: metrics.confidence_score },
              { category: "Risk", value: metrics.risk_score },
              { category: "Safety", value: 100 - metrics.risk_score },
              { category: "Prediction Strength", value: metrics.confidence_score },
              { category: "Reliability", value: metrics.status === "SAFE" ? 90 : 40 },
            ],
          };

          setResult(dashboardResult);
        } catch (err) {
          console.error("Analyze failed:", err);
        } finally {
          setIsAnalyzing(false);
        }
      };

    

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFileName(file.name);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'high':
        return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50';
      case 'low':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/50';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/50';
    }
  };

  const getTabTitle = () => {
    switch (activeTab) {
      case 'newspaper':
        return 'Fake News Detection';
      case 'malware':
        return 'Malware Analysis';
      case 'spam':
        return 'Spam and Ham Detection';
    }
  };

  const getTabDescription = () => {
    switch (activeTab) {
      case 'newspaper':
        return 'Analyze news articles and detect misinformation, fake sources, and propaganda';
      case 'malware':
        return 'Scan files and URLs for malicious software, trojans, and spyware';
      case 'spam':
        return 'Detect spam emails, phishing attempts, and distinguish from legitimate messages';
    }
  };

  return (
    <div className={`min-h-screen ${isDark ? 'bg-[#0F1729]' : 'bg-gray-50'} transition-colors duration-300`}>
      {/* Header */}
      <header className={`${isDark ? 'bg-[#1a2332] border-gray-800' : 'bg-white border-gray-200'} border-b transition-colors duration-300`}>
        <div className="max-w-[1600px] mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
           {/* Logo */}
            <div className="flex items-center gap-3">
              <img
                src="/Logo.jpg"
                alt="Team Logo"
                className="w-8 h-8 object-contain"
              />

              <div className="flex flex-col leading-tight">
                <h1
                  className={`text-lg font-bold ${
                    isDark ? "text-white" : "text-gray-900"
                  }`}
                >
                  TruthGuard
                </h1>

                <span className="text-xs text-gray-400">
                  Verify - Protect - Trust
                </span>
              </div>
            </div>
            
            {/* Navigation Tabs */}
            <div className={`flex items-center gap-2 ${isDark ? 'bg-[#0F1729]' : 'bg-gray-100'} p-1 rounded-lg`}>
              <button
                onClick={() => setActiveTab('newspaper')}
                className={`px-6 py-2 rounded-md transition-all ${
                  activeTab === 'newspaper'
                    ? isDark ? 'bg-purple-600 text-white' : 'bg-purple-500 text-white'
                    : isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Newspaper
              </button>
              <button
                onClick={() => setActiveTab('malware')}
                className={`px-6 py-2 rounded-md transition-all ${
                  activeTab === 'malware'
                    ? isDark ? 'bg-purple-600 text-white' : 'bg-purple-500 text-white'
                    : isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Malware
              </button>
              <button
                onClick={() => setActiveTab('spam')}
                className={`px-6 py-2 rounded-md transition-all ${
                  activeTab === 'spam'
                    ? isDark ? 'bg-purple-600 text-white' : 'bg-purple-500 text-white'
                    : isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Spam and Ham
              </button>
            </div>

            {/* User Controls */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                className={`p-2 rounded-lg ${isDark ? 'bg-[#0F1729] text-gray-400 hover:text-white' : 'bg-gray-100 text-gray-600 hover:text-gray-900'} transition-colors`}
              >
                {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <div className={`w-10 h-10 ${isDark ? 'bg-blue-600' : 'bg-blue-500'} rounded-full flex items-center justify-center`}>
                <User className="w-5 h-5 text-white" />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-[1600px] mx-auto px-6 py-8">
        {/* Input Section - Top Center */}
        <div className="max-w-3xl mx-auto mb-8">
          <div className={`${isDark ? 'bg-[#1a2332]' : 'bg-white'} rounded-xl p-6 transition-colors duration-300`}>
            <div className="mb-6">
              <h2 className={`text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'} mb-2`}>{getTabTitle()}</h2>
              <p className={`${isDark ? 'text-gray-400' : 'text-gray-600'} text-sm`}>{getTabDescription()}</p>
            </div>

            {/* Input Type Tabs */}
            {activeTab === 'newspaper' ? (
              // Newspaper: Text Entry and URL Only
              <div className={`flex gap-2 mb-6 ${isDark ? 'bg-[#0F1729]' : 'bg-gray-100'} p-1 rounded-lg`}>
                <button
                  onClick={() => setInputType('text')}
                  className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-md transition-all ${
                    inputType === 'text'
                      ? isDark ? 'bg-purple-600 text-white' : 'bg-purple-500 text-white'
                      : isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <FileText className="w-4 h-4" />
                  <span>Text Entry</span>
                </button>
                <button
                  onClick={() => setInputType('file')}
                  className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-md transition-all ${
                    inputType === 'file'
                      ? isDark ? 'bg-purple-600 text-white' : 'bg-purple-500 text-white'
                      : isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <LinkIcon className="w-4 h-4" />
                  <span>URL Only</span>
                </button>
              </div>
            ) : activeTab === 'malware' ? (
              // Malware: File Upload only
              <div className="mb-6">
                <div className={`${isDark ? 'bg-[#0F1729]' : 'bg-gray-100'} p-3 rounded-lg text-center`}>
                  <Upload className={`w-5 h-5 ${isDark ? 'text-purple-400' : 'text-purple-600'} inline-block mr-2`} />
                  <span className={isDark ? 'text-gray-300' : 'text-gray-700'}>File Upload Mode</span>
                </div>
              </div>
            ) : (
              // Spam and Ham: Text entry only
              <div className="mb-6">
                <div className={`${isDark ? 'bg-[#0F1729]' : 'bg-gray-100'} p-3 rounded-lg text-center`}>
                  <FileText className={`w-5 h-5 ${isDark ? 'text-purple-400' : 'text-purple-600'} inline-block mr-2`} />
                  <span className={isDark ? 'text-gray-300' : 'text-gray-700'}>Text Entry Mode</span>
                </div>
              </div>
            )}

            {/* Input Area */}
            {(activeTab === 'newspaper' && inputType === 'text') || activeTab === 'spam' ? (
              <div className="mb-6">
                <label className={`block ${isDark ? 'text-gray-300' : 'text-gray-700'} mb-2 text-sm`}>
                  {activeTab === 'newspaper' ? 'Enter article text' : 'Enter email or message text'}
                </label>
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder={
                    activeTab === 'newspaper'
                      ? 'Paste article text here...'
                      : 'Paste email or message content here...'
                  }
                  className={`w-full h-32 px-4 py-3 ${
                    isDark ? 'bg-[#0F1729] text-white border-gray-700' : 'bg-white text-gray-900 border-gray-300'
                  } border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-colors`}
                />
              </div>
            ) : activeTab === 'newspaper' && inputType === 'file' ? (
              <div className="mb-6">
                <label className={`block ${isDark ? 'text-gray-300' : 'text-gray-700'} mb-2 text-sm`}>
                  Enter URL to analyze
                </label>
                <input
                  type="url"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="https://example.com/article"
                  className={`w-full px-4 py-3 ${
                    isDark ? 'bg-[#0F1729] text-white border-gray-700' : 'bg-white text-gray-900 border-gray-300'
                  } border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors`}
                />
              </div>
            ) : (
              <div className="mb-6">
                <label className={`block ${isDark ? 'text-gray-300' : 'text-gray-700'} mb-2 text-sm`}>
                  Upload file for malware scan
                </label>
                <div
                  className={`border-2 border-dashed ${
                    isDark ? 'border-gray-700 bg-[#0F1729]' : 'border-gray-300 bg-gray-50'
                  } rounded-lg p-8 text-center transition-colors`}
                >
                  <Upload className={`w-10 h-10 ${isDark ? 'text-gray-600' : 'text-gray-400'} mx-auto mb-3`} />
                  <p className={`${isDark ? 'text-gray-400' : 'text-gray-600'} mb-2 text-sm`}>
                    {fileName || 'Drag and drop your file here'}
                  </p>
                  <label className="cursor-pointer">
                    <span className="text-purple-500 hover:text-purple-600 text-sm">Browse files</span>
                    <input type="file" className="hidden" onChange={handleFileUpload} />
                  </label>
                </div>
              </div>
            )}

            {/* Analyze Button */}
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className={`w-full py-4 rounded-lg font-semibold transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed ${
                isDark 
                  ? 'bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-700 hover:to-purple-600 text-white shadow-purple-500/50' 
                  : 'bg-gradient-to-r from-purple-500 to-purple-400 hover:from-purple-600 hover:to-purple-500 text-white shadow-purple-400/50'
              } hover:shadow-xl transform hover:-translate-y-0.5`}
            >
              {isAnalyzing ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </div>

        {/* Results Section - 2 Column Grid */}
        {result ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left Column Charts */}
            <div className="space-y-6">
              {/* Overall Score */}
              <div className={`${isDark ? 'bg-[#1a2332]' : 'bg-white'} rounded-xl p-6 transition-colors duration-300`}>
                <h3 className={`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'} mb-4`}>Detection Confidence</h3>
                <div className="text-center mb-6">
                  <div className={`text-6xl font-bold mb-2 ${result.overall >= 80 ? 'text-red-500' : result.overall >= 50 ? 'text-orange-500' : 'text-green-500'}`}>
                    {result.overall}%
                  </div>
                  <p className={`${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                    {result.overall >= 80 ? 'High Threat' : result.overall >= 50 ? 'Medium Threat' : 'Low Threat'}
                  </p>
                </div>

                {/* Categories Bar Chart */}
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={result.categories}>
                    <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
                    <XAxis dataKey="name" stroke={isDark ? '#9ca3af' : '#6b7280'} />
                    <YAxis stroke={isDark ? '#9ca3af' : '#6b7280'} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: isDark ? '#1a2332' : '#ffffff',
                        border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                        borderRadius: '8px',
                        color: isDark ? '#fff' : '#000',
                      }}
                    />
                    <Bar dataKey="score" radius={[8, 8, 0, 0]}>
                      {result.categories.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Timeline Chart */}
              <div className={`${isDark ? 'bg-[#1a2332]' : 'bg-white'} rounded-xl p-6 transition-colors duration-300`}>
                <h3 className={`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'} mb-4`}>Threat Activity Timeline</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={result.timeline}>
                    <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
                    <XAxis dataKey="time" stroke={isDark ? '#9ca3af' : '#6b7280'} />
                    <YAxis stroke={isDark ? '#9ca3af' : '#6b7280'} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: isDark ? '#1a2332' : '#ffffff',
                        border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                        borderRadius: '8px',
                        color: isDark ? '#fff' : '#000',
                      }}
                    />
                    <Line type="monotone" dataKey="threats" stroke="#3b82f6" strokeWidth={2} dot={{ fill: '#3b82f6' }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Right Column Charts */}
            <div className="space-y-6">
              {/* Radar Chart - Multi-dimensional Analysis */}
              <div className={`${isDark ? 'bg-[#1a2332]' : 'bg-white'} rounded-xl p-6 transition-colors duration-300`}>
                <h3 className={`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'} mb-4`}>Multi-dimensional Analysis</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={result.radarData}>
                    <PolarGrid stroke={isDark ? '#374151' : '#e5e7eb'} />
                    <PolarAngleAxis dataKey="category" stroke={isDark ? '#9ca3af' : '#6b7280'} />
                    <PolarRadiusAxis stroke={isDark ? '#9ca3af' : '#6b7280'} />
                    <Radar name="Threat Level" dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: isDark ? '#1a2332' : '#ffffff',
                        border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                        borderRadius: '8px',
                        color: isDark ? '#fff' : '#000',
                      }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              {/* Threat Details */}
              <div className={`${isDark ? 'bg-[#1a2332]' : 'bg-white'} rounded-xl p-6 transition-colors duration-300`}>
                <h3 className={`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'} mb-4`}>Detected Threats</h3>
                <div className="space-y-3">
                  {result.threats.map((threat, index) => (
                    <div
                      key={index}
                      className={`p-4 ${isDark ? 'bg-[#0F1729]' : 'bg-gray-50'} rounded-lg border ${getSeverityColor(threat.severity)} transition-colors`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <h4 className={`font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>{threat.type}</h4>
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${getSeverityColor(threat.severity)}`}>
                          {threat.severity}
                        </span>
                      </div>
                      <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>{threat.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className={`${isDark ? 'bg-[#1a2332]' : 'bg-white'} rounded-xl p-12 text-center transition-colors duration-300 max-w-2xl mx-auto`}>
            <img src="/Logo.jpg" alt="TruthGuard" className="mx-auto mb-4" />
            <h3 className={`text-xl font-semibold ${isDark ? 'text-white' : 'text-gray-900'} mb-2`}>No Analysis Yet</h3>
            <p className={`${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              Submit content to see detailed threat analysis and detection results
            </p>
          </div>
        )}
      </main>
    </div>
  );
}