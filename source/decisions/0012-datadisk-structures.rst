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
  ``offset_m``, ``ground_m`` (the point of the model that stands on the terrain, such as the foot of its stairs)
  and ``visible_m`` (how far away the server announces it). See ``datadisk.schema.json``.
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
  float a little or sink. Models should carry a foundation below their ground plane.
* Only characters are walked by the mesh, not animals; there are no doors, interiors or destruction.
* Walking by the mesh happens only within reach of a building (its bounding radius and 4 m); elsewhere movement is
  unchanged. A building of a datadisk is a large mesh and is a cost for every client in range, hence the size limit.
