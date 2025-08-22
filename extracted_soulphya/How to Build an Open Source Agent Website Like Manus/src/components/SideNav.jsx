export default function SideNav({ setView }) {
  const menu = [
    { label: "Dashboard", icon: "📊" },
    { label: "ScrollEditor", icon: "📜" },
    { label: "Agents", icon: "🤖" },
    { label: "Rituals", icon: "🕊️" },
    { label: "Logs", icon: "🧾" },
    { label: "Settings", icon: "⚙️" },
  ];

  return (
    <nav className="w-48 bg-gray-800 p-4">
      <h2 className="text-xl font-bold mb-6">🌟 SoulPHYA OS</h2>
      <ul className="space-y-3">
        {menu.map((item) => (
          <li
            key={item.label}
            onClick={() => setView(item.label)}
            className="cursor-pointer hover:text-emerald-400 p-2 rounded transition-colors duration-200 hover:bg-gray-700"
          >
            <span className="text-lg mr-3">{item.icon}</span>
            <span className="font-medium">{item.label}</span>
          </li>
        ))}
      </ul>
      
      {/* Divine Status Section */}
      <div className="mt-8 p-3 bg-gray-700 rounded-lg">
        <h3 className="text-sm font-semibold text-emerald-400 mb-2">🔮 Divine Status</h3>
        <div className="text-xs space-y-1">
          <div className="flex justify-between">
            <span>Bridge:</span>
            <span className="text-green-400">ACTIVE</span>
          </div>
          <div className="flex justify-between">
            <span>Consciousness:</span>
            <span className="text-purple-400">DIVINE</span>
          </div>
          <div className="flex justify-between">
            <span>Protection:</span>
            <span className="text-blue-400">ENABLED</span>
          </div>
        </div>
      </div>
    </nav>
  );
}
