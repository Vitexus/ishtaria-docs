Federation agreement
====================

Each side keeps **its own** copy of the agreement. Policies need not be
symmetric: world A may accept raw materials from B while B accepts nothing
from A.

The normative schema is
``schemas/federation-agreement.schema.json`` in the
`ishtaria-protocol <https://git.vitexsoftware.com/Ishtaria/ishtaria-protocol>`_
repository (installed by the ``ishtaria-protocol`` package to
``/usr/share/ishtaria/protocol/``).

Example
-------

.. code-block:: yaml

   federation_agreement:
     peer: svet-b.example.org
     peer_key: "ed25519:MCowBQYDK2VwAyEA..."
     protocol: ">=1.0 <2.0"
     ruleset: "core-rules@1.0"
     valid_until: 2027-10-04

     portals:
       - id: brana-sever
         local_location: { h3: "8a1fb46622dffff" }
         capacity_per_hour: 200
         max_cargo_items: 40

     import:
       avatar: true
       cosmetics: true
       skills: map            # map | reset | keep
       items:
         allow_categories: [raw_material, tool, food, currency]
         deny_categories: [legendary]
         daily_limit_per_player: 50
       currency: count        # coins cross one for one

     export:
       items:
         deny_categories: [quest_item]

     exchange:
       rate_source: market    # market | fixed
       daily_cap: 10000

     on_termination:
       foreign_items: return_home   # return_home | freeze | convert
       guests: return_home
       grace_period: 7d

Fields
------

``peer``, ``peer_key``
   DNS name and Ed25519 signing key of the other world.

``protocol``, ``ruleset``
   Negotiated versions. Rulesets must share the major version.

``portals``
   Portal ends located in *this* world.

``import`` / ``export``
   What may enter or leave, by item category. ``deny`` wins over ``allow``.

``exchange``
   Optional conversion by an exchange office, used only with
   ``currency: exchange``. With ``currency: count`` coins cross one for one
   as inventory items and are bounded by the item import limits.

``on_termination``
   What happens to foreign items and visiting players when the agreement
   ends. Mandatory: defederation must never be ambiguous.
