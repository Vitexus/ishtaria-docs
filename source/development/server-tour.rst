Tour of the server code
=======================

``ishtaria-server`` is one Rust binary (axum, SQLx, PostgreSQL). Every gameplay area is a module
with its own ``routes()`` that ``src/main.rs`` merges into the router, a SQL migration for its tables
and, where the content is data, a file in ``etc/``.

How a request is handled
------------------------

A typical action (``POST /players/me/...``) always does the same things in the same order:

#. ``players::player_id(&state, &players::token_hash(&headers)?)`` turns the bearer token into a
   character id (expired, revoked, dead and banned sessions are refused with 401).
#. The request body is parsed into a struct with ``#[serde(deny_unknown_fields)]`` and validated.
#. A transaction starts and ``survival::lock_alive`` locks the character's row. If the character is
   dead the handler returns ``Error::Obituary``.
#. The handler checks position, reach, cooldown and ownership, changes tables and commits, or
   returns an ``Error::Status(code, "fixed message")`` that rolls everything back.
#. The reply is usually ``players::profile(&state, player_id)`` so that the client's HUD and
   inventory are always in step.

Modules
-------

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - File
     - Responsibility
   * - ``main.rs``
     - configuration, router, start-up, world import
   * - ``players.rs``
     - accounts, login, sessions, profile, equipment
   * - ``survival.rs``
     - health, stamina, water, food, ``hurt``, death, graves, obituaries
   * - ``movement.rs``
     - walking, running, jumping, collision, ``/world/objects``, animal routes
   * - ``environment.rs``, ``terrain.rs``, ``atmosphere.rs``
     - local relief and spawning, imported height maps, the sun
   * - ``gathering.rs``
     - harvesting trees and rocks, crafting (``etc/recipes.json``, stations), equipment endpoints
   * - ``durability.rs``, ``experience.rs``
     - wear of tools, weapons and armour; experience and levels
   * - ``creatures.rs``
     - hunting animals, drops, milking (``etc/creatures.json``); also what a spell does to an animal
   * - ``combat.rs``
     - armour, blocking and the bites of dangerous animals (``etc/combat.json``)
   * - ``magic.rs``
     - mana, scrolls, spells (``etc/spells.json``, ADR 0010)
   * - ``placing.rs``, ``fishing.rs``
     - things put into the world, crops, stations, fishing (``etc/placeables.json``)
   * - ``shops.rs``, ``trade.rs``
     - merchants (``etc/shops.json``) and exchanges between players
   * - ``loot.rs``
     - drop and pick up ground piles, NPC scooping, wayfarer errands and merchant stock
   * - ``chat.rs``, ``social.rs``
     - nearby players, say and whisper, friends, the ``/events`` poll
   * - ``portals.rs``, ``federation.rs``, ``land.rs``
     - portals and links, signing and peers, real-money land leases
   * - ``hall.rs``, ``achievements.rs``
     - hall of fame; achievements (``etc/achievements.json`` and the datadisks' ``achievements.yaml``), granted
       inside the earning action, each with its Steam API name
   * - ``scenery.rs``, ``story/``
     - generated towns and props; datadisks, dialogue, quests, NPCs, settlements, wayfarers

Data files (``etc/``)
---------------------

Rules that a designer may change without writing Rust are JSON or YAML compiled into the binary
(``include_str!``) and parsed once at first use; a unit test in the owning module checks that the
file is consistent, and ``configured_items_exist`` checks that every item it names is in the
catalogue. To add one, see :doc:`cookbook`.

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - File
     - Content
   * - ``recipes.json``
     - crafting recipes: inputs, outputs, tool or station, experience
   * - ``resources.json``, ``world_objects.json``
     - what trees and rocks give; the generated object catalogue
   * - ``creatures.json``, ``world_fauna.json``
     - animals: hits, drops, respawn, weapon strength; where fauna lives
   * - ``combat.json``
     - armour defence and slots, dangerous animals
   * - ``placeables.json``
     - things to place, crops, fishing
   * - ``shops.json``, ``trader.yaml``, ``shipwright.yaml``, ``traveler.yaml``
     - merchants and their goods; dialogues of generated traders, shipwrights and wayfarers
   * - ``spells.json``
     - mana and spells
   * - ``portal.json``
     - portal materials

Tests
-----

``src/tests.rs`` holds the shared helpers (``initialize_spawn_world``, ``create_session``,
``player_request``, ``response_json``) and ``src/tests/*.rs`` one file per gameplay area. A test that
needs PostgreSQL is ``#[sqlx::test]`` and ``#[ignore]``; take ``AUTH_TESTS`` so that tests which
register players do not interleave. Look at ``src/tests/trade.rs`` for a test with two players and at
``src/tests/farming.rs`` for one that needs a different world.
