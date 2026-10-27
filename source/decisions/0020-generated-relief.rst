0020 – Relief is generated into the world map
=============================================

:Status: Accepted by the project owner and implemented in the working trees (not yet released)
:Date: 2026-10-27

Context
-------

Environment version 2 adds a continuous local relief of up to +/-12 m (``surface_environment.gd``,
``relief64`` added to the base elevation). The relief is computed on the client and the server
separately from the seed, on top of the persisted six-face heightmap. The coarse globe that the
surface meshes sit on has no relief, so shadows cast by the relieved scenery land on the unrelieved
surface and appear to sink below the ground. Making the shadow receiver follow the relief would
only hide the symptom: the world would still be two surfaces that must agree.

Decision (proposed)
-------------------

* The relief is generated into the world's height map when the world is generated, not added at
  run time. ``ishtaria-worldgen`` writes the relief into the strip; the server and the client read
  one height per point. Walking, scenery, spawns, water and the shadow receiver then use the same
  surface.
* Datadisks take part at generation time. A disk may force features (for example a landscape
  patch from ADR 0013, a river course or a hill) into the generated map before the places are
  placed, so its ``requires`` are checked against the final terrain. This replaces the run-time
  patch sampling in ``World::height``.
* The game is in early development and has no compatibility promise. Remote instances are replaced
  completely, with their database and newly generated world maps. The run-time relief of environment
  version 2 is removed from the server and the client, and no migration keeps old strips or old
  environment versions.
* The seed still identifies the world, and the relief is still deterministic from the seed and the
  coordinates, so terrain is generated and not stored as a planet dump (AGENTS.md).

Choices
-------

1. **Precision (chosen: a 16-bit strip for new worlds).** The strip is 8-bit with a step of 62.7 m (ADR 0017), but the relief is about
   +/-12 m. Baking the relief into that strip would flatten it. Options: a 16-bit strip for new
   worlds (double the size of the height file and of the transfer), or a separate relief layer at
   1 m or finer, stored next to the strip and summed by the server and the client.
2. **Old worlds (chosen: regenerate them).** Remote instances are reinstalled with their database
   and newly generated maps (project owner, 2026-10-27), so no old world needs to keep working.
3. **Shadow receiver (to measure after implementation).** Once the relief is in the map, the detail meshes and the shadow receiver
   come from the same heights. The cascade distance of the sun (``main.gd``, 250 m) and the
   relief's effect on shadow bias should then be measured again.

Consequences
------------

* The worldgen, server and client change together. A world's identity changes with its new
  height map, so existing worlds are not loaded after the change.
* The datadisk contract grows: a disk declares forced features for generation, so the
  ``world.terrain`` and ``terrain`` manifest entries need a new version and a migration note in
  ``ishtaria-protocol``.
* Implementation: ``ishtaria-worldgen`` writes the 16-bit strip (``strip`` and ``relief`` modules;
  ``--seed`` is required with ``--earth``), the server reads it (migration
  ``0058_sixteen_bit_heightmaps.sql``, environment version 3, ``/world/heightmap.png`` removed),
  ``ishtaria-server-init`` and ``ishtaria-admin`` pass the seed to worldgen, and the client reads
  ``/world/heightmap`` with a progress bar on the datadisk cover. Datadisk features forced at
  generation (beyond the real planet of ADR 0017) are still planned.
