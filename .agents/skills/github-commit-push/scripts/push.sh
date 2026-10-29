#!/usr/bin/env bash
# Rebase the current branch on its remote and push it, with safety checks.
# Run after committing:  .agents/skills/github-commit-push/scripts/push.sh
# Refuses to push with a dirty index, a detached HEAD, or failing SVG checks.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
branch="$(git branch --show-current)"

if [[ -z "$branch" ]]; then
  echo "push.sh: detached HEAD; switch to a branch first" >&2
  exit 1
fi
if ! git diff --cached --quiet; then
  echo "push.sh: staged but uncommitted changes; commit them first" >&2
  exit 1
fi

# Validate assets if anything brand-related is in the commits being pushed.
range="origin/$branch..HEAD"
git rev-parse --verify --quiet "origin/$branch" >/dev/null || range="HEAD"
if git diff --name-only "$range" -- '*.svg' tokens .agents/skills/chase-brand-assets 2>/dev/null | grep -q .; then
  python3 .agents/skills/chase-brand-assets/scripts/check_svg.py
fi

# Pull others' work first. --autostash keeps unrelated local edits (other agents) out of the way.
if git ls-remote --exit-code --heads origin "$branch" >/dev/null 2>&1; then
  git pull --rebase --autostash origin "$branch"
fi

git push origin HEAD
sha="$(git rev-parse --short HEAD)"
echo "pushed $branch @ $sha → https://github.com/TijlIvens/the-chase_branding/commit/$(git rev-parse HEAD)"
