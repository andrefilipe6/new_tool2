# htaccess auditor

- `htaccess_scan.py PATH...` — static scanner (stdlib only, `--json`, `--strict`). Exit 1 on errors.
- `.claude/agents/htaccess-auditor.md` — Claude Code subagent that runs the scanner and explains fixes.
- `tests/samples/` — a good and a bad example.

## CSS auditor

- `css_audit.py PATH...` — checks Bootstrap overrides and load order, `:root` var organisation, and JS that CSS could replace (`--json`, `--strict`).
- `.claude/agents/css-auditor.md` — subagent that runs it and explains fixes.
- `tests/css_samples/` — good/bad examples.

## Agent team

`CLAUDE.md` ties together `bootstrap-ui-designer`, `php-backend`, `gitea-workflow`, `css-auditor`, `htaccess-auditor`, `platform-tools-integrator` and `platform-tools-maintainer` (all in `.claude/agents/`).
