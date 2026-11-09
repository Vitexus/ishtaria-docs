Roadmap
=======

Each milestone produces something that can be installed and played or
operated on its own.

Where we are (November 2026)
----------------------------

The base game exists and is tested: walking on a generated planet, survival, gathering, crafting at
stations, hunting with armour and creatures that bite back, merchants and exchanges between players,
dropping items that NPCs and wayfarers scoop and resell, building, farming, fishing, nearby players
with text chat, magic, graves and permanent death, story datadisks, portals and share links between
worlds. A public server can be limited, observed and backed up, and a contributor can extend the game
with the :doc:`developer guide <development/contributing>`. Since October the game also gained a quest
log, achievements, a photo mode, generated trails and a first vehicle, and a tutorial datadisk; the public
web portal is online. The :doc:`November audit <development/audit-2026-11>` lists where documentation and
code still disagree. M1 is done. Parts of M2 (day and night,
animals) and M3 (inventories, merchants, exchanges between players) exist, but the seasons, the
cell-level ecosystem, player-made currencies and the double-entry ledger are still open, as are M4
to M7 in their full scope. The newest open work is listed in M7a to M9.

Milestones
----------

.. list-table::
   :header-rows: 1
   :widths: 8 30 62

   * - #
     - Milestone
     - Scope
   * - M0
     - Foundations
     - Repositories, Debian packaging, CI, documentation, identifiers and
       ruleset versions in ``ishtaria-core``, cube-sphere generator.
   * - M1
     - Single world, single biome
     - Authoritative server, client connects and walks on generated
       terrain, gathering and primitive crafting, persistence of deltas.
   * - M2
     - Living world
     - Simulation levels of detail, cell-level ecosystem, offline avatars,
       day/night and seasons.
   * - M3
     - Economy
     - Inventories, barter, player-made currency, double-entry ledger.
   * - M4
     - Federation: avatars
     - ``@user:server`` identities, server keys, portals carrying avatar
       and cosmetics only.
   * - M5
     - Federation: items
     - Item provenance, import/export policies, two-phase handover.
   * - M6
     - Federation: currencies
     - Exchange between world currencies with caps.
   * - M7a
     - Content without recompiling
     - The next, smaller step towards M7. Rules that are data today (recipes, spells, shops,
       crops, creatures) are read from a content directory or a datadisk instead of being compiled into
       the server, and items can be defined by data instead of by a migration. Today these files live in
       ``ishtaria-server/etc/`` and are compiled into the binary. Needs a decision
       record for the item catalogue (it is in the database now), validation of foreign content, and
       a way to ship the matching icons and models.
   * - M7
     - Custom content
     - Hash-addressed content packs, fallbacks for unknown kinds,
       sandboxed WASM server logic.
   * - M8
     - Community and visibility
     - Exists: achievements, the hall of fame, the public web portal, a developer guide
       (:doc:`development/contributing`) and a hardened, observable server
       (:doc:`operations/hardening`). Planned: share links for social networks
       (:doc:`decisions/0011-sharing-achievements`, a proposal only), memorial pages, a showcase on the
       web portal, the chronicle of a world, creator tools, a press kit with screenshots and a trailer
       made from the real client.
   * - M9
     - Complete the base game
     - What players of today expect and the game still lacks: skills instead of a single experience
       level, a general hotbar (only a spell hotbar exists), weather and sleeping in a bed, a built-in
       first-run tutorial, graphics and accessibility settings. (A minimap ships: the HUD draws one, and
       a datadisk may hand it a baked picture of a city. A photo mode ships, and the tutorial datadisk
       demonstrates the implemented features, but it is not a first-run flow.) Open design questions: player versus player, animals that chase,
       protection of leased land, collision of placed things.
   * - M10
     - Release on Steam (optional)
     - Only if the project owner decides so: conditions, costs, timeline and the gaps of today are in
       :doc:`development/steam`. The open decisions are the publisher, the platforms and what happens to
       real-money land leases, which Steam does not allow outside its wallet.
