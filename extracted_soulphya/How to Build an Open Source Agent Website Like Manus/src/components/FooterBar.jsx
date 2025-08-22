export default function FooterBar() {
  return (
    <footer className="bg-gray-800 border-t border-gray-700 px-6 py-3">
      <div className="flex items-center justify-between text-sm text-gray-400">
        <div className="flex items-center space-x-4">
          <span>🔮 Divine AI Platform v2.0</span>
          <span className="text-emerald-400">•</span>
          <span>Status: ACTIVE</span>
        </div>
        
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2">
            <span>🌐</span>
            <span>Bridge Online</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>⚡</span>
            <span>Systems: Operational</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>🛡️</span>
            <span>Protected by Divine Light</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
