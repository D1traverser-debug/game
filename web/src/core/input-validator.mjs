export const PlayerButtons = Object.freeze({ CAST_PRIMARY:1, CAST_SECONDARY:2, DODGE:4, INTERACT:8, CONFIRM:16 });
const ALLOWED_MASK = Object.values(PlayerButtons).reduce((mask, value) => mask | value, 0);
export const CommandValidationOutcome = Object.freeze({
  ACCEPTED:"accepted", UNKNOWN_PLAYER:"unknown_player", OUT_OF_ORDER:"duplicate_or_out_of_order",
  TICK_OUTSIDE_WINDOW:"tick_outside_window", INVALID_MOVEMENT:"invalid_movement", INVALID_BUTTONS:"invalid_buttons"
});
export class PlayerCommandValidator {
  constructor({ maxPastTicks = 120, maxFutureTicks = 8 } = {}) {
    if (!Number.isSafeInteger(maxPastTicks) || maxPastTicks < 0 || !Number.isSafeInteger(maxFutureTicks) || maxFutureTicks < 0) throw new RangeError("tick windows must be non-negative integers");
    this.maxPastTicks = maxPastTicks; this.maxFutureTicks = maxFutureTicks; this.lastSequence = new Map();
  }
  validate(command, activePlayerIds, hostTick) {
    if (!command || !(activePlayerIds instanceof Set) || !Number.isSafeInteger(hostTick) || hostTick < 0) throw new TypeError("command, active-player Set and valid hostTick are required");
    if (!activePlayerIds.has(command.playerId)) return CommandValidationOutcome.UNKNOWN_PLAYER;
    if (!Number.isSafeInteger(command.sequence) || command.sequence < 0) return CommandValidationOutcome.OUT_OF_ORDER;
    if (!Number.isSafeInteger(command.clientTick) || command.clientTick < 0 || command.clientTick < hostTick - this.maxPastTicks || command.clientTick > hostTick + this.maxFutureTicks) return CommandValidationOutcome.TICK_OUTSIDE_WINDOW;
    const previous = this.lastSequence.get(command.playerId);
    if (previous !== undefined && command.sequence <= previous) return CommandValidationOutcome.OUT_OF_ORDER;
    if (!Number.isFinite(command.moveX) || !Number.isFinite(command.moveY) || command.moveX*command.moveX + command.moveY*command.moveY > 1.0201) return CommandValidationOutcome.INVALID_MOVEMENT;
    if (!Number.isInteger(command.buttons) || command.buttons < 0 || (command.buttons & ~ALLOWED_MASK) !== 0) return CommandValidationOutcome.INVALID_BUTTONS;
    this.lastSequence.set(command.playerId, command.sequence);
    return CommandValidationOutcome.ACCEPTED;
  }
  resetPlayer(playerId) { this.lastSequence.delete(playerId); }
}
