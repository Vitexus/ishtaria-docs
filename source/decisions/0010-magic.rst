0010 – Magic: mana, scrolls and a small set of data-driven spells
=================================================================

:Status: Accepted and implemented (first slice)
:Date: 2026-10-07

Context
-------

The world has survival, hunting, crafting, trading and building, but no magic, although the
story's first item is a magical tablet (the Aetherglass) and players expect some. Magic must
fit the rules that already hold everywhere else:

* the server decides every outcome and clients only send intentions;
* content is **data**: no scripts and no executable code in packs or configuration;
* what real money buys is space and appearance, never power (:doc:`0006-monetization`);
* death is permanent, so a spell may never revive or restore a dead character;
* the server stores no language and no history.

Decision
--------

* **Mana** is a fourth reserve beside health, stamina, food and water. It is 0–100,
  starts full and **regenerates by the clock** (0.4 per second, also while offline), computed
  from `mana` and `mana_updated_at` when it is read, so there is no tick loop.
* **Spells are data** in ``etc/spells.json``: an id, a mana cost, a cooldown, a minimum level
  and one **effect from a fixed set** that the server implements: ``heal`` (health), ``refresh``
  (stamina), ``ward`` (less damage from creatures for a while) and ``bolt`` (work points
  against an animal in range, like a weapon swing). A new spell is a new row of data; a new
  *kind* of effect is code and needs a review.
* **Spells are learned from scrolls.** A scroll is an inventory item (``scroll_<spell>``,
  category ``document``). Reading it (``POST /players/me/learn``) needs the character's level,
  consumes the scroll and records the spell for that character for good (``player_spells``).
  Scrolls are made at a workbench from a **quartz crystal** (rare, from rocks) and ordinary
  materials. They are **not sold by merchants**, so magic is earned by play and not bought.
* **Casting** is ``POST /players/me/cast``. The server checks that the spell is known, its
  cooldown, mana and (for a bolt) the target and range, and does the whole effect in one
  transaction. Mana is spent atomically: the check and the subtraction are one statement under
  the character's row lock.
* **Balance rules.**

  - A bolt works from a distance, so a hunter avoids the bite of an animal that would strike
    back in melee; in return it costs mana, does less than a good weapon and brings no
    weapon wear. Within melee reach the animal still bites back.
  - ``ward`` multiplies the damage of creatures after armour and a raised shield; it never
    reduces damage below one and never lasts longer than a minute.
  - ``heal`` never exceeds the character's maximum health and does nothing for the dead (a
    dead character has no session).
  - Nothing here can change gold, items of others, or another character's state: all
    effects of this slice are on the caster or on generated animals.

* **No player versus player magic yet.** Spells cannot target players. Healing others, area
  effects, summoning, and anything that touches another player need their own decision.

Consequences
------------

* Magic reuses the combat rules (armour, shield, ward, creature bites) instead of a second
  simulation, and the hunting rules (animal state in ``world_object_state``, drops, respawn).
* The set of effects is deliberately small; the data format leaves room for more spells
  without server changes, and for datadisk-defined spells later (they would have to choose
  from the same effects and pass the same review as other datadisk content).
* The Aetherglass of the story stays a story item for now; connecting it to the spell
  system (for example as a focus that raises maximum mana) is left open.
* The client shows mana in the HUD, lists known spells in the inventory window with their
  costs, and casts the first nine with the number keys; the visual effect is only a short
  light flying to the target. Effects, sounds and icons are cosmetic and not authoritative.

Change (2026-10): day and night
-------------------------------

By the project owner's request two more effect kinds joined the fixed set (migration
``0041_day_night_scrolls.sql``): ``day`` (Scroll of Day, spell "Daybreak") and ``night``
(Scroll of Night, spell "Nightfall"). Casting one jumps the world's **shared solar clock**
to the caster's next dawn or dusk — the first crossing of the astronomical horizon in the
asked direction at the caster's position on the planet, found by a coarse scan and
bisection. The shift is a per-world offset (``worlds.solar_offset_seconds``, bounded to one
day) that ``GET /world`` adds to the real clock on top of the operator's
``--solar-offset-seconds``; each cast replaces it, so the offset never grows. This is the
first spell that changes the world rather than the caster: everyone online is told through
a ``solar`` event (their clients ask for ``/world`` again) and the cast answer carries the
new ``solar`` document for the caster. No player is targeted, nothing revives the dead,
and the sky itself stays astronomical: only the world's offset from the real clock moves.
