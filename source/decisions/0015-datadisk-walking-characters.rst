0015 – Characters of a datadisk may walk
=========================================

:Status: Accepted by the project owner and implemented in the working trees (not yet released)
:Date: 2026-10-13

Context
-------

The characters of a datadisk stood at their places and never moved, so a guard did not guard, a farmer did not
plough and a wild man did not roam. The animals of the world already walk: their positions depend only on their id
and the time, so nothing is stored and every process agrees. Characters can use the same idea.

Decision
--------

* A character (``npcs/*.yaml``) may carry ``movement``: ``kind`` ``wander`` (walks to spots on land within
  ``radius_m`` of where it stands, standing ``pause_s`` between walks) or ``patrol`` (walks the loop of
  ``waypoints``, metres east and south of its place as ``offset_m`` of a building, standing ``pause_s`` at each),
  and ``speed_m_s`` (0.2 to 8). A character that keeps a shop (tag ``shop:<id>``) cannot walk. See
  ``datadisk.schema.json``.
* Where a character is depends only on its id, its place and the time; a patrol starts at a point of its loop that
  depends on the id so that several guards do not walk in step. Nothing is stored and no migration is needed.
* ``GET /world/objects`` sends each walking character that is near (as far as it can walk, twice over) with a route
  ``wander``: waypoints ``[unix milliseconds, x, y, z]`` in metres that cover the next minute and a half (at most
  36), the same form as the routes of animals; ``position`` is where it stands now. The client walks the character
  along the route, turned towards where it goes, with the ``Walk`` clip of its model while it moves and ``Idle``
  while it stands, asks again every half minute, and keeps its entry at the place it is: talking to it, the minimap
  and the quest compass find it where it is.
* The server checks the reach of a conversation against where the character is now. Once a conversation is on, a
  walking character may have walked on while the player reads: it then counts as near within 25 metres.

Consequences
------------

* Walkers keep to land and to the ground of the world (heights are those of the terrain, patches included) but do
  not avoid obstacles: a route may lead through a wall or a fence. Disks keep patrols to open ground and
  wanderers' radii to what is free around their place.
* The compass markers of a quest point at the place of the character, not at where it walks.
* A character of a datadisk is a character, not a creature: it has no combat. Hostile creatures of a datadisk are
  a separate decision.
