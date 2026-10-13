0014 – A datadisk may give the player a character
=================================================

:Status: Accepted by the project owner and implemented in the working trees (not yet released)
:Date: 2026-10-13

Context
-------

Every new player chooses a look in the character creator. For a story disk about one hero that makes little
sense: in the Epic of Gilgamesh the player is Gilgamesh, not a stranger with a freely chosen look.

Decision
--------

* A datadisk manifest (``datadisk.yaml``) may set ``player_character``: a character of the creator as
  ``<pack>/<skin>``, for example ``protagonists/criminalMaleA``. See ``datadisk.schema.json``. A disk
  that does not set it leaves the choice to the player.
* The server checks the id when the disk is loaded (an unknown character rejects the disk), announces it in
  ``GET /world`` as ``player_character`` of the disk in ``datadisks``, and **gives it to every new player at
  registration**; the character the client asked for is ignored. When several disks of a world set one,
  the first in the order of application wins, as for ``spawn``.
* The disk may also set ``player_model``: a glTF binary below ``media/models/`` (at most 4 MiB, in metres, a
  skeleton with clips named ``Idle`` and ``Walk``) that clients draw for that character instead of its pack
  look. It needs ``player_character``, which stays the look stored in the profile and the fallback while
  the model loads. The server ships and announces it with the other media of the disk
  (``player_model`` in ``datadisks``).
* ``player_body`` (``height_m`` 0.5 to 8 m, ``toughness`` 1 to 20, needs ``player_character``) says how tall the
  character stands and how much more than a man it endures: clients draw it that tall (the people of the
  creator are 1.8 m) and follow it from higher up and further away, and the server hurts it less when it falls.
  A fall hurts by its landing speed (nothing up to 8 m/s, everything at 21 m/s for a man); for a body ``size``
  times a man's the speeds that count grow with the square root of the size (the drop is compared with the
  body), and the damage is divided by ``toughness``. This applies only to players who have that character, so
  men keep their fragility. An NPC of a disk may carry ``size`` (0.5 to 4) to stand that many times taller
  than its model as authored: gods towering over men.
* The client reads the announcement before the player form is shown: the choice of pack and look is hidden,
  the preview shows the given character, and neither a saved nor the default look can replace it. The player
  still chooses a nickname, password and language.

Consequences
------------

* No database migration and no change of existing players: the rule applies only when a player is created.
  A world that gains such a disk later keeps the looks of its players.
* The profile still holds a character of the Kenney or Quaternius packs. A player model is drawn
  wherever a character with that id is drawn: the creator preview, the own avatar and the other players. It is
  fetched without signing in (story media is public, like covers), so the first moments of a session may show the
  pack look until it arrives; a broken or oversized file is never used. Players who registered with another look
  keep it.
* All players of such a world look alike; nicknames still tell them apart.
* The look cannot be changed afterwards (it could not before either: only registration sets it).
