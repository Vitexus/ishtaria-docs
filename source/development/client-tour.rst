Tour of the client code
=======================

``ishtaria-client`` is a Godot 4.5 project that builds almost all of its interface in code. There is one
scene (``scenes/main.tscn``); ``scripts/main.gd`` creates every node, wires the signals and handles input.

Principles
----------

* **The client shows and asks; it does not decide.** Every ``*_client.gd`` and ``player_session.gd``
  is a thin HTTP layer that sends an intention and emits a signal with a *validated* answer.
* **Validate every answer.** Each client has static ``valid_*`` functions that check type, shape and
  range; what does not pass is dropped. They are the first thing to test.
* **Refusals are message keys.** Map the server's fixed error text to a translatable key in a static
  ``error_key`` function; never show server text.
* **A generation counter guards requests.** Each client increments ``_generation`` in ``stop()`` and
  ignores answers that belong to an earlier connection, so a late answer never changes a newly chosen
  server.
* **English is the source, Czech a translation** (``locales/client.csv``; add every new text key there).

Files
-----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - File
     - Responsibility
   * - ``main.gd``
     - the planet preview and surface view, input (``_input``: E, G, I, J, F, P, Enter, 1-9, Esc), wiring
   * - ``player_session.gd``
     - account, profile, equipment, gathering, crafting, eating, drinking
   * - ``character_controls.gd``, ``character_catalog.gd``, ``character_creator.gd``
     - walking and camera, the playable models, character creation
   * - ``surface_environment.gd``
     - generated scenery, animals, NPCs, props and placed things (``apply_*``, ``nearest_*``)
   * - ``remote_players.gd``
     - other players near you, with smooth movement
   * - ``social.gd``, ``chat_feed.gd``, ``friends_panel.gd``
     - friends, the ``/events`` poll, chat lines and the chat input
   * - ``trading.gd``, ``trade_panel.gd``
     - merchants and exchanges
   * - ``placed_client.gd``
     - placing, planting, picking up, harvesting, fishing
   * - ``magic_client.gd``
     - spells, scrolls, casting
   * - ``survival_panel.gd``, ``player_hud.gd``, ``item_icons.gd``
     - inventory, crafting and spells window; HUD meters; item icons
   * - ``minimap.gd``
     - top-down minimap showing nearby entities with colored icons (diamond for NPCs, square for places, star for quests, circle for objects), name initials, player arrow, and north direction; uses texture caching and optimized updates
   * - ``story_client.gd``, ``dialogue_panel.gd``, ``quest_panel.gd``
     - datadisk stories, conversations, quests
   * - ``portal_panel.gd``, ``escape_menu.gd``, ``control_settings.gd``
     - portals, the menu, key and sound settings

Keys and Settings
-----------------

Every gameplay key belongs in ``character_controls.ACTIONS`` (with a default and a Settings
label) and is handled through ``matches_action`` / ``spell_slot`` from ``main.gd``. Settings
lists them all and lets the player rebind them; that window is the in-game key reference.
``RESERVED_KEYS`` holds only Escape (menu / cancel capture). When you add a new action,
extend ``ACTIONS`` / ``DEFAULT_KEYS`` / ``LABELS``, wire it in ``main.gd``, and add the label
to ``locales/client.csv``.

Tests
-----

``tests/*.gd`` are ``SceneTree`` scripts started with ``godot4 --headless --script``; each has a
``make test-...`` target. A check calls ``_check(ok, "what")``, the script prints ``... passed``
and ``quit(1)`` on a failure. An error *inside* an ``await`` kills the script without ``quit``
and the run hangs: if a test seems to hang, run it with ``timeout`` and look for a script error.
