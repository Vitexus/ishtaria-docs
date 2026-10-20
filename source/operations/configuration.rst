Configuration
=============

``/etc/ishtaria/server.toml``

.. code-block:: toml

   # DNS name of this world; becomes part of every player and item id.
   server_name = "ishtaria.example.org"
   # Rules shared with federated worlds (must match peers' major version).
   ruleset = "core-rules@1.0"
   listen = "0.0.0.0:7400"
   # public_url = "https://world.example.org"   # HTTPS name in front of a reverse proxy

.. warning::

   ``server_name`` is permanent. Player ids (``@user:server``) and item ids
   (``server/uuid``) embed it, so changing it later breaks identities and
   federation. Choose a domain you will keep.

For a public world, terminate TLS on a reverse proxy (HAProxy, nginx or Caddy) and set
``public_url`` to that HTTPS address. See :doc:`hardening` for HAProxy and nginx examples,
``trust_proxy``, and why the client rejects plain HTTP to a remote host.

Limits, logs and metrics
------------------------

An optional ``[limits]`` table protects a public server. Every key has a default that suits a
small public world, and the guard is a plain middleware without further dependencies.

.. code-block:: toml

   [limits]
   auth_per_minute = 10          # registrations and logins per minute from one address
   requests_per_second = 100     # sustained requests per second from one address ...
   burst = 300                   # ... and the burst allowed on top of it
   trust_proxy = false           # true only behind your own reverse proxy
   access_log = "errors"         # "errors", "all" or "off"
   metrics_token = "long-random" # lets a remote scraper read /metrics

* Limits are kept per client address in memory (a restart forgets them). For IPv6 the client is the
  whole /64 network, because one subscriber owns billions of addresses in it. When the table of
  addresses is full (a flood from very many addresses) the newcomers share one allowance instead of
  being refused. Players behind one address
  (a school, a family, a mobile network) share it: raise ``requests_per_second`` and ``burst`` for such a
  world. A walking client sends about ten requests per second.
* ``trust_proxy = true`` takes the address from the **last** entry of ``X-Forwarded-For``, the one your own
  proxy added (HAProxy ``option forwardfor``, nginx ``proxy_set_header X-Forwarded-For``). Never set it on
  a server that clients reach directly, or anybody can pretend to be anybody. The key belongs under
  ``[limits]`` only; a top-level ``trust_proxy`` is ignored.
* A refused request gets ``429`` with ``Retry-After``. Every request has a 30 s time limit (``504``).
* ``/metrics`` answers loopback only (and not at all behind ``trust_proxy``), or a request with
  ``Authorization: Bearer <metrics_token>``. See :doc:`monitoring`.

Federation agreements
---------------------

Agreements live in ``/etc/ishtaria/federation/<peer>.yaml`` and follow the
schema in :doc:`../federation/agreement`. Validate before reloading:

.. code-block:: sh

   python3 -m jsonschema \
     -i /etc/ishtaria/federation/svet-b.example.org.yaml \
     /usr/share/ishtaria/protocol/schemas/federation-agreement.schema.json

.. todo:: Federation loading is not implemented yet (milestone M4).
