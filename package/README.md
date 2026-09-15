# Cartur's Follow Command

*Free, and always will be — if it improved your game you can [tip me on Patreon](https://www.patreon.com/c/cartur).*

**More from Cartur:** [HD Blood](https://thunderstore.io/c/valheim/p/Cartur/Carturs_HD_Blood/) ·
[Map Pins](https://thunderstore.io/c/valheim/p/Cartur/Carturs_Map_Pins/) ·
[Compass and Clock](https://thunderstore.io/c/valheim/p/Cartur/Carturs_Compass_and_Clock/) ·
[Safe Stamina](https://thunderstore.io/c/valheim/p/Cartur/Carturs_Safe_Stamina/)

Every tamed animal takes the follow command, not just wolves and lox.

Press your Use key on a tamed boar and it falls in behind you. Press it again
and it stays where it is. Same key, same two messages, same behaviour you
already know from a wolf — boars, chickens, hens, asksvin, and anything a
creature mod adds.

## How to use it

Walk up to a tamed animal and press **Use** (`E` by default).

- First press — *"follows"*. It walks after you.
- Second press — *"stays"*. It holds position.

That's the whole mod. There is no extra keybind to learn and nothing to
configure.

## Worth knowing

**It survives relogs.** Who an animal is following is written to its save data,
and the game re-issues the command when the world loads. Park a boar at the
copper mine, log out, come back — it is still waiting, and still yours.

**It works on a server.** The command goes through the game's own networked
call, so other players see the animal move and the follow state is shared.

**Petting still works on animals you haven't commanded.** The pet effect plays
on every press either way; what changes is that the press now also toggles
follow.

**Modded creatures are covered for free.** Nothing here is a list of animal
names — the switch is flipped on the component every tameable creature has, so
a creature mod's new pet behaves like a vanilla one on the day it installs.

## How it works

Follow-and-stay was never a wolf feature. It is a `Tameable` feature, and the
entire mechanism already ships in the base game — the command, the AI that
walks the animal after you, the two on-screen messages, the networking, and the
save that survives a relog. The only thing separating a wolf from a boar is a
single `m_commandable` checkbox that Iron Gate ticked on some creature prefabs
and not others.

So this mod does not implement following. It ticks the checkbox on every tamed
creature and lets the game do exactly what it already knew how to do. That is
the whole plugin, and it is why there is no new keybind, no config file, and
nothing here to drift out of sync when the game updates.

## Compatibility

Nothing is replaced and no original method is skipped — one value is set after
the game finishes reading it from the prefab. Taming mods, pet mods and
creature mods all stack fine: anything with a `Tameable` component gets the
command, whoever added it.
