# htaccess auditor

- `htaccess_scan.py PATH...` — static scanner (stdlib only, `--json`, `--strict`). Exit 1 on errors.
- `.claude/agents/htaccess-auditor.md` — Claude Code subagent that runs the scanner and explains fixes.
- `tests/samples/` — a good and a bad example.
