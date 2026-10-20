0019 – Characters tell what they know: knowledge cards
======================================================

:Status: Accepted by the project owner and implemented in the working trees (not yet released)
:Date: 2026-10-20

Context
-------

The game should teach a little. Every character a player talks to is a person from some trade or time, so it
can tell something true about itself: a short summary, one picture and the way to the article that says more.

Decision
--------

* **"Tell me about yourself"** is a button of the dialogue panel, offered by the client for every character that
  has a *knowledge card*. It is not an authored dialogue choice, so no dialogue has to be edited and it is
  offered at every node. A character without a card does not offer it.
* A **card** (``knowledge.yaml`` at the root of a datadisk, ``etc/knowledge.yaml`` for the generated characters)
  has an ``id``, ``title_key``, ``text_key`` (two to four sentences), ``image`` (a png or jpg below
  ``media/knowledge/``, at most 1 MiB), ``credit_key`` (author, work and licence of the picture) and
  ``wikipedia``: the title of the article by language, English required. A character names its card with
  ``about``. Cards are shared by id, so several characters may tell the same one.
* ``GET /story/npcs/{id}/about`` answers (token, the player within talking reach) with the keys, the media path
  of the picture and the article titles. **The server never stores a language and chooses none**: texts are keys of
  ``/story/strings`` and the client picks the language of the text and of the article. The dialogue reply says
  whether a card exists (``about``). No migration.
* The client shows the picture in place of the portrait, the text, the credit and two buttons: back to the
  conversation and "Read more on Wikipedia". The address is ``https://<language>.wikipedia.org/wiki/<title>`` with
  the language of the interface (English when the card has no article in it), and the browser is opened **only
  after the player confirms** a dialog that shows the address. Titles must hold no URL syntax (schema, server and
  client all check), so the host is always Wikipedia.
* Pictures are **shipped in the package** (the server's ``assets/knowledge/`` for generated characters, the
  datadisk's ``media/knowledge/``), never loaded from Wikipedia at play time: no outside traffic, no tracking of the
  player, and the licence is known. Only public-domain or freely licensed pictures; author, work and licence go
  into ``credit_key`` and into ``debian/copyright``.
* The generated characters (trader, gate guard, shepherd, shipwright) tell cards of the server. A card whose picture
  is not installed is left out and its character has no such option.

Consequences
------------

* Writing a card is data: a text in each language, a picture with its credit and two article titles.
* The text is the author's to keep true; the article is the reader's way to the rest.
* Planned: cards for the characters of the Gilgamesh and Endland disks and for places and animals.
