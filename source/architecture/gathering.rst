Gathering and crafting
======================

Trees and rocks of the generated world can be harvested. The outcome is decided
by the server: it regenerates the object a player names, checks reach, stamina
and a short cooldown between swings, and applies the result in one transaction.

Tools
-----

Axe, pickaxe and sword are inventory items (stack of five per slot). Every new
character starts with all three; characters created earlier received them with
migration ``0016_gathering.sql``. Only the tool **in hand** works: the inventory offers *Equip* for tools and weapons
(``POST /players/me/equip``; new characters hold the axe). The axe fells trees, the
pickaxe mines stone and also fells trees, but needs **twice as many swings**; the
axe does not work on stone, a sword in hand works on nothing. A swing is worth work
points (axe on a tree two, pickaxe one), so swings with different tools add up. The
equipment is cleared at death. The
sword is for defence once combat exists.

Resources
---------

``etc/resources.json`` maps object models to resources:

* **Trees** by species: pine, palm, oak and birch trees give pine, palm, oak and
  birch **logs**. Each felling may also drop food of that species (pine nuts,
  coconuts, acorns, pears or apples).
* **Rocks** give stone. Larger rocks give more and have a better chance of a
  rare mineral: iron ore, copper ore or quartz crystal.
* A harvested object is stored as a change of the generated world
  (``world_object_state``). A felled tree leaves a **stump** that can be walked
  over; a mined rock disappears. Both grow back after a configured time.
* Several hits are needed per object. Hits are forgotten after ten minutes.

Logs and wood
-------------

A log fills **ten inventory slots**. It must be chopped with an axe
(``chop_*_log``, 1 log into 20 pieces of wood); wood stacks to 100 per slot.
Planks are made from wood, stone blocks from stone (``GET /recipes``,
``POST /players/me/craft``).

API
---

``POST /players/me/harvest`` with ``{"object_id": …}`` returns the state of the
object (``hit`` or ``depleted``), the items gained and the updated player.
A full inventory refuses the final hit and leaves the object standing.

Client
------

The ``E`` key harvests the nearest tree or rock within reach (a prompt names the
action); the inventory panel (``I``) lists the recipes and crafts them. Item
icons are rendered from the Kenney Survival Kit models by
``tools/bake-item-icons.gd``; items without a model (coins, sword) show text only.

Experience and levels
---------------------

Every swing at a tree or a rock is worth **1 experience point**. Crafting is worth more
(3 for chopping a log, 4 for planks, 5 for a stone block) and building a portal still
more: 5 points for every unit of material delivered and 500 for a finished end. A
character reaches level *n* with ``25 · n · (n − 1)`` points: 50 for level 2, 150 for
level 3, 500 for level 5, 2 250 for level 10, 9 500 for level 20. Each level gives 10
inventory slots, up to level 30.

The **score** of a character is ``100 · level + 10 · days lived``. The hall of fame lists
the ten best characters of the world, living or dead; a dead character keeps the level
and the days, but the wealth shown next to them becomes zero once anyone has taken
something from their grave. This makes lost graves worth looking for.

RPG items
---------

The 55 models of the Quaternius *Ultimate RPG Items Bundle* (CC0) are items of
the catalog (migration ``0017_item_catalog.sql``): weapons, armour, shields,
potions, keys, books, valuables and remains. They have names, categories and
icons. Since migration ``0036_combat.sql`` armour has defense values and slots
(``etc/combat.json``), melee weapons have swing points (``etc/creatures.json``), and
the common ones can be crafted from iron ingots and hides; the rest have no
statistics yet and no way to be obtained. Items with a ``multi_slot`` stack (weapons, armour)
fill one slot each.

Animals and fish
----------------

Animals and fish are a separate layer of the generated world (``etc/world_fauna.json``)
with their own grid and identifiers, so adding them did not move any tree or rock.
Land animals (12 species of the Quaternius Animated Animal Pack) live in the
grassland, forest, mountain and snow biomes that suit them. Fish (35 species of the
Animated Fish Bundle) swim below the surface of oceans, lakes and rivers where the
water is at least three metres deep; freshwater fish stay in lakes and rivers.
Fish are scenery: they do not collide or react and cannot be harvested; the client
lets them circle around their place. Land animals do not collide either, but they walk.

**Walking.** The server keeps no state for walking animals. Every 30 seconds an animal
heads for a waypoint that depends only on its identifier and the time (within 40 metres of
where the seed put it, 14 around a pasture), walking for 21 seconds and then standing. The
reply of ``GET /world/objects`` carries ``server_time_ms`` and, for each land animal, a
``wander`` route of waypoints ``[unix ms, x, y, z]`` covering at least a minute; the client
walks the animal along it (the walking clip while it moves, the idle clip while it stands)
and asks for the routes again every 30 seconds. The server computes the same route when it
checks reach, with a few metres of tolerance.

**Farm animals.** Beside every generated settlement a pasture holds a herd (3, 6 or 10
animals for a hamlet, village or town): cows, bulls, horses, donkeys, an alpaca or a dog from
the Animated Animal Pack and chickens, pigs and sheep of the Quaternius farm animals
(CC0). Their identifiers (``<seed>:farm:<number>:<place>``) are a separate namespace, so
existing scenery does not change.

**Flocks and shepherds.** On top of that, every settlement has a flock of sheep and goats (5, 8
or 12 animals, three in ten of them goats; the goat is the Hyper3D Early Dynastic model) and,
where there is land to walk on, a shepherd. The flock lives in a cycle of about twelve minutes
that depends only on the settlement and the time (``src/herd.rs``): it rests in the fold
beside the settlement, is driven 140 metres out to a pasture at walking pace, grazes there and
is driven home. The flock animals carry the numbers after the village's own animals in the
same ``<seed>:farm:<number>:<place>`` namespace and keep their own spot about the centre of the
herd, milling slowly; the shepherd is a generated character (``shepherds:shepherd_NN``,
movement kind ``herd``, not available to datadisks) who walks a few seconds behind the centre.
The flocks of a world are out at different times. A conversation stops the shepherd like any
walking character (migration 0040), so after talking he falls behind the flock by that long.
Without land all the way to the pasture the flock keeps to its fold and there is no shepherd.
Sheep and goats can be butchered like other animals.

**Meat and milk.** ``POST /players/me/butcher`` swings the weapon in hand (sword, cleaver,
knife, dagger or axe, ``etc/creatures.json``) at an animal within reach; several swings
butcher it for raw meat (and bones), like felling a tree: the animal is stored as a change of
the world (``world_object_state``) and returns after its respawn time. Animals do not fight
back. ``POST /players/me/milk`` lets a character drink from a cow within reach (30 points of
water); each cow gives milk again after ten minutes (``creature_milked``, migration
``0034_creatures.sql``).

A whole animal can be carried as an item (migration ``0018_animal_items.sql``). It
fills as many inventory slots as its size suggests: a fox four, a wolf eight, a
horse twenty, a bull twenty-five; a fish one to eight. There is no hunting or
fishing yet, so the items cannot be obtained.

Planned
-------

Survival Kit items (logs, stumps, tools, campfire, bed, anvil and others) can be
carried and **placed in the world** for later use; a closed portal can be mined
for its materials with a pickaxe. Neither is implemented yet.
