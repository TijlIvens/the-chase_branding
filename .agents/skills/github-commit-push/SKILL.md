---
name: github-commit-push
description: Commit and push changes in The Chase branding repo to GitHub (TijlIvens/the-chase_branding). Use after finishing any task that changed files in this repo, or when asked to commit, push, save, sync, publish or upload work to GitHub. Covers what to stage, commit message format, validation before committing, pulling and rebasing, and safe pushing when several agents work at once.
---

# Commit and push to GitHub

Remote: `origin` → `https://github.com/TijlIvens/the-chase_branding.git`, default branch `main`.
The owner wants finished work in this repo committed **and** pushed; do it at the end of
every task that changed files, without waiting to be asked. Skip it only if the user said
not to, or the work is unfinished or failing checks (then say so in your reply).

## 1. Check the state

```bash
git status --short
git branch --show-current
```
- If you're on a branch other than `main`, stay on it. Don't switch branches
  without being told to.
- If there are changes you did **not** make (another agent or the user is working),
  leave them alone. You commit only your own files.

## 2. Validate before committing

If any `.svg`, `tokens/` or `.agents/skills/chase-brand-assets/` file changed:
```bash
python3 .agents/skills/chase-brand-assets/scripts/check_svg.py   # must end "N/N SVGs pass"
python3 .agents/skills/chase-brand-assets/scripts/gallery.py     # keeps assets/gallery.html current
```
Don't commit if the check fails. Fix the problem, or stop and report it.

## 3. Stage explicitly

Stage the paths you changed by name. **Never** use `git add -A`, `git add .` or `git commit -a`:
they sweep up other agents' half-finished work.
```bash
git add assets/icons/game/crystal-shard.svg assets/gallery.html BRAND_BOOK.md
git diff --cached --stat     # confirm only your files are staged
```
Never commit: `.DS_Store`, `.env*`, keys/tokens, `*.pem`, editor folders, files over 10 MB,
or anything in `.gitignore`. `base-images/` is read-only, so don't commit changes to it
unless the user added images on purpose.

## 4. Commit message

[Conventional Commits](https://www.conventionalcommits.org), imperative, ≤ 72 chars subject:

```
<type>(<scope>): <what changed>

<optional body: why, and anything a reviewer should know>
```

| type | when |
|---|---|
| `feat` | new asset, icon, variant, skill, script feature |
| `fix` | corrected asset, wrong colour, broken script |
| `docs` | BRAND_BOOK.md, AGENTS.md, SKILL.md wording |
| `refactor` | restructure without visual change |
| `chore` | gallery rebuild, .gitignore, tooling |

Scopes: `logo`, `icons`, `tokens`, `brand-book`, `skills`, `app`, `lettering`, `repo`.

Examples:
- `feat(icons): add crystal-shard game icon`
- `fix(tokens): correct serpent-belly hex to match key art`
- `docs(brand-book): document ink lockups for light backgrounds`

One logical change per commit. If you did two unrelated things, make two commits.
Add your tool's own attribution trailer if it has one (e.g. `Co-Authored-By:`).

```bash
git commit -m "feat(icons): add crystal-shard game icon" -m "Optional body."
```

## 5. Sync, then push

```bash
git pull --rebase origin "$(git branch --show-current)"
git push origin HEAD
```
Or run both steps plus the safety checks in one go:
```bash
.agents/skills/github-commit-push/scripts/push.sh
```

**If the rebase conflicts:** another agent changed the same file. Resolve the conflict so that
both changes survive (for `assets/gallery.html`, just rerun `gallery.py` and `git add` it),
then `git rebase --continue`. If you cannot tell which version is right, run
`git rebase --abort` and ask the user.

**If the push is rejected** because `main` is protected or you lack permission, push a branch
and open a pull request instead:
```bash
git switch -c <type>/<short-name>
git push -u origin HEAD
gh pr create --fill --base main
```
Give the user the PR link.

## Never

- `git push --force` / `-f` / `--force-with-lease` on `main`, or `git reset --hard` on pushed commits
- Rewrite or amend commits that are already pushed
- `--no-verify` to skip hooks
- Delete remote branches, change repo settings, or edit `.git/config` / credentials
- Commit secrets. If you notice one was committed, stop and tell the user. Don't try to scrub history yourself.

## Report back

End with: commit hash(es) and subject(s), the branch pushed, and the GitHub URL
(`https://github.com/TijlIvens/the-chase_branding/commit/<hash>`, or the PR link).
If you skipped committing or pushing, say why.
