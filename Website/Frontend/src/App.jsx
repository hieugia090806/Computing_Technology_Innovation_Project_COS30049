import React, { useState } from 'react';
import Header from './components/Header';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className={`min-h-screen flex flex-col transition-colors duration-300 ${isDarkMode ? 'bg-[#020617]' : 'bg-[#F9FAFB]'}`}>
      
      {/*-- Header --*/}
      <Header isDarkMode={isDarkMode} toggleTheme={toggleTheme} />

      {/*-- Body doesn't have content yet. --*/}
      <main className="flex-grow pt-32 flex flex-col items-center justify-center">
        <div className="text-center opacity-20">
          <h1 className={`text-5xl font-black ${isDarkMode ? 'text-white' : 'text-black'}`}>
            BODY AREA
          </h1>
        </div>
      </main>

      <footer className={`py-6 border-t text-center text-sm ${isDarkMode ? 'border-gray-800 text-gray-600' : 'border-gray-200 text-gray-400'}`}>
        © 2026 TruthGuard Team • Built for Advanced Analysis
      </footer>

    </div>
  );
}

export default App;