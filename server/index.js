/**
 * Sophiella Orchestrator - Main Server
 * Webhook processor and n8n integration hub
 */
const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (req, res) => {
    res.json({ 
        status: 'alive', 
        service: 'sophiella-orchestrator',
        timestamp: new Date().toISOString()
    });
});

// Webhook endpoint for n8n workflows
app.post('/webhook/:workflowId', async (req, res) => {
    try {
        const { workflowId } = req.params;
        const payload = req.body;
        
        console.log(`📥 Webhook received for workflow: ${workflowId}`);
        console.log('Payload:', JSON.stringify(payload, null, 2));
        
        // Forward to device interface if needed
        if (payload.action === 'system_control') {
            const response = await axios.post('http://127.0.0.1:5001/open_app', {
                name: payload.app
            });
            
            return res.json({
                success: true,
                workflow: workflowId,
                system_response: response.data
            });
        }
        
        // Default response
        res.json({
            success: true,
            workflow: workflowId,
            received: payload,
            timestamp: new Date().toISOString()
        });
        
    } catch (error) {
        console.error('❌ Webhook error:', error.message);
        res.status(500).json({
            error: 'Webhook processing failed',
            message: error.message
        });
    }
});

// Agent interaction endpoint
app.post('/agent/:agentType', async (req, res) => {
    try {
        const { agentType } = req.params;
        const { message, context } = req.body;
        
        console.log(`🤖 Agent request: ${agentType}`);
        
        // Route to appropriate agent
        switch (agentType) {
            case 'claude':
                // Placeholder for Claude integration
                res.json({
                    agent: 'claude',
                    response: 'Claude integration coming in Stage 4',
                    input: message
                });
                break;
                
            case 'openai':
                // Placeholder for OpenAI integration
                res.json({
                    agent: 'openai',
                    response: 'OpenAI integration coming in Stage 4',
                    input: message
                });
                break;
                
            case 'agent-s':
                // Placeholder for Agent-S integration
                res.json({
                    agent: 'agent-s',
                    response: 'Agent-S integration coming in Stage 4',
                    input: message
                });
                break;
                
            default:
                res.status(400).json({
                    error: 'Unknown agent type',
                    available: ['claude', 'openai', 'agent-s']
                });
        }
        
    } catch (error) {
        console.error('❌ Agent error:', error.message);
        res.status(500).json({
            error: 'Agent processing failed',
            message: error.message
        });
    }
});

// Cloud Function trigger endpoint
app.post('/trigger/cloud-function', async (req, res) => {
    try {
        const { functionName, data } = req.body;
        
        console.log(`☁️ Cloud function trigger: ${functionName}`);
        
        // Placeholder for Google Cloud Function integration
        res.json({
            success: true,
            function: functionName,
            data: data,
            status: 'Cloud function integration coming soon',
            timestamp: new Date().toISOString()
        });
        
    } catch (error) {
        console.error('❌ Cloud function error:', error.message);
        res.status(500).json({
            error: 'Cloud function trigger failed',
            message: error.message
        });
    }
});

// Voice interface endpoint
app.post('/voice/process', async (req, res) => {
    try {
        const { audioData, command } = req.body;
        
        console.log('🎤 Voice command received');
        
        // Forward to device interface
        if (command) {
            const response = await axios.post('http://127.0.0.1:5001/voice_command', {
                command: command
            });
            
            return res.json({
                success: true,
                voice_response: response.data
            });
        }
        
        res.json({
            success: true,
            message: 'Voice processing placeholder - Stage 3 implementation pending'
        });
        
    } catch (error) {
        console.error('❌ Voice processing error:', error.message);
        res.status(500).json({
            error: 'Voice processing failed',
            message: error.message
        });
    }
});

// Start server
app.listen(PORT, () => {
    console.log('🕊️ Sophiella Orchestrator Server Starting...');
    console.log(`🌐 Server running on http://localhost:${PORT}`);
    console.log('✨ Ready for webhook processing and agent orchestration');
});

module.exports = app;
