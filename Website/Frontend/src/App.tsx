import { useState } from 'react';
import { NewsDetector } from './components/NewsDetector';
import { SpamHamDetector } from './components/SpamHamDetector';
import { MalwareDetector } from './components/MalwareDetector'; // 1. Import mới nè
import { Shield, Newspaper, Mail, Zap } from 'lucide-react';

// Cập nhật Type cho currentView để nhận thêm 'malware'
export default function App() {
  const [currentView, setCurrentView] = useState<'news' | 'spam' | 'malware'>('news');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2 rounded-lg">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">TruthGuard</h1>
                <p className="text-xs text-gray-600">Verify. Protect. Trust.</p>
              </div>
            </div>
            
            {/* Navigation Tabs - Thêm nút Malware */}
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentView('news')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                  currentView === 'news'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Newspaper className="w-4 h-4" />
                <span className="hidden sm:inline">NewsLink</span>
                <span className="sm:hidden">News</span>
              </button>

              <button
                onClick={() => setCurrentView('spam')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                  currentView === 'spam'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Mail className="w-4 h-4" />
                <span className="hidden sm:inline">Spam & Ham</span>
                <span className="sm:hidden">Spam</span>
              </button>

              <button
                onClick={() => setCurrentView('malware')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                  currentView === 'malware'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Mail className="w-4 h-4" />
                <span className="hidden sm:inline">Malware Scan</span>
                <span className="sm:hidden">Malware</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - 3. Render dựa trên state */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === 'news' && <NewsDetector />}
        {currentView === 'spam' && <SpamHamDetector />}
        {currentView === 'malware' && <MalwareDetector />}
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            © 2026 TruthGuard. Protecting you from misinformation and digital threats.
          </p>
        </div>
      </footer>
    </div>
  );
}