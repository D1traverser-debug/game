const MASK_64 = (1n << 64n) - 1n;
const UINT32_RANGE = 1n << 32n;

// PCG-XSH-RR 32-bit stream. Keep gameplay RNG out of rendering, UI and audio.
export class SeededRng {
  constructor(seed, sequence = 54n) {
    if (!(typeof seed === "bigint" || Number.isSafeInteger(seed))) throw new TypeError("seed must be a bigint or safe integer");
    if (!(typeof sequence === "bigint" || Number.isSafeInteger(sequence))) throw new TypeError("sequence must be a bigint or safe integer");
    this.state = 0n;
    this.increment = ((BigInt(sequence) << 1n) | 1n) & MASK_64;
    this.nextUint32();
    this.state = (this.state + BigInt(seed)) & MASK_64;
    this.nextUint32();
  }
  nextUint32() {
    const oldState = this.state;
    this.state = (oldState * 6364136223846793005n + this.increment) & MASK_64;
    const shifted = Number(BigInt.asUintN(32, ((oldState >> 18n) ^ oldState) >> 27n));
    const rotation = Number(oldState >> 59n);
    return ((shifted >>> rotation) | (shifted << ((-rotation) & 31))) >>> 0;
  }
  nextFloat01() { return (this.nextUint32() >>> 8) / 16777216; }
  nextInt(minInclusive, maxExclusive) {
    if (!Number.isSafeInteger(minInclusive) || !Number.isSafeInteger(maxExclusive) || maxExclusive <= minInclusive) {
      throw new RangeError("integer range must be non-empty and safe");
    }
    const span = BigInt(maxExclusive - minInclusive);
    if (span > UINT32_RANGE) throw new RangeError("range cannot exceed 2^32");
    const threshold = (UINT32_RANGE - span) % span;
    let value;
    do { value = BigInt(this.nextUint32()); } while (value < threshold);
    return minInclusive + Number(value % span);
  }
}
