export class FixedStepClock {
  constructor({ stepSeconds = 1 / 60, maxStepsPerAdvance = 8, epsilon = 1e-10 } = {}) {
    if (!Number.isFinite(stepSeconds) || stepSeconds <= 0) throw new RangeError("stepSeconds must be finite and positive");
    if (!Number.isInteger(maxStepsPerAdvance) || maxStepsPerAdvance <= 0) throw new RangeError("maxStepsPerAdvance must be a positive integer");
    this.stepSeconds = stepSeconds;
    this.maxStepsPerAdvance = maxStepsPerAdvance;
    this.epsilon = epsilon;
    this.tick = 0;
    this.accumulator = 0;
  }
  get pendingSeconds() { return this.accumulator; }
  get interpolationAlpha() { return Math.min(1, this.accumulator / this.stepSeconds); }
  advance(elapsedSeconds, { paused = false, simulateTick } = {}) {
    if (typeof simulateTick !== "function") throw new TypeError("simulateTick callback is required");
    if (!Number.isFinite(elapsedSeconds) || elapsedSeconds < 0) throw new RangeError("elapsedSeconds must be finite and non-negative");
    // Paused wall time is discarded. Existing fractional simulation debt is preserved.
    if (paused) return 0;
    this.accumulator += elapsedSeconds;
    let steps = 0;
    while (this.accumulator + this.epsilon >= this.stepSeconds && steps < this.maxStepsPerAdvance) {
      simulateTick(this.tick, this.stepSeconds);
      this.tick += 1;
      this.accumulator -= this.stepSeconds;
      if (this.accumulator < 0 && this.accumulator > -this.epsilon) this.accumulator = 0;
      steps += 1;
    }
    return steps;
  }
}
