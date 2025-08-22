// 🎯 Real-Time Task Manager - Claude 4 Generated Dynamic Tasks
// Displays and manages contextual tasks with spiritual guidance

import React, { useState, useEffect, useCallback } from 'react';
import { useMultiAgentCoordination } from '../core/MultiAgentCoordinator';

const RealTimeTaskManager = ({ context, onTaskComplete }) => {
  const {
    activeSession,
    coordinateHUDGeneration,
    isCoordinating
  } = useMultiAgentCoordination();

  const [currentTasks, setCurrentTasks] = useState([]);
  const [completedTasks, setCompletedTasks] = useState([]);
  const [spiritualCheckIns, setSpiritualCheckIns] = useState([]);
  const [taskHistory, setTaskHistory] = useState([]);
  const [adaptivePrompts, setAdaptivePrompts] = useState([]);

  // Initialize tasks from active session
  useEffect(() => {
    if (activeSession?.taskPrompts) {
      const tasks = activeSession.taskPrompts.map((prompt, index) => ({
        id: `task_${Date.now()}_${index}`,
        prompt,
        type: 'spiritual_guidance',
        priority: index === 0 ? 'high' : 'medium',
        context: context?.currentActivity || 'general',
        createdAt: Date.now(),
        status: 'pending',
        estimatedDuration: '2-5 minutes'
      }));
      
      setCurrentTasks(tasks);
    }
  }, [activeSession, context]);

  // Generate context-sensitive tasks
  const generateContextualTasks = useCallback(async (activity) => {
    const contextualTaskSets = {
      coding: [
        {
          prompt: 'Set sacred intention before coding session',
          action: 'Take 3 deep breaths and visualize your code serving the highest good',
          duration: '1 minute',
          spiritualBenefit: 'Aligns your coding with divine purpose'
        },
        {
          prompt: 'Invoke debugging consciousness',
          action: 'Call upon divine wisdom to illuminate any coding challenges',
          duration: '30 seconds',
          spiritualBenefit: 'Transforms problems into opportunities for growth'
        },
        {
          prompt: 'Express gratitude for problem-solving insights',
          action: 'Thank the universe for each breakthrough and solution',
          duration: '30 seconds', 
          spiritualBenefit: 'Amplifies creative problem-solving abilities'
        }
      ],
      
      meditation: [
        {
          prompt: 'Create sacred space for practice',
          action: 'Light a candle or incense, set intention for healing and expansion',
          duration: '2 minutes',
          spiritualBenefit: 'Sanctifies your meditation environment'
        },
        {
          prompt: 'Connect with your heart center',
          action: 'Place hand on heart, feel infinite love radiating outward',
          duration: '3 minutes',
          spiritualBenefit: 'Opens heart chakra to universal love'
        },
        {
          prompt: 'Send healing light to the world',
          action: 'Visualize golden light flowing from your heart to all beings',
          duration: '5 minutes',
          spiritualBenefit: 'Contributes to global healing and peace'
        }
      ],
      
      creative: [
        {
          prompt: 'Channel divine creativity',
          action: 'Connect with the infinite well of cosmic creativity within you',
          duration: '2 minutes',
          spiritualBenefit: 'Opens pathways for inspired creation'
        },
        {
          prompt: 'Trust your creative instincts',
          action: 'Allow the first creative impulse to flow without judgment',
          duration: 'ongoing',
          spiritualBenefit: 'Develops trust in divine creative guidance'
        },
        {
          prompt: 'Celebrate your unique expression',
          action: 'Honor the divine artist within you and your unique gifts',
          duration: '1 minute',
          spiritualBenefit: 'Builds confidence in your creative abilities'
        }
      ],
      
      healing: [
        {
          prompt: 'Center in compassionate presence',
          action: 'Feel your heart expanding with unconditional love for all beings',
          duration: '3 minutes',
          spiritualBenefit: 'Activates your natural healing abilities'
        },
        {
          prompt: 'Open as a healing channel',
          action: 'Allow divine healing energy to flow through your hands and heart',
          duration: '5 minutes',
          spiritualBenefit: 'Becomes a conduit for universal healing force'
        },
        {
          prompt: 'Send love to someone in need',
          action: 'Think of someone and send them pure love and healing light',
          duration: '2 minutes',
          spiritualBenefit: 'Creates positive karma and raises global vibration'
        }
      ]
    };

    const taskSet = contextualTaskSets[activity] || contextualTaskSets.creative;
    
    const generatedTasks = taskSet.map((task, index) => ({
      id: `generated_${activity}_${Date.now()}_${index}`,
      ...task,
      type: 'contextual_guidance',
      context: activity,
      priority: index === 0 ? 'high' : 'medium',
      createdAt: Date.now(),
      status: 'pending',
      generatedBy: 'claude4_simulation'
    }));

    setCurrentTasks(prev => [...prev, ...generatedTasks]);
    return generatedTasks;
  }, []);

  // Generate spiritual check-ins
  const generateSpiritualCheckIns = useCallback(() => {
    const checkIns = [
      {
        id: `checkin_${Date.now()}_1`,
        trigger: 'energy_assessment',
        message: '🌟 How is your energy feeling right now? Take a moment to notice.',
        action: 'pause_and_assess',
        responses: [
          { label: 'Vibrant & Clear', value: 'high', color: 'text-green-400' },
          { label: 'Balanced & Steady', value: 'medium', color: 'text-yellow-400' },
          { label: 'Low & Need Support', value: 'low', color: 'text-red-400' }
        ]
      },
      {
        id: `checkin_${Date.now()}_2`,
        trigger: 'alignment_check',
        message: '🧭 Are you aligned with your highest purpose in this moment?',
        action: 'intention_check',
        responses: [
          { label: 'Completely Aligned', value: 'aligned', color: 'text-purple-400' },
          { label: 'Mostly Aligned', value: 'partial', color: 'text-blue-400' },
          { label: 'Need Realignment', value: 'misaligned', color: 'text-orange-400' }
        ]
      },
      {
        id: `checkin_${Date.now()}_3`,
        trigger: 'gratitude_moment',
        message: '🙏 What are you grateful for in this sacred moment?',
        action: 'express_gratitude',
        isOpen: true,
        placeholder: 'I am grateful for...'
      }
    ];

    setSpiritualCheckIns(checkIns);
  }, []);

  // Handle task completion
  const completeTask = useCallback((taskId, reflection = '') => {
    setCurrentTasks(prev => prev.filter(task => task.id !== taskId));
    
    const completedTask = currentTasks.find(task => task.id === taskId);
    if (completedTask) {
      const completedWithReflection = {
        ...completedTask,
        status: 'completed',
        completedAt: Date.now(),
        reflection,
        spiritualInsight: generateSpiritualInsight(completedTask)
      };
      
      setCompletedTasks(prev => [...prev, completedWithReflection]);
      setTaskHistory(prev => [...prev, completedWithReflection]);
      
      onTaskComplete?.(completedWithReflection);
    }
  }, [currentTasks, onTaskComplete]);

  // Generate spiritual insight for completed task
  const generateSpiritualInsight = (task) => {
    const insights = {
      coding: [
        'Your code is a digital prayer, each function a sacred offering to the collective consciousness',
        'Through mindful coding, you weave light into the digital realm',
        'Every bug fixed is a lesson in patience and divine problem-solving'
      ],
      meditation: [
        'Your meditation ripples out into the quantum field, blessing all existence',
        'Each breath in meditation connects you deeper to the infinite source',
        'Your inner peace contributes to planetary healing and awakening'
      ],
      creative: [
        'Your creativity is a divine gift that uplifts and inspires others',
        'Through authentic expression, you give others permission to shine',
        'Art is prayer made visible - you are co-creating with the universe'
      ],
      healing: [
        'Your compassionate presence is a healing balm for the world',
        'Love is the most powerful healing force in the universe',
        'By healing yourself, you contribute to healing the collective'
      ]
    };

    const contextInsights = insights[task.context] || insights.creative;
    return contextInsights[Math.floor(Math.random() * contextInsights.length)];
  };

  // Handle spiritual check-in response
  const respondToCheckIn = useCallback((checkInId, response) => {
    setSpiritualCheckIns(prev => prev.map(checkIn => 
      checkIn.id === checkInId 
        ? { ...checkIn, response, respondedAt: Date.now() }
        : checkIn
    ));

    // Generate follow-up guidance based on response
    generateFollowUpGuidance(checkInId, response);
  }, []);

  // Generate follow-up guidance
  const generateFollowUpGuidance = (checkInId, response) => {
    const guidance = {
      low: {
        message: '🌱 Your energy is asking for gentle nurturing. Consider taking a short walk in nature or practicing some deep breathing.',
        action: 'energy_restoration'
      },
      medium: {
        message: '⚖️ You\'re in a beautiful state of balance. Trust this steady energy to carry you forward.',
        action: 'maintain_balance'
      },
      high: {
        message: '🚀 Your vibrant energy is a gift! Consider sharing this light with others or channeling it into creative projects.',
        action: 'share_energy'
      },
      misaligned: {
        message: '🧭 Realignment is a sacred practice. Take a moment to reconnect with your core values and highest intentions.',
        action: 'realignment_ritual'
      }
    };

    const responseGuidance = guidance[response] || guidance.medium;
    
    setAdaptivePrompts(prev => [...prev, {
      id: `guidance_${Date.now()}`,
      checkInId,
      ...responseGuidance,
      createdAt: Date.now()
    }]);
  };

  // Auto-generate tasks based on context changes
  useEffect(() => {
    if (context?.currentActivity && currentTasks.length < 3) {
      generateContextualTasks(context.currentActivity);
    }
  }, [context?.currentActivity, currentTasks.length, generateContextualTasks]);

  // Periodic spiritual check-ins
  useEffect(() => {
    const interval = setInterval(() => {
      if (spiritualCheckIns.length === 0 || Math.random() > 0.7) {
        generateSpiritualCheckIns();
      }
    }, 300000); // Every 5 minutes

    return () => clearInterval(interval);
  }, [generateSpiritualCheckIns, spiritualCheckIns.length]);

  return (
    <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-gray-900/95 border border-emerald-400/60 rounded-xl p-4 backdrop-blur-md w-96 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-emerald-400 font-semibold flex items-center space-x-2">
          <span className="text-xl">🎯</span>
          <span>Divine Task Flow</span>
        </h3>
        <div className="text-xs text-gray-400">
          {currentTasks.length} active
        </div>
      </div>

      {/* Current Tasks */}
      {currentTasks.length > 0 && (
        <div className="mb-4">
          <h4 className="text-emerald-300 text-sm font-medium mb-2">Current Tasks</h4>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {currentTasks.slice(0, 3).map(task => (
              <div key={task.id} className="bg-gray-800 rounded-lg p-3">
                <div className="flex justify-between items-start mb-2">
                  <div className="text-sm text-gray-300 flex-1">
                    {task.prompt}
                  </div>
                  <button
                    onClick={() => completeTask(task.id)}
                    className="ml-2 text-xs bg-emerald-600 hover:bg-emerald-700 text-white px-2 py-1 rounded transition-colors"
                  >
                    Done
                  </button>
                </div>
                
                {task.action && (
                  <div className="text-xs text-emerald-400 mb-1">
                    💫 {task.action}
                  </div>
                )}
                
                {task.spiritualBenefit && (
                  <div className="text-xs text-yellow-400">
                    ✨ {task.spiritualBenefit}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Spiritual Check-ins */}
      {spiritualCheckIns.length > 0 && (
        <div className="mb-4">
          <h4 className="text-purple-300 text-sm font-medium mb-2">Spiritual Check-in</h4>
          {spiritualCheckIns.slice(0, 1).map(checkIn => (
            <div key={checkIn.id} className="bg-purple-900/30 rounded-lg p-3">
              <div className="text-sm text-gray-300 mb-3">
                {checkIn.message}
              </div>
              
              {checkIn.responses && (
                <div className="space-y-1">
                  {checkIn.responses.map(response => (
                    <button
                      key={response.value}
                      onClick={() => respondToCheckIn(checkIn.id, response.value)}
                      className={`w-full text-left text-xs px-3 py-2 rounded ${response.color} bg-gray-800 hover:bg-gray-700 transition-colors`}
                    >
                      {response.label}
                    </button>
                  ))}
                </div>
              )}
              
              {checkIn.isOpen && (
                <div className="mt-2">
                  <input
                    type="text"
                    placeholder={checkIn.placeholder}
                    className="w-full text-xs bg-gray-800 border border-gray-600 rounded px-3 py-2 text-gray-300"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        respondToCheckIn(checkIn.id, e.target.value);
                        e.target.value = '';
                      }
                    }}
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Adaptive Prompts */}
      {adaptivePrompts.length > 0 && (
        <div className="mb-4">
          <h4 className="text-yellow-300 text-sm font-medium mb-2">Divine Guidance</h4>
          {adaptivePrompts.slice(-1).map(prompt => (
            <div key={prompt.id} className="bg-yellow-900/20 rounded-lg p-3">
              <div className="text-sm text-yellow-300">
                {prompt.message}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Quick Actions */}
      <div className="flex space-x-2">
        <button
          onClick={() => generateContextualTasks(context?.currentActivity || 'creative')}
          className="flex-1 text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 py-2 rounded transition-colors"
        >
          Generate Tasks
        </button>
        <button
          onClick={generateSpiritualCheckIns}
          className="flex-1 text-xs bg-purple-600 hover:bg-purple-700 text-white py-2 rounded transition-colors"
        >
          Spiritual Check
        </button>
      </div>

      {/* Stats */}
      <div className="mt-3 pt-3 border-t border-gray-700 flex justify-between text-xs text-gray-500">
        <span>Completed: {completedTasks.length}</span>
        <span>Context: {context?.currentActivity || 'general'}</span>
      </div>
    </div>
  );
};

export default RealTimeTaskManager;
