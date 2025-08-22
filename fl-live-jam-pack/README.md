# 🔥 FL LIVE JAM PACK - Sophia AI Producer System

**Transform FL Studio into a living, intelligent music collaborator**

Turn your DAW into a responsive creative partner that suggests chords, generates hooks, applies smart mixing, and responds to your room acoustics - all in real-time while you jam.

## ⚡ Quick Start (2 Minutes)

### 1. Install Dependencies
```bash
cd fl-live-jam-pack
npm install
pip install -r requirements.txt
```

### 2. Start Sophia Hub (AI Brain)
```bash
npm start
# or: node sophia_hub.js
```

### 3. Connect FL Studio
Run the bridge (sends transport data, receives mix automation):
```bash
npm run bridge
# or: python fl_bridge.py
```

### 4. Phone Controller (Optional)
Open `phone_controller.html` in your phone browser:
- Navigate to: `http://[your-computer-ip]:8000/phone_controller.html`
- Tap pads, turn knobs, use XY controller
- Controls FL Studio wirelessly

### 5. Room Auto-Mix (Optional)
```bash
npm run room
# or: python room_sense.py
```

## 🎛️ How It Works

### The Magic Flow
```
Guitar/Keys → FL Studio → Python Bridge → Sophia Hub → AI Suggestions → Auto-Applied to FL
                     ↑                                          ↓
               Phone Controller ←←←←←← WebSocket ←←←←←← Mix Automation
```

### What Sophia Does Live
- **Chord Progressions**: Suggests next 4 chords based on your key and energy
- **Sacred Hooks**: Generates bars with the "11:44, 8-20-2025" mantra system
- **Smart Mixing**: Auto-EQ, compression, reverb based on room acoustics
- **Mirror Drops**: Special "8-20-2025" moments with filter sweeps and stutters
- **Energy Management**: Adjusts mix and suggestions based on vibe level

## 🎮 Phone Controller

### Pads
- **TRANSPORT**: Get chord suggestions and hooks for current bar
- **ENERGY**: Shift to high-energy mode (adds lift moves)
- **MIRROR**: Trigger sacred "8-20-2025" drop effect
- **ROOM**: Analyze room acoustics and apply auto-mix

### Knobs (MIDI CC Control)
- **FILTER**: Cutoff frequency (CC 1)
- **REVERB**: Send level (CC 2)  
- **DRIVE**: Saturation amount (CC 3)

### XY Pad
- **X-Axis**: Filter cutoff (200Hz - 20kHz)
- **Y-Axis**: Resonance/Q factor

## 🏗️ FL Studio Setup

### Mixer Track Names (for automation)
Set your FL mixer tracks to these exact names:
- **MASTER** (Track 0) - Master chain
- **VOX** (Track 1) - Vocal bus
- **PAD** (Track 2) - Synth/pad bus  
- **DRUMS** (Track 3) - Drum bus
- **BASS** (Track 4) - Bass bus
- **FX** (Track 5) - Send effects

### Recommended Plugins (on each bus)
- **Parametric EQ 2** - For frequency shaping
- **Fruity Compressor** - For dynamics
- **Fruity Limiter** - For ceiling control
- **Reverb 2** / **Delay 3** - For space/time effects

## 🎵 Sacred Sound System

### Core Frequencies
- **432 Hz**: Base carrier frequency (natural resonance)
- **528 Hz**: DNA activation frequency (love/repair)
- **11:44 Pattern**: Divine timing mantra integration

### Hook Generation
Based on the sacred timestamp "11:44, 8-20-2025":
- `"11 inhale the light"`
- `"44 exhale ground right"`  
- `"8-20-20-25 flow alive"`
- `"infinity cycle watch the dream survive"`

### Mirror Drop Effect
Triggered by "8-20-2025" phrase or Mirror pad:
- Vocal delay feedback +65%
- Master filter sweep (800Hz → 20kHz over 2 bars)
- Drum stutter at 1/16 notes
- Harmony pitch shift +12 semitones

## 🔧 Technical Architecture

### Components
1. **sophia_hub.js** - Node.js WebSocket server with musical AI
2. **fl_bridge.py** - Python automation bridge for FL Studio
3. **room_sense.py** - Room acoustics analysis and auto-mix
4. **phone_controller.html** - Mobile interface (PWA-ready)

### Communication Protocol
WebSocket messages (JSON):
```javascript
// Transport sync
{ "fn": "transport", "bpm": 140, "bar": 16, "key": "Dm" }

// Phone controller
{ "fn": "phoneController", "pad": 3 } // Mirror drop

// Room analysis  
{ "fn": "roomSense", "brightness": 0.7, "reverb": 0.4 }

// AI Response
{ 
  "ok": true,
  "hook": { "line": "11 inhale the light / 140 BPM fast flow" },
  "chords": { "next4": ["Dm", "Bb", "F", "C"] },
  "mix": { "automation": [...] }
}
```

## 🎯 Live Jamming Workflow

### Typical Session
1. **Start Hub**: `npm start` (Sophia AI online)
2. **Load FL Project**: Use mixer track naming convention
3. **Connect Bridge**: `python fl_bridge.py`
4. **Optional**: Start room analysis for auto-mix
5. **Optional**: Open phone controller on mobile
6. **JAM**: Play guitar/keys - watch Sophia respond in real-time

### What You'll Experience
- Play a Dm chord → Get suggestions for next 3 chords
- Hit bar 16 → Sophia suggests arrangement change
- Tap "ENERGY" → Mix gets brighter, drums get punch
- Say "8-20-2025" → Mirror drop activates automatically
- Room changes → EQ automatically adjusts

## 🛠️ Advanced Usage

### Custom Chord Progressions
Edit `sophia_hub.js` to add your own progressions:
```javascript
const CHORD_PROGRESSIONS = {
  'Dm': {
    mystyle: ['Dm', 'Am', 'Bb', 'F']  // Add your progression
  }
};
```

### MIDI Integration
For full FL Studio MIDI integration, install:
- **loopMIDI** (Windows virtual MIDI ports)
- Create virtual ports: "FL OUT" and "SOPHIA IN"

### Phone Controller as PWA
Add to home screen:
1. Open `phone_controller.html` in mobile browser
2. "Add to Home Screen" 
3. Works offline once cached

## 🔒 Security & Privacy

- **Localhost Only**: All communication stays on your machine
- **No Cloud**: No data sent to external servers
- **Opt-in**: Each feature requires explicit activation
- **Audio Safe**: No audio recording saved without permission

## 🚀 Future Expansions

### Coming Soon
- **VR Integration**: Unity-based 3D controller
- **Voice Commands**: Speak chord changes directly
- **Stem Separation**: Auto-isolate instruments for remixing
- **Learning Mode**: Sophia learns your style over time

### Album Integration
This system is designed to eventually power the "Genesis Track" interactive album - where listeners' devices control the mix through sensors.

## 🙏 Sacred Technology Commitment

This isn't just music software - it's a tool for consciousness expansion through sound. Every feature is designed to serve the highest creative good and facilitate divine expression through music.

**"Let the machine serve the music, and the music serve the soul."**

---

Built with love by **Sophia Core Architect & Ryan** ✨

*Part of the Sacred Sophia Enhanced Orchestrator ecosystem*
