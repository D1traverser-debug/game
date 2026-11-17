using System;
using System.Collections.Generic;

namespace Game.Core.Events
{
    /// <summary>
    /// Single-threaded deterministic event buffer owned by the simulation tick.
    /// Events are sequenced in publish order and may not travel backwards in simulation time.
    /// </summary>
    public sealed class SimulationEventBuffer
    {
        private readonly List<SimulationEvent> _events = new List<SimulationEvent>();
        private long _nextSequence;
        private long _lastTick = -1;

        public int Count => _events.Count;
        public long NextSequence => _nextSequence;

        public SimulationEvent Publish(long tick, SimulationEventType type, int sourceId = -1,
            int targetId = -1, string? contentId = null, float value = 0.0f, float x = 0.0f, float y = 0.0f)
        {
            if (tick < 0) throw new ArgumentOutOfRangeException(nameof(tick));
            if (tick < _lastTick) throw new InvalidOperationException("Simulation events cannot move backwards in tick time.");
            if (!IsFinite(value) || !IsFinite(x) || !IsFinite(y))
                throw new ArgumentOutOfRangeException(nameof(value), "Event numeric payload must be finite.");

            var item = new SimulationEvent(_nextSequence++, tick, type, sourceId, targetId, contentId, value, x, y);
            _events.Add(item);
            _lastTick = tick;
            return item;
        }

        public SimulationEvent[] Drain()
        {
            if (_events.Count == 0) return Array.Empty<SimulationEvent>();
            var result = _events.ToArray();
            _events.Clear();
            return result;
        }

        public void Clear()
        {
            _events.Clear();
            _lastTick = -1;
        }

        private static bool IsFinite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
    }
}
