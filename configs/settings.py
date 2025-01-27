DELAY_BEFORE_START = False  # Random sleep 0-12 hours before start current account. True if you have 100+ accounts

ENABLED_OPERATIONS = {
    "wrap": True,
    "unwrap": True,
    "claim": True,
    "stake": True,
    "unstake": True,
    "bridge_sfi": True,
    "bridge_sep": False,
}

OPERATION_LIMITS: dict[str, tuple[float, float]] = {
    "wrap": (0.01, 0.2),
    "unwrap": (0.01, 0.2),
    "stake": (0.001, 0.01),
    "unstake": (0.001, 0.05),
    "bridge_sfi": (0.001, 0.05),
    "bridge_sep": (0.001, 0.01),
}
