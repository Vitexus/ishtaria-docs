Persistence
===========

Base world is a function
------------------------

At 1 m resolution an Earth-sized height map would have about
5·10\ :sup:`14` samples. Ishtaria never stores it: base terrain is a pure
function of ``(seed, position)``. Only **deltas** are stored.

Stores
------

.. list-table::
   :header-rows: 1

   * - Data
     - Store
   * - Accounts, inventories, trades, currency ledger
     - PostgreSQL (with PostGIS for spatial queries)
   * - Cell deltas, placed objects, aggregate cell state
     - PostgreSQL, indexed by H3 cell id (planned)
   * - Avatars, content packs, large blobs
     - S3-compatible object storage, content-addressed

Current server implementation
-----------------------------

The server connects to PostgreSQL and applies versioned SQL migrations
embedded from its ``migrations/`` directory before serving HTTP requests.
World identities and imported PGM heightmap previews are persisted in the
``worlds`` and ``heightmaps`` tables. Imports are transactional; identical
imports are idempotent and conflicting maps, seeds or rulesets are rejected.

The original PGM, decoded 8-bit samples and SHA-256 checksum are stored for
byte-exact retrieval. This finite preview is not the full procedural planet.
Accounts, the ledger, cell deltas and object storage remain unimplemented.
Schema changes must be added as new migrations, not edits to applied files.

Economy ledger
--------------

Every transfer of currency or traded goods is a double-entry transaction:
nothing appears or disappears without a matching entry. This is also what
makes federated exchange auditable (see :doc:`../federation/items-and-economy`).
