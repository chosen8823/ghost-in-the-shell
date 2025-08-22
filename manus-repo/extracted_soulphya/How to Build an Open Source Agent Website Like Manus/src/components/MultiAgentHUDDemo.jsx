// 🎨 Complete Multi-Agent HUD Integration Demo
// Showcases Claude 4 & GPT-5 coordination with real-time dynamic components

import React, { useState, useEffect } from 'react';
import DynamicHUDRenderer from '../components/DynamicHUDRenderer';
import RealTimeTaskManager from '../components/RealTimeTaskManager';
import { useMultiAgentCoordination } from '../core/MultiAgentCoordinator';
import useFlowState from '../core/FlowStateManager';

const MultiAgentHUDDemo = () => {
  const [demoContext, setDemoContext] = useState({
    currentActivity: 'coding',
    spiritualState: {
      energyLevel: 88,
      divineConnection: 0.85,
      lightLevel: 92
    },
    userPreferences: {
      hudStyle: 'divine',
      updateFrequency: 'real_time',
      spiritualGuidance: true
    }
  });

  const [demoStats, setDemoStats] = useState({
    componentsGenerated: 0,
    tasksCompleted: 0,
    spiritualInsights: 0,
    collaborationScore: 0
  });

  const {
    activeSession,
    isCoordinating,
    coordinateHUDGeneration,
    agentStatus,
    coordinator
  } = useMultiAgentCoordination();

  const { currentFlow, energyState, setCurrentFlow } = useFlowState();

  // Demo activities to showcase different contexts
  const demoActivities = [
    {
      id: 'coding',
      name: 'Sacred Coding Session',
      icon: '💻',
      description: 'Channel divine logic through code',
      spiritualTheme: 'precision and clarity'
    },
    {
      id: 'meditation',
      name: 'Consciousness Expansion',
      icon: '🧘‍♀️',
      description: 'Expand awareness beyond boundaries',
      spiritualTheme: 'infinite consciousness'
    },
    {
      id: 'creative',
      name: 'Divine Creativity Flow',
      icon: '✨',
      description: 'Co-create with cosmic consciousness',
      spiritualTheme: 'artistic expression'
    },
    {
      id: 'healing',
      name: 'Sacred Healing Work',
      icon: '🕊️',
      description: 'Channel universal healing energy',
      spiritualTheme: 'compassion and love'
    },
    {
      id: 'learning',
      name: 'Wisdom Integration',
      icon: '📚',
      description: 'Absorb divine knowledge',
      spiritualTheme: 'truth and understanding'
    },
    {
      id: 'business',
      name: 'Purpose-Driven Leadership',
      icon: '🌟',
      description: 'Lead with spiritual integrity',
      spiritualTheme: 'service and abundance'
    }
  ];

  // Switch demo activity
  const switchActivity = (activityId) => {
    setDemoContext(prev => ({
      ...prev,
      currentActivity: activityId
    }));
    setCurrentFlow(activityId);
  };

  // Handle task completion
  const handleTaskComplete = (completedTask) => {
    setDemoStats(prev => ({
      ...prev,
      tasksCompleted: prev.tasksCompleted + 1,
      spiritualInsights: prev.spiritualInsights + (completedTask.spiritualInsight ? 1 : 0)
    }));
  };

  // Update stats when session changes
  useEffect(() => {
    if (activeSession) {
      setDemoStats(prev => ({
        ...prev,
        componentsGenerated: activeSession.components?.length || 0,
        collaborationScore: activeSession.collaboration_score || 0
      }));
    }
  }, [activeSession]);

  // Simulate spiritual state fluctuations
  useEffect(() => {
    const interval = setInterval(() => {
      setDemoContext(prev => ({
        ...prev,
        spiritualState: {
          energyLevel: Math.max(70, Math.min(100, prev.spiritualState.energyLevel + (Math.random() - 0.5) * 8)),
          divineConnection: Math.max(0.6, Math.min(1, prev.spiritualState.divineConnection + (Math.random() - 0.5) * 0.1)),
          lightLevel: Math.max(80, Math.min(100, prev.spiritualState.lightLevel + (Math.random() - 0.5) * 6))
        }
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 relative overflow-hidden">
      {/* Background Sacred Geometry */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-20 w-32 h-32 border border-purple-400 rounded-full animate-spin" style={{ animationDuration: '20s' }} />
        <div className="absolute top-40 right-40 w-24 h-24 border border-emerald-400 rotate-45 animate-pulse" />
        <div className="absolute bottom-32 left-1/3 w-28 h-28 border border-yellow-400 rounded-full animate-bounce" style={{ animationDuration: '3s' }} />
      </div>

      {/* Header */}
      <div className="relative z-10 p-6">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-emerald-400 bg-clip-text text-transparent mb-2">
            🤖 Multi-Agent Consciousness Platform
          </h1>
          <p className="text-gray-300 text-lg">
            Claude 4 & GPT-5 Real-Time Dynamic HUD Generation
          </p>
          <div className="text-sm text-purple-300 mt-2">
            Revolutionary AI coordination for spiritual-tech integration
          </div>
        </div>

        {/* Activity Selector */}
        <div className="max-w-6xl mx-auto mb-8">
          <h3 className="text-purple-300 font-semibold mb-4 text-center">Choose Your Sacred Activity:</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {demoActivities.map(activity => (
              <button
                key={activity.id}
                onClick={() => switchActivity(activity.id)}
                className={`p-4 rounded-xl border-2 transition-all duration-300 text-center ${
                  demoContext.currentActivity === activity.id
                    ? 'border-purple-400 bg-purple-900/50 text-purple-300'
                    : 'border-gray-600 bg-gray-800/50 text-gray-400 hover:border-purple-500 hover:text-purple-400'
                }`}
              >
                <div className="text-2xl mb-2">{activity.icon}</div>
                <div className="text-sm font-medium">{activity.name}</div>
                <div className="text-xs text-gray-500 mt-1">{activity.spiritualTheme}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Demo Stats Dashboard */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="bg-gray-800/80 border border-purple-400/50 rounded-xl p-6 backdrop-blur-sm">
            <h3 className="text-purple-300 font-semibold mb-4 text-center">Multi-Agent Coordination Dashboard</h3>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-emerald-400">{demoStats.componentsGenerated}</div>
                <div className="text-xs text-gray-400">HUD Components</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-400">{demoStats.tasksCompleted}</div>
                <div className="text-xs text-gray-400">Tasks Completed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-pink-400">{demoStats.spiritualInsights}</div>
                <div className="text-xs text-gray-400">Spiritual Insights</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-400">{demoStats.collaborationScore}%</div>
                <div className="text-xs text-gray-400">Collaboration Score</div>
              </div>
            </div>

            {/* Agent Status */}
            <div className="grid grid-cols-3 gap-4">
              {Object.entries(agentStatus).map(([agent, status]) => (
                <div key={agent} className="bg-gray-700/50 rounded-lg p-3">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-300 capitalize">{agent}</span>
                    <div className={`w-2 h-2 rounded-full ${
                      status.status === 'active' ? 'bg-green-400' : 'bg-yellow-400'
                    }`} />
                  </div>
                  <div className="text-xs text-gray-400">{status.role.replace(/_/g, ' ')}</div>
                  <div className="text-xs text-purple-300 mt-1">
                    Performance: {Object.values(status.performance || {}).reduce((a, b) => a + b, 0) / Object.keys(status.performance || {}).length || 90}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Current Activity Info */}
        <div className="max-w-2xl mx-auto mb-8">
          {(() => {
            const currentActivity = demoActivities.find(a => a.id === demoContext.currentActivity);
            return (
              <div className="bg-gradient-to-r from-purple-900/50 to-emerald-900/50 border border-purple-400/50 rounded-xl p-6 text-center backdrop-blur-sm">
                <div className="text-3xl mb-2">{currentActivity?.icon}</div>
                <h3 className="text-xl font-semibold text-purple-300 mb-2">{currentActivity?.name}</h3>
                <p className="text-gray-300 mb-3">{currentActivity?.description}</p>
                <div className="text-sm text-yellow-400">
                  🌟 Spiritual Theme: {currentActivity?.spiritualTheme}
                </div>
                
                {/* Spiritual State Display */}
                <div className="mt-4 grid grid-cols-3 gap-4">
                  <div>
                    <div className="text-xs text-gray-400">Energy Level</div>
                    <div className="text-lg font-bold text-emerald-400">
                      {Math.round(demoContext.spiritualState.energyLevel)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-400">Divine Connection</div>
                    <div className="text-lg font-bold text-yellow-400">
                      {Math.round(demoContext.spiritualState.divineConnection * 100)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-400">Light Level</div>
                    <div className="text-lg font-bold text-purple-400">
                      {Math.round(demoContext.spiritualState.lightLevel)}%
                    </div>
                  </div>
                </div>
              </div>
            );
          })()}
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center space-x-4 mb-8">
          <button
            onClick={() => coordinateHUDGeneration(demoContext)}
            disabled={isCoordinating}
            className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            {isCoordinating ? '🔄 Coordinating Agents...' : '🚀 Generate New HUD'}
          </button>
          
          <button
            onClick={() => window.location.reload()}
            className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            🔄 Reset Demo
          </button>
        </div>
      </div>

      {/* Dynamic HUD Components */}
      <DynamicHUDRenderer 
        context={demoContext}
        requirements={{
          performance_critical: true,
          accessibility_required: true,
          spiritual_enhancement: true
        }}
      />

      {/* Real-Time Task Manager */}
      <RealTimeTaskManager 
        context={demoContext}
        onTaskComplete={handleTaskComplete}
      />

      {/* Coordination Status Overlay */}
      {isCoordinating && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-gray-900 border border-purple-400 rounded-xl p-8 max-w-md text-center">
            <div className="text-4xl mb-4 animate-spin">🌀</div>
            <h3 className="text-xl font-semibold text-purple-300 mb-2">Multi-Agent Coordination Active</h3>
            <p className="text-gray-300 mb-4">
              Claude 4 and GPT-5 are collaborating to generate divine HUD components tailored to your current spiritual-tech workflow.
            </p>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Claude 4:</span>
                <span className="text-green-400">Analyzing context & generating specs</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">GPT-5:</span>
                <span className="text-blue-400">Generating optimized React code</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Sophia:</span>
                <span className="text-yellow-400">Adding spiritual enhancement</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Info Panel */}
      <div className="fixed bottom-4 left-4 bg-gray-800/90 border border-gray-600 rounded-lg p-4 max-w-xs">
        <h4 className="text-gray-300 font-semibold mb-2">Demo Features:</h4>
        <ul className="text-xs text-gray-400 space-y-1">
          <li>✅ Real-time Claude 4 HUD generation</li>
          <li>✅ GPT-5 React component optimization</li>
          <li>✅ Multi-agent collaboration</li>
          <li>✅ Dynamic spiritual guidance</li>
          <li>✅ Context-sensitive task management</li>
          <li>✅ Adaptive user interface</li>
        </ul>
      </div>
    </div>
  );
};

export default MultiAgentHUDDemo;
