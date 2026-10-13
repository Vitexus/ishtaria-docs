0016 – Places of a datadisk lie where history puts them
=========================================================

:Status: Accepted by the project owner and implemented in the working trees (not yet released)
:Date: 2026-10-13

Context
-------

A place could be put only *near* another, at a distance within a range and in a random direction, and inside the
radius of its parent. The Cedar Forest of the Epic of Gilgamesh was 1 to 5 km from Uruk, and a temple of Uruk stood
wherever the generator found room. The planet is as large as the Earth, so a story that happens in real places can
put them where they were: the cedars grew in the mountains of Lebanon, 950 km from Uruk.

Decision
--------

* A place may carry ``locate``: ``from`` (another place), ``bearing_deg`` (0 up the map, north, 90 east),
  ``distance_m`` and ``tolerance_m`` (default a twentieth of the distance, at least 30 m). The site is on the great
  circle ``distance_m`` from ``from`` in that direction; the bearing is read in **the frame of the map of ``from``**,
  the frame of its landscape patch and buildings, because the orientation of a generated planet is arbitrary and the
  map of a place must agree with the geography around it. See ``datadisk.schema.json``.
* The planet is not the Earth, so its coasts, mountains and seas lie elsewhere. The server takes the **nearest site that
  satisfies the** ``requires`` of the place: it tries points that spread out from the historical one, within
  ``tolerance_m`` first, then within four times and sixteen times as much, and logs how far from the historical point the
  place had to go. Placement fails, as before, only when there is no fit at all. ``locate`` cannot be combined with ``at``.
* A located place may still have a ``parent`` (so that it does not push its siblings away).

Consequences
------------

* Gilgamesh: Uruk is the place that the generator finds; the Cedar Forest lies 953 km to the west-north-west (292°),
  Mount Mashu 68 km south-east of it, Babylon 177 km north-west (320°), the head of the Gulf 333 km south-east and
  Dilmun 756 km south-east (139°). Inside Uruk the Eanna precinct and the Anu ziggurat stand where the excavations put
  them (217 m at 43° and 244 m at 34° from the middle of the site), the White Temple on the ziggurat, and new players
  appear just inside the Ishtar Gate (1254 m at 178°).
* Journeys of the story are as long as they were: 950 km to the Cedar Forest is some 65 hours of walking. Faster travel
  (ships, portals, caravans) is a separate decision.
* A different planet may put a place further from its historical point. Disks should therefore keep the
  ``requires`` of a located place loose.
