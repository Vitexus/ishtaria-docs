Quests and characters
=====================

Stories in Ishtaria are **data, not code**. A story datadisk lists places, characters,
dialogues and quests; the server places them in the world and evaluates every effect, the
client only shows what the server announces. This page explains the player's view and the
authoring model. The file formats are in :doc:`architecture/story` and
:doc:`decisions/0008-story-datadisks`; the schema is ``ishtaria-protocol/schemas/datadisk.schema.json``.

The pilot disks
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Datadisk
     - Content
   * - ``ishtaria-datadisk-gilgamesh``
     - The Epic of Gilgamesh on the Early Dynastic Earth: about 400 places, 190 characters,
       70 dialogues and 11 quests, with Czech and English text and spoken lines. Uruk is drawn from a plan
       of the real city (walls, gates, streets, thousands of houses, canals, fields and a quay on the
       Euphrates) and has a map of its own.
   * - ``ishtaria-datadisk-endland``
     - The End Land: the town of Udrury, the Blackhorn Tavern and an old graveyard where new
       characters wake up.
   * - ``ishtaria-datadisk-tutorial``
     - Four places, 12 characters and two quests that demonstrate every implemented feature.

Datadisk artwork belongs to its author; it is not bundled client material.

Talking to characters
---------------------

A character stands at a place chosen by the world generator. Walk up to one (within 6 m) and
press ``E``: a dialogue panel opens with the portrait, the text and the choices. A line is
spoken aloud when the disk ships a recording (``media/voice/<language>/<text_key>.ogg``,
rendered with Piper when the package is built); the interface-sound switch also mutes voices.
The client may send the language it wants **per request**, and the server answers in it; the
server never stores a language.

Characters are passable and static in the current version. Story characters show a health bar
only when hurt, and striking one makes it hostile (see :doc:`gameplay`).

*Tell me about yourself.* A character with a knowledge card offers a button that shows a
public-domain picture, a short text and a link to the Wikipedia article in the client's
language, opened only after confirmation (:doc:`decisions/0019-knowledge-cards`). The generated
trader, gate guard, shepherd and shipwright and the tutorial's Hammerin have cards, and the
Gilgamesh disk ships 51 of them in its ``knowledge.yaml`` -- twelve on characters and the rest on
readable structures. The Endland characters have none yet.

Dialogue model
--------------

A dialogue is a decision tree. A node holds a ``text_key`` with optional ``choices`` or a
``branch`` list (the first entry whose ``if`` holds is taken, the last has none). A choice may
have an ``if`` condition, ``effects`` and a ``goto``; with no ``goto`` the conversation ends.
``once: {key, effects}`` applies its effects only the first time a player takes it.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Conditions (``if``)
     - ``flag``, ``quest_stage``, ``has_item``, ``gold_at_least``, combined with ``all``,
       ``any`` and ``not``. The server also offers the flag ``festival:akitu`` while the Mesopotamian New Year is on
       (the first new moon after the spring equinox and the eleven days after it, counted from the sky, never stored).
   * - Effects
     - ``give_item``, ``take_item``, ``gold``, ``set_flag``, ``set_stage``, ``once``,
       ``flourish``, ``set_playable`` (switch the character you play), ``teleport_place`` and
       ``reveal_places`` (a character tells you where places lie: they stay on your map and compass).

Effects are applied by the server in one transaction; a stale or repeated choice is refused.
That keeps rewards honest: a client cannot grant itself gold or items.

Quests
------

A quest is a **stage machine**: each stage has a text, optionally a place to ``guide`` the player
to (or ``reach``), and a ``final`` flag. Dialogue effects move the quest between stages with
``set_stage``. The *quest log* (``J``) lists the player's quests and the current stage. Markers
and a compass point to the place of the current stage. A place the player has been sent to (or where
one of his quests began) stays on the map and compass as a *known place* after the quest moves on.
A quest that has not begun points to its ``start_place`` only once the player has the aetherglass
item (the Endland intro gives it; the Gilgamesh disk does not, so unknown quests stay hidden).

A stage may also be moved on by reaching a place (``reach``, ``story/api.rs`` ``advance_reach``),
which five stages of the Gilgamesh questline use, and the hunting quest is carried by the snares
of ``etc/traps.json``. Not implemented yet: schedules for characters, and carrying story state
through portals.

A worked example: the Epic of Gilgamesh
---------------------------------------

The Gilgamesh disk is a **finite narrative**, a short arc rather than a grind. The player
plays several protagonists in turn: the hunter at the water-hole, then Šamḫat, then Enkidu
and finally Gilgameš. The hunter asks at the market of Uruk where the king is to be found and
walks to the palace; whoever dies in Uruk with the king's errand returns to the palace. The disk ships eleven quests:

* The Hunter and the Wild Man
* Šamḫat and the Wild Man
* Enkidu's Awakening
* Enkidu and the King
* The Meeting of Equals
* The Tyranny of Gilgamesh
* The Cedar Forest Journey
* Ishtar's Wrath
* The Death of Enkidu
* The Search for Immortality
* The Return to Uruk

Long journeys (the Cedar Forest, Dilmun) use story travel (``teleport_place``) instead of
walking real distances. If the character dies or a quest fails (for instance Šamḫat on the
road), what happens depends on the quest:

* Without an active quest, or still on its first stage, the death is permanent and leaves a
  memorial with the inventory, as anywhere else in the game.
* Past the first stage the active quest **restarts at its checkpoint**: the character returns,
  with full reserves and the stage kept, to where the quest last changed its stage (recorded by the
  server whenever a stage changes), or to the quest's ``start_place`` when that spot is unknown or
  under water. A stage's ``fail_restart`` names the stage and place to return to instead. Everything
  gained since the checkpoint is lost: each item, gold included, goes back to what was carried
  then; what was used up meanwhile stays used.

The server-side logic is in ``ishtaria-server/src/story/checkpoint.rs``.

Uruk, Humbaba's lair, the Scorpion Gate and other places are pinned to their historical sites
on the disk's real planet (``geo: latitude/longitude``) and stand exactly there; see
:doc:`world-overview`.  The research behind the questline is in the disk's
``research/`` directory.

Where and when a character stands
---------------------------------

A character stands at its ``place``. Two optional fields change that:

* ``visible_if`` (a condition, the same as in a dialogue choice): the character is in the world, and can be talked to, only for
  a player of whom it holds, so a character the story has not brought forth yet is not there. The Gilgamesh disk keeps the
  civilized Enkidu out of Uruk until Šamḫat has brought him.
* ``lift_m``: metres above the ground at which a character without a walk stands, such as the goddess and her priests on the top
  platform of the stepped tower of Ishtar, whose stairs a player climbs.

What a character knows follows the story: a character speaks of an event only once the player has got there (a branch on the
quest stages), and before that gives an answer without it, so that no dialogue spoils what is still to come.

A landscape patch may carry a ``map`` (an RGBA picture over the same rectangle as its rasters) that the minimap draws: the walls,
streets, houses and canals of a city (the Gilgamesh disk draws Uruk from its plan with ``tools/build_map.py``).

Generated characters
--------------------

Independent of any disk, every world grows a few dozen settlements. Each has a **trader**
(goods in ``etc/shops.json``), a **gate guard**; coastal ones have a **shipwright**, and
settlements keep a flock cared for by a **shepherd** who drives it from the fold to the pasture
and home on a cycle of about twelve minutes. Wayfarers walk the footpaths between towns.

Writing a datadisk
------------------

#. Copy ``ishtaria-datadisk-tutorial`` and edit ``datadisk.yaml``.
#. Add places, characters, dialogues and quests; put every text under ``i18n/<lang>.yaml``.
#. Check the disk: ``python3 ../ishtaria-protocol/tests/validate_datadisk.py .``
#. Install the package to ``/usr/share/ishtaria/datadisks/<id>/`` and generate a world with it
   (``ishtaria-admin`` or ``ishtaria-server-init <seed> <size> <id>``).

A disk's version and content hash are pinned to the world; **changing a disk means generating
a new world**.
