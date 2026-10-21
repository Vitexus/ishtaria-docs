0018 – Datadisk wildlife overlays and cover / ambient music
===========================================================

:Status: Accepted by the project owner and implemented in the working trees
:Date: 2026-10-18

Context
-------

A datadisk can pin real terrain (ADR 0013, 0017) and play place music, but wild flora and
fauna still come only from the seeded biome map. Historical disks such as Gilgamesh need
date palms and reeds around Uruk without changing the whole planet's climate. Cover art
also had no soundtrack; travel on the plains had no default track outside place radii.

Decision
--------

* A place may declare ``wildlife`` with weighted ``flora`` / ``fauna`` catalog ids,
  optional ``radius_m`` and ``density``. Inside that radius the server picks scenery and
  land animals from those weights instead of the global biome table; ``clear`` and water
  rules are unchanged. An entry may set ``waterside: true`` so it only spawns within about
  60 m of patch water, a river or the sea (crocodiles, waterfowl, gulls).
* The manifest may name ``cover_music`` (logo jingle while the cover shows) and
  ``ambient_music`` (default background outside place music). Both are track ids from
  ``music/*.yaml``. The world announcement includes their media URLs when set.

Consequences
------------

* Gilgamesh (and similar disks) can describe Early Dynastic plant and animal lists in
  research notes and encode them as overlays without a full climate rebuild.
* Clients play the cover jingle with the cover image and fall back to ambient travel music.
