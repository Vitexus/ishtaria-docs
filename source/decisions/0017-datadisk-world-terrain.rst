0017 – Datadisks bring the whole real planet
============================================

:Status: Accepted and implemented; its 8-bit strip superseded by :doc:`0020-generated-relief`
:Date: 2026-10-15

Context
-------

ADR 0013 gives a datadisk the real landscape around a single place, but the planet the story
plays on is still generated from noise: a world made with the Gilgamesh disk puts the cities of
Sumer on invented continents, and the story's own historical geography (ADR 0016) has to be
anchored to whatever coastlines the seed happens to make. For a story whose subject is the real
world (the Epic of Gilgamesh: Mesopotamia, the Cedar Forest of Lebanon, Dilmun, the Persian
Gulf), the disk needs the world itself: the real outline of the continents, the real heights and
the water as it was when the story takes place — for instance the Early Dynastic Persian Gulf,
into which the Euphrates and the Tigris discharge.

Decision
--------

* A datadisk manifest may define ``world.terrain``: two equirectangular rasters below
  ``media/world/`` (see ``ishtaria-protocol/schemas/datadisk.schema.json``):
  ``heightmap``, a 16-bit P5 PGM (maxval 65535, big-endian, width = 2 x height, row 0 at
  +90 degrees, column 0 at -180 degrees) whose pixel is the elevation in metres as a signed
  16-bit value (0 is sea level, bathymetry is negative), and ``water``, an 8-bit P5 PGM of the
  same size (0 land, 255 water) that decides the coastline. Plain PGM keeps the generator free
  of image dependencies; the disk's tooling builds both from open elevation data
  (Gilgamesh: ETOPO 2022, public domain) and a documented historical reconstruction.
* Only one selected disk may define the world; the server refuses a combination of two.
* ``ishtaria-worldgen --earth HEIGHT --water MASK [face_size]`` renders the six-face strip
  from the rasters instead of the noise, with the sphere mapped to the planet's real
  geography as latitude = asin(y) and longitude = atan2(-z, x) (the +Y face is the north
  pole), so the server's compass bearings and historical distances are the real ones. The
  strip kept the standard 8-bit encoding when this was written and is 16-bit since
  :doc:`0020-generated-relief`; the water mask clamps every water pixel at or
  below sea level and every land pixel above it, so shallow seas and dry depressions survive
  the quantisation.
* The seed stays part of the world's identity (it drives the seeded local relief and the
  biomes' moisture) but no longer decides the planet of such a world. As with the seed
  today, the server cannot verify that an imported strip really comes from the disk's
  rasters; ``ishtaria-server-init`` and ``ishtaria-admin`` generate it through
  ``ishtaria-server --print-world-terrain``, which prints the rasters of the selected disks.
* The rasters are part of the disk's content hash, so a changed coastline or river course is
  an identity change of worlds generated with the disk (the same as any other manifest
  change). No migration: worlds already generated keep their stored strip.

* A disk with a real planet may also tell its great rivers (``rivers/<name>.yaml``, a course of
  ``[latitude, longitude, width_m]`` points from the source to the mouth). The coarse map's rivers
  are at most a few tens of metres wide and end where the cell ends, while the Euphrates of the
  Gilgamesh disk is 160 m wide at Uruk and has to run from the Armenian highland to the Gulf.
  The server carves a channel along the course (the profile of the coarse rivers: 2 m deep, the
  water 0.6 m below the ground, ``ishtaria-server`` ``movement::disk_river_carve``), announces it
  in ``GET /world`` (``rivers``, unit directions and widths) and the client carves and draws
  the same line (``surface_environment.gd`` ``set_disk_rivers``). A landscape patch replaces the
  ground under it and carries its own river, so the course passes through the patch's river
  (Gilgamesh: ``tools/build_rivers.py`` takes it from the patch's water mask). The course is
  part of the disk's content hash. The schema is ``river`` in ``ishtaria-protocol``.

Consequences
------------

* The world's map of such a disk shows the real continents, the real ocean floors and the
  reconstructed rivers and shorelines at the base map's resolution (about 10 km per pixel at
  face size 1024, 62.7 m per grey step); the fine relief around a place is still the job of
  the ADR 0013 patches. Everest rounds to 7998 m in the strip.
* Historical reconstructions (the Early Dynastic Gulf shoreline, the rivers' ancient
  courses) are data shipped by the disk and documented there (Gilgamesh:
  ``research/WORLD.md``), not logic of the generator; the generator projects whatever it is
  given.
* The world's climate is still derived from latitude, elevation and seeded moisture; a
  Bronze-Age vegetation (reed banks, palms, wetter Mesopotamia) needs a further extension.
