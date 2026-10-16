# Proton-Apex 1.0

Proton-Apex is a conservative development fork of Valve Proton 11.0. It keeps upstream Proton's Wine, DXVK, VKD3D-Proton, NVAPI, EAC bridge, and BattlEye bridge integration intact instead of pretending that environment variables can replace those components.

## Performance defaults

`user_settings.py` now enables the normal Vulkan path, DXVK state caching, quiet DXVK/VKD3D diagnostics, fsync/esync capability negotiation, and large-address-aware behavior. It deliberately does not enable `DXVK_ASYNC`, force a VKD3D feature level, or inject made-up Reflex/LatencyFLEX variables. Those settings are either unsupported upstream or can reduce compatibility.

## Configuration manager

The `apex-config` command provides a simple interface without adding GUI dependencies:

```bash
./apex-config show
./apex-config preset balanced
./apex-config preset diagnostic
./apex-config reset
```

The manager creates a `.bak` backup before replacing `user_settings.py`. For testing or a separate per-user overlay, set `PROTON_APEX_SETTINGS=/path/to/user_settings.py`. `balanced` is intended for normal play; `diagnostic` enables logs temporarily and should not be used as a performance preset.

## Online games and anti-cheat

Easy Anti-Cheat and BattlEye are **not bypassed** and cannot be enabled by a generic flag. A game must opt in to Proton, ship a compatible anti-cheat runtime, and allow the required Linux/Proton configuration. The profile catalogue records this status and applies only safe cache settings. It never injects, disables, or circumvents anti-cheat checks.

## LatencyFLEX and NVIDIA Reflex

LatencyFLEX and NVIDIA Reflex require support in the game, driver, and relevant runtime components. `LFX_ENABLED`, `NVEXT_ENABLE_REFLEX`, and similar invented variables are deliberately not set because they do not implement either technology and may create false confidence or break a game. The recommended path is the game's own Reflex option where available, stable frame pacing, and a tested frame-rate limiter.

## Current implementation

The fork currently adds a conservative global `user_settings.py`, a read-only AppID profile catalogue, a Vulkan diagnostic collector, a shader-cache helper, and the `apex-config` CLI. The profile catalogue is advisory until it is wired into a tested launch integration. No profile is considered a compatibility guarantee.

## Validation

Run the following checks from the repository root:

```bash
python3 -m py_compile user_settings.py game_profiles.py apex-diag apex-shader-optimizer apex-config
./apex-config show
./apex-diag
```

A complete Proton build still requires the container-based Proton SDK described in `README.md`; this sandbox does not contain a Steam client or a game runtime for end-to-end anti-cheat testing.
