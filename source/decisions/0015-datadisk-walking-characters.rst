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

* Walkers keep to land and to the ground of the world (heights are those of the terrain, patches included) and
  **do not walk through obstacles** (2026-10-13): a walk whose straight line would meet a wall of a datadisk's
  building (its collision mesh), a fence, a tree or a rock (steps up to 0.7 m are climbed) is not made. A wanderer
  then goes to its home first and from there to the next spot, a spot it cannot reach in a straight line from home is
  not chosen, and a patrol whose leg is blocked goes by its place. A disk keeps patrols to open ground and a
  wanderer's radius to what is free around its place all the same: the route is a straight line, not a path-finder.
* The compass markers of a quest point at the place of the character, not at where it walks.
* A character of a datadisk is a character, not a creature: it has no combat. Hostile creatures of a datadisk are
  a separate decision.

Addendum: a character that is talked to stands still (2026-10-13)
-----------------------------------------------------------------

* While a player talks to a walking character it stands still, turned to the player, and afterwards goes on to where it
  was going. The walk of a character depends only on the time, so the conversation stops the *character's own clock*
  (migration ``0040_npc_pauses.sql``): the table keeps, per character, how long it has stood in earlier conversations
  (``shift_ms``) and the current stop (``pause_from_ms`` to ``pause_to_ms``). The time of the walk is ``now`` less the
  time stood, so it is continuous: the character resumes exactly where it stood and nothing jumps.
* ``POST /story/dialogue/start`` and every answer open or renew the stop (five minutes ahead, so that a client that is
  gone does not stop the character for good); leaving the conversation (``DELETE /story/dialogue``) or reaching its
  end closes it at once. Routes in ``GET /world/objects`` are given in real time (shifted by what the character has
  stood) and, while it stands, are two waypoints at its position.
* The client keeps the character in conversation where it is and turns it to the player (a character that only stood
  turns back afterwards), and after the conversation asks for the routes again, so the next route goes on from where it
  stood. If the answer does not come within four seconds it goes on by the route it has.

