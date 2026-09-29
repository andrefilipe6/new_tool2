# Project guide for Claude

PHP + Bootstrap 5 web project, served by Apache (`.htaccess`, extensionless URLs) and hosted on **Gitea**.

## Agents (`.claude/agents/`)

| Agent | Owns | Delegate when |
|---|---|---|
| `bootstrap-ui-designer` | HTML/PHP views, CSS, front-end JS, theming | Anything the user sees: pages, components, layout, styling |
| `php-backend` | Routing, controllers, validation, DB, auth, APIs, `.htaccess` | Server logic, data, security, URL rewriting |
| `gitea-workflow` | Branches, commits, PRs, reviews, merges on Gitea | Commit / push / open PR / review PR / release |
| `css-auditor` | Read-only CSS review | After UI changes, or "check my CSS" |
| `htaccess-auditor` | Read-only `.htaccess` review | After routing changes, or "check my htaccess" |

## How they work together
1. **Plan:** split the task into backend and UI parts. Backend comes first when the UI needs new data.
2. **php-backend** implements the logic and states the exact variables/JSON each view receives.
3. **bootstrap-ui-designer** builds the view against that contract, reusing `:root` tokens and Bootstrap components.
4. **Audit:** `css-auditor` / `htaccess-auditor` (or the scripts directly) on changed files. Fix errors before moving on.
5. **gitea-workflow** runs the quality gate, commits on a feature branch, pushes, and opens a PR when the user asks.

For a small single-area change, use just that one agent. Don't fan out needlessly.

## Shared conventions
- **Security:** prepared statements, escape all output, CSRF on POST, no secrets in git, `display_errors` off in production.
- **CSS:** Bootstrap is never edited. Custom CSS loads after it, uses `:root` tokens and `--bs-*` vars, adds no global overrides of core classes, and prefers CSS over JS.
- **URLs:** extensionless (`/about` → `about.php`). `/about.php` 301-redirects to `/about`, and rewrite rules check `-f`/`!-d`.
- **Git:** feature branches, Conventional Commits, no direct pushes to `main`, no force-push on shared branches.

## Checks
```bash
php -l path/to/file.php                          # every changed PHP file
python3 css_audit.py --json <css/html/js paths>  # CSS / Bootstrap / CSS-over-JS
python3 htaccess_scan.py --json <.htaccess paths> # rewrite & security rules
```
Run the project's own tests/linters too (`vendor/bin/phpunit`, `phpstan`) if present. Report what was actually run; never claim unrun checks passed.
