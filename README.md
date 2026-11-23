# English wiki for ESPSomfy-RTS

This branch holds an English translation of [xkain's French wiki](https://github.com/xkain/ESPSomfy-RTS/wiki).
Pushing to it publishes `wiki/` to this fork's [wiki](https://github.com/olliemaller/ESPSomfy-RTS/wiki)
through `.github/workflows/publish-wiki.yml`.

`wiki/.sync/` keeps it in step with the French wiki: `pages.json` maps French pages to English
ones, `state.json` records which French version each page was translated from, and `sync.py`
lists what changed (`status`), rewrites links in a new translation (`fix`) and checks every link
and heading (`check`). `wiki/.sync/INSTRUCTIONS.txt` is the update procedure.
