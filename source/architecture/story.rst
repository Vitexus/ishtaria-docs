Story datadisks
===============

See :doc:`../decisions/0008-story-datadisks` for the reasons. This page describes
what exists.

Files
-----

.. code-block:: text

   datadisk.yaml      id, version, requires/conflicts, ruleset, licence, attribution, rating, cover image
   places/*.yaml      sites the generator looks for (city, building, graveyard, landmark, camp)
   npcs/*.yaml        characters at a place: Kenney character, dialogue, portrait
   dialogues/*.yaml   decision trees: text nodes with choices, and automatic branch nodes
   quests/*.yaml      scenarios as stage machines
   lore/*.yaml        codex entries (never spawned)
   music/*.yaml       OGG tracks a dialogue may play
   media/             cover, portraits (PNG/JPEG up to 1 MiB) and music (OGG up to 8 MiB)
   i18n/<lang>.yaml   every text, in every language the disk declares

A dialogue node holds either ``text_key`` with optional ``choices`` or a ``branch``
(first entry whose ``if`` holds; the last has none). Choices have an optional ``if``,
``effects`` and ``goto`` (omitted: the conversation ends). ``once: {key, effects}``
grants its effects the first time only.

Generating a world with datadisks
---------------------------------

Installed disks live in ``/usr/share/ishtaria/datadisks/<id>/`` (override with
``ISHTARIA_DATADISK_DIR``). ``ishtaria-server --list-datadisks`` lists them and
``--check-datadisks a,b`` checks that they can be combined.

* ``ishtaria-admin`` → *World maps* → *Generate map* asks which installed disks the
  world should take into account (nothing is asked when none is installed). The choice
  is stored with the map; *Load* applies it and clears the placed sites.
* ``ishtaria-server-init <seed> <size> <disk-id> ...`` does the same from the command line.

``GET /world`` announces the world's disks (``datadisks``: id, version, name and the
URL of the ``cover`` image when the manifest names one). Covers are public media, so a
client can show them before anyone signs in.

The server places the places on first use (migration ``0026_story.sql`` stores them
in ``story_anchors`` with the heightmap hash) and pins each disk's content hash in
``world_datadisks``.

HTTP API
--------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Request
     - Purpose
   * - ``GET /world/objects`` (``npcs``)
     - Characters near a position: id, name key, character model, position, portrait.
   * - ``POST /story/dialogue/start``
     - ``{npc_id, lang?}``: opens a conversation; the player must stand within 6 m. ``lang`` (two
       letters, never stored) selects the spoken line (``node.voice``, an OGG under ``/story/media``).
   * - ``POST /story/dialogue/choose``
     - ``{npc_id, seq, choice, lang?}``: applies a choice once; a stale ``seq`` is refused.
   * - ``DELETE /story/dialogue``
     - Closes the conversation.
   * - ``GET /story/quests``
     - The player's quests with their current stage.
   * - ``GET /story/markers``
     - Places the player's quests point to (``guide``/``reach`` of the current stage; the ``start_place`` of a
       quest not yet begun only while the player holds the aetherglass), followed by the places the player
       knows from earlier stages (``known: true``, migration ``0060_known_places.sql``).
   * - ``GET /story/strings``
     - Translations of every language (``ETag``).
   * - ``GET /story/media/<disk>/<path>``
     - A portrait or a track named by a loaded disk (``ETag``, ``nosniff``).

Client
------

Characters are drawn with the Kenney character packs and named above the head in the
player's language. ``E`` talks to the nearest one within reach. The dialogue panel
shows the portrait beside the speech and plays the track of the dialogue; music follows
the interface-sound switch of the HUD, and so do the spoken lines of the characters.

Settlements and harbours
------------------------

Independent of any datadisk, every world grows a few dozen settlements (``ISHTARIA_SETTLEMENTS``,
default 36, ``0`` for none). They are places of a built-in disk ``world``: a hamlet, village or
walled town with a plaza, roads and houses (Fantasy Town, Castle and Retro Fantasy Kits), and **a graveyard
outside every settlement** (Graveyard Kit). One in four is founded by the sea; any settlement
that ends up near the sea gets a **harbour** (Pirate Kit: hut, pier, boats and ships) and a
shipwright who sells rowing boats and ships for gold. The shop is ordinary dialogue data
(``etc/shipwright.yaml``); the vessels are inventory items (migration ``0029_ships.sql``), sailing
does not exist yet. Footpaths between towns carry **wayfarers** (``MovementKind::Travel``,
``etc/traveler.yaml``) who pocket dropped goods and sell them to the nearest trader at a
markup; see :doc:`trading`. Datadisk places can ask for the same buildings with
``scenery: {preset: town, size: village}``, ``{preset: graveyard}`` or ``{preset: fortress}``.
Among the modular houses every settlement gets ready-made Quaternius buildings (a temple in
villages and towns, a bell tower and barracks in towns, fantasy houses, houses and towers), placed
with a random stream of their own so the older part of a layout does not move. **A fortress**
(``fort_NN``, a keep inside a ring of 24 stone wall segments with a gate, barracks and towers) stands
300-1200 m from every fourth town; a world generated earlier places its fortresses the next time it
is loaded, and a fortress that finds no room is left out. The server sends the
buildings as ``props`` in ``GET /world/objects``. Walls, fences, towers, gravestones, crates and
the like also block walking: the server keeps round obstacles for them (``scenery::colliders``),
while doors, gates, roofs, piers and ships stay open. Characters of the story are still passable.

Spawn point
-----------

A town of size ``town`` has a wall with a gate on each of its four roads. A child place with
``at: gate`` stands just inside the north gate and ``at: alley`` in a back alley in the far
south-west of the town, about 150 m from the gate and out of the guard's sight and hearing
(``scenery::town_spot``); the generator dresses the alley with crates and barrels and keeps houses
away. The Endland disk puts Faust and the gate guard at the gate and Fawn in the alley.

A place with ``spawn: true`` is where new characters of the world appear (at most one per disk; with
several disks the first in the order of application wins). The server picks a free spot near its centre,
clear of walls, gravestones and characters, the first time a character needs a position; existing
characters stay where they are. The Endland disk makes the old graveyard the spawn point, next to Faust,
so a new character wakes up as in the story's opening. Without such a place the usual safe spawn is used.

Not yet
-------

Character schedules (hours of the day), quest triggers on owning an item at a
given time, collisions with characters, story state travelling through portals,
and carrying a finder's errand through a portal. Walking characters (wander,
patrol, herd, travel), a quest log screen and the ``reach`` trigger -- a stage
moved on by arriving somewhere -- are implemented; see
:doc:`../decisions/0015-datadisk-walking-characters`.
