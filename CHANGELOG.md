# v35

- New option: [Better Lobby Management](https://github.com/CowboyBingus/BetterLobbyManagement) v1.0, host tools in the escape menu's GAME tab. DISBAND SQUAD kicks every other player back to their own ship. PROMOTE announces the new host with the game's own "*name* is the new squad leader" line, kicks them home with the game's own player-menu KICK, finds their new lobby and moves the whole squad to their ship; only the host needs the mod. It also shortens the Galactic Map lobby scanner's recharge from 20 to 5 seconds (adjustable in Mod Options Menu, never longer than the game's own) and offers an own-continent lobby filter. Measured in recorded play, as separate mods before the merge: 0.003 ms per frame for the lobby tools and 0.001 ms for the scanner.
- Seventeen independent options. Use one copy of Better Lobby Management: the standalone package or the pack option.
- Faster build: the option-selection checks replay every selection of at most two options, every selection missing at most two and 256 seeded random selections (564 of 131,072) instead of every one, and the bundled mods' own test suites run in parallel. Each package builds in about 15 seconds instead of over 4 minutes.
- The other sixteen bundled mods are unchanged from v34.

## [35.1.0](https://github.com/grenudi/VanillaPlusMegapack/compare/v35.0.0...v35.1.0) (2026-09-30)


### Features

* add Armory Preview Cache option ([115a1e9](https://github.com/grenudi/VanillaPlusMegapack/commit/115a1e9ded56aea9a664e8443a378e78a5a321a6))
* add bundled Clickable Scrollbars v2.1 ([a1a9d9a](https://github.com/grenudi/VanillaPlusMegapack/commit/a1a9d9a974b6f866e8e771f3b054802b4d17ddcf))
* add controllable hover pack to bundle ([c6ee843](https://github.com/grenudi/VanillaPlusMegapack/commit/c6ee843d0cc135676611cdc0e789aa4ad2b8c5be))
* add individual megapack mod options ([1adf073](https://github.com/grenudi/VanillaPlusMegapack/commit/1adf073101a451e3caebfb87ca45189ffdc3e4bf))
* add rows alternative to v8 ([df5b0ce](https://github.com/grenudi/VanillaPlusMegapack/commit/df5b0cede1ebcf7ca49425dd11a8f0f2c255ef7e))
* adopt loader addon discovery ([2600dce](https://github.com/grenudi/VanillaPlusMegapack/commit/2600dcee0456f99997e4a981a086f60b6500f21a))
* bundle Arc Thrower Revamped as the twelfth option (v15) ([dced7da](https://github.com/grenudi/VanillaPlusMegapack/commit/dced7da8bed31a0847b3de8005ceb1369f6e6571))
* bundle Better Lobby Management v1.0 in Megapack v35 ([1b943e6](https://github.com/grenudi/VanillaPlusMegapack/commit/1b943e61d2436f204fb5d8740a6082f44a780e42))
* bundle Flame Damage Fixed v1.1 in Megapack v34 ([45fe820](https://github.com/grenudi/VanillaPlusMegapack/commit/45fe8200e4ddd1ea4c26562d99d9c0e1434bdde3))
* bundle Flame Damage Fixed, Mod Options Menu and Mod Bindings Menu in Megapack v33 ([7ca9184](https://github.com/grenudi/VanillaPlusMegapack/commit/7ca91842b707af912d2cfd3ed4430da0c9a30e0b))
* bundle Know Your Constellation ([b7b899e](https://github.com/grenudi/VanillaPlusMegapack/commit/b7b899ec8b5d610e9041580b8fab0344111d49ac))
* bundle Ship Station Hotkeys v1.7 in Megapack v29 ([4f5f0d7](https://github.com/grenudi/VanillaPlusMegapack/commit/4f5f0d7cfff663a8e614d23f16a7852f3b5e70e9))
* publish seven-mod vanilla megapack ([f67cb46](https://github.com/grenudi/VanillaPlusMegapack/commit/f67cb469145f272228ae223b102c42f2a3dac894))
* release updated standard and Rows packs ([66b6c1a](https://github.com/grenudi/VanillaPlusMegapack/commit/66b6c1aadda43ebb13d2fd390c8287a87181001f))
* update bundled Armory Preview Cache to v18 ([74ae9db](https://github.com/grenudi/VanillaPlusMegapack/commit/74ae9dbacc56cea1b7548bf99c412b90b68e6268))
* update bundled Clickable Scrollbars to v2.2 ([2f0dd90](https://github.com/grenudi/VanillaPlusMegapack/commit/2f0dd90ee07555a5355195ec94d74af531c8c267))


### Bug Fixes

* bundle Arc Thrower startup fix in v17 ([d525e15](https://github.com/grenudi/VanillaPlusMegapack/commit/d525e15afda2b87bcf09470a1edb3b02182babae))
* bundle verified scrollbars in v16 ([2506b4f](https://github.com/grenudi/VanillaPlusMegapack/commit/2506b4f372da4d2222741a00c78b25e960d5a91e))
* **ci:** correct Windows MSVC setup, unused import, and luacheck strictness ([9f22a89](https://github.com/grenudi/VanillaPlusMegapack/commit/9f22a893bfc537fd1781193cab8905e8ed245049))
* **ci:** fix AI-audit changelog insertion landing at end of file instead of after the current release ([0a5e585](https://github.com/grenudi/VanillaPlusMegapack/commit/0a5e58541e0df217b1c71469863fb6a57338e7c4))
* **ci:** stop luacheck's warnings-only exit code from aborting the step early ([4086488](https://github.com/grenudi/VanillaPlusMegapack/commit/4086488484c1b224b5825b5e7062980dea5f33e3))
* support game build 25327279 ([90e216d](https://github.com/grenudi/VanillaPlusMegapack/commit/90e216dda4c01b14cc9c465672a7d10a251a675a))
* support game build 25480438 ([27c2a65](https://github.com/grenudi/VanillaPlusMegapack/commit/27c2a65000361b91f841a9ee38868cc916f7175a))
* update bundled mission fixes and logs ([beaac9d](https://github.com/grenudi/VanillaPlusMegapack/commit/beaac9da37962012154a0f380bcf3e711e86313d))


### Performance Improvements

* bundle Shallow Water Diving v3.8 in Megapack v32 ([f689cb3](https://github.com/grenudi/VanillaPlusMegapack/commit/f689cb32895b53b1fe785d34309da1c9df5103e8))
* bundle the reduced-overhead component releases in v30 ([d370ad4](https://github.com/grenudi/VanillaPlusMegapack/commit/d370ad44222871eb82317e02e4acb885199f08bb))
* require loader v18 for the shared LuaJIT code cache ([ea92513](https://github.com/grenudi/VanillaPlusMegapack/commit/ea92513180a9e944fdc7909608cc8fc3bae95f67))
* update bundled performance fixes ([f3868a4](https://github.com/grenudi/VanillaPlusMegapack/commit/f3868a42f4482de7316eb653e8934dcbbc7587f3))

## v34

- [Flame Damage Fixed](https://github.com/CowboyBingus/FlameDamageFixed) v1.1 fixes v1.0's flame passing through armoured targets. v1.0 kept the flame off the Lumberer by moving it to a copy of its collision layer without layer 20, which is also the game's heavy-armour and vehicle layer: Chargers, the Factory Strider, tank turrets, the Illuminate dropship and more could not be hit. Now each Lumberer or Flame Sentry shares a private Havok collision group with its own flame, from its first burst until it is gone, and members of that group skip each other; no collision layer is changed, so everything else collides with the flame as in the base game. In recorded play the flame landed 4,822 hits on layer-20 hit-boxes (acid Chargers, Chargers, Impalers) and none on the Lumberer that fired it while the fix was running.
- The two flame parts Flame Damage Fixed restored are no longer drawn: they still hit, but the flame no longer shows a second short, wide cone near the nozzle.
- Flame Damage Fixed's measured cost: 0.008 ms per frame in missions and 0.002 ms per frame aboard the ship; most burst starts under 0.5 ms, and 0.8-1.7 ms once for a Lumberer's first burst.
- The other fifteen bundled mods are unchanged from v33. Use one copy of Flame Damage Fixed: the standalone package or the pack option.

## v33

- New option: [Flame Damage Fixed](https://github.com/CowboyBingus/FlameDamageFixed) v1.0. The Lumberer's flamethrower arm and the Flame Sentry share one flame, and two of its five damaging parts never spawned: their start-up curves assume the Cremator's 64 s effect lifetime, but the shared flame's is 1e10 s. They now start with the Cremator's timing, the flame starts at the Cremator's distances from the nozzle, and it no longer hits the Lumberer itself. In recorded play on bugs the Lumberer averaged 4.7 hits per damage window without the fix and 14.7 with it; the Cremator averaged 14.6 (different fights, so a rough comparison). Measured cost: 0.0015 ms per frame aboard the ship and 0.008 ms per frame in missions.
- New option: [Mod Options Menu](https://github.com/CowboyBingus/ModOptionsMenu) v1.0.1, the native MODS tab on the Options screen, where Shallow Water Diving sets its maximum dive depth. It was a separate install before.
- New option: [Mod Bindings Menu](https://github.com/CowboyBingus/ModBindingsMenu) v2.0, the native MODS tab on the keyboard and controller binding pages, where Ship Station Hotkeys' shortcuts are rebound. It was a separate install before. Like its standalone release, the option also deploys its `content/input.config` override with the native input actions; another mod that replaces that resource must be merged with it.
- Sixteen independent options. Use one copy of each of the three: the standalone package or the pack option.
- The other thirteen bundled mods are unchanged from v32.

## v32

- Shallow Water Diving v3.8: with [Mod Options Menu](https://github.com/CowboyBingus/ModOptionsMenu) installed, MODS > SHALLOW WATER DIVING > Max Dive Water Depth sets the deepest water a dive can start in, from 0.20 (lower shin; the previous fixed limit and still the default) up to 1.30, where the Helldiver starts swimming. It applies with the menu's Apply (Tab). Without Mod Options Menu nothing changes.
- Shallow Water Diving checks the water record's memory page once per record table instead of before every write. A protection query costs about 0.2-0.3 ms in game; v31 made four at every dive start and two at every landing, now the first assisted dive after loading into a mission makes one and later dives and landings none.
- Shallow Water Diving's per-frame checks allocate no memory (about 1.9 KB of garbage per frame aboard the ship before) and read far less: outside a mission one check per frame; in a mission, one read of your dive controller per check, with a full identity check every 31st check. Its log is written at startup, at shutdown and when it stops instead of on every status change. Measured in recorded play: 0.022 -> 0.006 ms per frame aboard the ship and 0.141 -> 0.009 ms per frame in missions.
- INSTALL lists the bundled revisions again (the list had not been updated since v29).
- The other twelve bundled mods are unchanged from v31.

## v31

- Require Bingus Shared Loader v18, which raises the game's shared LuaJIT code cache before any mod starts: 16 MB of machine code and 8,000 traces instead of the game's 512 KB and 1,000, shared by the game and every mod. Filling either limit made LuaJIT discard all compiled code at once and recompile it during play.
- Measured in recorded real play with all thirteen options enabled (19 minutes aboard the ship and an 11-minute mission): the old 512 KB was already full aboard the ship, the session ended at 960 KB of machine code in 946 traces, and the cache never flushed.
- If an older loader is still installed, the pack raises the same limits once at startup, without the loader's growth after a flush or its log line; with v18 it leaves the cache to the loader.
- Correct the pack's self-reported revision, which still read megapack-v28.
- No per-frame work and no gameplay change: the thirteen bundled mods are unchanged from v30. This removes repeated recompilation, not a promised frame-rate change, which depends on the machine.

## v30

- Reduce the per-frame work of the bundled mods: in recorded real play, their combined main-thread time per frame fell from about 2.0 ms to 0.85 ms in missions and from about 1.05 ms to 0.37 ms aboard the ship, even with Shallow Water Diving now active.
- Reinforcement Beacons Fixed v4.5 and Hellpod Steering Unlocked v7.4 check memory protection only before a write; in game that query costs about 0.3 ms each. Reinforcement Beacons Fixed dropped from about 0.99 ms to 0.03 ms per frame in missions.
- Shallow Water Diving v3.7 fixes the mod stopping itself in missions on this game build ("Native dive timeout changed") and reads only identity and dive records outside a dive.
- Consistent Vaulting v8.8 reads only the input state while no assist is active and the input is released, verifies native tables once and decodes fields without copying buffers: about 0.44 ms to 0.25 ms per frame in missions.
- Enemy Collision Synchronized v2.11.0 validates guards without per-block string copies, halves per-poll garbage in synthetic scenes and adds a one-second cooldown before re-posing the same actor for small corrections (under 10 cm and 5 degrees): about 0.29 ms to 0.14 ms per frame in missions.
- Sentry Aim Retention v1.0.13 and Controllable Hover Pack v1.7 skip per-frame work that could not act (no deployed sentries, no hover pack) and reuse decode and read buffers.
- Every changed mod was checked in live play: beacon corrections, vault, slope and ledge assists, dives and the shallow-water correction, early hover descent, sentry aim holds and corpse realignments. Gameplay behavior is otherwise unchanged; these are CPU savings, not a promised frame-rate change, which depends on the machine.

## v29

- Replace the Galactic Menu Hotkey option with Ship Station Hotkeys v1.7: Tab map, F1 Armory, F5 Control Center, F6 Ship Management, F7 Stratagem Hero and F8 instant Hellpod entry.
- Name the option Ship Station Hotkeys; its option folder and addon resource are unchanged, so managers update it in place.
- Rebind all six shortcuts, choose activation types and assign controller buttons with the separate Mod Bindings Menu v2.0.
- List the exact bundled component versions in the README and install notes.
- All other bundled components are unchanged from v28.

## v28

- Update both Megapack layouts for Steam build 25480438.
- Include the refreshed addresses, guards and corpse state-machine hashes from the standalone mods.
- Keep all thirteen independent options and the separate Mod Bindings Menu dependency.
- Offline builds and package checks pass; live gameplay validation remains pending.

## v27

- Add Galactic Menu Hotkey v1.1 as an independent option.
- Include Arc Thrower Revamped v1.5 recovery fixes and Clickable Scrollbars v2.13 Display drag input fixes.
- Keep Mod Bindings Menu v1.0 as a separate dependency for keyboard rebinding; it is not bundled.
- Update both standard and Rows packages with the same thirteen mod options.
- Offline regression and packaging checks pass; new fixes still need in-game confirmation.

# v19

- Update the bundled scrollbar, Arc Thrower, sentry, vaulting, hover-pack, collision and Armory performance fixes.
- Reduce click-related native reads, routine disk writes and default profiling work.
- Preserve all twelve options and the existing Rows layout.
- Offline regression checks cover this update; live frame-time verification remains pending.

# v18

- Update Clickable Scrollbars to v2.7 and Arc Thrower Revamped to v1.2 in standard and Rows.
- Stop scrollbar screenshot scanning and routine log writes on gameplay clicks.
- Bound Arc Thrower scanning and remove duplicate render work and verbose firing logs.
- Preserve all twelve options and the existing Rows layout; in-game validation is pending.

# v17

- Update Arc Thrower Revamped to v1.1 in both standard and Rows packages.
- Fix startup stopping with "kernel32 bindings unavailable" or a missing `GetModuleHandleA` declaration.
- Exercise the first update and render callbacks with real Windows LuaJIT bindings during validation.
- Keep the other eleven components, twelve independent options, and existing Rows layout unchanged.
- Offline startup, integration, and package validation; live gameplay verification pending. Requires Bingus Shared Loader v15 or newer.

# v16

- Update Clickable Scrollbars to the in-game verified v2.6 in both standard and Rows packages.
- Fix smooth dragging in equipment and Career, including sideways pointer movement.
- Prevent scrollbar dragging from opening other tabs or activating items.
- Keep all twelve mod options and the existing Rows constellation layout.

# v15

- Adds Arc Thrower Revamped v1 as a twelfth independent option: hold the fire
  button and the ARC-3 Arc Thrower keeps firing through its own charge cycle.
- Arc Thrower Revamped keeps stock charge times, cadence, damage and arc
  settings, follows a second thrower called down mid-mission, and shares a
  re-entry guard with its standalone package.
- Keeps the other eleven pinned gameplay implementations unchanged; standard and
  Rows packages carry identical components.
- Requires Bingus Shared Loader v15 or newer. Arc Thrower Revamped is loaded
  through declared-entry discovery because the shared loader's built-in
  registry predates it.

# v14

- Updates the bundled Clickable Scrollbars to v2.2.
- Scales the scrollbar geometry to the display height, so 1080p, 1440p and 4K screens keep the same relative behaviour.
- Keeps the verified 1440p values as the reference and follows a resolution or monitor change on the next click.
- Finds a thumb taller than the capture strip with one doubled retry pass instead of ignoring the click.
- Keeps the other ten pinned gameplay implementations unchanged; standard and Rows packages carry identical components.
- Requires Bingus Shared Loader v15 or newer.

# v13

- Adds Clickable Scrollbars v2.1 as an eleventh independent option.
- Lets a track click move the item-list scrollbar thumb to the pointer, and a press on the thumb drag it with the mouse.
- Keeps the other ten pinned gameplay implementations unchanged; standard and Rows packages carry identical components.
- Requires Bingus Shared Loader v15 or newer.

# v12

- Updates the bundled Armory Preview Cache to v18.
- Refreshes a weapon's preview when the game re-renders it, so changing a pattern or attachment updates the thumbnail.
- Retires the previous preview immediately after a weapon is re-configured instead of waiting for the whole category to rebuild.
- Keeps the other nine pinned gameplay implementations unchanged; standard and Rows packages carry identical components.
- Requires Bingus Shared Loader v15 or newer.

# v11

- Adds plaintext discovery entries for the pack identity and all ten components.
- Preserves original module names, arguments and the exact pinned gameplay bytecode.
- Requires Bingus Shared Loader v15 or newer, retaining API 1 and both manager GUIDs.
- Standard and Rows keep ten independent options.
- Rollback: replace this package with v10.1, review options, then Purge / Deploy. Loader v15 supports the previous pack.

# v10.1

- Updates all ten bundled mods to their latest versions.
- Includes the hover-pack recovery and mission-type fixes for hover, reinforcement placement, vaulting and shallow-water diving.
- Updates both the standard and Rows packages; independent mod options are preserved.
- Moves logs to `%LOCALAPPDATA%\CowboyBingus\Helldivers2\Logs`.
- Requires Bingus Shared Loader v14 for the shared log folder.
