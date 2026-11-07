Repositories
============

The **primary source** of every repository is the ``Ishtaria`` organisation on
`git.vitexsoftware.com <https://git.vitexsoftware.com/Ishtaria>`_ (Forgejo), where
development happens. `GitHub <https://github.com/Vitexus>`_ (``github.com/Vitexus``) is a
**secondary mirror** of the same repositories. Packages and binaries are **not built from
GitHub**; they are built from the primary repository.

.. list-table::
   :header-rows: 1
   :widths: 22 14 64

   * - Repository
     - Licence
     - Purpose
   * - `ishtaria-core <https://git.vitexsoftware.com/Ishtaria/ishtaria-core>`_
     - MIT
     - Shared Rust library: identities, items, rulesets, later physics and
       crafting rules. Linked into server, worldgen and client.
   * - `ishtaria-server <https://git.vitexsoftware.com/Ishtaria/ishtaria-server>`_
     - AGPL-3.0
     - Authoritative world server and federation endpoint.
   * - `ishtaria-client <https://git.vitexsoftware.com/Ishtaria/ishtaria-client>`_
     - MIT
     - Godot 4 client.
   * - `ishtaria-worldgen <https://git.vitexsoftware.com/Ishtaria/ishtaria-worldgen>`_
     - MIT
     - Deterministic cube-sphere terrain generator.
   * - `ishtaria-protocol <https://git.vitexsoftware.com/Ishtaria/ishtaria-protocol>`_
     - MIT
     - Federation protocol: JSON Schema, CDDL, examples.
   * - `ishtaria-content <https://git.vitexsoftware.com/Ishtaria/ishtaria-content>`_
     - CC BY-SA 4.0
     - Base content pack ``core-rules``.
   * - `ishtaria-docs <https://git.vitexsoftware.com/Ishtaria/ishtaria-docs>`_
     - CC BY-SA 4.0
     - This documentation (Sphinx, reStructuredText).
   * - `ishtaria-admin <https://git.vitexsoftware.com/Ishtaria/ishtaria-admin>`_
     - MIT
     - Text-mode administration of a world server (Turbo Vision, C++): maps, players,
       linked worlds, the service and the solar clock.
   * - `ishtaria-web <https://git.vitexsoftware.com/Ishtaria/ishtaria-web>`_
     - CC BY-SA 4.0
     - The public portal: what the game is, how to start, where to download it.
   * - `ishtaria-datadisk-gilgamesh <https://git.vitexsoftware.com/Ishtaria/ishtaria-datadisk-gilgamesh>`_
     - CC BY-SA 4.0
     - The Epic of Gilgamesh: Early Dynastic Uruk on a reconstructed Earth, with its
       places, characters, dialogues, quests and spoken lines.
   * - `ishtaria-datadisk-tutorial <https://git.vitexsoftware.com/Ishtaria/ishtaria-datadisk-tutorial>`_
     - CC BY-SA 4.0
     - A datadisk that demonstrates the implemented features through guided tutorials.
   * - `ishtaria-datadisk-endland <https://git.vitexsoftware.com/Ishtaria/ishtaria-datadisk-endland>`_
     - CC BY-SA 4.0
     - The pilot story datadisk, set in The End Land universe.

Why these licences: see :doc:`../decisions/0004-licensing`.
