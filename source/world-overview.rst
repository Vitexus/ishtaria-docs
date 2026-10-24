World overview
==============

Every Ishtaria server hosts **one independent planet**. This page explains what that planet
is made of and how the pieces fit. It describes the implementation of 0.3.0; planned parts are
marked.

A planet in layers
------------------

.. graphviz::

   digraph world {
     rankdir=LR; node [shape=box, style=rounded];
     seed   [label="seed + coordinates"];
     terrain[label="base terrain\n(deterministic, never stored)"];
     env    [label="environment grid\n(biome, heat, humidity, rivers)"];
     objects[label="generated layer\n(trees, rocks, settlements,\nroads, wildlife)"];
     disk   [label="datadisks\n(places, NPCs, quests,\nreal terrain, overlays)"];
     deltas [label="player deltas\n(PostgreSQL)", shape=cylinder];
     client [label="client view\n(/world, /world/objects)"];
     seed -> terrain -> env -> objects -> client;
     disk -> objects; disk -> terrain;
     deltas -> client;
   }

Base terrain
------------

* The planet has roughly Earth's size and is described as a **cube sphere**: six faces of a
  heightmap (``ishtaria-worldgen`` renders them from a seed, ``planet-seed42-256.pgm`` is the
  example). A server imports one map; the importer rejects a conflicting map or seed, so a world's
  terrain can never silently change.
* Terrain is **deterministic**: the base surface is computed from the seed and coordinates and is
  never stored as a planet dump. Only what players change (gathered trees, placed objects, graves,
  inventories) is persisted as deltas in PostgreSQL.
* The imported six-face map is a finite preview, not Earth-scale detail. Up close, **local relief**
  of up to ±12 metres is added so that walking, spawning and scenery agree between server and
  client (environment version 2, double precision before origin subtraction).
* The server announces the atmosphere (sky, sun colour, fog) and the shared solar clock
  (sun and moon direction) in ``GET /world``; the client renders
  the surface sky and a space sky when approaching from space. Local preferences never override it.

Environment: biomes and climate
-------------------------------

A coarse environment grid (at most 64 cells a face, a cell is roughly 150 km on an Earth-sized
planet) carries elevation class, water (ocean, lake, river with upstream flow), heat and humidity.
The generator derives **land biomes** from heat and humidity noise; a datadisk may paint biomes
explicitly (``world.biomes.map``). Biomes decide the vegetation tables in
``etc/world_objects.json`` (lowland palms, olives and figs, cypresses, Aleppo pines, cedars on
mountains, …) and the wildlife in ``etc/world_fauna.json``.

Generated content
-----------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Layer
     - What the generator produces
   * - Scenery
     - All 161 natural Nature Kit variants, 0 A.D. trees and shrubs, rocks, grass, flowers and
       mushrooms. Trees and rocks are harvestable; decorative plants are passable.
   * - Settlements
     - A few dozen hamlets, villages and walled towns (default 36), each with a plaza, houses,
       a trader, gate guard and a graveyard outside the walls. Every fourth town has a
       fortress 300–1200 m away. One in four is founded by the sea; coastal ones get a harbour
       and shipwright.
   * - Roads
     - Footpaths from each town to its graveyard, harbour, pasture and the nearest town within 3 km:
       A* routes over the ground, avoiding deep water, fording shallow rivers and crossing
       deep ones on rope bridges, drawn as stepping stones.
   * - Wildlife
     - Standing and wandering land animals, flying birds, fish swimming in water. Domestic
       flocks graze on pastures with a shepherd. Hunted animals fall and return later.
   * - Water
     - Sea, lakes, ponds and rivers. Wading, swimming and drowning follow the same rule on
       server and client; the client draws local water with a depth-shaded shader.

The world clock
---------------

The sun is astronomical: its position follows the real sidereal day of the planet. The *Day* and
*Night* spells shift the world's shared clock by an offset (``solar_offset_seconds``) relative to
it, and all online players are notified.

Real planets from datadisks
---------------------------

A datadisk may bring its own **real planet** (:doc:`decisions/0017-datadisk-world-terrain`): two
equirectangular rasters (a 16-bit height map in signed metres and an 8-bit water mask) that
``ishtaria-worldgen --earth`` turns into the heightmap strip, mapped to true geography
(latitude = asin(y), longitude = atan2(−z, x)). Only one such disk is allowed in a world.

The Gilgamesh disk uses this to build the **Early Dynastic Earth**: ETOPO 2022 relief with the
Persian Gulf extended to its shoreline of about 2700 BCE and both rivers running into it. Uruk
stands at its historical site (31.3228° N, 45.6389° E). Because the environment grid is coarse,
the cell that holds Uruk, Ur and Lagash is a river cell; the places are pinned by coordinates
and stand exactly where history puts them anyway. Biomes and climate of this world are still
seeded or derived and are **not** part of the reconstruction. Details: the disk's
``research/WORLD.md``.

A datadisk can also add terrain **patches** (the landscape around Uruk, the hunter's water-hole),
wildlife overlays and structures; see :doc:`decisions/0012-datadisk-structures`,
:doc:`decisions/0013-datadisk-terrain` and :doc:`decisions/0018-datadisk-wildlife-and-cover-music`.

Federation
----------

Worlds are separate planets. When two operators agree, players can build **portals** linked by a
share link and cross with a signed, expiring travel ticket (:doc:`federation/index`). The schemas
and examples exist in ``ishtaria-protocol``; the secure end-to-end handover and carrying story
state through portals are **planned**.

Not finished yet
----------------

First physical landing from space, an animated parachute arrival, full mesh physics, sailing,
colliding placed objects and federation handovers are not complete and must not be described as
shipped.

See also
--------

:doc:`gameplay`, :doc:`quests-and-npcs`, :doc:`architecture/simulation`,
:doc:`architecture/persistence`.
