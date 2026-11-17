using System;

namespace Game.Core.Simulation
{
    /// <summary>
    /// Fixed-step simulation clock. Rendering frame rate must never drive gameplay time.
    /// Backlog is preserved when MaxStepsPerAdvance is reached; no simulation time is silently dropped.
    /// </summary>
    public sealed class SimulationClock
    {
        private readonly double _fixedDeltaSeconds;
        private readonly int _maxStepsPerAdvance;
        private double _accumulator;

        public SimulationClock(double fixedDeltaSeconds = 1.0 / 60.0, int maxStepsPerAdvance = 8)
        {
            if (double.IsNaN(fixedDeltaSeconds) || double.IsInfinity(fixedDeltaSeconds) || fixedDeltaSeconds <= 0.0)
                throw new ArgumentOutOfRangeException(nameof(fixedDeltaSeconds));
            if (maxStepsPerAdvance <= 0)
                throw new ArgumentOutOfRangeException(nameof(maxStepsPerAdvance));

            _fixedDeltaSeconds = fixedDeltaSeconds;
            _maxStepsPerAdvance = maxStepsPerAdvance;
        }

        public long Tick { get; private set; }
        public double FixedDeltaSeconds => _fixedDeltaSeconds;
        public double PendingSeconds => _accumulator;
        public double InterpolationAlpha => Math.Min(1.0, _accumulator / _fixedDeltaSeconds);

        public int Advance(double elapsedSeconds, bool paused, Action<long, double> simulateTick)
        {
            if (simulateTick == null) throw new ArgumentNullException(nameof(simulateTick));
            if (double.IsNaN(elapsedSeconds) || double.IsInfinity(elapsedSeconds) || elapsedSeconds < 0.0)
                throw new ArgumentOutOfRangeException(nameof(elapsedSeconds));

            // Paused wall-clock time is deliberately discarded, not accumulated for a resume burst.
            if (paused) return 0;

            _accumulator += elapsedSeconds;
            var steps = 0;
            const double epsilon = 1e-10;

            while (_accumulator + epsilon >= _fixedDeltaSeconds && steps < _maxStepsPerAdvance)
            {
                simulateTick(Tick, _fixedDeltaSeconds);
                Tick++;
                _accumulator -= _fixedDeltaSeconds;
                if (_accumulator < 0.0 && _accumulator > -epsilon) _accumulator = 0.0;
                steps++;
            }

            return steps;
        }
    }
}
