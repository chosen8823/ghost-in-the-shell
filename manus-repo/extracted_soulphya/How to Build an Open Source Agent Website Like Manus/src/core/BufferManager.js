// 🧊 BufferManager - Controls spatial/temporal spawning of dynamic tools & HUD modules
// Prevents UI overwhelm by enforcing buffer occupancy, priorities, and decay rules

export const BUFFER_TYPES = {
  PRIMARY: 'primary',        // Core persistent HUD (max 3)
  SECONDARY: 'secondary',    // Contextual helpers (max 4)
  OVERLAY: 'overlay',        // Modal / walkthrough / simulation (1 active)
  EPHEMERAL: 'ephemeral',    // Flash guidance / micro prompts (stack size 3)
  BACKGROUND: 'background'   // Silent tasks / async generators (unlimited tracked)
};

const DEFAULT_LIMITS = {
  [BUFFER_TYPES.PRIMARY]: 3,
  [BUFFER_TYPES.SECONDARY]: 4,
  [BUFFER_TYPES.OVERLAY]: 1,
  [BUFFER_TYPES.EPHEMERAL]: 3,
  [BUFFER_TYPES.BACKGROUND]: Infinity
};

const DECAY_MS = {
  [BUFFER_TYPES.EPHEMERAL]: 25_000,   // Auto remove after 25s if not pinned
  [BUFFER_TYPES.SECONDARY]: 10 * 60_000, // 10m
  [BUFFER_TYPES.OVERLAY]: 15 * 60_000 // Force close after 15m idle
};

export class BufferManager {
  constructor(limits = {}) {
    this.limits = { ...DEFAULT_LIMITS, ...limits };
    this.buffers = new Map(); // bufferType -> array of entries
    Object.values(BUFFER_TYPES).forEach(t => this.buffers.set(t, []));
    this.listeners = new Set();
    this.metrics = { spawns: 0, rejects: 0, evictions: 0 };
  }

  onChange(cb) { this.listeners.add(cb); return () => this.listeners.delete(cb); }
  emit() { this.listeners.forEach(cb => cb(this.snapshot())); }

  snapshot() {
    const obj = {};
    for (const [k,v] of this.buffers.entries()) obj[k] = v.map(e => ({ id: e.id, kind: e.kind, createdAt: e.createdAt, pinned: e.pinned }));
    return { buffers: obj, metrics: { ...this.metrics } };
  }

  canSpawn(type) {
    const arr = this.buffers.get(type) || [];
    return arr.length < this.limits[type];
  }

  spawn({ id, type, kind, payload, priority = 50, ttl, pinned = false, meta = {} }) {
    if (!BUFFER_TYPES[type.toUpperCase()]) {
      console.warn('Unknown buffer type', type); // attempt fallback
    }
    const t = type;
    if (!this.canSpawn(t)) {
      // Try eviction of lowest priority if priority high
      const arr = this.buffers.get(t);
      const weakest = arr.reduce((acc, e) => (e.priority < acc.priority ? e : acc), arr[0]);
      if (weakest && weakest.priority < priority) {
        this.evict(weakest.id, t, 'priority_replacement');
      } else {
        this.metrics.rejects++;
        return { accepted: false, reason: 'capacity', type: t };
      }
    }
    const entry = {
      id: id || `${t}_${Date.now()}_${Math.random().toString(36).slice(2,7)}`,
      type: t,
      kind,
      payload,
      priority,
      createdAt: Date.now(),
      pinned,
      ttl: ttl || DECAY_MS[t] || null,
      meta
    };
    this.buffers.get(t).push(entry);
    this.metrics.spawns++;
    this.emit();
    return { accepted: true, entry };
  }

  touch(id) {
    for (const arr of this.buffers.values()) {
      const e = arr.find(x => x.id === id);
      if (e) { e.lastTouched = Date.now(); this.emit(); return true; }
    }
    return false;
  }

  evict(id, type, reason = 'manual') {
    const arr = this.buffers.get(type);
    const idx = arr.findIndex(e => e.id === id);
    if (idx !== -1) {
      arr.splice(idx,1);
      this.metrics.evictions++;
      this.emit();
      return { removed: true, reason };
    }
    return { removed: false };
  }

  prune() {
    const now = Date.now();
    let removed = 0;
    for (const [type, arr] of this.buffers.entries()) {
      for (let i = arr.length -1; i >=0; i--) {
        const e = arr[i];
        if (e.pinned) continue;
        if (e.ttl && now - e.createdAt > e.ttl) {
          arr.splice(i,1); removed++; this.metrics.evictions++; 
        }
      }
    }
    if (removed) this.emit();
    return removed;
  }

  promote(id, targetType) {
    for (const [type, arr] of this.buffers.entries()) {
      const idx = arr.findIndex(e => e.id === id);
      if (idx !== -1) {
        const [e] = arr.splice(idx,1);
        e.type = targetType;
        return this.spawn(e);
      }
    }
    return { accepted: false, reason: 'not_found' };
  }
}

// Reactive singleton pattern (optional)
let _globalBufferManager;
export const getBufferManager = () => {
  if (!_globalBufferManager) _globalBufferManager = new BufferManager();
  return _globalBufferManager;
};

export default BufferManager;
