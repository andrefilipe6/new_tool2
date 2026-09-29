---
name: orchestrate
description: Plan and dispatch work across this project's subagents (bootstrap-ui-designer, php-backend, gitea-workflow, css-auditor, htaccess-auditor, platform-tools-integrator, platform-tools-maintainer), choosing the right model and keeping context and token use low. Use for any multi-step task that spans more than one area, when deciding whether to delegate at all, or when the user types /orchestrate.
---

# Orchestrate

You (the main conversation) are the manager. Subagents cannot start other subagents, so every hand-off goes through you. The job is to use as few agents as possible, on the cheapest model that can do each part well, with tight briefs and short returns.

## 1. Decide whether to delegate at all
Do it yourself, with no agent, when:
- it's a question, an explanation, or a one-file or few-line change
- you already have the relevant files in context (an agent would re-read them from scratch)
- the next step needs back-and-forth with the user (agents can't ask questions)

Delegate when:
- the work reads many files you don't need to see (an audit, a PR review, wiring a site)
- it's a self-contained unit with a clear "done"
- it benefits from a narrower tool set (read-only auditors) or a stronger model

## 2. Route: who and on which model

| Task | Agent | Model | Escalate to |
|---|---|---|---|
| Run the CSS or `.htaccess` scanner and summarise | `css-auditor` / `htaccess-auditor` | haiku | sonnet if findings need judgement (CSS-over-JS trade-offs, rewrite logic) |
| Commit, branch, open a PR | `gitea-workflow` | sonnet | haiku for a plain commit + push |
| Review a PR | `gitea-workflow` | sonnet | opus for security-heavy or large diffs |
| Pages, components, styling | `bootstrap-ui-designer` | sonnet | none |
| PHP logic, forms, DB, APIs | `php-backend` | sonnet | opus for auth, crypto, sessions, payments, migrations on live data |
| Wire a site to platform-tools / adopt a shared feature | `platform-tools-integrator` | sonnet | none |
| Change platform-tools itself | `platform-tools-maintainer` | opus | never downgrade: it deploys to the whole fleet |
| Find where something is in a big codebase | built-in `Explore` | haiku | none |

Each agent's default model is set in its frontmatter. Override it for a single call with the Agent tool's `model` parameter; don't edit the file for a one-off.

**Model rules of thumb**
- **haiku:** mechanical work: running scripts, grepping, summarising JSON, simple commits. Cheapest and fastest.
- **sonnet:** the default for writing and reviewing code.
- **opus:** only where a mistake is expensive: security, shared or fleet-wide code, tricky migrations, or a sonnet attempt that already failed.
- Never use opus for scanning, searching or formatting.

## 3. Standard pipelines
- **UI-only change:** `bootstrap-ui-designer`, then `css-auditor` (haiku).
- **Feature needing data:** `php-backend` (defines the view contract), then `bootstrap-ui-designer` with that contract pasted in, then the auditors in parallel.
- **Routing change:** `php-backend`, then `htaccess-auditor`.
- **New platform:** `platform-tools-integrator`, then `htaccess-auditor`, then `gitea-workflow`.
- **Shared code change:** `platform-tools-maintainer` (opus), then `gitea-workflow` PR review (sonnet or opus), then the integrator for any per-site steps.
- **Ship:** `gitea-workflow`, only when the user asks to commit, push or open a PR.

Run independent steps in parallel (several Agent calls in one message) or in the background. Run dependent steps in order, passing forward only what the next one needs.

## 4. Write a tight brief
Agents start cold. A good brief saves them from re-exploring:
- **Goal:** one sentence, with a definition of done.
- **Files:** exact paths to read or change. Don't say "look around".
- **Context you already have:** the contract, decisions, constraints. Paste it; don't make the agent rediscover it.
- **Out of scope:** what not to touch.
- **Return format:** e.g. "Reply in 15 lines or fewer: files changed, checks run with results, open questions. No code dumps, no restating the brief."

## 5. Save context and tokens
- **Make scripts do the work.** Run `css_audit.py --json` and `htaccess_scan.py --json` directly when you only need the findings; an agent only adds value when the findings need interpreting.
- **Continue, don't respawn.** To follow up with an agent that just finished, use SendMessage to its id/name; a new Agent call starts from zero.
- **One agent per area per task.** Don't split one file's work across two agents, and don't fan out to "check everything".
- **Don't re-read what an agent read.** Trust its summary; open a file yourself only to verify a specific claim.
- **Keep returns small.** Ask for summaries, paths and line numbers, never whole files. Big outputs go in files in the scratchpad, referenced by path.
- **Read-only where possible.** Auditors report; you or the owning agent apply fixes. This avoids two agents editing the same file.
- **Stop early.** If an agent returns blocked (missing access, secrets, a decision), don't retry with another agent. Ask the user.

## 6. After dispatching
- Check each result: did it run the checks it claims? Verify one key claim cheaply (e.g. `git diff --stat`, re-run the script).
- Report to the user what each agent did, which model it used, and what's left. Never report unrun checks as passing.
