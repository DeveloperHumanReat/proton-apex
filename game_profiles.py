"""Proton-Apex game profile catalogue.

This catalogue is intentionally conservative. EAC and BattlEye are not enabled
by arbitrary environment variables: the game, its runtime, and the anti-cheat
vendor must support Proton. LatencyFLEX and NVIDIA Reflex likewise require
actual runtime/driver support and cannot be emulated by setting a made-up flag.

The values below are suitable launch-option candidates and diagnostics. They do
not bypass anti-cheat protections.
"""

GAME_PROFILES = {
    "730": {
        "name": "Counter-Strike 2",
        "anti_cheat": "Valve Anti-Cheat",
        "env": {"DXVK_STATE_CACHE": "1"},
        "latency": "Use the game's NVIDIA Reflex setting when exposed; otherwise use an in-game limiter.",
    },
    "1172470": {
        "name": "Apex Legends",
        "anti_cheat": "Easy Anti-Cheat; Proton support depends on the game's current configuration",
        "env": {"DXVK_STATE_CACHE": "1"},
        "latency": "No fake Reflex/LatencyFLEX flags; verify the game's own low-latency option.",
    },
    "1245620": {
        "name": "Elden Ring",
        "anti_cheat": "Easy Anti-Cheat; supported runtime required",
        "env": {"DXVK_STATE_CACHE": "1"},
        "latency": "Keep frame pacing stable; do not inject unsupported latency shims.",
    },
    "1091500": {
        "name": "Cyberpunk 2077",
        "anti_cheat": "None required for the single-player runtime",
        "env": {"DXVK_STATE_CACHE": "1"},
        "latency": "VKD3D-Proton and the game's frame limiter are the preferred path.",
    },
    "271590": {
        "name": "Grand Theft Auto V",
        "anti_cheat": "BattlEye in supported online configurations",
        "env": {"DXVK_STATE_CACHE": "1"},
        "latency": "Use the game/driver limiter; BattlEye compatibility is vendor-controlled.",
    },
}


def profile_for_app(app_id, environment=None):
    """Return a profile without mutating the process environment."""
    profile = GAME_PROFILES.get(str(app_id))
    if profile is None:
        return None
    if environment is not None:
        return {key: environment.get(key, value) for key, value in profile["env"].items()}
    return profile


def describe_app(app_id):
    profile = profile_for_app(app_id)
    if profile is None:
        return {"known": False, "app_id": str(app_id)}
    return {"known": True, "app_id": str(app_id), **profile}


if __name__ == "__main__":
    import json
    import os
    print(json.dumps(describe_app(os.environ.get("STEAM_COMPAT_APP_ID", "")), indent=2))
