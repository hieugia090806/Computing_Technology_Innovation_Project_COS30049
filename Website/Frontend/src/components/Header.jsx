import React, { useState, useEffect } from 'react';
import { Sun, Moon, Camera, User, Settings, LogOut, CheckCircle } from 'lucide-react';
import logoTeam from '../assets/logo.png'; 

const Header = ({ isDarkMode, toggleTheme }) => {
  const [showAvatarMenu, setShowAvatarMenu] = useState(false);
  const [showToast, setShowToast] = useState(false);

  const handleThemeChange = () => {
    toggleTheme();
    setShowToast(true);
  };

  useEffect(() => {
    if (showToast) {
      const timer = setTimeout(() => setShowToast(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [showToast]);

  return (
    <header className={`w-full h-24 border-b flex items-center justify-between px-10 fixed top-0 z-50 transition-all duration-300 
      ${isDarkMode ? 'bg-[#0B0F19]/90 border-gray-800 backdrop-blur-md text-white' : 'bg-white/90 border-gray-200 backdrop-blur-md text-gray-900'}`}>
      
      {/* 1. LOGO TRUTHGUARD (Size to oai phong) */}
      <div className="flex items-center gap-4 cursor-pointer shrink-0 group">
        <div className="p-1 transition-transform group-hover:scale-105 duration-300">
          <img src={logoTeam} alt="Logo" className="h-14 w-auto object-contain" />
        </div>
        <div className="flex flex-col">
          <span className="text-2xl font-black tracking-tighter uppercase leading-none">TruthGuard</span>
          <span className="text-[10px] font-bold tracking-[0.2em] text-blue-500 uppercase">Verify. Trust. Protect</span>
        </div>
      </div>

      {/* 2. MENU GIỮA */}
      <nav className="hidden lg:flex items-center gap-12 text-sm font-bold opacity-70">
        <button className="hover:text-blue-500 transition-colors uppercase tracking-widest">Spam and ham</button>
        <button className="hover:text-blue-500 transition-colors uppercase tracking-widest">Malware</button>
        <button className="hover:text-blue-500 transition-colors uppercase tracking-widest">Newspaper</button>
      </nav>

      {/* 3. PHẢI: THEME & AVATAR */}
      <div className="flex items-center gap-6">
        
        {/* Nút Chỉnh Sáng/Tối */}
        <button 
          onClick={handleThemeChange}
          className={`p-3 rounded-2xl border transition-all duration-300 ${isDarkMode ? 'bg-gray-800 border-gray-700 text-yellow-400' : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-blue-500'}`}
        >
          {isDarkMode ? <Sun size={22} /> : <Moon size={22} />}
        </button>

        {/* CỤM AVATAR + MENU DROPDOWN */}
        <div className="relative">
          <button 
            onClick={() => setShowAvatarMenu(!showAvatarMenu)}
            className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-700 flex items-center justify-center text-white font-black border-2 border-white/20 shadow-xl cursor-pointer active:scale-90 transition-all"
          >
            U
          </button>

          {showAvatarMenu && (
            <>
              <div className="fixed inset-0 z-[-1]" onClick={() => setShowAvatarMenu(false)}></div>
              <div className={`absolute right-0 mt-4 w-64 rounded-3xl shadow-2xl border p-3 animate-in fade-in zoom-in slide-in-from-top-2 duration-200
                ${isDarkMode ? 'bg-[#111827] border-gray-800 text-white' : 'bg-white border-gray-100 text-gray-900'}`}>
                
                <div className="px-4 py-3 mb-2 border-b border-gray-800/50">
                  <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Account</p>
                  <p className="font-bold truncate">Hieu Nguyen</p>
                </div>

                <div className="flex flex-col gap-1">
                  <button className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-semibold transition-colors ${isDarkMode ? 'hover:bg-gray-800' : 'hover:bg-gray-50'}`}>
                    <Camera size={18} className="text-blue-500" /> Upload Photo
                  </button>
                  <button className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-semibold transition-colors ${isDarkMode ? 'hover:bg-gray-800' : 'hover:bg-gray-50'}`}>
                    <User size={18} className="text-emerald-500" /> My Profile
                  </button>
                  
                  {/* NÚT SETTINGS ÔNG MỚI YÊU CẦU ĐÂY */}
                  <button className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-semibold transition-colors ${isDarkMode ? 'hover:bg-gray-800' : 'hover:bg-gray-50'}`}>
                    <Settings size={18} className="text-orange-500" /> Settings
                  </button>
                </div>

                <div className={`my-2 border-t ${isDarkMode ? 'border-gray-800' : 'border-gray-100'}`}></div>
                
                <button className="w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm text-red-500 hover:bg-red-500/10 transition-colors font-bold">
                  <LogOut size={18} /> Logout
                </button>
              </div>
            </>
          )}
        </div>

        {/* TOAST THÔNG BÁO MẤY APP LỚN HAY DÙNG */}
        {showToast && (
          <div className={`fixed bottom-10 left-1/2 -translate-x-1/2 flex items-center gap-3 px-8 py-4 rounded-2xl shadow-2xl border animate-in slide-in-from-bottom-5 duration-300 z-[100]
            ${isDarkMode ? 'bg-white text-black border-gray-200' : 'bg-black text-white border-white/10'}`}>
            <CheckCircle size={20} className="text-green-500" />
            <span className="font-bold tracking-tight uppercase">
              {isDarkMode ? 'Dark Mode' : 'Light Mode'} Enabled
            </span>
          </div>
        )}

      </div>
    </header>
  );
};

export default Header;