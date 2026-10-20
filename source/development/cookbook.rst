Cookbook: adding things to the game
===================================

Each recipe lists the files to touch, in the order to touch them, and the checks that must be
green before you open a pull request. All of them assume the rules of
:doc:`invariants` and a running local world (:doc:`local-setup`). Tour of the code:
:doc:`server-tour` and :doc:`client-tour`.

Commands used below, from the repository you are changing:

* server: ``cargo fmt && cargo clippy --locked --all-targets -- -D warnings`` and the PostgreSQL tests
  of :doc:`local-setup`;
* client: ``godot4 --headless --path . --editor --import`` after adding an asset, and ``make test-...``.

Add an item
-----------

#. **Migration** ``ishtaria-server/migrations/NNNN_name.sql`` (next free number, never edit an old one):

   .. code-block:: sql

      INSERT INTO item_types (id, name, calories, capacity_bonus, stack_limit, multi_slot, slot_cost, category)
      VALUES ('ruby', 'Ruby', 0, 0, 20, false, 1, 'valuable');

   ``category`` is one of the values of ``item_types_category_check``. ``misc`` is reserved for
   uncategorised items and a test fails if you use it; to add a category drop and recreate the
   constraint as ``0038_building_farming_fishing.sql`` does. Add ``water`` for food that quenches
   thirst and ``max_durability`` for things that wear out.
#. **Name**: add a row ``Ruby,Ruby,Rubín`` to ``ishtaria-client/locales/client.csv`` and run the
   import (it rebuilds the ``.translation`` files).
#. **Icon**: ``ishtaria-client/assets/icons/items/ruby.png``, 128x128 with an alpha channel. Draw
   it, render a bundled model with ``tools/bake-item-icons.gd``, or generate it (record this in the
   README credits). A Food Kit picture can be reused with ``FOOD_FILES`` in ``scripts/item_icons.gd``.
#. **Where it comes from**: a drop (``etc/creatures.json``, ``etc/resources.json``), a recipe, a shop
   or a story reward. An item nobody can get is only a catalogue entry.
#. **Checks**: ``configured_items_exist`` (every item named in ``etc/`` exists) and the catalogue test
   in ``src/tests/harvest.rs``.

Add a recipe
------------

Append an object to ``ishtaria-server/etc/recipes.json``:

.. code-block:: json

   {"id": "make_ruby_ring", "station": "anvil",
    "inputs": [{"item": "ruby", "quantity": 1}, {"item": "iron_ingot", "quantity": 2}],
    "outputs": [{"item": "ring", "quantity": 1}], "xp": 20}

``tool`` (an item the character owns, ``axe`` or ``pickaxe``) and ``station`` (a placed object
within four metres: ``campfire``, ``workbench``, ``anvil``) are optional. Stations come from
``etc/placeables.json``. The unit test ``configuration_is_consistent`` and ``configured_items_exist``
cover the file; copy the pattern of ``weapons_and_armour_are_made_from_ore_and_hides`` in
``src/tests/combat.rs`` for a crafting test. The client lists new recipes by itself.

Add a spell
-----------

#. Scroll item (migration, as above) named ``scroll_<id>`` with category ``document``, and its icon.
#. ``ishtaria-server/etc/spells.json``: ``id``, ``name``, ``scroll``, ``mana``, ``cooldown_ms``,
   ``min_level`` and an ``effect`` of kind ``heal``, ``refresh``, ``ward`` or ``bolt``. A new *kind*
   of effect is Rust in ``src/magic.rs`` (an ``Effect`` variant and a match arm) and needs a note in
   ADR 0010 on balance.
#. A recipe for the scroll at a workbench (not a shop: magic is earned, see ADR 0010).
#. Translations of the spell and scroll names in ``client.csv``. Spells are listed and cast by
   number keys automatically.
#. Tests: ``bundled_spells_are_consistent`` runs by itself; add a case to ``src/tests/magic.rs``.

Add a crop, a thing to place, or fishing
----------------------------------------

``ishtaria-server/etc/placeables.json`` has ``things`` (an item that can be put into the world, with
``model``, ``scale``, ``spacing_m`` and an optional ``station``), ``crops`` (``seed_<name>`` with the
produce, amounts and ``grow_minutes``) and ``fishing``. Add the items by migration, the model to the
client under ``assets/`` with its licence (models are named ``<kit>.<file>`` and the kits are in
``PROP_KITS`` in ``scripts/surface_environment.gd``), translations and icons. Crops grow by the
clock, so no code is needed. Test with ``src/tests/farming.rs`` as the pattern.

Add a merchant or a shop
------------------------

* Goods and prices: ``ishtaria-server/etc/shops.json``. Selling must pay less than buying costs (a unit
  test checks it), and ``daily_sell_limit_gold`` bounds the gold a merchant creates.
* A merchant is an NPC with the tag ``shop:<id>``: in a datadisk add ``tags: [shop, 'shop:general']``
  to the NPC, or give a generated NPC the tag in ``src/story/settlements.rs``. Nothing else is needed;
  the client opens the shop when the player presses ``E`` next to the NPC.

Add or change an animal
-----------------------

``etc/creatures.json`` (hits to butcher, respawn, drops; the ``weapons`` table is the strength of
each weapon) and, if it bites back, ``etc/combat.json`` (``fierce``: damage and chance). The
model must exist in the world's fauna (``etc/world_fauna.json``).

Add an endpoint
---------------

#. A function in the module of the area (or a new module with ``fn routes() -> Router<AppState>``
   merged in ``main.rs``) that follows *How a request is handled* in :doc:`server-tour`.
#. Add a migration for new tables with constraints that hold the invariants (``CHECK``, unique
   indexes, ``ON DELETE``); do not rely on the code alone.
#. Test it with the helpers in ``src/tests.rs``: a refused request changes nothing, a repeated one
   is harmless, two players do not step on each other, the dead and strangers get the right status.
#. Document the route in the server README and, if it is a persisted contract, in a decision record.

Add a window or a key to the client
-----------------------------------

#. A ``*_client.gd`` with ``start(url, token)``, ``stop()`` (bump ``_generation``), validators and
   fixed error keys; copy ``scripts/trading.gd`` or ``scripts/placed_client.gd``.
#. A panel (``CanvasLayer``) that emits signals and only shows what it is given; copy
   ``scripts/trade_panel.gd``.
#. Create both in ``scripts/main.gd``, connect signals, start them where the others are started
   and stop them when the profile becomes empty (leaving a server).
#. Keys: add an entry to ``character_controls.ACTIONS`` (default + Settings label), handle it
   via ``matches_action`` in ``_input``, and include the panel in ``_game_ui_open``.
#. A ``tests/<name>.gd`` script and a ``make test-<name>`` target; text keys in ``client.csv``.
#. Look at the result with your own eyes.

Add an NPC or a quest
---------------------

Story content belongs in a datadisk (see ``ishtaria-protocol/DATADISK-SPEC.md``): places, NPCs,
dialogue trees, quests and strings in English and Czech. Datadisks are pinned by hash and carry no
code. Generated towns and their traders are in ``src/story/settlements.rs``.

A character can tell what it knows: add a card to ``knowledge.yaml`` (text keys in every language, a picture below
``media/knowledge/`` with its credit, the Wikipedia titles) and name it with ``about`` on the NPC; the generated
characters use ``etc/knowledge.yaml`` and ``assets/knowledge/`` of the server (decision 0019).
