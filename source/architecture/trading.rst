Trading, ground loot and wayfarers
==================================

Gold enters a world only through merchants' purchases, story effects and loot.
There is no auction, market board or player-set price. Merchants and player
exchanges are server-authoritative: the client shows offers and sends intentions.

Merchants
---------

An NPC tagged ``shop:<id>`` keeps a shop whose goods and prices live in
``ishtaria-server/etc/shops.json``. Every generated town has a trader at the
plaza (``etc/trader.yaml``, tag ``shop:general``); coastal towns also get a
shipwright. A datadisk may tag any standing character the same way.

* ``GET /shops/{npc_id}`` lists what the shop sells and buys (character within
  talking reach). Selling pays less than buying costs.
* ``POST /shops/{npc_id}/buy|sell`` exchanges items for gold in one transaction.
  One character may sell at most ``daily_sell_limit_gold`` (400) a day to a shop
  (``shop_sales``), which bounds the gold the world creates.
* Better tiers of the same kind of gear (migration ``0050_item_quality.sql``)
  cost more in the shop list and carry higher ``max_durability`` (and, for
  weapons, more swing strength). A blacksmith shop with ``repairs: true``
  restores worn weapons, armour and shields for gold.

Player exchanges
----------------

Between players there is one open exchange at a time (migration
``0037_trade_and_shops.sql``, ``src/trade.rs``):

* ``POST /trades {"with": name}`` (both within 10 m), ``GET|DELETE /trades/current``,
  ``PUT /trades/current/offer``, ``POST /trades/current/accept``.
* Changing an offer withdraws both acceptances. When both have accepted, the
  server re-checks ownership, distance and capacity and swaps everything or
  nothing.
* Used pieces (with remaining durability) cannot be traded, so trading cannot
  make a worn tool new. Exchanges expire after five minutes; the partner is
  told by a ``trade`` event.

Dropping and ground piles
-------------------------

Unequipped inventory can be thrown at the character's feet (migration
``0051_ground_loot.sql``, ``src/loot.rs``):

* ``POST /players/me/drop`` with ``{"item_id", "quantity"}``. An item in hand or
  worn as armour cannot be dropped until it is unequipped
  (``DELETE /players/me/equip``). Worn gear leaves the pack one piece at a time
  so its remaining durability stays on the ground.
* ``POST /ground/{id}/pickup`` takes a pile within a few metres into the pack.
* ``GET /world/objects`` (and the region reply) lists nearby ``ground_items``;
  the client draws them as sprites.

Piles stay until a player picks them up or an NPC comes within view and pockets
them into ``npc_inventory``. Standing NPCs scoop within about four metres;
wayfarers see about fourteen.

Buying from a finder
--------------------

While an NPC still holds a find, dialogue answers carry ``can_trade: true`` and
the client offers a **Trade** button. ``GET /npcs/{id}/found`` and
``POST /npcs/{id}/found/buy`` sell those stacks at the finder's price (the
general shop's sell price when the item is on a list, otherwise a small floor).
That is cheaper than waiting for the same item to reach a merchant.

Wayfarers
---------

Independent of any datadisk, the settlement generator places **wayfarers** on
the footpaths between towns that have a market (``MovementKind::Travel``,
``etc/traveler.yaml``, migration ``0052_travelers.sql``). Travel is a long
patrol along trail waypoints (preferring the stones the generator already laid);
it is not offered to datadisk authors (see :doc:`../decisions/0015-datadisk-walking-characters`).

When a wayfarer pockets a pile it records an errand toward the nearest general
merchant and its route is diverted along those road waypoints. On arrival it
hands everything into ``merchant_stock`` and clears the errand. The finder's
pack is empty, so Trade with them no longer offers the item.

While that limited stock sits on the merchant's shelf, ``GET /shops/{npc_id}``
lists it with a quantity at **twice** the finder's asking price, replacing the
infinite catalogue price for that item until the stock is sold. Buying depletes
``merchant_stock`` first; afterwards the ordinary catalogue price returns.

Gameplay consequence: on the road between towns it pays to talk to every
wayfarer — a find bought from them is cheaper than the same piece after it
reaches the market.

Client
------

``E`` at a merchant opens the shop panel. Dialogue with a character that holds
finds offers **Trade** and reuses the same panel (``trading.gd`` /
``trade_panel.gd``, kind ``found``). Inventory marks held and worn pieces,
allows unequip, and offers Drop only for unequipped stacks. Ground piles are
drawn from the region reply; ``G`` is the usual pick-up binding where the
client wires it to ``/ground/{id}/pickup``.
