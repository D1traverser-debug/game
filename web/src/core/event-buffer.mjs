export class SimulationEventBuffer {
  constructor() { this.events = []; this.nextSequence = 0; this.lastTick = -1; }
  get count() { return this.events.length; }
  publish(tick, type, { sourceId = -1, targetId = -1, contentId = null, value = 0, x = 0, y = 0 } = {}) {
    if (!Number.isSafeInteger(tick) || tick < 0) throw new RangeError("tick must be a non-negative safe integer");
    if (tick < this.lastTick) throw new RangeError("events cannot move backwards in simulation time");
    if (typeof type !== "string" || type.length === 0) throw new TypeError("event type is required");
    for (const n of [value, x, y]) if (!Number.isFinite(n)) throw new RangeError("event numeric payload must be finite");
    const event = Object.freeze({ sequence:this.nextSequence++, tick, type, sourceId, targetId, contentId, value, x, y });
    this.events.push(event); this.lastTick = tick; return event;
  }
  drain() { const result = this.events; this.events = []; return result; }
  clear() { this.events = []; this.lastTick = -1; }
}
