#!/usr/bin/env bash
# Rewrite the deprecated top-level `doi:` front-matter field as `hugoblox.ids.doi`.
#
# `academic import` still emits `doi:` at the top level. Hugo Blox deprecated that
# form, and b6c8c4d migrated all 137 existing pages off it, so every freshly
# generated page reintroduces a field the rest of the site no longer uses.
#
# Only touches files that have a top-level `doi:` and no `hugoblox:` block, so it
# is safe to re-run and cannot clobber a page that already carries the new form.
set -euo pipefail

shopt -s nullglob
migrated=0
skipped=0

for f in content/publication/*/index.md; do
  grep -q '^doi:' "$f" || continue

  if grep -q '^hugoblox:' "$f"; then
    echo "::warning file=$f::top-level doi: alongside an existing hugoblox: block — left alone"
    skipped=$((skipped + 1))
    continue
  fi

  sed -i 's|^doi: \(.*\)$|hugoblox:\n  ids:\n    doi: \1|' "$f"
  echo "  migrated $f"
  migrated=$((migrated + 1))
done

echo "✅ doi field migration: $migrated rewritten, $skipped needing a look"
