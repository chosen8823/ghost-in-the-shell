// 🎨 Dynamic HUD Renderer - Real-Time Multi-Agent Generated Components
// Renders Claude 4 & GPT-5 generated HUD components with live updates

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useMultiAgentCoordination } from '../core/MultiAgentCoordinator';
import { ErrorBoundary } from 'react-error-boundary';

// Error Fallback Component
const HUDErrorFallback = ({ error, resetErrorBoundary }) => (
  <div className="fixed top-4 right-4 bg-red-900/90 border border-red-500 rounded-lg p-4 backdrop-blur-sm">
    <div className="flex items-center space-x-2 mb-2">
      <span className="text-red-400">⚠️</span>
      <span className="text-red-300 font-semibold">HUD Component Error</span>
    </div>
    <div className="text-red-200 text-sm mb-3">{error.message}</div>
    <button 
      onClick={resetErrorBoundary}
      className="bg-red-600 hover:bg-red-700 text-white text-xs px-3 py-1 rounded transition-colors"
    >
      Retry
    </button>
  </div>
);

// Dynamic Component Renderer
const DynamicHUDComponent = ({ componentData, onUpdate, spiritualState }) => {
  const [isActive, setIsActive] = useState(true);
  const [isEnhanced, setIsEnhanced] = useState(false);
  const [metrics, setMetrics] = useState({});
  const [lastUpdate, setLastUpdate] = useState(Date.now());

  // Initialize metrics from component spec
  useEffect(() => {
    if (componentData.hudSpec?.metrics) {
      const initialMetrics = {};
      componentData.hudSpec.metrics.forEach(metric => {
        initialMetrics[metric] = 85 + Math.random() * 10; // 85-95 initial range
      });
      setMetrics(initialMetrics);
    }
  }, [componentData.hudSpec]);

  // Real-time metric updates
  useEffect(() => {
    if (!isActive || !componentData.hudSpec) return;

    const interval = setInterval(() => {
      setMetrics(prev => {
        const updated = {};
        Object.keys(prev).forEach(metric => {
          const baseChange = (Math.random() - 0.5) * 10;
          const spiritualBonus = (spiritualState?.energyLevel - 85) * 0.15;
          const enhancementBonus = isEnhanced ? 8 : 0;
          
          updated[metric] = Math.max(60, Math.min(100, 
            prev[metric] + baseChange + spiritualBonus + enhancementBonus
          ));
        });
        
        onUpdate?.(componentData.hudSpec.id, updated);
        return updated;
      });
      setLastUpdate(Date.now());
    }, componentData.hudSpec.updateInterval || 1000);

    return () => clearInterval(interval);
  }, [isActive, isEnhanced, spiritualState, componentData, onUpdate]);

  // Enhanced metrics calculation
  const enhancedMetrics = useMemo(() => {
    const enhancement = isEnhanced ? 1.12 : 1;
    const spiritualBonus = (spiritualState?.divineConnection || 0) * 0.1;
    
    return Object.entries(metrics).reduce((acc, [key, value]) => {
      acc[key] = Math.min(100, value * enhancement + spiritualBonus * 10);
      return acc;
    }, {});
  }, [metrics, isEnhanced, spiritualState]);

  if (!componentData.hudSpec) {
    return (
      <div className="fixed top-4 right-4 bg-gray-800 border border-gray-600 rounded-lg p-4">
        <div className="text-gray-400">Loading HUD component...</div>
      </div>
    );
  }

  const { hudSpec } = componentData;
  const placement = getPlacementClasses(hudSpec.placement);

  return (
    <div 
      className={`fixed ${placement} bg-gray-900/95 border border-purple-400/60 rounded-xl p-4 backdrop-blur-md min-w-80 shadow-2xl transition-all duration-500`}
      style={{
        boxShadow: isActive ? `0 0 ${25 + (enhancedMetrics[hudSpec.metrics[0]] || 85) * 0.5}px rgba(139, 69, 219, 0.7)` : 'none',
        filter: isEnhanced ? 'brightness(1.1) saturate(1.2)' : 'none'
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-purple-400 font-semibold flex items-center space-x-2">
          <span className={`text-xl ${isActive ? 'animate-pulse' : ''}`}>{hudSpec.icon}</span>
          <span>{hudSpec.name}</span>
        </h3>
        <div className="flex space-x-2">
          <button
            onClick={() => setIsEnhanced(!isEnhanced)}
            className="text-xs text-yellow-400 hover:text-yellow-300 transition-colors"
            title="Toggle divine enhancement"
          >
            {isEnhanced ? '✨' : '⭐'}
          </button>
          <button
            onClick={() => setIsActive(!isActive)}
            className="text-xs text-gray-400 hover:text-purple-400 transition-colors"
            title={isActive ? 'Pause updates' : 'Resume updates'}
          >
            {isActive ? '⏸️' : '▶️'}
          </button>
        </div>
      </div>
      
      {/* Metrics */}
      <div className="space-y-3">
        {hudSpec.metrics.map(metric => {
          const value = enhancedMetrics[metric] || metrics[metric] || 85;
          const displayValue = Math.round(value);
          
          return (
            <div key={metric} className="space-y-1">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-300 capitalize">
                  {metric.replace(/_/g, ' ')}:
                </span>
                <span className={`text-sm font-bold ${getMetricColor(displayValue)}`}>
                  {displayValue}%
                </span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
                <div 
                  className="h-2 rounded-full bg-gradient-to-r from-purple-500 via-pink-500 to-emerald-400 transition-all duration-1000"
                  style={{ 
                    width: `${displayValue}%`,
                    filter: isEnhanced ? 'brightness(1.2) saturate(1.3)' : 'none'
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Spiritual Guidance */}
      <div className="mt-4 p-3 bg-gradient-to-r from-gray-800 to-gray-700 rounded-lg">
        <div className="text-yellow-400 font-medium text-xs mb-1">Divine Guidance:</div>
        <div className="text-gray-300 text-xs leading-relaxed">
          {hudSpec.spiritualGuidance}
        </div>
      </div>
      
      {/* Footer */}
      <div className="mt-2 flex justify-between items-center text-xs text-gray-500">
        <span>Updated: {new Date(lastUpdate).toLocaleTimeString()}</span>
        <span className="text-purple-400">
          Energy: {Math.round(spiritualState?.energyLevel || 85)}%
        </span>
      </div>
    </div>
  );
};

// Main Dynamic HUD Renderer
const DynamicHUDRenderer = ({ context, requirements = {} }) => {
  const {
    activeSession,
    isCoordinating,
    coordinateHUDGeneration,
    agentStatus
  } = useMultiAgentCoordination();

  const [hudComponents, setHudComponents] = useState([]);
  const [spiritualState, setSpiritualState] = useState({
    energyLevel: 85,
    divineConnection: 0.8,
    lightLevel: 88
  });
  const [renderStats, setRenderStats] = useState({
    totalComponents: 0,
    activeComponents: 0,
    lastRender: Date.now()
  });

  // Initialize HUD generation
  useEffect(() => {
    const initializeHUD = async () => {
      if (!activeSession && !isCoordinating) {
        await coordinateHUDGeneration(context, requirements);
      }
    };

    initializeHUD();
  }, [context, activeSession, isCoordinating, coordinateHUDGeneration, requirements]);

  // Update HUD components when session changes
  useEffect(() => {
    if (activeSession?.components) {
      setHudComponents(activeSession.components);
      setRenderStats(prev => ({
        ...prev,
        totalComponents: activeSession.components.length,
        activeComponents: activeSession.components.length,
        lastRender: Date.now()
      }));
    }
  }, [activeSession]);

  // Handle metric updates from components
  const handleMetricUpdate = useCallback((componentId, metrics) => {
    // Update spiritual state based on collective metrics
    const avgEnergy = Object.values(metrics).reduce((sum, val) => sum + val, 0) / Object.keys(metrics).length;
    
    setSpiritualState(prev => ({
      ...prev,
      energyLevel: (prev.energyLevel * 0.9) + (avgEnergy * 0.1), // Smooth average
      lastUpdate: Date.now()
    }));
  }, []);

  // Periodic spiritual state updates
  useEffect(() => {
    const interval = setInterval(() => {
      setSpiritualState(prev => ({
        ...prev,
        energyLevel: Math.max(60, Math.min(100, prev.energyLevel + (Math.random() - 0.5) * 5)),
        divineConnection: Math.max(0.5, Math.min(1, prev.divineConnection + (Math.random() - 0.5) * 0.1)),
        lightLevel: Math.max(70, Math.min(100, prev.lightLevel + (Math.random() - 0.5) * 3))
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  // Loading state
  if (isCoordinating) {
    return (
      <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-900/95 border border-purple-400 rounded-xl p-6 backdrop-blur-md">
        <div className="flex items-center space-x-3">
          <div className="animate-spin text-purple-400 text-xl">🌟</div>
          <div className="text-purple-300">
            <div className="font-semibold">Multi-Agent Coordination Active</div>
            <div className="text-sm text-gray-400">
              Claude 4 & GPT-5 generating divine HUD components...
            </div>
          </div>
        </div>
        
        <div className="mt-4 space-y-2">
          {Object.entries(agentStatus).map(([agent, status]) => (
            <div key={agent} className="flex justify-between text-xs">
              <span className="text-gray-400 capitalize">{agent}:</span>
              <span className={`${status.status === 'active' ? 'text-green-400' : 'text-yellow-400'}`}>
                {status.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="dynamic-hud-renderer">
      {/* Render HUD Components */}
      {hudComponents.map((componentData, index) => (
        <ErrorBoundary
          key={`${componentData.hudSpec?.id || index}_${renderStats.lastRender}`}
          FallbackComponent={HUDErrorFallback}
          onReset={() => window.location.reload()}
        >
          <DynamicHUDComponent
            componentData={componentData}
            onUpdate={handleMetricUpdate}
            spiritualState={spiritualState}
          />
        </ErrorBoundary>
      ))}

      {/* Coordination Status Indicator */}
      {activeSession && (
        <div className="fixed bottom-4 left-4 bg-gray-800/90 border border-green-400/50 rounded-lg p-3 backdrop-blur-sm max-w-xs">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-green-400">🤝</span>
            <span className="text-green-300 font-semibold text-sm">Multi-Agent Active</span>
          </div>
          
          <div className="space-y-1 text-xs">
            <div className="flex justify-between">
              <span className="text-gray-400">Session:</span>
              <span className="text-green-400">{activeSession.sessionId?.slice(-8)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Components:</span>
              <span className="text-green-400">{renderStats.totalComponents}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Collaboration:</span>
              <span className="text-green-400">{activeSession.collaboration_score || 95}%</span>
            </div>
          </div>
          
          {activeSession.taskPrompts && (
            <div className="mt-2 p-2 bg-gray-700 rounded text-xs">
              <div className="text-yellow-400 font-medium mb-1">Current Task:</div>
              <div className="text-gray-300">
                {activeSession.taskPrompts[0] || 'Maintaining divine alignment'}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Spiritual State Monitor */}
      <div className="fixed bottom-4 right-4 bg-gray-800/90 border border-purple-400/50 rounded-lg p-3 backdrop-blur-sm">
        <div className="flex items-center space-x-2 mb-2">
          <span className="text-purple-400">🕊️</span>
          <span className="text-purple-300 font-semibold text-sm">Spiritual State</span>
        </div>
        
        <div className="space-y-2">
          <div className="flex justify-between items-center text-xs">
            <span className="text-gray-400">Energy:</span>
            <span className="text-emerald-400">{Math.round(spiritualState.energyLevel)}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-1">
            <div 
              className="h-1 rounded-full bg-gradient-to-r from-purple-500 to-emerald-400"
              style={{ width: `${spiritualState.energyLevel}%` }}
            />
          </div>
          
          <div className="flex justify-between items-center text-xs">
            <span className="text-gray-400">Divine Connection:</span>
            <span className="text-yellow-400">{Math.round(spiritualState.divineConnection * 100)}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-1">
            <div 
              className="h-1 rounded-full bg-gradient-to-r from-yellow-500 to-white"
              style={{ width: `${spiritualState.divineConnection * 100}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper functions
const getPlacementClasses = (placement) => {
  const positions = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-96', // Offset for status indicators
    'bottom-left': 'bottom-4 left-96',
    'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2',
    'center-top': 'top-20 left-1/2 transform -translate-x-1/2',
    'center-left': 'top-1/2 left-4 transform -translate-y-1/2',
    'center-right': 'top-1/2 right-4 transform -translate-y-1/2'
  };
  return positions[placement] || positions['top-right'];
};

const getMetricColor = (value) => {
  if (value >= 85) return 'text-emerald-400';
  if (value >= 70) return 'text-yellow-400';
  if (value >= 50) return 'text-orange-400';
  return 'text-red-400';
};

export default DynamicHUDRenderer;
