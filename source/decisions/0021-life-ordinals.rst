0021 – The number of a life on a memorial
==========================================

:Status: Accepted by the project owner and implemented in the working trees (not yet released)
:Date: 2026-11-03

Context
-------

Death is permanent, but a login may be used again: the next character of the same name is a new life. On the
memorial two stones of the same name look alike. Rulers solve this with a number after the name (*Charles II*).
The Gilgamesh datadisk wants that number written in Sumerian (cuneiform) numerals; other worlds do not.

Decision
--------

* The server counts the lives of a login per world: ``players.ordinal`` is set at registration (one more than the
  characters of that name before it) and copied to ``graves.ordinal`` (migration ``0068_life_ordinal.sql``; a
  memorial's number is permanent like the rest of it). The login itself does not change.
* The first life carries no number. The obituary (``GET /graves/{id}``, the death answer) has ``ordinal`` from
  the second life on; the memorial shows ``Name II``.
* The server stores a **count**, never a script or language. How it is written is the client's choice. The engine
  default is Roman numerals (``life_ordinal.gd``; a number above 3999 stays decimal).
* A datadisk may choose another system in its manifest: ``ordinal_numerals: sumerian`` (``roman`` or
  ``sumerian``) and ``ordinal_font``, a ``.ttf`` or ``.otf`` below ``media/fonts/`` (at most 1 MiB) that
  carries the glyphs; ``sumerian`` requires the font. They are announced in ``GET /world`` ``datadisks``; the
  client fetches the font from the story media route and draws it as a fallback of the theme font.
* Sumerian numerals are sexagesimal: U+1230B (ten) and U+12079 (one) repeated within a place of up to fifty-nine,
  places separated by a space. The Gilgamesh disk ships Noto Sans Cuneiform cut to those two signs
  (SIL OFL 1.1, ``media/fonts/License-noto.txt``).

Consequences
------------

* Existing characters are numbered by their registration order in a migration; the graves follow their players.
* The hall of fame and the 3D memorial do not show the number yet; only the memorial panel does.
* Only the manifest and the client know about numeral systems; adding another means one more entry in
  ``ordinal_numerals``, its glyphs in the client's ``LifeOrdinal`` and the schema in ``ishtaria-protocol``.
