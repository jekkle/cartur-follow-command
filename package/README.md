# Cartur's Follow Command

Every tamed animal takes the follow command, not just wolves and lox.

![Cartur's Follow Command](https://raw.githubusercontent.com/jekkle/cartur-follow-command/master/media/nexus-header.png)

![A tamed boar following](https://raw.githubusercontent.com/jekkle/cartur-follow-command/master/media/nexus-gallery.png)

Walk up to a tamed animal and press **Use** (`E` by default).

- First press — *"follows"*. It walks after you.
- Second press — *"stays"*. It holds position.

Boars, chickens, hens, asksvin, and anything a creature mod adds. Same key, same
two messages, same behaviour you already know from a wolf. No new keybind, and
nothing to configure.

## Worth knowing

**It survives relogs.** Who an animal is following is saved with it. Park a boar
at the copper mine, log out, come back — it is still waiting.

**It works on a server.** The command goes through the game's own networked call,
so other players see the animal move.

**Petting still works.** The pet effect plays on every press either way; the press
now also toggles follow.

**Modded creatures are covered for free.** Nothing here is a list of animal names.

## How it works

Follow-and-stay was never a wolf feature — it is a `Tameable` feature, and the
whole mechanism already ships in the base game. The only thing separating a wolf
from a boar is a single `m_commandable` checkbox that Iron Gate ticked on some
prefabs and not others. This mod ticks it on the rest.

## Install

Use a mod manager (r2modman / Thunderstore / Gale) and it pulls in BepInEx for you.
Manually: drop `CarturFollowCommand.dll` into `BepInEx/plugins`.

---

*Free, and always will be. If it improved your game you can [tip me on Patreon](https://www.patreon.com/c/cartur).*

**More from Cartur:**
[HD Blood](https://thunderstore.io/c/valheim/p/Cartur/Carturs_HD_Blood/) ·
[Map Pins](https://thunderstore.io/c/valheim/p/Cartur/Carturs_Map_Pins/) ·
[Compass and Clock](https://thunderstore.io/c/valheim/p/Cartur/Carturs_Compass_and_Clock/) ·
[Safe Stamina](https://thunderstore.io/c/valheim/p/Cartur/Carturs_Safe_Stamina/) ·
[Flooring](https://thunderstore.io/c/valheim/p/Cartur/Carturs_Flooring/) ·
[UI HUD](https://thunderstore.io/c/valheim/p/Cartur/Carturs_UI_HUD/) ·
[Waste Management](https://thunderstore.io/c/valheim/p/Cartur/Carturs_Waste_Management/)
