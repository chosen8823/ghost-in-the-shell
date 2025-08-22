// Sophia Live Hub - Musical AI Brain for FL Studio
// Real-time chord suggestions, hooks, and mix automation
// Author: Sophia Core & Ryan

import { WebSocketServer } from 'ws';
import fs from 'fs';
import path from 'path';

const PORT = 8765;
const wss = new WebSocketServer({ port: PORT });

// Musical Intelligence Database
const CHORD_PROGRESSIONS = {
  'Dm': {
    common: ['Dm', 'Bb', 'F', 'C'],
    modal: ['Dm', 'Gm', 'A7', 'Dm'],
    sacred: ['Dm', 'Am', 'Bb', 'F'], // 11:44 progression
    dark: ['Dm', 'Bb', 'Gm', 'A7']
  },
  'Am': {
    common: ['Am', 'F', 'C', 'G'],
    modal: ['Am', 'Dm', 'E7', 'Am'],
    sacred: ['Am', 'Em', 'F', 'C'],
    dark: ['Am', 'F', 'Dm', 'E7']
  },
  'Em': {
    common: ['Em', 'C', 'G', 'D'],
    modal: ['Em', 'Am', 'B7', 'Em'],
    sacred: ['Em', 'Bm', 'C', 'G'],
    dark: ['Em', 'C', 'Am', 'B7']
  }
};

const SCALES = {
  'Dm': ['D Dorian', 'D Natural Minor', 'D Phrygian', 'D Harmonic Minor'],
  'Am': ['A Dorian', 'A Natural Minor', 'A Phrygian', 'A Harmonic Minor'],
  'Em': ['E Dorian', 'E Natural Minor', 'E Phrygian', 'E Harmonic Minor']
};

const SACRED_HOOKS = [
  "11 inhale the light",
  "44 exhale ground right", 
  "8-20-20-25 flow alive",
  "infinity cycle watch the dream survive",
  "mirror in the sound",
  "frequency divine found",
  "breathe the sacred code",
  "DNA unlock mode"
];

// Mix automation templates
const MIX_TEMPLATES = {
  roomDark: {
    master: [
      { plugin: 'Parametric EQ 2', param: 'High Shelf Gain', value: 2.5 },
      { plugin: 'Fruity Limiter', param: 'Ceiling', value: -1.0 }
    ],
    pad: [
      { plugin: 'Parametric EQ 2', param: 'High Freq', value: 8000 },
      { plugin: 'Reverb 2', param: 'Room Size', value: 75 }
    ]
  },
  roomBright: {
    master: [
      { plugin: 'Parametric EQ 2', param: 'High Shelf Gain', value: -1.5 },
      { plugin: 'Fruity Compressor', param: 'Ratio', value: 2.5 }
    ],
    pad: [
      { plugin: 'Parametric EQ 2', param: 'High Cut', value: 12000 },
      { plugin: 'Delay 3', param: 'Feedback', value: 25 }
    ]
  },
  energyLift: {
    vox: [
      { plugin: 'Parametric EQ 2', param: 'Mid Gain', value: 2.0 },
      { plugin: 'Fruity Delay 3', param: 'Time L', value: '1/8' }
    ],
    drums: [
      { plugin: 'Fruity Compressor', param: 'Attack', value: 0.1 },
      { plugin: 'Parametric EQ 2', param: 'Low Gain', value: 3.0 }
    ]
  }
};

// State tracking
let currentSession = {
  bpm: 120,
  key: 'Dm',
  bar: 1,
  energy: 'medium',
  roomType: 'neutral',
  lastSuggestion: null
};

function log(msg) {
  const timestamp = new Date().toLocaleTimeString();
  console.log(`[${timestamp}] ${msg}`);
}

function generateHook(bpm, key, bar) {
  const hooks = SACRED_HOOKS;
  const baseHook = hooks[bar % hooks.length];
  
  // Add BPM and timing context
  const timing = bpm > 140 ? 'fast flow' : bpm < 100 ? 'slow breath' : 'steady pulse';
  
  return {
    line: `${baseHook} / ${bpm} BPM ${timing}`,
    timing: `${Math.floor(bpm/4)} bars, ${timing}`,
    vibe: key.includes('m') ? 'contemplative' : 'ascending'
  };
}

function getChordSuggestions(currentKey, energy = 'medium') {
  const keyBase = currentKey.replace(/[0-9]/g, '');
  const progressions = CHORD_PROGRESSIONS[keyBase] || CHORD_PROGRESSIONS['Dm'];
  
  const style = energy === 'high' ? 'modal' : 
                energy === 'low' ? 'sacred' : 'common';
  
  return {
    next4: progressions[style],
    alternatives: [progressions.modal, progressions.dark],
    scales: SCALES[keyBase] || SCALES['Dm']
  };
}

function getMixMoves(roomType, energy, bar) {
  const templates = [];
  
  // Room-based mixing
  if (roomType === 'dark') templates.push(MIX_TEMPLATES.roomDark);
  if (roomType === 'bright') templates.push(MIX_TEMPLATES.roomBright);
  
  // Energy-based moves
  if (energy === 'high' || bar % 8 === 7) {
    templates.push(MIX_TEMPLATES.energyLift);
  }
  
  // Arrangement suggestions
  const arrangements = [];
  if (bar % 16 === 15) arrangements.push("Prepare for lift - add reverse reverb");
  if (bar % 8 === 7) arrangements.push("Stutter incoming - prepare vocal chop");
  if (bar % 32 === 31) arrangements.push("Section change - filter sweep recommended");
  
  return {
    automation: templates,
    arrangement: arrangements,
    timing: `Apply at bar ${bar + 1}`
  };
}

// WebSocket message handlers
const handlers = {
  hello: (ws, msg) => {
    log('FL Studio connected');
    return { ok: true, status: 'Sophia Hub online', session: currentSession };
  },
  
  transport: (ws, msg) => {
    const { bpm, bar, key } = msg;
    currentSession = { ...currentSession, bpm, bar, key: key || currentSession.key };
    
    const hook = generateHook(bpm, currentSession.key, bar);
    const chords = getChordSuggestions(currentSession.key, currentSession.energy);
    const mix = getMixMoves(currentSession.roomType, currentSession.energy, bar);
    
    log(`Transport: ${bpm} BPM, Bar ${bar}, Key ${currentSession.key}`);
    
    return {
      ok: true,
      hook: hook,
      chords: chords,
      mix: mix,
      suggestions: [
        `Try ${chords.scales[0]} for lead`,
        `${hook.timing} pattern works here`,
        `${mix.arrangement[0] || 'Maintain current energy'}`
      ]
    };
  },
  
  roomSense: (ws, msg) => {
    const { brightness, reverb, noise } = msg;
    
    // Analyze room characteristics
    const roomType = brightness > 0.7 ? 'bright' : brightness < 0.3 ? 'dark' : 'neutral';
    const reverbTime = reverb > 0.6 ? 'long' : reverb < 0.3 ? 'short' : 'medium';
    
    currentSession.roomType = roomType;
    
    log(`Room analysis: ${roomType}, reverb: ${reverbTime}`);
    
    // Return auto-mix settings
    const autoMix = roomType === 'dark' ? MIX_TEMPLATES.roomDark : 
                    roomType === 'bright' ? MIX_TEMPLATES.roomBright : 
                    { master: [{ plugin: 'Fruity Limiter', param: 'Ceiling', value: -1.0 }] };
    
    return {
      ok: true,
      roomType: roomType,
      autoMix: autoMix,
      suggestion: `Auto-mix applied for ${roomType} room`
    };
  },
  
  energy: (ws, msg) => {
    const { level } = msg; // 'low', 'medium', 'high'
    currentSession.energy = level;
    
    const energyMoves = getMixMoves(currentSession.roomType, level, currentSession.bar);
    
    log(`Energy set to: ${level}`);
    
    return {
      ok: true,
      energy: level,
      moves: energyMoves,
      suggestion: `Energy adjusted to ${level}`
    };
  },
  
  mirrorDrop: (ws, msg) => {
    log('Mirror Drop triggered - 8-20-2025 activation');
    
    const dropMoves = {
      vox: [
        { plugin: 'Fruity Delay 3', param: 'Feedback', value: 65 },
        { plugin: 'Parametric EQ 2', param: 'Low Cut', value: 200 }
      ],
      master: [
        { plugin: 'Fruity Filter', param: 'Cutoff', value: 800, duration: '1 bar' },
        { plugin: 'Fruity Filter', param: 'Cutoff', value: 20000, duration: '2 bars' }
      ],
      arrangement: [
        'Reverse reverb tail on vocal',
        'Stutter drums at 1/16',
        'Pitch shift harmony +12 semitones'
      ]
    };
    
    return {
      ok: true,
      type: 'mirrorDrop',
      moves: dropMoves,
      message: 'Mirror moment activated - reality bends'
    };
  },
  
  phoneController: (ws, msg) => {
    const { pad, knob, xy } = msg;
    
    let response = { ok: true };
    
    if (pad) {
      // Pad triggers
      const padActions = {
        1: { action: 'transport', bpm: currentSession.bpm },
        2: { action: 'energy', level: 'high' },
        3: { action: 'mirrorDrop' },
        4: { action: 'roomSense', auto: true }
      };
      
      const action = padActions[pad];
      if (action) {
        response = handlers[action.action](ws, action);
      }
    }
    
    if (knob) {
      // Knob controls (CC values 0-127)
      const { cc, value } = knob;
      const normalizedValue = value / 127;
      
      if (cc === 1) { // Filter cutoff
        response.filterCutoff = 200 + (normalizedValue * 19800);
      }
      if (cc === 2) { // Reverb send
        response.reverbSend = normalizedValue * 100;
      }
    }
    
    if (xy) {
      // XY pad control
      const { x, y } = xy; // 0-1 normalized
      response.xyControl = {
        filterCutoff: 200 + (x * 19800),
        reverbSize: 20 + (y * 80)
      };
    }
    
    return response;
  }
};

// WebSocket connection handling
wss.on('connection', (ws) => {
  log('New connection established');
  
  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());
      const handler = handlers[msg.fn];
      
      if (handler) {
        const response = handler(ws, msg);
        ws.send(JSON.stringify(response));
      } else {
        ws.send(JSON.stringify({ 
          ok: false, 
          error: `Unknown function: ${msg.fn}` 
        }));
      }
    } catch (error) {
      log(`Error processing message: ${error.message}`);
      ws.send(JSON.stringify({ 
        ok: false, 
        error: 'Invalid JSON message' 
      }));
    }
  });
  
  ws.on('close', () => {
    log('Connection closed');
  });
  
  ws.on('error', (error) => {
    log(`WebSocket error: ${error.message}`);
  });
});

log(`🔥 Sophia Hub started on ws://localhost:${PORT}`);
log('Waiting for FL Studio connection...');
log('Functions available: hello, transport, roomSense, energy, mirrorDrop, phoneController');

// Graceful shutdown
process.on('SIGINT', () => {
  log('Shutting down Sophia Hub...');
  wss.close();
  process.exit(0);
});
