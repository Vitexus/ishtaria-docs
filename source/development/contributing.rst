Contributing
============

Ishtaria is built to be extended by people who play it. This page is for you if you want to add
a spell, a crop, a quest, a town, a mechanic or a fix.

.. note::

   The primary source of Ishtaria is ``git.vitexsoftware.com/Ishtaria`` (Forgejo). The
   repositories on GitHub (``github.com/Vitexus``) are a secondary mirror, and packages and
   binaries are not built from GitHub. See :doc:`repositories`.

Before you start
----------------

#. Read :doc:`invariants`. They are short, and a pull request that breaks one is not merged.
#. Run a private world (:doc:`local-setup`) and play with the thing you want to change.
#. Look at the :doc:`cookbook`: most additions are a data file, a migration, a translation and a
   test, not a new system.
#. Discuss a larger change in an issue first. An architectural one (a new kind of effect, a
   new persisted contract, a change of an ADR) is written as a decision record
   (:doc:`../decisions/index`) before the code.

Working with Claude Code
------------------------

Every repository has a ``CLAUDE.md`` that Claude Code reads at the start of a session; it holds the
commands, the rules and the map of that repository. A good session looks like this:

#. Open Claude Code in the repository you are changing and describe the *behaviour* you want, not
   the files. Ask for a plan first (plan mode) for anything that spans server and client.
#. Let it read the cookbook entry for your kind of change and the nearest existing example.
   Prefer "do it the way ``trade.rs`` does it" to a new pattern.
#. Make it run the checks (fmt, clippy, tests) and show the output. Ask what it could **not**
   verify; for anything visible, run the client and look.
#. Review the diff yourself. Generated code is your code: read the SQL, the locking, the
   validation, and every place where a client value reaches the server.
#. Keep the change small and in one repository where possible. Cross-repository changes (a
   server route and its client) go in linked pull requests.

Things a generated change must never do: weaken or skip a failing test, edit a released
migration, trust a client value, log a secret, add a dependency without a reason, or describe an
unfinished feature as finished.

Definition of done
------------------

A change is ready when

* ``cargo fmt --check``, ``cargo clippy --locked --all-targets -- -D warnings`` and the tests pass
  (server, core, worldgen), or the ``make test-...`` targets of the client you touched pass;
* the change has a test that fails without it, including the refusal paths (not enough mana, too far,
  not yours, dead, twice in a row);
* new text is in ``client.csv`` in English and Czech, new assets have their licence recorded,
  and the READMEs, ``etc/`` consistency tests and, for a contract, the documentation are updated;
* the pull request says what was tested, what was not, and what remains planned.

Conventions
-----------

* Commits are small and follow Conventional Commits (``feat(ishtaria-server): ...``). The default
  branch is ``main``.
* Rust: ``cargo fmt`` and ``clippy -D warnings`` clean; errors are controlled ``Error::Status`` values;
  no ``unwrap`` on request data.
* GDScript: typed where Godot can infer it, no ``await`` without a test that would catch an error,
  every server answer validated.
* Protocol changes need an updated schema, an example and a passing
  ``tests/validate_examples.py``.
* Documentation is English. Czech translation of the game is welcome in ``locales/client.csv``;
  of this documentation through ``sphinx-intl`` (``locale/cs``).
* By contributing you agree to license your work under the repository's licence (:doc:`repositories`).

Security
--------

Report a vulnerability privately as described in ``SECURITY.md`` of the repository, not in a public
issue. Never put a token, a password or a private key in an issue, a log or a screenshot.
