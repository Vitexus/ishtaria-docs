Hardening a public world
========================

A world that anybody can reach needs more than the defaults of a development machine. Work through
this list before you announce your server.

Network and TLS
---------------

* Put the server behind a reverse proxy that terminates **TLS** (HAProxy, nginx, Caddy). Never offer
  accounts over plain HTTP to the internet: passwords and session tokens would travel in the clear.
  The client refuses remote credentials over HTTP (only ``http://127.0.0.1``, ``localhost`` and
  ``[::1]`` are allowed without TLS).
* Bind the server so only the proxy can reach it (``listen = "127.0.0.1:7400"`` on the same host, or
  a private address the proxy uses). Open only 443 (and 80 for the certificate) toward the public
  internet; PostgreSQL stays on its local socket.
* Set ``public_url`` to the **HTTPS** URL players and peers use (the name on the certificate), not the
  internal ``host:7400`` address.
* Under ``[limits]``, set ``trust_proxy = true`` **only** behind a proxy you run, so limits and the
  access log see the real client from ``X-Forwarded-For``. A top-level ``trust_proxy`` key is ignored.

HAProxy
~~~~~~~

HAProxy terminates TLS and forwards plain HTTP to the world process. Prefer a TCP or a light HTTP
health check: ``GET /`` returns 404 on this server, so a check that expects ``200`` on ``/`` marks the
backend down. ``GET /world`` is a small JSON metadata reply (a few SQL queries, not the heightmap)
and is fine as a check every few seconds.

Example backend (TLS certificates and the ``frontend`` that selects by ``Host`` are outside this
snippet; Spoje.NET operators keep the live list in the ``haproxy-ansible-role`` inventory):

.. code-block:: haproxy

   backend world_example_org
       mode http
       balance roundrobin
       option forwardfor
       option httpchk GET /world
       http-check send meth GET uri /world ver HTTP/1.1 hdr Host world.example.org
       http-check expect status 200
       server world 10.0.0.10:7400 check

Matching ``/etc/ishtaria/server.toml`` on the world host:

.. code-block:: toml

   listen = "0.0.0.0:7400"   # or the private address HAProxy uses
   public_url = "https://world.example.org"

   [limits]
   trust_proxy = true

Players enter ``https://world.example.org`` in the client (no ``:7400``). Federation share links and
``public_url`` must use the same HTTPS name.

nginx
~~~~~

A minimal nginx site (the package ``ishtaria-web`` ships a fuller example for the portal):

.. code-block:: nginx

   server {
       listen 443 ssl http2;
       server_name world.example.org;
       # ssl_certificate ... ssl_certificate_key ...  (for example from certbot)
       client_max_body_size 64k;                       # the server refuses more anyway
       location / {
           proxy_pass http://127.0.0.1:7400;
           proxy_set_header Host $host;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_read_timeout 35s;                      # the server times requests out at 30 s
       }
   }

Accounts and limits
-------------------

* Keep the default ``auth_per_minute`` (10 per address). Registration and login share it, which
  slows guessing and the making of accounts alike.
* Passwords are stored as Argon2id hashes and session tokens only as hashes; tokens expire and can be
  revoked (log out). Nothing in the logs contains a password, a token or a query string.
* Consider also rate limiting in the proxy (``limit_req``) and a ban tool such as ``fail2ban`` on the
  access log lines with ``status=429``.
* Bans of abusive players and scheduled shutdowns are done with ``ishtaria-admin``.

The system service
------------------

The package runs the server as a systemd unit under its own user. Keep it that way: no root, the
configuration file readable only by that user, and ``DATABASE_URL`` (if you use it) in the environment of the
unit, not in a world-readable file. Federation signing keys live in the database; back it up
(:doc:`backup`) and treat the backup as a secret.

Checklist
---------

.. list-table::
   :header-rows: 1
   :widths: 5 95

   * - ☐
     - TLS in front, server bound to loopback, firewall closed except 80/443
   * - ☐
     - ``trust_proxy`` set exactly when a proxy of yours is in front
   * - ☐
     - ``[limits]`` reviewed for the number of players per address you expect
   * - ☐
     - ``/metrics`` readable by your monitoring only (:doc:`monitoring`)
   * - ☐
     - backups run and a restore was tried on another machine (:doc:`backup`)
   * - ☐
     - the operator policy of federation is ``approve`` or ``closed`` unless you know why not
   * - ☐
     - packages are updated (``apt upgrade``); read the changelog before a server upgrade
