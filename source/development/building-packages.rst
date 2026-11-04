Building packages
=================

Every repository contains a ``debian/`` directory (native format, debhelper
13) and builds with the standard tools:

.. code-block:: sh

   sudo apt build-dep .
   dpkg-buildpackage -us -uc -b

Notes per repository
--------------------

Rust (server, worldgen)
   ``debian/rules`` calls ``cargo build --release``. Crates are fetched
   from crates.io during the build, which fits the VitexSoftware build
   pipeline but not the official Debian archive.

Client
   Needs a Godot 4.5 binary and Linux export templates. Run
   ``tools/fetch-godot.sh`` first or set ``GODOT=/path/to/godot``.

Documentation
   ``sphinx-build -W`` – warnings fail the build.

CI
--

The packages and binaries of a release are built from the primary repository
(``git.vitexsoftware.com``) and published to ``repo.vitexsoftware.com`` by the existing
Jenkins + Aptly pipeline. They are **not built from the GitHub mirror**: the GitHub
Actions workflows (``.github/workflows``) that remain only run tests (and build the
documentation) on the mirror, none of them builds a package or a binary, and the release
files on GitHub are copies of the builds made from the primary repository.
