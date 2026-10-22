#!/usr/bin/env bash
# Merge upstream/main into the current branch, then re-apply the MHGA branding.
# Writes result=clean|conflict to $GITHUB_OUTPUT (and stdout).
#
# A conflict is auto-resolved ONLY when every conflicted file is one the branding
# script owns (see .github/scripts/rebrand.py): for those, upstream's version is taken
# and the branding is re-applied on top. Any other conflict aborts the merge untouched
# so a human resolves it (the workflow then opens an issue).
set -u
BRAND_FILES=" README.md INSTALL.txt TRANSLATING.md assets/source/covers.py "
emit() { echo "result=$1"; [ -n "${GITHUB_OUTPUT:-}" ] && echo "result=$1" >> "$GITHUB_OUTPUT"; return 0; }

if ! git merge --no-ff upstream/main -m "merge: sync with upstream ${UPSTREAM:-upstream} main"; then
  conflicts=$(git diff --name-only --diff-filter=U)
  for f in $conflicts; do
    case "$BRAND_FILES" in *" $f "*) ;; *) git merge --abort; emit conflict; exit 0 ;; esac
  done
  [ -n "$conflicts" ] || { git merge --abort; emit conflict; exit 0; }
  for f in $conflicts; do git checkout --theirs -- "$f" && git add -- "$f"; done
  git commit -q --no-edit || { git merge --abort 2>/dev/null; emit conflict; exit 0; }
fi

python3 .github/scripts/rebrand.py
# README's fork-badge table lives in a file we may just have taken from upstream; rebuild it.
python3 .github/scripts/fork_badges.py >/dev/null 2>&1 || true
if ! git diff --quiet; then
  git add -A
  git commit -q -m "chore: re-apply MHGA branding after upstream sync"
fi
emit clean
