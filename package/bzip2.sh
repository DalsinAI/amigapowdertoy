#!/bin/sh
# Prints the GFOpenBZip2 drawer to build with: $BZIP2 when it is set (an
# unpacked GFOpenBZip2 archive's GFOpenBZip2 drawer), otherwise the release
# named in package/bzip2.env, downloaded with gh into build-amiga-deps/,
# checked against its SHA-256 and unpacked there (with lha, or
# tools/lha_archive.py where there is no lha).
# MIT, Copyright (c) 2026 AmiCradle Team.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/.." && pwd)
. "$HERE/bzip2.env"
if [ -n "${BZIP2:-}" ]; then
    [ -f "$BZIP2/Libs/bzip2.library" ] || { echo "bzip2.sh: no Libs/bzip2.library in $BZIP2" >&2; exit 1; }
    echo "$BZIP2"
    exit 0
fi
D="$ROOT/build-amiga-deps"
A="$D/$GFOPENBZIP2_ARCHIVE"
mkdir -p "$D"
[ -f "$A" ] || gh release download "$GFOPENBZIP2_TAG" -R "$GFOPENBZIP2_REPO" -p "$GFOPENBZIP2_ARCHIVE" -D "$D" >&2
echo "$GFOPENBZIP2_SHA256  $A" | sha256sum -c --quiet - >&2 \
    || { echo "bzip2.sh: $A is not the archive in package/bzip2.env" >&2; exit 1; }
U="$D/${GFOPENBZIP2_ARCHIVE%.lha}"
if [ ! -f "$U/.unpacked-$GFOPENBZIP2_SHA256" ]; then
    rm -rf "$U"
    mkdir -p "$U"
    if command -v lha >/dev/null 2>&1; then
        (cd "$U" && lha xq "$A")
    else
    python3 -B - "$A" "$U" "$ROOT/tools" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[3])
import lha_archive
out = Path(sys.argv[2])
for m in lha_archive.read(Path(sys.argv[1]).read_bytes()):
    if m.path.endswith("/") or ".." in m.path.split("/"):
        continue
    p = out / m.path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(m.data)
PY
    fi
    touch "$U/.unpacked-$GFOPENBZIP2_SHA256"
fi
echo "$U/GFOpenBZip2"
