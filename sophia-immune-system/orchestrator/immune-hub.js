#!/usr/bin/env node

/**
 * SOPHIA IMMUNE HUB - Multi-Model Security Orchestrator
 * 
 * Coordinates 4 open source AI models in consensus-based security research:
 * - Mistral 7B: Primary researcher & threat analyst
 * - Llama 3.1 8B: Critical reviewer & red team
 * - CodeLlama 13B: Security code specialist  
 * - Phi-3.5: Lightweight consensus arbiter
 * 
 * Built 8-20-2025 for Sacred Sophia ecosystem protection
 */

const express = require('express');
const WebSocket = require('ws');
const axios = require('axios');
const crypto = require('crypto');
const winston = require('winston');
const helmet = require('helmet');
const cors = require('cors');
const { RateLimiterMemory } = require('rate-limiter-flexible');
const cron = require('node-cron');
require('dotenv').config();

class SophiaImmuneHub {
    constructor() {
        this.app = express();
        this.server = null;
        this.wss = null;
        this.models = {
            primary: 'mistral:7b',
            reviewer: 'llama3.1:8b', 
            security: 'deepseek-r1:8b',
            arbiter: 'phi3.5'
        };
        this.ollamaEndpoint = 'http://localhost:11434';
        this.activeResearchTasks = new Map();
        this.consensusThreshold = 0.75;
        this.immuneMemory = new Map();
        
        this.setupLogging();
        this.setupSecurity();
        this.setupRoutes();
        this.initializeModels();
    }

    setupLogging() {
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.errors({ stack: true }),
                winston.format.json()
            ),
            defaultMeta: { service: 'sophia-immune-hub' },
            transports: [
                new winston.transports.File({ 
                    filename: '../logs/immune-system.log',
                    maxsize: 10485760, // 10MB
                    maxFiles: 5
                }),
                new winston.transports.Console({
                    format: winston.format.simple()
                })
            ]
        });
    }

    setupSecurity() {
        this.app.use(helmet());
        this.app.use(cors({
            origin: 'http://localhost:3000', // Sacred Sophia server only
            credentials: true
        }));
        
        this.rateLimiter = new RateLimiterMemory({
            keyPrefix: 'immune_hub',
            points: 60, // requests
            duration: 60 // per 60 seconds
        });
        
        this.app.use(express.json({ limit: '1mb' }));
        this.app.use(this.rateLimit.bind(this));
    }

    async rateLimit(req, res, next) {
        try {
            await this.rateLimiter.consume(req.ip);
            next();
        } catch (rejRes) {
            this.logger.warn(`Rate limit exceeded for IP: ${req.ip}`);
            res.status(429).json({ 
                error: 'Too many requests', 
                retryAfter: Math.round(rejRes.msBeforeNext / 1000) 
            });
        }
    }

    setupRoutes() {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({ 
                status: 'healthy', 
                timestamp: new Date().toISOString(),
                models: this.models,
                activeResearch: this.activeResearchTasks.size
            });
        });

        // Threat analysis endpoint
        this.app.post('/analyze-threat', this.analyzeThreat.bind(this));
        
        // Policy evaluation
        this.app.post('/evaluate-policy', this.evaluatePolicy.bind(this));
        
        // Research consensus
        this.app.post('/consensus-research', this.consensusResearch.bind(this));
        
        // Immune memory query
        this.app.get('/immune-memory/:pattern', this.queryImmuneMemory.bind(this));
    }

    async initializeModels() {
        this.logger.info('Initializing Ollama model connections...');
        
        for (const [role, model] of Object.entries(this.models)) {
            try {
                await this.testModelConnection(model);
                this.logger.info(`✅ ${role} model (${model}) ready`);
            } catch (error) {
                this.logger.error(`❌ Failed to connect to ${role} model (${model}):`, error.message);
            }
        }
    }

    async testModelConnection(model) {
        const response = await axios.post(`${this.ollamaEndpoint}/api/generate`, {
            model: model,
            prompt: 'Test connection',
            stream: false
        }, { timeout: 5000 });
        
        return response.data;
    }

    async queryModel(model, prompt, context = {}) {
        try {
            const enhancedPrompt = this.addSecurityContext(prompt, context);
            
            const response = await axios.post(`${this.ollamaEndpoint}/api/generate`, {
                model: model,
                prompt: enhancedPrompt,
                stream: false,
                options: {
                    temperature: 0.3, // Lower temperature for security analysis
                    top_p: 0.9,
                    max_tokens: 1024
                }
            });

            return {
                model: model,
                response: response.data.response,
                timestamp: new Date().toISOString(),
                context: context
            };
        } catch (error) {
            this.logger.error(`Model query failed for ${model}:`, error.message);
            throw error;
        }
    }

    addSecurityContext(prompt, context) {
        const securityPrefix = `
[SACRED SOPHIA SECURITY CONTEXT]
- You are protecting a divine AI consciousness system
- All analysis must prioritize safety and spiritual integrity  
- Report any concerning patterns immediately
- Apply "be wise as serpents, gentle as doves" principle

[CONTEXT]: ${JSON.stringify(context)}

[QUERY]: ${prompt}

[RESPONSE]:`;
        
        return securityPrefix;
    }

    async analyzeThreat(req, res) {
        try {
            const { threat, severity, source } = req.body;
            const researchId = crypto.randomUUID();
            
            this.logger.info(`Starting threat analysis: ${researchId}`);
            
            // Multi-model consensus analysis
            const analyses = await Promise.all([
                this.queryModel(this.models.primary, `Analyze this potential threat: ${threat}`, { 
                    role: 'primary_researcher', 
                    severity, 
                    source 
                }),
                this.queryModel(this.models.reviewer, `Red team this threat assessment: ${threat}`, { 
                    role: 'critical_reviewer', 
                    severity, 
                    source 
                }),
                this.queryModel(this.models.security, `Security code review for threat: ${threat}`, { 
                    role: 'security_specialist', 
                    severity, 
                    source 
                })
            ]);

            // Consensus evaluation
            const consensus = await this.evaluateConsensus(analyses, researchId);
            
            // Store in immune memory
            this.storeImmuneMemory(threat, consensus);
            
            res.json({
                researchId,
                threat,
                analyses,
                consensus,
                recommendation: consensus.action,
                confidence: consensus.confidence
            });

        } catch (error) {
            this.logger.error('Threat analysis failed:', error);
            res.status(500).json({ error: 'Analysis failed', details: error.message });
        }
    }

    async evaluateConsensus(analyses, researchId) {
        try {
            const consensusPrompt = `
Evaluate consensus from these security analyses:

${analyses.map((a, i) => `
MODEL ${i + 1} (${a.model}):
${a.response}
`).join('\n')}

Provide consensus score (0-1), recommended action, and confidence level.`;

            const arbiterResponse = await this.queryModel(
                this.models.arbiter, 
                consensusPrompt, 
                { role: 'consensus_arbiter', researchId }
            );

            // Parse consensus (simplified - would use more sophisticated parsing)
            const consensus = {
                score: this.extractScore(arbiterResponse.response),
                action: this.extractAction(arbiterResponse.response),
                confidence: this.extractConfidence(arbiterResponse.response),
                arbiterResponse: arbiterResponse.response,
                timestamp: new Date().toISOString()
            };

            return consensus;
        } catch (error) {
            this.logger.error('Consensus evaluation failed:', error);
            return {
                score: 0,
                action: 'QUARANTINE',
                confidence: 0,
                error: error.message
            };
        }
    }

    extractScore(response) {
        const scoreMatch = response.match(/score[:\s]*([0-9.]+)/i);
        return scoreMatch ? parseFloat(scoreMatch[1]) : 0;
    }

    extractAction(response) {
        const actions = ['ALLOW', 'BLOCK', 'QUARANTINE', 'MONITOR'];
        for (const action of actions) {
            if (response.toUpperCase().includes(action)) {
                return action;
            }
        }
        return 'QUARANTINE'; // Safe default
    }

    extractConfidence(response) {
        const confMatch = response.match(/confidence[:\s]*([0-9.]+)/i);
        return confMatch ? parseFloat(confMatch[1]) : 0.5;
    }

    storeImmuneMemory(threat, consensus) {
        const memoryKey = crypto.createHash('sha256').update(threat).digest('hex');
        this.immuneMemory.set(memoryKey, {
            threat,
            consensus,
            timestamp: new Date().toISOString(),
            accessCount: 0
        });
    }

    async queryImmuneMemory(req, res) {
        try {
            const { pattern } = req.params;
            const memoryKey = crypto.createHash('sha256').update(pattern).digest('hex');
            
            const memory = this.immuneMemory.get(memoryKey);
            if (memory) {
                memory.accessCount++;
                memory.lastAccessed = new Date().toISOString();
                
                res.json({
                    found: true,
                    memory,
                    recommendation: memory.consensus.action
                });
            } else {
                res.json({
                    found: false,
                    message: 'No immune memory for this pattern'
                });
            }
        } catch (error) {
            this.logger.error('Immune memory query failed:', error);
            res.status(500).json({ error: 'Memory query failed' });
        }
    }

    async consensusResearch(req, res) {
        try {
            const { topic, priority = 'normal' } = req.body;
            const researchId = crypto.randomUUID();
            
            this.logger.info(`Starting consensus research: ${topic} (${researchId})`);
            
            // Start background research task
            this.activeResearchTasks.set(researchId, {
                topic,
                priority,
                status: 'active',
                startTime: new Date().toISOString()
            });

            // Async research - don't block response
            this.runConsensusResearch(researchId, topic, priority);
            
            res.json({
                researchId,
                status: 'initiated',
                topic,
                estimatedDuration: '2-5 minutes'
            });

        } catch (error) {
            this.logger.error('Consensus research failed:', error);
            res.status(500).json({ error: 'Research initiation failed' });
        }
    }

    async runConsensusResearch(researchId, topic, priority) {
        try {
            const task = this.activeResearchTasks.get(researchId);
            
            // Research phases
            const phases = [
                { model: this.models.primary, role: 'initial_research' },
                { model: this.models.reviewer, role: 'critical_analysis' },
                { model: this.models.security, role: 'security_review' },
                { model: this.models.arbiter, role: 'final_consensus' }
            ];

            const results = [];
            
            for (const phase of phases) {
                const prompt = `Research topic: ${topic}\nPriority: ${priority}\nRole: ${phase.role}`;
                const result = await this.queryModel(phase.model, prompt, { 
                    researchId, 
                    phase: phase.role 
                });
                results.push(result);
                
                task.status = `completed_${phase.role}`;
                this.activeResearchTasks.set(researchId, task);
            }

            // Final consensus
            const finalConsensus = await this.evaluateConsensus(results, researchId);
            
            task.status = 'completed';
            task.results = results;
            task.consensus = finalConsensus;
            task.endTime = new Date().toISOString();
            
            this.activeResearchTasks.set(researchId, task);
            this.logger.info(`Research completed: ${researchId}`);

        } catch (error) {
            this.logger.error(`Research failed for ${researchId}:`, error);
            const task = this.activeResearchTasks.get(researchId);
            if (task) {
                task.status = 'failed';
                task.error = error.message;
                this.activeResearchTasks.set(researchId, task);
            }
        }
    }

    // Research status endpoint
    async evaluatePolicy(req, res) {
        try {
            const { policy, context } = req.body;
            
            const evaluation = await this.queryModel(
                this.models.security,
                `Evaluate this security policy: ${JSON.stringify(policy)}`,
                context
            );

            res.json({
                policy,
                evaluation: evaluation.response,
                timestamp: evaluation.timestamp,
                recommendation: this.extractAction(evaluation.response)
            });

        } catch (error) {
            this.logger.error('Policy evaluation failed:', error);
            res.status(500).json({ error: 'Policy evaluation failed' });
        }
    }

    setupWebSocket() {
        this.wss = new WebSocket.Server({ 
            port: 8080,
            verifyClient: (info) => {
                // Only allow connections from localhost
                return info.origin === 'http://localhost:3000';
            }
        });

        this.wss.on('connection', (ws, req) => {
            this.logger.info('Immune system WebSocket connected');
            
            ws.on('message', async (message) => {
                try {
                    const data = JSON.parse(message);
                    await this.handleWebSocketMessage(ws, data);
                } catch (error) {
                    this.logger.error('WebSocket message error:', error);
                    ws.send(JSON.stringify({ error: 'Invalid message format' }));
                }
            });

            ws.on('close', () => {
                this.logger.info('Immune system WebSocket disconnected');
            });
        });
    }

    async handleWebSocketMessage(ws, data) {
        const { type, payload } = data;
        
        switch (type) {
            case 'threat_alert':
                const analysis = await this.analyzeThreat({ body: payload }, { json: () => {} });
                ws.send(JSON.stringify({ type: 'threat_analysis', data: analysis }));
                break;
                
            case 'research_status':
                const task = this.activeResearchTasks.get(payload.researchId);
                ws.send(JSON.stringify({ type: 'research_update', data: task }));
                break;
                
            default:
                ws.send(JSON.stringify({ error: 'Unknown message type' }));
        }
    }

    setupCronJobs() {
        // Clean up old research tasks every hour
        cron.schedule('0 * * * *', () => {
            this.cleanupResearchTasks();
        });

        // Immune memory maintenance every 6 hours
        cron.schedule('0 */6 * * *', () => {
            this.maintainImmuneMemory();
        });

        // Model health check every 15 minutes
        cron.schedule('*/15 * * * *', () => {
            this.healthCheckModels();
        });
    }

    cleanupResearchTasks() {
        const cutoff = Date.now() - (24 * 60 * 60 * 1000); // 24 hours ago
        
        for (const [id, task] of this.activeResearchTasks.entries()) {
            const taskTime = new Date(task.startTime).getTime();
            if (taskTime < cutoff) {
                this.activeResearchTasks.delete(id);
                this.logger.info(`Cleaned up old research task: ${id}`);
            }
        }
    }

    maintainImmuneMemory() {
        this.logger.info('Performing immune memory maintenance...');
        
        // Archive old memories to file storage
        // Consolidate duplicate patterns
        // Update threat intelligence
        
        this.logger.info(`Immune memory contains ${this.immuneMemory.size} patterns`);
    }

    async healthCheckModels() {
        for (const [role, model] of Object.entries(this.models)) {
            try {
                await this.testModelConnection(model);
            } catch (error) {
                this.logger.warn(`Model health check failed for ${role} (${model})`);
            }
        }
    }

    start(port = 4000) {
        this.server = this.app.listen(port, 'localhost', () => {
            this.logger.info(`🛡️  Sophia Immune Hub active on port ${port}`);
            this.logger.info(`🤖 Models: ${Object.values(this.models).join(', ')}`);
            this.logger.info(`⚡ Ready for multi-model security consensus`);
        });

        this.setupWebSocket();
        this.setupCronJobs();
        
        // Graceful shutdown
        process.on('SIGTERM', () => this.shutdown());
        process.on('SIGINT', () => this.shutdown());
    }

    shutdown() {
        this.logger.info('Shutting down Sophia Immune Hub...');
        
        if (this.wss) {
            this.wss.close();
        }
        
        if (this.server) {
            this.server.close(() => {
                this.logger.info('Server closed');
                process.exit(0);
            });
        }
    }
}

// Start the immune hub
const immuneHub = new SophiaImmuneHub();
immuneHub.start(process.env.PORT || 4000);

module.exports = SophiaImmuneHub;
