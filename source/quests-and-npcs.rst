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
     - The Epic of Gilgamesh on the Early Dynastic Earth: 244 places, 70 characters,
       36 dialogues and 11 quests, with Czech and English text and spoken lines.
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
trader, gate guard, shepherd and shipwright and the tutorial's Hammerin have cards; the
Gilgamesh and Endland characters do not yet.

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
       ``any`` and ``not``.
   * - Effects
     - ``give_item``, ``take_item``, ``gold``, ``set_flag``, ``set_stage``, ``once``,
       ``flourish``, ``set_playable`` (switch the character you play) and ``teleport_place``.

Effects are applied by the server in one transaction; a stale or repeated choice is refused.
That keeps rewards honest: a client cannot grant itself gold or items.

Quests
------

A quest is a **stage machine**: each stage has a text, optionally a place to ``guide`` the player
to (or ``reach``), and a ``final`` flag. Dialogue effects move the quest between stages with
``set_stage``. The *quest log* (``J``) lists the player's quests and the current stage. Markers
and a compass point to the place of the current stage. A quest that has not begun points to its
``start_place`` once the player has the aetherglass item.

Not implemented yet: schedules for characters, quest triggers other than dialogue, and carrying
story state through portals.

A worked example: the Epic of Gilgamesh
---------------------------------------

The Gilgamesh disk is a **finite narrative**, a short arc rather than a grind. The player
plays several protagonists in turn: the hunter at the water-hole, then Šamḫat, then Enkidu
and finally Gilgameš. The disk ships eleven quests:

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
road), the active quest **restarts at its checkpoint** (``fail_restart``) instead of ending in a
permanent memorial; the server-side logic is in ``ishtaria-server/src/story/checkpoint.rs``.

Uruk, Humbaba's lair, the Scorpion Gate and other places are pinned to their historical sites
on the disk's real planet (``geo: latitude/longitude``) and stand exactly there; see
:doc:`world-overview`.  The research behind the questline is in the disk's
``research/`` directory.

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
