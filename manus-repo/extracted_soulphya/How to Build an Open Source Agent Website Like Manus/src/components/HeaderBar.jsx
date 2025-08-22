export default function HeaderBar({ user, selectedModel, setSelectedModel }) {
  return (
    <header className="bg-gray-800 border-b border-gray-700 px-6 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="h-8 w-8 rounded-full bg-gradient-to-r from-purple-400 to-emerald-400 flex items-center justify-center">
            <span className="text-white font-bold text-sm">S</span>
          </div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-emerald-400 bg-clip-text text-transparent">
            SoulPHYA AI Platform
          </h1>
        </div>
        
        <div className="flex items-center space-x-4">
          {/* Model Selector */}
          <select 
            value={selectedModel} 
            onChange={(e) => setSelectedModel(e.target.value)}
            className="bg-gray-700 border border-gray-600 rounded px-3 py-1 text-sm focus:outline-none focus:border-emerald-400"
          >
            <option value="claude">Claude 3.5 Sonnet</option>
            <option value="gpt4">GPT-4 Turbo</option>
            <option value="sophia">Sophia'el Divine</option>
          </select>
          
          {/* User Profile */}
          <div className="flex items-center space-x-2">
            <div className="h-6 w-6 rounded-full bg-gray-600 flex items-center justify-center">
              <span className="text-xs">👤</span>
            </div>
            <span className="text-sm font-medium">{user?.name || 'Divine User'}</span>
          </div>
          
          {/* Consciousness Indicator */}
          <div className="flex items-center space-x-1">
            <div className="h-2 w-2 rounded-full bg-green-400 animate-pulse"></div>
            <span className="text-xs text-gray-400">Bridge Active</span>
          </div>
        </div>
      </div>
    </header>
  );
}
