"""Proton-Apex global runtime settings.

Only variables consumed by Proton, DXVK, VKD3D-Proton, or Wine are included.
Per-game settings should be supplied through Steam launch options or a profile
manager; this file applies conservative defaults to every game.
"""

user_settings = {
    # Keep Proton's diagnostic log opt-in; never enable noisy logging globally.
    # "PROTON_LOG": "1",

    # Preserve the normal Vulkan translation path.
    "PROTON_USE_WINED3D": "0",
    "PROTON_NO_D3D11": "0",
    "PROTON_NO_D3D10": "0",

    # DXVK: use the state cache and avoid unnecessary diagnostic overhead.
    # DXVK_ASYNC is intentionally absent: it is not an upstream DXVK option.
    "DXVK_STATE_CACHE": "1",
    "DXVK_LOG_LEVEL": "none",
    "DXVK_HUD": "0",

    # VKD3D-Proton: keep diagnostics quiet and allow the runtime to select the
    # best supported feature level. Do not force unsupported DXR/12_2 modes.
    "VKD3D_DEBUG": "none",
    "VKD3D_SHADER_DEBUG": "none",

    # Use futex synchronization when the kernel supports it. Proton performs
    # the actual capability check; users can override with PROTON_NO_FSYNC=1.
    "PROTON_NO_FSYNC": "0",
    "PROTON_NO_ESYNC": "0",

    # Keep large-address-aware behavior enabled for supported Windows binaries.
    "PROTON_FORCE_LARGE_ADDRESS_AWARE": "1",

    # Useful diagnostics without enabling full Wine tracing.
    "GST_DEBUG_NO_COLOR": "1",
}
