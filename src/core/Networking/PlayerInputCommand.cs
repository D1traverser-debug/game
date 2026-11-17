using System;

namespace Game.Core.Networking
{
    [Flags]
    public enum PlayerButtons : ushort
    {
        None = 0,
        CastPrimary = 1 << 0,
        CastSecondary = 1 << 1,
        Dodge = 1 << 2,
        Interact = 1 << 3,
        Confirm = 1 << 4
    }

    public readonly struct PlayerInputCommand
    {
        public PlayerInputCommand(int playerId, long sequence, long clientTick,
            float moveX, float moveY, PlayerButtons buttons)
        {
            PlayerId = playerId;
            Sequence = sequence;
            ClientTick = clientTick;
            MoveX = moveX;
            MoveY = moveY;
            Buttons = buttons;
        }

        public int PlayerId { get; }
        public long Sequence { get; }
        public long ClientTick { get; }
        public float MoveX { get; }
        public float MoveY { get; }
        public PlayerButtons Buttons { get; }
    }

    public enum CommandValidationOutcome
    {
        Accepted = 0,
        UnknownPlayer = 1,
        DuplicateOrOutOfOrder = 2,
        TickOutsideWindow = 3,
        InvalidMovement = 4,
        InvalidButtons = 5
    }

    public readonly struct CommandValidationResult
    {
        public CommandValidationResult(CommandValidationOutcome outcome) { Outcome = outcome; }
        public CommandValidationOutcome Outcome { get; }
        public bool Accepted => Outcome == CommandValidationOutcome.Accepted;
    }

    /// <summary>
    /// Host-side input envelope validator. It validates identity, sequence, tick window,
    /// movement bounds and button flags. It does not trust client-authored world state.
    /// </summary>
    public sealed class PlayerCommandValidator
    {
        private readonly System.Collections.Generic.Dictionary<int, long> _lastSequence =
            new System.Collections.Generic.Dictionary<int, long>();
        private readonly long _maxPastTicks;
        private readonly long _maxFutureTicks;

        public PlayerCommandValidator(long maxPastTicks = 120, long maxFutureTicks = 8)
        {
            if (maxPastTicks < 0) throw new ArgumentOutOfRangeException(nameof(maxPastTicks));
            if (maxFutureTicks < 0) throw new ArgumentOutOfRangeException(nameof(maxFutureTicks));
            _maxPastTicks = maxPastTicks;
            _maxFutureTicks = maxFutureTicks;
        }

        public CommandValidationResult Validate(PlayerInputCommand command,
            System.Collections.Generic.ISet<int> activePlayerIds, long hostTick)
        {
            if (activePlayerIds == null) throw new ArgumentNullException(nameof(activePlayerIds));
            if (hostTick < 0) throw new ArgumentOutOfRangeException(nameof(hostTick));

            if (!activePlayerIds.Contains(command.PlayerId))
                return new CommandValidationResult(CommandValidationOutcome.UnknownPlayer);
            if (_lastSequence.TryGetValue(command.PlayerId, out var last) && command.Sequence <= last)
                return new CommandValidationResult(CommandValidationOutcome.DuplicateOrOutOfOrder);
            if (command.ClientTick < hostTick - _maxPastTicks || command.ClientTick > hostTick + _maxFutureTicks)
                return new CommandValidationResult(CommandValidationOutcome.TickOutsideWindow);
            if (!IsFinite(command.MoveX) || !IsFinite(command.MoveY) ||
                command.MoveX * command.MoveX + command.MoveY * command.MoveY > 1.0201f)
                return new CommandValidationResult(CommandValidationOutcome.InvalidMovement);

            const PlayerButtons allowed = PlayerButtons.CastPrimary | PlayerButtons.CastSecondary |
                PlayerButtons.Dodge | PlayerButtons.Interact | PlayerButtons.Confirm;
            if ((command.Buttons & ~allowed) != 0)
                return new CommandValidationResult(CommandValidationOutcome.InvalidButtons);

            _lastSequence[command.PlayerId] = command.Sequence;
            return new CommandValidationResult(CommandValidationOutcome.Accepted);
        }

        public void ResetPlayer(int playerId) { _lastSequence.Remove(playerId); }
        private static bool IsFinite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
    }
}
