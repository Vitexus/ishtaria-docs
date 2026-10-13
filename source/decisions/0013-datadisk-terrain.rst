0013 – Datadisks bring local terrain
===================================

:Status: Accepted by the project owner and implemented in the working trees (not yet released)
:Date: 2026-10-13

Context
-------

The planet's base terrain is an eight-bit six-face heightmap of an Earth-sized sphere (about 10 km
per pixel at the largest face size and 62.7 m per grey step), so the relief around a story place —
a river bank, a tell, a plain around a city — is far below its resolution. The Gilgamesh disk
wants the real landscape of Uruk: the relief preserved from the Mesopotamian floodplain (taken
from open elevation data), with the Euphrates returned to its Early Dynastic course, because the
channel has moved tens of kilometres in the five thousand years since. OpenStreetMap holds the
hydrography and the archaeological sites but no elevation; the relief comes from the Copernicus
DEM.

Decision
--------

* A place may carry ``terrain``: a landscape patch anchored at the placed place. See
  ``ishtaria-protocol/schemas/datadisk.schema.json``:
  ``heightmap`` (16-bit greyscale PNG below ``media/terrain/``, at most 4 MiB) whose values are
  decimetres **above the anchor's placed height** (0x8000 = the anchor), an optional ``water``
  mask of the same size (0 = dry land, otherwise the water surface in decimetres above the
  anchor, 0x8000 = the anchor), ``extent_m`` (the rectangle in the local x/z frame), ``offset_m`` (its centre from the
  anchor) and ``feather_m`` (default 100).
* Heights are relative, never absolute metres above sea level: the patch must land on any world
  whose base terrain satisfies the place's ``requires``. The server samples the patch inside
  ``World::height`` and blends it into the base terrain plus procedural relief across the
  feather margin, so there is no seam and the disk stays portable between worlds.
* Water of the patch (a river at its historical course) takes part in the same checks as
  generated lakes: drinking, fishing and keeping spawns and buildings on dry land.
* The server announces the patch through ``/world/objects`` when the player is within its reach:
  anchor coordinates, extent, feather and the media URLs of the PNGs. The client fetches them
  from ``/story/media`` (as for models and portraits) and overrides its local elevation and water
  sampling, so its detail mesh, walking and minimap agree with the server.
* The patch is data of the disk, not world state: no migration. Like structures, it hangs on the
  persisted place anchor (``height_m``); a changed landscape file needs the usual re-pinning.

Consequences
------------

* The place's own ``requires`` (slope, height range, biome) still apply to the **base** terrain,
  because the generator finds the anchor before any patch exists. Disks must demand flat-enough
  base ground for a landscape whose relief is metres, or accept a small cliff at the feather
  margin.
* A patch overrides the procedural relief inside its rectangle; no other biome, climate or
  generated scenery changes. Generated settlements inside the rectangle may stand on patched
  ground; a disk that wants none gives its city no ``scenery``, as Uruk does.
* The patches are loaded before anything is put on the ground: structures, NPCs and the spawn stand on
  the patched terrain, not on the base map below it. A model's height is taken at its origin (or
  ``ground_m``), so a datadisk building that spans relief (a city wall) follows the patch by carrying the
  patch's heights in its own geometry, relative to that point.
* Generated scenery never stands in the water of a patch, and fish swim where the mask says water (and
  it is at least three metres deep); other animals do not know the patch.
* The patch's local frame is the client's: +x east, +z south when the map is drawn with east to the
  right (the frame is right-handed with +y up), row 0 of the PNGs is the smallest z.
* Elevation data derived from Copernicus DEM and OpenStreetMap must be attributed in the disk's
  ``attribution`` (Copernicus DEM licensed under the ESA terms, OSM under ODbL), like any other
  third-party content.
