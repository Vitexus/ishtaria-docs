Publishing on Steam
===================

This page lists what has to be true before Ishtaria can be sold or given away on Steam, what it
costs, how long it takes, and where the project stands today. It is a planning document, not a decision:
whether to release on Steam at all is a decision of the project owner (:doc:`../roadmap`, milestone M10).

.. note::

   Checked on **2026-10-07** against the public pages of the Steamworks documentation (sources at
   the end). Valve changes its rules; re-read the pages before every step. Some pages (the Steam
   Distribution Agreement, details of the revenue share, rules shown only to partners) are visible
   only after signing in as a partner and are **not** covered here. Nothing on this page is legal or tax
   advice.

The decisions that come first
-----------------------------

Four questions decide how the work looks, so settle them before spending money:

#. **Who is the publisher?** Steam wants a legal person or business that owns or has the right to
   publish the game, with bank and tax papers in the same name. A person acting as a sole
   proprietor and a company are handled differently by tax and by liability.
#. **Which platforms?** Steam serves Windows, macOS and Linux/SteamOS. The project supports Debian and
   Ubuntu on x86-64 only (:doc:`../decisions/0003-debian-only`). A Linux-only listing is allowed, but the
   product must work on every system the store page names, and it reaches only Linux and Steam Deck players.
   Adding Windows means changing that decision (Godot export presets for Windows and macOS exist in
   ``ishtaria-client/export_presets.cfg``, but those platforms are not supported, built by the CI or tested).
#. **How will real money work?** Valve requires that in-game purchases of a Steam product go through the
   Steam Wallet. That conflicts with the real-money land leases of :doc:`../decisions/0006-monetization`
   (see *Money* below). The simplest answer is a Steam build without real-money features.
#. **Who runs the worlds?** Steam does not host game servers. Ishtaria needs at least one official world
   that is online at launch, with the capacity and support that implies (:doc:`../operations/hardening`).

What Valve requires
-------------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Step
     - Requirement
   * - Steamworks account and agreements
     - Join the Steamworks partner programme and sign the Non-Disclosure Agreement and the Steam
       Distribution Agreement.
   * - App fee
     - **US$100 (or equivalent) per app**, not refundable but recoupable once the app earns at
       least US$1,000 of adjusted gross revenue on Steam. Every new app (also a free one, also a
       separate soundtrack or tool) needs its own fee.
   * - Identity, bank and tax
     - The legal name of the company must match the bank account holder and the tax papers. Bank
       details and tax information (a W-9 equivalent for US persons, a W-8BEN equivalent for people in treaty
       countries) are verified by a third party, which "may take 10 to 15 business days".
   * - Waiting period
     - A **21-day** wait after the fee is paid before release is possible.
   * - Coming Soon page
     - The store page must be public as *Coming Soon* for **at least two weeks** before release.
   * - Store page review
     - 3–5 business days. Submit at least 7 days before the date you want, in case Valve asks for changes.
   * - Build review
     - 3–5 business days. The build on the default branch must be substantially complete, must launch on
       every OS the store page lists, and every advertised feature must work. Later updates need no review.
   * - Release
     - Nothing is released automatically: the developer presses *Release App* after the checklists
       *Store Presence* and *Game Build* are marked ready and approved.
   * - Content survey
     - Three parts: general content (it produces the regional age ratings), mature content, and generative
       AI content. Inaccurate answers can affect approval.

Timeline: if the paperwork, the store page and the build are ready, the earliest release is about **three to
five weeks** after the fee is paid (the 21-day wait and the two weeks of Coming Soon overlap with the
reviews). Plan for more, because the tax verification alone takes up to three weeks.

Technical requirements for a Linux build
----------------------------------------

* **Steamworks SDK and SteamPipe.** Games are uploaded with ``steamcmd`` from the ``ContentBuilder`` of
  the Steamworks SDK, using a build script (a VDF file) that maps folders to **depots**. The
  ``default`` branch is the one players get; it can only be set live in the web interface; other branches
  (for example ``beta``) are for testing. Keep pack files below roughly 1–2 GB so that updates stay small.
  A Debian package is not what Steam distributes: the depot holds the exported game.
* **Linux and the runtime.** Valve recommends Ubuntu LTS for development and testing. Ship 64-bit
  binaries. After a launch option for Linux exists, choose the *Steam Linux Runtime 3 (sniper)* container
  under *Installation → Linux Runtime*. Vulkan is the preferred graphics API, OpenGL is supported.
* **Declare the platforms** in two places (Steamworks settings and the store page) and give system
  requirements for each; do not tick a platform before it is tested on a beta branch.
* **The Steamworks API in the game is optional.** Achievements, overlay, cloud saves and Steam login
  need it (Godot has a community integration, GodotSteam, whose licence must be checked); uploading needs
  only the SDK tools.
* **Steam Deck** has its own review, which is **not mandatory** but decides the badge players see. Criteria
  include full controller support by default without changing settings, correct button prompts, text of at least
  9 pixels at 1280×800, no launcher that needs a mouse, and 30 frames per second at default settings.

Store page and graphics
-----------------------

The text must describe only what exists at launch, be detailed and coherent, and **contain no links to
external websites**. Screenshots must show gameplay: no concept art, cinematics, awards or marketing text.
Capsules must show a readable title or logo.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Asset
     - Size (pixels)
     - Note
   * - Header capsule, library header
     - 920 × 430
     - logo and artwork only
   * - Small capsule
     - 462 × 174
     - logo and artwork only
   * - Main capsule
     - 1232 × 706
     - logo and artwork only
   * - Vertical capsule
     - 748 × 896
     - logo and artwork only
   * - Library capsule
     - 600 × 900
     - logo and artwork only
   * - Library hero
     - 3840 × 1240, PNG
     - artwork only
   * - Library logo
     - 1280 wide or 720 tall, PNG
     - drawn over the hero
   * - Screenshots
     - 1920 × 1080 or larger, 16:9
     - at least one is required; five or more are sensible; gameplay only
   * - Page background (optional)
     - 1438 × 810
     - subtle
   * - Shortcut icon / app icon
     - 256 × 256 (.ico or .png) / 184 × 184 (.jpg)
     -
   * - Event cover
     - 800 × 450
     - needed for the first announcement

A trailer is optional but expected. The branding of the project (emblem, wordmark and splash in
``ishtaria-client/assets/branding/``) is a start, but nothing in the repository has the sizes above yet, and the
two screenshots of the web portal are 1200 × 675 and too small.

Content rules and disclosures
-----------------------------

* **Content survey.** Ishtaria has violence (hunting, creatures that bite, permanent death with graves) and no
  sexual content. Answer honestly; even content in the build that players cannot reach must be disclosed.
* **Generative AI.** Valve distinguishes *pre-generated* content (made with AI tools during development and
  shipped to players: art, sound, narrative, localisation) and *live-generated* content (made while the game
  runs). Pre-generated content is judged like any other: no illegal or infringing material and consistent with the
  store page. For live-generated content you must describe the guardrails. In Ishtaria today:

  - pictures generated with InvokeAI (the application icon and splash, the portrait of the gate guard, item
    icons including the spell scrolls), and spoken dialogue rendered with Piper, are **pre-generated AI
    content** and must be declared (the list is in ``ishtaria-client/README.md``);
  - dialogue drafted with a local language model and reviewed by a person counts as AI-assisted narrative;
  - **no** content is generated while the game runs: no language model runs on the server (ADR 0008).
    Keep it that way, or the guardrail description becomes part of the review. Code written with an
    assistant is not content consumed by players, but the project should still be honest about it.
* **Rights.** You promise that you own or may distribute everything in the build. The assets of the
  client are CC0 (Kenney, most of Quaternius) or require **attribution** (some Quaternius and Poly Pizza
  models are CC BY 3.0). Add an in-game credits screen before release, keep the licence files, and
  get a **written licence for commercial distribution** of every datadisk whose artwork belongs to its author
  (the *Endland* datadisk is not Kenney or bundled material). The client is MIT and the server AGPL: neither
  prevents a sale, but the AGPL server is not part of the Steam download.
* **Privacy.** Accounts (a nickname and a password hash) and chat are personal data. Publish a privacy
  policy and the terms of the official world before launch, and give players a way to ask for deletion
  (:doc:`0011-sharing-achievements <../decisions/0011-sharing-achievements>` describes what is shared and how
  it is revoked).
* **Accounts.** Players of Ishtaria use an account of the world they join, not a Steam account. Steam
  store pages show when a game requires a third-party account; describe the requirement plainly. Whether to
  add *Sign in with Steam* (Steam authentication tickets checked by the server) is an open design decision.

Money
-----

The build review states: *"Your product must use Steam Wallet for any in-game transactions"* and the
product *"cannot direct users to external payment systems"*; the microtransaction documentation says that
for any in-game purchase Steam customers can only pay from the Steam Wallet.

Ishtaria's current monetization (:doc:`../decisions/0006-monetization`) lets a world sell **land leases**
for real money through a payment gateway and a signed webhook (``ishtaria-server/src/land.rs``). The client has
no purchase window, but the server does expose it. For a Steam release there are three honest options:

#. **A Steam build without real-money features.** The land leases stay off (they are off by default), and
   the first release earns money from the game's price (or nothing, if it is free). This is the cheapest
   and the one this page recommends for a first release.
#. **Steam Microtransactions.** Implement Steam's microtransaction API on the server (it needs the
   player's Steam identity, which Ishtaria does not use today) and sell leases through the wallet. A large change
   that also touches the federation, because worlds of other operators would sell in a client that Steam
   distributes.
#. **Do not sell on Steam.** Distribute the packages only through the project's own repository.

Whichever you choose, read the Steam Distribution Agreement before the first payment of any kind. The
rule that money buys space and appearance and never power (:doc:`invariants`) holds in every case.

Achievements
------------

Ishtaria's achievements are already shaped for Steam, but nothing talks to Steam yet:

* **The server decides.** An achievement is granted only inside the action that earns it
  (``ishtaria-server/src/achievements.rs``) and announced to its owner as an ``achievement`` event. A Steam build
  would only *mirror* an announced achievement with the Steamworks API (``SetAchievement`` and ``StoreStats``,
  for example through GodotSteam); the client never decides one itself.
* **Stable names.** Every entry of ``GET /achievements`` carries ``steam``, its API name in Steamworks: the id in
  capitals with a datadisk's ``:`` written as ``__`` (``first_harvest`` → ``FIRST_HARVEST``,
  ``gilgamesh:foundation_reader`` → ``GILGAMESH__FOUNDATION_READER``). Ids never contain a double underscore,
  so two achievements never share a name. Never rename or reuse an id once it is released.
* **What Steamworks needs.** Each achievement is entered in the Steamworks settings of the app with its API name,
  a localised name and description, the hidden flag and two icons (earned and not earned). The catalog has all
  of them except the icons, which are inventory icons today and have to be rendered at Steam's size; check the
  *Stats and Achievements* pages of Steamworks for the current rules.
* **Datadisks.** A disk's achievements (``achievements.yaml``) exist on Steam only if they are entered in the
  app's settings, so only disks published with the game can have Steam achievements. The client ignores names
  Steam does not know.
* **Trust.** Players can join worlds run by anyone, and any world server can announce any achievement. A Steam
  build has to mirror achievements only from worlds it trusts (the official worlds, by their world identity), or
  Steam achievements could be farmed on a private server.

Where Ishtaria stands
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 14 56

   * - Condition
     - Status
     - What is missing
   * - Linux build that launches
     - partly
     - ``make build`` exports ``ishtaria-client.x86_64`` with Godot; a depot, a SteamPipe script and a test on
       Ubuntu LTS and SteamOS are missing.
   * - Controller support
     - missing
     - Keyboard and mouse only; no gamepad mapping or button prompts. Needed for a good Steam Deck result
       (milestone M9).
   * - Graphics settings and text size
     - partly
     - Language and sound settings exist; no graphics options, UI scale or accessibility settings (M9).
   * - Tutorial for new players
     - missing
     - Reviewers and players start cold (M9).
   * - Official online world
     - missing
     - A server with TLS, backups, monitoring and moderation (:doc:`../operations/hardening`); a terms of
       service and privacy policy.
   * - Content survey and AI disclosure
     - to do
     - The lists above; a person has to answer for them.
   * - Credits and licences
     - partly
     - README credits and Debian copyright exist; an in-game credits screen and a written licence for
       commercial use of third-party datadisks do not.
   * - Store page and graphics
     - missing
     - Capsules, hero, logo, five or more 1920 × 1080 gameplay screenshots, a description with no external
       links, and a trailer, all made from the real client (M8, press kit).
   * - Money rules
     - decision
     - See *Money*.
   * - Company, bank, tax, app fee
     - missing
     - Not a technical task: start early, because the verification takes weeks.
   * - Achievements
     - partly
     - The server grants them and names each for Steamworks (*Achievements* above); the Steamworks API in the
       client, the trusted-world rule and icons in Steam's size are missing.
   * - Features advertised on the page
     - rule
     - Advertise only what works at launch: no planned federation, no share links (ADR 0011), no seasons.

Checklist
---------

.. list-table::
   :header-rows: 1
   :widths: 6 94

   * - ☐
     - Publisher chosen; legal name, bank account and tax papers ready and consistent
   * - ☐
     - Platform decision recorded (a new ADR if it changes :doc:`../decisions/0003-debian-only`)
   * - ☐
     - Money decision recorded (a new ADR if it changes :doc:`../decisions/0006-monetization`); Distribution Agreement read
   * - ☐
     - Official world running with TLS, backups and monitoring; terms of service and privacy policy published
   * - ☐
     - Steamworks partner account, agreements signed, US$100 app fee paid, tax interview submitted
   * - ☐
     - Linux export in a depot, SteamPipe script, Steam Linux Runtime selected, tested on a ``beta`` branch on Ubuntu LTS and SteamOS
   * - ☐
     - Controller support, UI scale and graphics settings, tutorial (if a Steam Deck badge matters)
   * - ☐
     - Credits screen; licences of every asset and datadisk checked for commercial distribution
   * - ☐
     - Content survey answered (violence; AI disclosure for icons, images and voices)
   * - ☐
     - Store page: text without external links, all graphics, five or more gameplay screenshots, trailer; set to *Coming Soon* (two weeks minimum)
   * - ☐
     - Store presence and game build submitted and approved; release date at least 7 days after the submission
   * - ☐
     - Release App pressed by a person, with the world ready for the first players

Sources
-------

Steamworks documentation (public pages, 2026-10-07):

* `Getting started <https://partner.steamgames.com/doc/gettingstarted>`_ and `Onboarding <https://partner.steamgames.com/doc/gettingstarted/onboarding>`_
* `Steam Direct fee <https://partner.steamgames.com/doc/gettingstarted/appfee>`_
* `Release process <https://partner.steamgames.com/doc/store/releasing>`_ and `Review process <https://partner.steamgames.com/doc/store/review_process>`_
* `Store graphical assets <https://partner.steamgames.com/doc/store/assets>`_
* `Content survey <https://partner.steamgames.com/doc/gettingstarted/contentsurvey>`_ (including generative AI)
* `Uploading to Steam <https://partner.steamgames.com/doc/sdk/uploading>`_, `Platforms <https://partner.steamgames.com/doc/store/application/platforms>`_,
  `Developing for SteamOS and Linux <https://partner.steamgames.com/documentation/linux_landing>`_
* `Steam Deck compatibility review <https://partner.steamgames.com/doc/steamhardware/compat>`_
* `Microtransactions <https://partner.steamgames.com/doc/features/microtransactions>`_
