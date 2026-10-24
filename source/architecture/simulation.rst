Simulation and persistent time
==============================

A full-fidelity simulation of an Earth-sized planet is impossible. Ishtaria
spends detail only where it is observed.

Levels of detail
----------------

.. list-table::
   :header-rows: 1

   * - Level
     - Where
     - What is simulated
   * - L0 – active
     - around players
     - individual animals and plants, rigid-body physics, 20–60 Hz
   * - L1 – near
     - surroundings
     - individual entities, simplified behaviour, no physics
   * - L2 – aggregate
     - everywhere else
     - per-cell populations (predator–prey, vegetation growth), weather,
       seasons; steps of minutes to hours

Catch-up
--------

When a player enters an L2 cell, the server **materialises** concrete
individuals from the aggregate state and a deterministic seed. To an
observer the result is indistinguishable from continuous simulation, at a
fraction of the cost.

Offline players
---------------

Time runs while players are away.

* The avatar stays in the world, asleep, and keeps its needs (hunger,
  warmth).
* Shelters protect sleeping avatars; designing them well is essential,
  otherwise logging out becomes punishing.
* Property – fields, animals, workshops – continues at L2 fidelity.

.. todo:: Decide penalties and protections for avatars sleeping outdoors.

Inventory, survival and permanent memorials
-------------------------------------------

The server persists a permanent UUID for each character. A new character starts
with 100 gold coins, four food stacks and 100 inventory slots, granted once on
creation. Gold coins are inventory items stacking to 10,000 per slot; unlike
other items they may occupy several slots (migration ``0015_gold_in_inventory.sql``). capacity increases by ten per level after the first and through
carried bags or suitcases. Food items have distinct calorie values. Eating is an
authenticated intention; the server consumes an owned item and updates nutrition.
Seven real days without eating cause starvation, including offline time.
Water is different: a sleeping (disconnected) character loses none, only time while
the client is connected is charged. Some food, such as an apple, restores a little
water; a fountain in a settlement or fresh water (lake or river) restores more when
the character drinks within reach.

Death is permanent. It revokes every session and transfers remaining possessions
to a grave atomically. Correct credentials for a dead character return an obituary,
not a session. Continuing requires a new character with a different UUID. Current
registration also requires a different nickname; separate accounts holding several
characters are not implemented. Other death causes have authoritative damage hooks,
but their physics, disease and combat simulations remain planned.

Memorial size reflects lifetime accumulated gold, not the remaining balance:
headstones below 1,000, monuments up to and including 1,000,000, and a mausoleum
only above 1,000,000. Historical receipts before this migration are unavailable;
existing balances and the starting grant establish the initial historical baseline.

Each grave preserves an immutable obituary: name, complete real days lived since
creation, lifetime wealth and the number of friendship relations at death. The
same obituary appears on refused login after password verification and on local
grave interaction. Friendship editing is not implemented yet. Removing possessions
or later friendship changes never alters these facts. Empty graves remain in the
database; triggers prevent deletion or rewriting memorial facts. Durable backups
and restricted database administration are still required for long-term retention.

There is no global grave browser. A living character must physically reach the
grave before inspecting its contents or taking items; both APIs check server-owned
positions within three units in the same world. Unknown positions deny access.
The client currently provides a planet preview and contextual memorial UI, not
surface walking or in-world grave discovery. These integrations must precede a
claim that the complete recovery journey or permanent planet placement is playable.
