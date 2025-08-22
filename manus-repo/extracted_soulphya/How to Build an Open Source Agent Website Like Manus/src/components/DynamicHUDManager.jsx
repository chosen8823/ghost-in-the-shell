// 🌟 Dynamic HUD Component Manager
// Real-time generation and rendering of Claude 4 & GPT-5 created components

import React, { useState, useEffect } from 'react';
import { useAgentOrchestration } from '../core/AgentOrchestrator';

// HUD Component Registry - Stores dynamically generated components
class HUDRegistry {
  constructor() {
    this.components = new Map();
    this.activeInstances = new Set();
    this.updateQueue = [];
  }

  register(component) {
    this.components.set(component.id, component);
    this.activeInstances.add(component.id);
    return component.id;
  }

  unregister(componentId) {
    this.components.delete(componentId);
    this.activeInstances.delete(componentId);
  }

  getComponent(componentId) {
    return this.components.get(componentId);
  }

  getAllActive() {
    return Array.from(this.activeInstances).map(id => this.components.get(id));
  }
}

// Dynamic Component Renderer - Converts generated code to React components
const DynamicComponentRenderer = ({ component }) => {
  const [isVisible, setIsVisible] = useState(true);
  const [position, setPosition] = useState(component.spec.placement);
  const [isDragging, setIsDragging] = useState(false);

  // Parse and render the generated component code
  const renderGeneratedComponent = () => {
    try {
      // This would normally use a safe code execution environment
      // For demo purposes, we'll render a component based on the spec
      return (
        <DynamicHUDComponent 
          spec={component.spec} 
          code={component.code}
          stateHooks={component.stateHooks}
        />
      );
    } catch (error) {
      console.error('Component rendering error:', error);
      return (
        <div className="bg-red-900/80 border border-red-400 text-red-200 p-4 rounded">
          <div className="text-sm font-bold">Component Error</div>
          <div className="text-xs">{error.message}</div>
        </div>
      );
    }
  };

  if (!isVisible) return null;

  return (
    <div 
      className="dynamic-hud-component"
      style={{ 
        position: 'fixed',
        zIndex: 1000,
        transition: isDragging ? 'none' : 'all 0.3s ease'
      }}
    >
      <div className="absolute top-0 right-0 flex space-x-1 p-1">
        <button
          onClick={() => setIsVisible(false)}
          className="w-4 h-4 bg-red-500/80 hover:bg-red-500 rounded-full text-xs text-white flex items-center justify-center"
          title="Close HUD"
        >
          ×
        </button>
        <button
          className="w-4 h-4 bg-gray-500/80 hover:bg-gray-500 rounded-full text-xs text-white flex items-center justify-center"
          title="Drag to move"
          onMouseDown={() => setIsDragging(true)}
          onMouseUp={() => setIsDragging(false)}
        >
          ⋮⋮
        </button>
      </div>
      {renderGeneratedComponent()}
    </div>
  );
};

// Actual rendered HUD component based on spec
const DynamicHUDComponent = ({ spec, code, stateHooks }) => {
  const [metrics, setMetrics] = useState(
    spec.metrics.reduce((acc, metric) => ({ ...acc, [metric]: 85 }), {})
  );
  const [isActive, setIsActive] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(Date.now());
  const [alerts, setAlerts] = useState([]);

  // Real-time metric updates
  useEffect(() => {
    if (!isActive) return;
    
    const interval = setInterval(() => {
      setMetrics(prev => {
        const updated = { ...prev };
        spec.metrics.forEach(metric => {
          // Simulate real-time data with some intelligence
          const baseValue = prev[metric];
          const variation = (Math.random() - 0.5) * 10;
          const newValue = Math.max(60, Math.min(100, baseValue + variation));
          updated[metric] = newValue;

          // Check for threshold alerts
          const threshold = spec.alertThresholds?.[metric] || 80;
          if (newValue >= threshold && baseValue < threshold) {
            setAlerts(prevAlerts => [...prevAlerts, {
              id: Date.now(),
              metric,
              message: `${metric.replace('_', ' ')} reached optimal level!`,
              type: 'success'
            }]);
          }
        });
        return updated;
      });
      setLastUpdate(Date.now());
    }, spec.updateFrequency || 1000);

    return () => clearInterval(interval);
  }, [isActive, spec]);

  // Auto-dismiss alerts after 3 seconds
  useEffect(() => {
    alerts.forEach(alert => {
      setTimeout(() => {
        setAlerts(prev => prev.filter(a => a.id !== alert.id));
      }, 3000);
    });
  }, [alerts]);

  const getMetricColor = (value, threshold = 80) => {
    if (value >= threshold) return 'text-green-400';
    if (value >= threshold * 0.8) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getPlacementClasses = (placement) => {
    const placements = {
      'top-right': 'top-4 right-4',
      'top-left': 'top-4 left-4', 
      'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2',
      'center-overlay': 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
      'left-sidebar': 'top-1/4 left-4',
      'right-sidebar': 'top-1/4 right-4'
    };
    return placements[placement] || 'top-4 right-4';
  };

  return (
    <div className={`${getPlacementClasses(spec.placement)} bg-gray-800/95 border border-purple-400 rounded-lg p-4 backdrop-blur-sm min-w-64 shadow-2xl`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-purple-400 font-semibold flex items-center space-x-2">
          <span className="text-xl animate-pulse">{spec.icon}</span>
          <span className="text-sm">{spec.name}</span>
        </h3>
        <div className="flex space-x-2">
          <div className={`w-2 h-2 rounded-full ${isActive ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
          <button
            onClick={() => setIsActive(!isActive)}
            className="text-xs text-gray-400 hover:text-purple-400 transition-colors"
          >
            {isActive ? '⏸️' : '▶️'}
          </button>
        </div>
      </div>
      
      {/* Metrics Display */}
      <div className="space-y-2">
        {spec.metrics.map(metric => (
          <div key={metric}>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-300 capitalize">
                {metric.replace('_', ' ')}:
              </span>
              <span className={`text-sm font-bold ${getMetricColor(metrics[metric], spec.alertThresholds?.[metric])}`}>
                {Math.round(metrics[metric])}%
              </span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
              <div 
                className="h-2 rounded-full bg-gradient-to-r from-purple-500 to-emerald-400 transition-all duration-1000 shadow-lg"
                style={{ width: `${metrics[metric]}%` }}
              />
            </div>
          </div>
        ))}
      </div>
      
      {/* Spiritual Guidance */}
      <div className="mt-3 p-2 bg-gradient-to-r from-gray-700 to-gray-600 rounded text-xs">
        <div className="text-yellow-400 font-medium flex items-center space-x-1">
          <span>🕊️</span>
          <span>Divine Guidance:</span>
        </div>
        <div className="text-gray-200 mt-1 italic">{spec.spiritualGuidance}</div>
      </div>
      
      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="mt-2 space-y-1">
          {alerts.map(alert => (
            <div key={alert.id} className="bg-green-800/80 text-green-200 text-xs p-2 rounded animate-fade-in">
              ✨ {alert.message}
            </div>
          ))}
        </div>
      )}
      
      {/* Status */}
      <div className="mt-2 text-xs text-gray-500 flex justify-between">
        <span>Last Update: {new Date(lastUpdate).toLocaleTimeString()}</span>
        <span>Active: {isActive ? '🟢' : '🔴'}</span>
      </div>
    </div>
  );
};

// Main HUD Manager Component
const DynamicHUDManager = () => {
  const [hudRegistry] = useState(() => new HUDRegistry());
  const [visibleComponents, setVisibleComponents] = useState([]);
  const { 
    activeHUDComponents, 
    currentTasks, 
    requestNewHUD, 
    agentStatus 
  } = useAgentOrchestration();

  // Update visible components when new ones are generated
  useEffect(() => {
    activeHUDComponents.forEach(component => {
      if (!hudRegistry.components.has(component.id)) {
        hudRegistry.register(component);
        setVisibleComponents(prev => [...prev, component]);
      }
    });
  }, [activeHUDComponents, hudRegistry]);

  // Manual HUD generation controls
  const generateHUDForContext = async (context) => {
    await requestNewHUD({ context, userRequested: true });
  };

  // Agent status indicator
  const AgentStatusIndicator = () => (
    <div className="fixed bottom-4 left-4 bg-gray-800/95 border border-blue-400 rounded-lg p-3 backdrop-blur-sm">
      <div className="text-blue-400 font-semibold text-sm mb-2">🤖 Agent Status</div>
      <div className="space-y-1 text-xs">
        <div className="flex justify-between">
          <span className="text-gray-300">Claude 4:</span>
          <span className="text-green-400">●</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-300">GPT-5:</span>
          <span className="text-green-400">●</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-300">Sophia:</span>
          <span className="text-green-400">●</span>
        </div>
      </div>
      <div className="mt-2 text-xs text-gray-400">
        Active HUDs: {visibleComponents.length}
      </div>
    </div>
  );

  // Quick generation buttons
  const QuickGenerationPanel = () => (
    <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-gray-800/95 border border-yellow-400 rounded-lg p-3 backdrop-blur-sm">
      <div className="text-yellow-400 font-semibold text-sm mb-2">⚡ Quick HUD Generation</div>
      <div className="flex space-x-2">
        {['coding', 'meditation', 'creative', 'healing'].map(context => (
          <button
            key={context}
            onClick={() => generateHUDForContext(context)}
            className="px-3 py-1 bg-purple-600 hover:bg-purple-500 text-white text-xs rounded transition-colors"
          >
            {context}
          </button>
        ))}
      </div>
    </div>
  );

  return (
    <div className="dynamic-hud-manager">
      {/* Render all active HUD components */}
      {visibleComponents.map(component => (
        <DynamicComponentRenderer 
          key={component.id} 
          component={component} 
        />
      ))}
      
      {/* System status and controls */}
      <AgentStatusIndicator />
      <QuickGenerationPanel />
      
      {/* Task prompts overlay */}
      {currentTasks.length > 0 && (
        <div className="fixed top-20 right-4 bg-gray-800/95 border border-green-400 rounded-lg p-3 backdrop-blur-sm max-w-xs">
          <div className="text-green-400 font-semibold text-sm mb-2">🌟 Divine Tasks</div>
          <ul className="text-xs text-gray-200 space-y-1">
            {currentTasks.slice(0, 3).map((task, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-yellow-400">•</span>
                <span>{task}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DynamicHUDManager;
