namespace Game.Core.Events
{
    public enum SimulationEventType
    {
        SpellCast = 0,
        ProjectileSpawned = 1,
        DamageResolved = 2,
        StatusApplied = 3,
        CombatantDied = 4,
        CombatantRevived = 5,
        ObjectiveProgressed = 6,
        BossPhaseChanged = 7
    }

    /// <summary>
    /// Immutable domain event. Presentation/audio/network adapters observe these events;
    /// they must not mutate simulation state in response.
    /// </summary>
    public readonly struct SimulationEvent
    {
        public SimulationEvent(long sequence, long tick, SimulationEventType type, int sourceId,
            int targetId, string? contentId, float value, float x, float y)
        {
            Sequence = sequence;
            Tick = tick;
            Type = type;
            SourceId = sourceId;
            TargetId = targetId;
            ContentId = contentId ?? string.Empty;
            Value = value;
            X = x;
            Y = y;
        }

        public long Sequence { get; }
        public long Tick { get; }
        public SimulationEventType Type { get; }
        public int SourceId { get; }
        public int TargetId { get; }
        public string ContentId { get; }
        public float Value { get; }
        public float X { get; }
        public float Y { get; }
    }
}
