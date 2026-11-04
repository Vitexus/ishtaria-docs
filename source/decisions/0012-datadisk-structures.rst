0012 – Datadisks bring buildings of their own
=============================================

:Status: Accepted by the project owner and implemented in the working trees (not yet released)
:Date: 2026-10-13

Context
-------

A datadisk could place only the generated scenery presets (``town``, ``graveyard``) at its places.
The Gilgamesh disk ships models of the Anu ziggurat, the Etemenanki and the walls of Uruk built to match the Ishtar
Gate, which could not be shown, and the generated medieval town of Uruk did not fit its time.

Decision
--------

* A place may carry a ``structure`` instead of ``scenery``: a self-contained glTF binary below ``media/models/``
  (at most 4 MiB, in metres, +Y up), with optional ``collision`` (a simpler model), ``scale_m``, ``yaw_deg``,
  ``offset_m``, ``ground_m`` (the point of the model that stands on the terrain, such as the foot of its stairs),
  ``visible_m`` (how far away the server announces it) and ``at_sea`` (stand at mean sea level for ships and
  floating docks, with no mesh collider). See ``datadisk.schema.json``.
* The server announces the building as a prop whose model is ``disk:<disk>:<media path>``; the client fetches the file
  from ``/story/media`` (as for character models), draws it when it arrives and caches it.
* Characters walk **by the mesh** of the building: the server reads the triangles of the glTF
  (``src/glb.rs``), keeps them as a collision mesh and moves a character near a building with the swept capsule.
  A step of up to 0.7 m is climbed without jumping and stairs up to about 45 degrees are walkable, so ziggurats can be
  climbed, gate passages walked through and wall walks reached by their stairs.
* The parts of a generated town that would stand inside a building are left out. A disk that wants no generated
  town simply gives its city place no ``scenery``.

Consequences
------------

* No database migration: props derive from the disk and the persisted place anchors. A changed disk needs the usual
  re-pinning.
* The model stands at the terrain height at its ``ground_m`` point; on uneven ground the rest of the building may
  float a little or sink. Models should carry a foundation below their ground plane. With ``at_sea: true`` the
  radial height is mean sea level (0 m), matching generated harbour props.
* Only characters are walked by the mesh, not animals; there are no doors, interiors or destruction.
* Walking by the mesh happens only within reach of a building (its bounding radius and 4 m); elsewhere movement is
  unchanged. A building of a datadisk is a large mesh and is a cost for every client in range, hence the size limit.

Addendum: many buildings (``buildings/*.yaml``)
-----------------------------------------------

A city of thousands of houses cannot be thousands of places, so a disk may list buildings around the anchor of one of its
places in ``buildings/<name>.yaml`` (``datadisk.schema.json``, ``$defs/buildings``; at most 6000 items, each file at
most 1 MiB). Each item names a glTF binary of the disk (origin in the middle of its footprint on the ground, front
``+Z``), a position ``x``/``z`` in metres east and south of the anchor (the frame of ``structure.offset_m``), a compass
bearing ``yaw_deg`` for the front, a ``scale`` per model axis (a house fitted to its plot) and the ``footprint`` of the
plot. The Uruk file is written by ``tools/build_buildings.py`` from the city plan, which also decides which houses stay
in the quarter models (``tools/city_kinds.py``).

* The server announces every item as a prop like a structure, standing on the lowest ground under its footprint, sunk
  1 m into it (the 0 A.D. houses are made to be raised on a slope, their walls end at the floor), and
  turned by ``pi - bearing``; the prop carries ``scale_xyz`` (and ``scale_m``, the largest of the three, for clients that
  do not know it). Visibility is 400 m.
* A building blocks walking with round colliders (radius half the shorter side, at least 1 m, up to four along the
  longer side), not with its mesh: thousands of meshes would cost every client and every step of every character.
* An item whose model the disk does not ship is left out and logged; an unknown place, a bearing outside 0..360 or a
  scale outside 0.05..20 rejects the disk.

Addendum: the sky of a disk's world (``astronomy``)
---------------------------------------------------

A story may happen in another age or on another planet, so the manifest has an optional ``astronomy`` mapping
(``year``, ``obliquity_deg``, ``sidereal_day_seconds``; all optional, default today's Earth). The ``year`` is the
astronomical year (2700 BCE is ``-2699``) and gives the axial tilt (Laskar 2004 polynomial: 24.0 degrees in 2700 BCE,
23.8 in 700 BCE, 23.44 today) and the precession of the star field (general precession in longitude, Capitaine et al.
2003: the field is turned 65-66 degrees against today's in 2700 BCE, when Thuban was the pole star). ``obliquity_deg``
and ``sidereal_day_seconds`` override the tilt and the length of the planet's turn (another planet).

* The server (``atmosphere.rs``) applies the sky of the world's disk to the sun and the moon and announces it in
  ``GET /world`` ``solar`` as ``obliquity_degrees``, ``precession_degrees`` and ``sidereal_day_seconds``; the client
  (``planet_sky.gd``) checks the announced sun against its own computation with those values and turns the star map
  (``planet_sky.gdshader``, ``precession``) accordingly. Without ``astronomy`` nothing changes.
* The sun's seasons still follow the real date, only the tilt, the turn and the star field are those of the disk. The
  year and the month are those of Earth: a planet with another year or moons needs orbital elements, which a disk
  cannot give yet.
* Only one disk of a world should set it; the first disk that does decides.
