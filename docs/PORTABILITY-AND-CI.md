# Portability and CI

Proton-Apex does not hard-code CachyOS, Arch, Debian, Fedora, or openSUSE package commands. The runtime uses Proton's existing Steam Runtime and the build uses Valve's containerized Proton SDK. This keeps host distribution differences outside the shipped compatibility tool.

`apex-platform-check` reports distribution, kernel, architecture, Vulkan availability, container engine, Steam, and synchronization-related capabilities without changing the system. It is diagnostic only and does not replace the Proton SDK checks.

## GitHub Actions

`.github/workflows/proton-apex.yml` contains two jobs. `validate` runs on every push and pull request, performs Python/manifests smoke tests, and runs the portable platform report. `full-build` is deliberately manual because a Proton SDK build is large, can take hours, downloads substantial dependencies, and GitHub-hosted runners are not a good game-performance benchmark. Trigger it from Actions with `full_build=true`; it uploads the redist directory and build log as artifacts.

The build job uses Docker on an Ubuntu runner and calls Proton's upstream `configure.sh`/`make redist` flow. It is a packaging/build check, not proof of compatibility or FPS. Real GPU and anti-cheat testing still requires supported hardware and games.

## Publishing plan

The current local checkout still has ValveSoftware/Proton as `origin`. It must not be pushed there. Before public release, create a separate repository, review licenses and upstream notices, add a project README, and decide whether the first repository should be public or private. Only then should the repository get a new `origin` URL and a tagged release.
