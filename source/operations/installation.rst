Installation
============

All Ishtaria components are Debian packages for **Debian and Ubuntu on
x86-64**. Windows and macOS are not supported.

Packages
--------

.. list-table::
   :header-rows: 1

   * - Package
     - Contents
   * - ``ishtaria-server``
     - world server, systemd unit, ``/etc/ishtaria/server.toml``
   * - ``ishtaria-client``
     - game client (``ishtaria-client``), desktop entry
   * - ``ishtaria-worldgen``
     - planet generator command-line tool
   * - ``ishtaria-content``
     - base ruleset ``core-rules`` in ``/usr/share/ishtaria/content``
   * - ``ishtaria-protocol``
     - federation schemas in ``/usr/share/ishtaria/protocol``
   * - ``ishtaria-datadisk-gilgamesh``
     - story datadisk: the Epic of Gilgamesh on the Early Dynastic Earth
   * - ``ishtaria-datadisk-endland``
     - story datadisk: The End Land
   * - ``ishtaria-datadisk-tutorial``
     - tutorial datadisk demonstrating every implemented feature
   * - ``ishtaria-doc``
     - this documentation in HTML

Adding the repository
---------------------

Packages are published in the VitexSoftware APT repository:

.. code-block:: sh

   echo "deb http://repo.vitexsoftware.com $(lsb_release -sc) main" \
     | sudo tee /etc/apt/sources.list.d/vitexsoftware.list
   sudo wget -O /etc/apt/trusted.gpg.d/vitexsoftware.gpg \
     http://repo.vitexsoftware.com/keyring.gpg
   sudo apt update

Playing
-------

.. code-block:: sh

   sudo apt install ishtaria-client

Running a world
---------------

.. code-block:: sh

   sudo apt install ishtaria-server ishtaria-content ishtaria-worldgen postgresql
   sudoedit /etc/ishtaria/server.toml     # set server_name (permanent)
   sudo ishtaria-server-init              # generate a planet and import it (once)
   sudo systemctl enable --now ishtaria-server
   journalctl -u ishtaria-server -f

The package creates the PostgreSQL role and database ``ishtaria`` when
PostgreSQL is running during installation (peer authentication over the local
socket). It never touches an existing role or database. ``ishtaria-server-init
[seed] [face_size]`` runs ``ishtaria-worldgen`` and imports the result; the
server refuses to replace an already imported world.

Running a world with a story datadisk
-------------------------------------

Datadisks are installed to ``/usr/share/ishtaria/datadisks/<id>/`` and chosen **when the
world is generated**; a disk's version and content hash are pinned to the world, so changing
or upgrading a disk means generating a new world. The example below creates the Gilgamesh
world (an empty database is required; the server never replaces an imported world):

.. code-block:: sh

   sudo apt install ishtaria-server ishtaria-content ishtaria-worldgen \
     ishtaria-datadisk-gilgamesh postgresql
   sudoedit /etc/ishtaria/server.toml     # set server_name (permanent)
   ishtaria-server --list-datadisks
   sudo ishtaria-server-init "" 256 gilgamesh
   sudo systemctl enable --now ishtaria-server
   curl -s http://127.0.0.1:7400/world    # "datadisks" must list gilgamesh

The packaged service starts on installation; stop it and fix ``server_name`` before the first
start, because the name is permanent once a world row exists. A world with a datadisk that
brings its own planet (Gilgamesh) is rendered from the disk's rasters instead of procedural noise.
Put the server behind a TLS reverse proxy before exposing accounts publicly; see
:doc:`hardening`. To recreate a world, drop and recreate the database from ``template0``
(``createdb -T template0 -O ishtaria ishtaria``) and run ``ishtaria-server-init`` again; this
**deletes all accounts and changes** and needs a backup (:doc:`backup`) and the operator's consent.

Administration
--------------

.. code-block:: sh

   sudo apt install ishtaria-admin
   sudo -u ishtaria ishtaria-admin

``ishtaria-admin`` is a text-mode tool that works directly on the server's
database: save, load, rename, delete and export world maps; rename, ban and
delete players; manage portals to linked worlds; and schedule a server
shutdown. A scheduled shutdown shows players a non-dismissable system notice
with a countdown (``messages`` in ``GET /world``) and then stops the service
cleanly (exit status 0, so systemd does not restart it). Portals are records
only until federation is implemented. These functions are deliberately not part
of ``ishtaria-client``.

The first-time setup wizard (F7, also offered when no world exists yet) stops
the ``ishtaria-server`` systemd unit, drops the public schema (all accounts and
world data), generates and imports a new planet, then starts the service again.
On an existing world the operator must type ``RESET``. This replaces the manual
``dropdb`` / ``createdb`` / ``ishtaria-server-init`` sequence.

The ``ishtaria-server`` package installs ``/etc/sudoers.d/ishtaria-server`` so
the ``ishtaria`` user can start, stop and restart the systemd unit without a
password (used by *Start service* / *Stop service* and the setup wizard in the
admin tool).
