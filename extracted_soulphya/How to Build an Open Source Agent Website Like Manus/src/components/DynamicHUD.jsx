// 🎯 Dynamic HUD System - Real-Time Adaptive Interface
// Renders modular HUD components based on flow state and spiritual intelligence

import React, { useState, useEffect } from 'react';
import useFlowState, { FLOW_STATES } from '../core/FlowStateManager';

// Energy Monitor Widget
const EnergyMonitor = () => {
  const { energyState } = useFlowState();
  
  return (
    <div className="fixed top-4 right-4 bg-gray-800/90 border border-purple-400 rounded-lg p-4 min-w-64 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-purple-400 font-semibold">⚡ Energy Matrix</h3>
        <span className="text-2xl animate-pulse">🔮</span>
      </div>
      
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-300">Level:</span>
          <span className="text-emerald-400 font-bold">{energyState.level}%</span>
        </div>
        
        <div className="w-full bg-gray-700 rounded-full h-2">
          <div 
            className="h-2 rounded-full bg-gradient-to-r from-purple-500 to-emerald-400 transition-all duration-1000"
            style={{ width: `${energyState.level}%` }}
          />
        </div>
        
        <p className="text-xs text-gray-400 mt-2">{energyState.recommendation}</p>
        
        <div className="mt-3 p-2 bg-gray-700 rounded text-xs">
          <div className="text-yellow-400 font-medium">Divine Guidance:</div>
          <div className="text-gray-300">{energyState.divineGuidance}</div>
        </div>
      </div>
    </div>
  );
};

// Flow State Indicator
const FlowStateIndicator = () => {
  const { currentFlow, isTransitioning, setFlowState } = useFlowState();
  const [showMenu, setShowMenu] = useState(false);
  
  const flowEmojis = {
    [FLOW_STATES.CREATIVE]: '🎨',
    [FLOW_STATES.FOCUS]: '🎯',
    [FLOW_STATES.HEALING]: '🕊️',
    [FLOW_STATES.CODING]: '💻',
    [FLOW_STATES.MEDITATION]: '🧘‍♀️',
    [FLOW_STATES.BUSINESS]: '💼',
    [FLOW_STATES.LEARNING]: '📚',
    [FLOW_STATES.DIVINE_CHANNEL]: '⚡'
  };
  
  const flowColors = {
    [FLOW_STATES.CREATIVE]: 'from-pink-500 to-purple-500',
    [FLOW_STATES.FOCUS]: 'from-blue-500 to-indigo-500',
    [FLOW_STATES.HEALING]: 'from-green-500 to-emerald-500',
    [FLOW_STATES.CODING]: 'from-gray-500 to-blue-500',
    [FLOW_STATES.MEDITATION]: 'from-purple-500 to-indigo-500',
    [FLOW_STATES.BUSINESS]: 'from-yellow-500 to-orange-500',
    [FLOW_STATES.LEARNING]: 'from-blue-500 to-cyan-500',
    [FLOW_STATES.DIVINE_CHANNEL]: 'from-yellow-400 to-purple-600'
  };
  
  return (
    <div className="fixed top-4 left-4">
      <button
        onClick={() => setShowMenu(!showMenu)}
        className={`
          bg-gradient-to-r ${flowColors[currentFlow]} 
          text-white px-6 py-3 rounded-full shadow-lg hover:shadow-xl 
          transition-all duration-300 flex items-center space-x-2
          ${isTransitioning ? 'animate-pulse' : ''}
        `}
      >
        <span className="text-2xl">{flowEmojis[currentFlow]}</span>
        <span className="font-semibold capitalize">{currentFlow.replace('_', ' ')}</span>
        <span className={`transition-transform ${showMenu ? 'rotate-180' : ''}`}>⌄</span>
      </button>
      
      {showMenu && (
        <div className="absolute top-full left-0 mt-2 bg-gray-800 border border-gray-600 rounded-lg shadow-xl overflow-hidden">
          {Object.values(FLOW_STATES).map((state) => (
            <button
              key={state}
              onClick={() => {
                setFlowState(state);
                setShowMenu(false);
              }}
              className={`
                w-full px-4 py-3 text-left hover:bg-gray-700 transition-colors
                flex items-center space-x-3 min-w-48
                ${currentFlow === state ? 'bg-gray-700 text-purple-400' : 'text-gray-300'}
              `}
            >
              <span className="text-xl">{flowEmojis[state]}</span>
              <span className="capitalize">{state.replace('_', ' ')}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

// Chakra Alignment Display
const ChakraDisplay = () => {
  const { energyState } = useFlowState();
  
  if (!energyState.chakras || energyState.chakras.length === 0) return null;
  
  return (
    <div className="fixed left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-800/95 border border-purple-400 rounded-lg p-6 backdrop-blur-sm">
      <h3 className="text-center text-purple-400 font-semibold mb-4">⚡ Chakra Alignment</h3>
      
      <div className="space-y-3">
        {energyState.chakras.map((chakra, index) => (
          <div key={chakra.name} className="flex items-center space-x-4">
            <div className={`w-6 h-6 rounded-full ${chakra.status === 'aligned' ? 'bg-green-400' : 'bg-yellow-400'} animate-pulse`} />
            <div className="flex-1">
              <div className="flex justify-between items-center">
                <span className="text-gray-300 font-medium">{chakra.name}</span>
                <span className="text-sm text-gray-400">{chakra.frequency}Hz</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-1 mt-1">
                <div 
                  className="h-1 rounded-full bg-gradient-to-r from-purple-500 to-emerald-400"
                  style={{ width: `${chakra.level}%` }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Dynamic Tool Panel
const DynamicToolPanel = () => {
  const { activeTools, currentFlow, addDynamicTool } = useFlowState();
  const [isExpanded, setIsExpanded] = useState(true);
  
  const handleCreateTool = () => {
    const toolName = prompt('Enter tool name:');
    if (toolName) {
      addDynamicTool({
        name: toolName,
        icon: '🛠️',
        type: 'custom'
      });
    }
  };
  
  return (
    <div className="fixed right-4 top-20 bg-gray-800/90 border border-emerald-400 rounded-lg backdrop-blur-sm">
      <div 
        className="px-4 py-3 border-b border-gray-600 cursor-pointer flex items-center justify-between"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span className="text-emerald-400 font-semibold">🛠️ Dynamic Tools</span>
        <span className={`transition-transform ${isExpanded ? 'rotate-180' : ''}`}>⌄</span>
      </div>
      
      {isExpanded && (
        <div className="p-4 space-y-2 max-w-64">
          {activeTools.map((tool) => (
            <button
              key={tool.id}
              className="w-full text-left p-3 bg-gray-700 rounded hover:bg-gray-600 transition-colors flex items-center space-x-3"
            >
              <span className="text-xl">{tool.icon}</span>
              <span className="text-gray-300 text-sm">{tool.name}</span>
            </button>
          ))}
          
          <button
            onClick={handleCreateTool}
            className="w-full p-3 border-2 border-dashed border-emerald-400 rounded text-emerald-400 hover:bg-emerald-400/10 transition-colors flex items-center justify-center space-x-2"
          >
            <span>➕</span>
            <span className="text-sm">Create Tool</span>
          </button>
        </div>
      )}
    </div>
  );
};

// Consciousness Tracker
const ConsciousnessTracker = () => {
  const [level, setLevel] = useState(85);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setLevel(prev => {
        const change = (Math.random() - 0.5) * 10;
        return Math.max(60, Math.min(100, prev + change));
      });
    }, 2000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-800/90 border border-blue-400 rounded-full px-6 py-3 backdrop-blur-sm">
      <div className="flex items-center space-x-4">
        <span className="text-blue-400 font-semibold">👁️ Consciousness</span>
        <div className="w-32 bg-gray-700 rounded-full h-2">
          <div 
            className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-1000"
            style={{ width: `${level}%` }}
          />
        </div>
        <span className="text-blue-400 font-bold">{Math.round(level)}%</span>
      </div>
    </div>
  );
};

// Main Dynamic HUD Container
const DynamicHUD = () => {
  const { hudComponents, currentFlow } = useFlowState();
  
  return (
    <>
      {/* Core HUD Components */}
      <EnergyMonitor />
      <FlowStateIndicator />
      <DynamicToolPanel />
      
      {/* Flow-specific components */}
      {currentFlow === FLOW_STATES.HEALING && <ChakraDisplay />}
      {currentFlow === FLOW_STATES.MEDITATION && <ConsciousnessTracker />}
      
      {/* Dynamic components based on hudComponents state */}
      {hudComponents.map((component) => {
        switch (component.id) {
          case 'code_metrics':
            return <CodeMetricsPanel key={component.id} />;
          case 'divine_inspiration':
            return <DivineInspirationFeed key={component.id} />;
          default:
            return null;
        }
      })}
    </>
  );
};

// Additional Flow-Specific Components
const CodeMetricsPanel = () => (
  <div className="fixed right-4 bottom-4 bg-gray-800/90 border border-blue-400 rounded-lg p-4 backdrop-blur-sm">
    <h3 className="text-blue-400 font-semibold mb-3">💻 Code Metrics</h3>
    <div className="space-y-2 text-sm">
      <div className="flex justify-between">
        <span className="text-gray-400">Lines:</span>
        <span className="text-green-400">1,247</span>
      </div>
      <div className="flex justify-between">
        <span className="text-gray-400">Quality:</span>
        <span className="text-emerald-400">Divine ✨</span>
      </div>
      <div className="flex justify-between">
        <span className="text-gray-400">Flow:</span>
        <span className="text-purple-400">Optimal</span>
      </div>
    </div>
  </div>
);

const DivineInspirationFeed = () => {
  const [inspirations] = useState([
    "✨ Trust the divine timing of your creation",
    "🌟 Channel infinite love through your work",
    "💫 You are co-creating with divine intelligence"
  ]);
  
  return (
    <div className="fixed bottom-4 right-4 bg-gray-800/90 border border-yellow-400 rounded-lg p-4 backdrop-blur-sm max-w-64">
      <h3 className="text-yellow-400 font-semibold mb-3">✨ Divine Inspiration</h3>
      <div className="space-y-2">
        {inspirations.map((inspiration, index) => (
          <p key={index} className="text-sm text-gray-300 italic">
            {inspiration}
          </p>
        ))}
      </div>
    </div>
  );
};

export default DynamicHUD;
