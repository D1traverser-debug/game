namespace Game.Core.Determinism
{
    /// <summary>
    /// PCG-XSH-RR 32-bit generator. Keep this stream inside simulation only;
    /// render, audio, UI and camera effects must use separate non-gameplay randomness.
    /// </summary>
    public sealed class DeterministicRng
    {
        private ulong _state;
        private readonly ulong _increment;

        public DeterministicRng(ulong seed, ulong sequence = 54UL)
        {
            _state = 0UL;
            _increment = (sequence << 1) | 1UL;
            NextUInt();
            _state += seed;
            NextUInt();
        }

        public uint NextUInt()
        {
            var oldState = _state;
            _state = unchecked(oldState * 6364136223846793005UL + _increment);
            var xorShifted = (uint)(((oldState >> 18) ^ oldState) >> 27);
            var rotation = (int)(oldState >> 59);
            return (xorShifted >> rotation) | (xorShifted << ((-rotation) & 31));
        }

        public float NextFloat01()
        {
            return (NextUInt() >> 8) * (1.0f / 16777216.0f);
        }

        public int NextInt(int minInclusive, int maxExclusive)
        {
            if (maxExclusive <= minInclusive) throw new System.ArgumentOutOfRangeException(nameof(maxExclusive));
            var range = (uint)(maxExclusive - minInclusive);
            var threshold = unchecked((uint)(0U - range)) % range;
            uint value;
            do { value = NextUInt(); } while (value < threshold);
            return minInclusive + (int)(value % range);
        }
    }
}
