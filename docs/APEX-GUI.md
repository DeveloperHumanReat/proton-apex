# Proton-Apex GUI draft

The GUI draft is implemented with **PySide6 / Qt6** in `apex-gui.py`. It displays every current AppID profile, anti-cheat status, environment values, and latency guidance. The configuration panel applies the existing `apex-config` presets and invokes the shader-cache inspector.

Run it after installing the optional dependency:

```bash
python3 -m pip install --user PySide6
python3 apex-gui.py
```

The sandbox used for this prototype does not have PySide6 installed, so the source was syntax-checked but not rendered here. The GUI intentionally does not claim to enable EAC, BattlEye, NVIDIA Reflex, or LatencyFLEX.

## Shader cache behavior

The helper creates or scans `DXVK_STATE_CACHE_PATH`, counts cache files and bytes, and prints the safe launch variables. It does not precompile shaders; shader compilation is performed by DXVK/VKD3D-Proton while a real game runs. Therefore cache inspection time is not game FPS and cannot prove a reduction in shader stutter.

Benchmark the helper itself with:

```bash
./apex-shader-bench
```

A valid performance study requires the same game, scene, driver, resolution, frame limiter, Proton build, and cache state in cold-cache and warm-cache runs. Record average FPS, 1% low, frame-time variance, shader compilation events, and input latency. No game FPS result is claimed from this sandbox because no Steam game runtime is present.
