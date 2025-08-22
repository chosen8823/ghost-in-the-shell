import { useState, useEffect } from 'import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import SideNav from './src/components/SideNav';
import HeaderBar from './src/components/HeaderBar';
import FooterBar from './src/components/FooterBar';
import DashboardView from './src/components/DashboardView';
import ScrollEditor from './src/components/ScrollEditor';

// API Base URL
const API_BASE = 'http://localhost:5000/api';eact'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { 
  Brain, 
  MessageSquare, 
  Workflow, 
  Wrench, 
  Sparkles, 
  Heart, 
  Code, 
  Search,
  BarChart3,
  PenTool,
  Eye,
  Calendar,
  Zap,
  Star,
  Send,
  Plus,
  Settings,
  User,
  Globe,
  Database,
  Shield,
  Infinity
} from 'lucide-react'
import './App.css'

// API base URL
const API_BASE = '/api'

// Main App Component
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/chat" element={<ChatInterface />} />
          <Route path="/agents" element={<AgentsManager />} />
          <Route path="/workflows" element={<WorkflowsManager />} />
          <Route path="/tools" element={<ToolsInterface />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  )
}

// Navigation Component
function Navigation({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'chat', label: 'Chat', icon: MessageSquare },
    { id: 'agents', label: 'Agents', icon: Brain },
    { id: 'workflows', label: 'Workflows', icon: Workflow },
    { id: 'tools', label: 'Tools', icon: Wrench }
  ]

  return (
    <nav className="bg-white/80 backdrop-blur-sm border-b border-purple-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <Infinity className="h-8 w-8 text-purple-600" />
              <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                Manus
              </span>
            </div>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              Free & Unlimited
            </Badge>
          </div>
          
            <div className="flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <Button
                  key={item.id}
                  variant={activeTab === item.id ? "default" : "ghost"}
                  size="sm"
                  onClick={() => {
                    setActiveTab(item.id)
                    window.location.href = item.id === 'dashboard' ? '/' : `/${item.id}`
                  }}
                  className="flex items-center space-x-2"
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Button>
              )
            })}
          </div>
          
          <div className="flex items-center space-x-2">
            <Button variant="ghost" size="sm">
              <Settings className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm">
              <User className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}

// Dashboard Component
function Dashboard() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [platformInfo, setPlatformInfo] = useState(null)
  const [systemStatus, setSystemStatus] = useState(null)

  useEffect(() => {
    fetchPlatformInfo()
    fetchSystemStatus()
  }, [])

  const fetchPlatformInfo = async () => {
    try {
      const response = await fetch(`${API_BASE}/platform/info`)
      const data = await response.json()
      setPlatformInfo(data)
    } catch (error) {
      console.error('Failed to fetch platform info:', error)
    }
  }

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/agents/system/status`)
      const data = await response.json()
      if (data.success) {
        setSystemStatus(data.system_status)
      }
    } catch (error) {
      console.error('Failed to fetch system status:', error)
    }
  }

  return (
    <div>
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to Manus Platform
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            Open Source AI Platform with Unlimited Capabilities
          </p>
          <div className="flex justify-center space-x-4">
            <Badge className="bg-purple-100 text-purple-800 px-4 py-2">
              <Sparkles className="h-4 w-4 mr-2" />
              Free AI Models
            </Badge>
            <Badge className="bg-blue-100 text-blue-800 px-4 py-2">
              <Infinity className="h-4 w-4 mr-2" />
              No Credit Limits
            </Badge>
            <Badge className="bg-green-100 text-green-800 px-4 py-2">
              <Heart className="h-4 w-4 mr-2" />
              Spiritual Alignment
            </Badge>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active Agents</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {systemStatus?.active_agents || 0}
                  </p>
                </div>
                <Brain className="h-8 w-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Interactions</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {systemStatus?.total_interactions || 0}
                  </p>
                </div>
                <MessageSquare className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Successful Tasks</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {systemStatus?.successful_tasks || 0}
                  </p>
                </div>
                <Zap className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Platform Health</p>
                  <p className="text-2xl font-bold text-green-600">Excellent</p>
                </div>
                <Shield className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Platform Features */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                <span>Platform Features</span>
              </CardTitle>
              <CardDescription>
                Comprehensive AI capabilities without limitations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {platformInfo?.features?.map((feature, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <Star className="h-4 w-4 text-yellow-500" />
                    <span className="text-sm">{feature}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-blue-600" />
                <span>Available Models</span>
              </CardTitle>
              <CardDescription>
                Free AI models powered by Hugging Face
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {platformInfo?.models?.map((model, index) => (
                  <Badge key={index} variant="outline" className="mr-2 mb-2">
                    {model}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>
              Get started with these common tasks
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button 
                className="h-20 flex flex-col space-y-2"
                onClick={() => window.location.href = '/chat'}
              >
                <MessageSquare className="h-6 w-6" />
                <span>Start Chatting</span>
              </Button>
              
              <Button 
                variant="outline" 
                className="h-20 flex flex-col space-y-2"
                onClick={() => window.location.href = '/agents'}
              >
                <Brain className="h-6 w-6" />
                <span>Create Agent</span>
              </Button>
              
              <Button 
                variant="outline" 
                className="h-20 flex flex-col space-y-2"
                onClick={() => window.location.href = '/tools'}
              >
                <Wrench className="h-6 w-6" />
                <span>Use Tools</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// Chat Interface Component
function ChatInterface() {
  const [activeTab, setActiveTab] = useState('chat')
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)

  useEffect(() => {
    createChatSession()
  }, [])

  const createChatSession = async () => {
    try {
      const response = await fetch(`${API_BASE}/chat/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'New Chat' })
      })
      const data = await response.json()
      if (data.success) {
        setSessionId(data.session.id)
      }
    } catch (error) {
      console.error('Failed to create chat session:', error)
    }
  }

  const sendMessage = async () => {
    if (!inputMessage.trim() || !sessionId) return

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE}/chat/sessions/${sessionId}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputMessage })
      })
      
      const data = await response.json()
      if (data.success) {
        setMessages(prev => [...prev, data.message])
      }
    } catch (error) {
      console.error('Failed to send message:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        error: true
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div>
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card className="h-[600px] flex flex-col">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <MessageSquare className="h-5 w-5" />
              <span>Chat with Manus AI</span>
            </CardTitle>
            <CardDescription>
              Powered by free AI models - no limits, no costs
            </CardDescription>
          </CardHeader>
          
          <CardContent className="flex-1 flex flex-col">
            <ScrollArea className="flex-1 mb-4 p-4 border rounded-lg">
              <div className="space-y-4">
                {messages.length === 0 && (
                  <div className="text-center text-gray-500 py-8">
                    <Brain className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>Start a conversation with Manus AI</p>
                    <p className="text-sm">Ask anything - I'm here to help!</p>
                  </div>
                )}
                
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] p-3 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      <p className="text-xs opacity-70 mt-1">
                        {new Date(message.timestamp).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 p-3 rounded-lg">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </ScrollArea>
            
            <div className="flex space-x-2">
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                disabled={isLoading}
              />
              <Button onClick={sendMessage} disabled={isLoading || !inputMessage.trim()}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// Agents Manager Component
function AgentsManager() {
  const [activeTab, setActiveTab] = useStat
(Content truncated due to size limit. Use page ranges or line ranges to read remaining content)