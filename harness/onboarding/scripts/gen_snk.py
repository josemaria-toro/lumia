#!/usr/bin/env python3
"""Generates a temporary strong-name key pair (.snk) without mono. Requires `openssl`.

Usage: gen_snk.py OUTPUT.snk
The key must NOT be committed: keep it outside the repo or in a git-ignored path, and store the
base64 of the private key as the GitHub secret STRONG_NAME_KEY (`base64 -w0 key.snk | gh secret set STRONG_NAME_KEY`).
"""
from __future__ import annotations

import re
import struct
import subprocess
import sys


def main(out: str) -> int:
    pem = subprocess.run(["openssl", "genrsa", "2048"], capture_output=True, text=True, check=True).stdout
    text = subprocess.run(["openssl", "rsa", "-noout", "-text"], input=pem, capture_output=True, text=True, check=True).stdout

    def field(name: str) -> bytes:
        m = re.search(rf"^{name}:\s*\n((?:[ \t]+[0-9a-f:]+\n)+)", text, re.M)
        return bytes.fromhex(re.sub(r"[^0-9a-f]", "", m.group(1)))

    def le(b: bytes, size: int) -> bytes:
        return b.lstrip(b"\0").rjust(size, b"\0")[::-1]

    bits = 2048
    blob = (struct.pack("<BBHI", 0x07, 0x02, 0, 0x2400) + b"RSA2" + struct.pack("<II", bits, 65537)
            + le(field("modulus"), bits // 8) + le(field("prime1"), bits // 16) + le(field("prime2"), bits // 16)
            + le(field("exponent1"), bits // 16) + le(field("exponent2"), bits // 16)
            + le(field("coefficient"), bits // 16) + le(field("privateExponent"), bits // 8))
    with open(out, "wb") as f:
        f.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]) if len(sys.argv) == 2 else print(__doc__) or 1)
