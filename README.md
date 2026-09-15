# Cartur's Follow Command

BepInEx/Harmony mod for Valheim. Every tamed animal accepts the follow/stay
command, not just wolves and lox. Press Use on a tamed boar, chicken or asksvin
and it follows you.

Thunderstore package name `Carturs_Follow_Command`, plugin GUID
`com.jekkle.valheim.carturfollowcommand`. Nexus mod 3728.

## How it works

One Harmony postfix, one line in it:

```csharp
[HarmonyPatch(typeof(Tameable), "Awake")]
static void Postfix(Tameable __instance) => __instance.m_commandable = true;
```

Follow/stay is not a wolf feature. It is a `Tameable` feature that only wolves
and lox have switched on. The whole mechanism already ships in the base game:

```
Tameable.Interact             -> if (m_commandable) Command(user)
Tameable.Command              -> InvokeRPC("Command")
Tameable.RPC_Command          -> MonsterAI.SetFollowTarget(player)
                                 / SetFollowTarget(null) + SetPatrolPoint()
                                 and persists the owner in ZDOVars.s_follow
Tameable.UpdateSavedFollowTarget -> re-issues Command() on world load
MonsterAI.UpdateAI            -> if (m_follow) Follow(m_follow, dt)
```

There is no species check anywhere in that chain. The single thing gating it is
the `m_commandable` bool, set per-prefab in the Unity asset and false on boar,
chicken, hen, asksvin and the rest.

So there is nothing to implement. Flip the flag after `Awake` has read the
prefab value and the vanilla path handles the button press, the toggle, the
`$hud_tamefollow` / `$hud_tamestay` message, the networking and the save. It
survives relogs because vanilla's own `UpdateSavedFollowTarget` re-issues the
command on load, and it covers modded creatures for free because anything with
a `Tameable` gets the same treatment.

`RPC_Command` already null-checks `m_monsterAI`, so a `Tameable` without an AI —
saddle-only cases — stays a no-op rather than throwing.

The button is the existing Use key (E by default), exactly as with a wolf. No
new keybind: a second one would be a worse duplicate of the one players already
know.

## Build

Requires .NET 8 SDK and a Valheim install with BepInEx.

```
cd src
dotnet build
```

Managed DLLs for compiling come from the Steam install (`VALHEIM_INSTALL`); the
built plugin deploys to the r2modman profile (`R2MODMAN_PROFILE`). Override
either rather than editing the csproj:

```
dotnet build -p:VALHEIM_INSTALL="D:\SteamLibrary\steamapps\common\Valheim"
```

Fully quit Valheim through r2modman and relaunch — BepInEx only scans plugins
on startup.

## Packaging and publishing

```
powershell -ExecutionPolicy Bypass -File tools\pack.ps1
powershell -ExecutionPolicy Bypass -File tools\publish.ps1 -WhatIf
powershell -ExecutionPolicy Bypass -File tools\publish.ps1         # Thunderstore
powershell -ExecutionPolicy Bypass -File tools\publish-nexus.ps1   # Nexus
```

`pack.ps1` builds Release and writes both zips to `dist\` — the Thunderstore
one with `manifest.json`, `icon.png`, `README.md`, `CHANGELOG.md` and
`plugins\CarturFollowCommand.dll`, and a Nexus one holding only
`BepInEx/plugins/CarturFollowCommand.dll`, because Nexus unpacks into the game
folder rather than reading a manifest. It refuses to pack if `manifest.json`
and `PluginVersion` in `src\Plugin.cs` disagree.

Both publishers upload the zip `pack.ps1` already made rather than building
their own, take `-WhatIf` to print the plan without sending anything, and
refuse a zip older than the last source edit. Credentials come from
`TCLI_AUTH_TOKEN` and `NEXUS_API_KEY`; neither is stored in the repo.

## Config

None. There is one behaviour and no reason to turn half of it off.

## Compatibility

Client-side. The server does not need it. Another player without it simply
cannot command their own chickens — nothing desyncs, because the command uses
vanilla's own RPC and ZDO field.

Anything else patching `Tameable.Awake` will interleave fine; this only writes
one bool and reads nothing.
