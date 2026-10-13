#!/usr/bin/env bash
# Publish .wiki/ to this repository's GitHub wiki (<owner>/<repo>.wiki.git).
# Replaces the former GitHub Actions workflow .github/workflows/wiki-sync.yml (removed 2026-10-13: LabOnoM does
# not use GitHub Actions), which ran on every push to master that touched .wiki/** and on manual dispatch.
# When to run: by hand, from the repository root on an up-to-date master, after merging a change under .wiki/.
# Credentials: the owner's own GitHub login (`gh auth login`); nothing is read from a file in the repository.
set -euo pipefail
cd "$(dirname "$0")/.."

# Guards: the workflow published what was pushed to master, so publish only a clean, pushed master.
branch=$(git rev-parse --abbrev-ref HEAD)
[ "$branch" = master ] || { echo "FAIL  publish from master, not $branch" >&2; exit 1; }
git fetch --quiet origin master
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/master)" ] || { echo "FAIL  local master differs from origin/master" >&2; exit 1; }
[ -z "$(git status --porcelain -- .wiki)" ] || { echo "FAIL  .wiki/ has uncommitted changes" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "FAIL  not logged in to GitHub; run gh auth login" >&2; exit 1; }

repo=$(gh repo view --json nameWithOwner -q .nameWithOwner)
remote="https://github.com/$repo.wiki.git"
sha=$(git rev-parse HEAD)
auth=(-c credential.helper= -c 'credential.helper=!gh auth git-credential')
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# Step 1, was "Sync Wiki" (Andrew-Chen-Wang/github-wiki-action@v4, strategy clone, path .wiki, ignore index.md):
# the wiki's tree becomes .wiki/ (pages removed from .wiki/ are removed from the wiki), index.md is not added.
git "${auth[@]}" clone --quiet --bare "$remote" "$tmp/wiki.git"
(
  export GIT_DIR="$tmp/wiki.git" GIT_WORK_TREE="$PWD/.wiki"
  git config --unset core.bare
  echo "index.md" >> "$GIT_DIR/info/exclude"
  cd .wiki
  git add -A
  git commit --quiet --allow-empty -m "Update wiki $sha"
  git "${auth[@]}" push --quiet origin master
)

# Step 2, was "Set Home.md (Landing Page)": .wiki/index.md becomes the wiki's Home.md.
git "${auth[@]}" clone --quiet "$remote" "$tmp/wiki-repo"
cp .wiki/index.md "$tmp/wiki-repo/Home.md"
git -C "$tmp/wiki-repo" add Home.md
if ! git -C "$tmp/wiki-repo" diff --staged --quiet; then
  git -C "$tmp/wiki-repo" commit --quiet -m "Auto-sync index.md to Home.md"
  git "${auth[@]}" -C "$tmp/wiki-repo" push --quiet origin master
fi

echo "OK    wiki published from $sha: https://github.com/$repo/wiki"
