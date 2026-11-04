Gameplay guide
==============

This page describes what a player can do in Ishtaria 0.3.0. Everything listed here is
implemented; parts that are only planned are marked as such. The server decides every
outcome, the client sends intentions. Design background lives under :doc:`architecture/index`.

Starting out
------------

#. Install the client (see :doc:`operations/installation`) and enter the address of a
   world server. Remote servers must be reached over HTTPS before accounts are accepted.
#. Register an account and create a character: a name and one of the Kenney or Quaternius
   character models. The choice is stored by the server.
#. A new character receives **100 gold coins**, a few food stacks, a starter tool kit, one
   *Scroll of Day* and 100 inventory slots. This is granted exactly once, when the
   character is created; signing in again never grants it again.
#. If a story datadisk marks a spawn place (for example the hunter's water-hole in the
   Gilgamesh disk), the character wakes up there; otherwise a safe spot is chosen.

The language of the interface (English or Czech) and the interface sounds are client
preferences. Changing them never reconnects or changes server state. Passwords and
tokens are never saved on disk; restarting the client requires signing in again.

Controls
--------

All keys can be remapped in *Settings*; only ``Esc`` is reserved.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Default key
     - Action
   * - ``W`` ``A`` ``S`` ``D``
     - Walk. The mouse turns the camera.
   * - ``Shift`` / ``Space``
     - Run (uses stamina) / jump.
   * - ``E``
     - Interact: talk to the nearest character, harvest a tree or rock, drink at a fountain
       or fresh water, fish near water.
   * - ``G``
     - Pick up an item from the ground.
   * - ``I`` / ``C``
     - Inventory / crafting panel.
   * - ``J``
     - Quest log. A compass and markers point to the current quest place.
   * - ``Enter`` / ``F``
     - Chat / friends.
   * - ``M`` / ``P``
     - Minimap / portals.
   * - ``1`` – ``9``
     - Cast the learned spells in list order.

Staying alive
-------------

* **Stamina, water, food and health** are shown in the HUD. Walking and running consume
  stamina; rest restores it. At zero stamina you cannot run; exhausted walking damages health.
* **Food**: eat items from the inventory. Seven real days without eating cause starvation,
  including offline time. Full food lets you heal.
* **Water** falls only while the client is connected. Drink at a settlement fountain or at
  fresh water (lake, river), or eat watery food.
* **Swimming**: wading up to chest depth is slower; deeper water means swimming at a
  fraction of walking speed, without running or jumping. Moving through deep water costs
  stamina and no health. Only a character whose stamina is low (20 or less, the level at
  which the HUD bar blinks) drowns: it loses health, about a minute from full, until the
  stamina is above that level again. Drowning is a cause of death.
* **Death is permanent.** A dead character leaves one memorial (a grave) holding its
  belongings and gold, with an obituary showing the name, days lived, lifetime gold and the
  cause of death; from the second life under a login the name carries its number (``Name II``, in the numerals
  of the world's datadisk, ADR 0021). Other characters may loot a grave. Story quests of datadisks that say so
  restart at a checkpoint instead; see :doc:`quests-and-npcs`.

Gathering and crafting
----------------------

* Trees and rocks are harvested with an axe or pickaxe (``E``); tools wear out and eventually
  break (durability).
* Logs are chopped into wood and crafted into planks; the crafting panel lists recipes from
  the world's ruleset. Some recipes need a station within reach: smelting and cooking at a
  campfire, smithing at an anvil.
* Weapons and armour are crafted from iron ingots and hides. Armour (body, hands) and shields
  reduce damage taken.
* Experience is earned by gathering, crafting and building. Every level adds ten inventory
  slots up to level 30.

Building, farming and fishing
-----------------------------

Characters place campfires, benches, anvils, tents and fences, and plant crops. A fishing rod
catches fish near water. Placed things do not yet block movement and are not yet protected
from other players; bedrolls do not yet let a character sleep (**planned**).

Hunting and combat
------------------

Animals can be hunted with the weapon in hand. Dangerous animals bite back after a hit they
survive, and a creature can kill a character. Animals do not chase and there is **no
player-versus-player damage**. Story characters show a health bar only when hurt; striking one
makes it hostile until a dialogue apology (50 gold) clears the grudge.

Magic
-----

Mana regenerates with time. Six data-driven spells (refresh, firebolt, healing hands, ward,
day, night) are learned from scrolls, which are crafted from quartz and never sold. Spells affect
only the caster and generated animals, never other players, and nothing revives the dead.
The *Day* and *Night* spells move the world's shared solar clock to the caster's next dawn or
dusk, and everyone online is told.

Trading
-------

Merchants buy and sell for gold with a daily sell limit. Players exchange items and gold in a
two-sided confirmed trade. Wayfarers on the footpaths pick up dropped goods and resell them to
the nearest trader. Gold enters the world only through merchants' purchases, story effects and
loot. There is no auction house yet (**planned**). Ships are items sold by shipwrights;
sailing is **planned**.

Social
------

Text chat works within one world (say and whisper). Friends are mutual, show online status and
short-lived event notifications. A player may opt in to showing a flag beside their name.
Blocking and cross-world chat are **planned**. A hall of fame lists the ten most successful
characters, scored ``100 * level + 10 * days lived``.

Where to go next
----------------

* :doc:`quests-and-npcs` – how stories, quests and characters work.
* :doc:`world-overview` – what the planet is made of.
* :doc:`architecture/trading` and :doc:`architecture/gathering` – the rules in detail.
