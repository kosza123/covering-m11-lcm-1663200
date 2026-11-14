#!/usr/bin/env python3
"""Clean-room verifier for claimed covering systems of the integers.

Usage: verify_cover_cr.py FILE.json L m

FILE.json holds either a list of [residue, modulus] pairs, or an object with
key "congruences", "found", "covering" or "best_cong" holding such a list.

Checks:
  (1) moduli are pairwise distinct integers >= 2
  (2) min modulus == m
  (3) lcm(moduli) == L
  (4) every integer is covered (checked over one period 0..lcm-1)

Coverage method: big-integer bitmask. For each congruence r mod M, the
bit pattern with bits r, r+M, r+2M, ... is built by repeated doubling
(p |= p << span; span *= 2), truncated to P bits, and OR-ed into an
accumulator; the result is compared with (1 << P) - 1.

Prints one JSON line; exit code 0 iff ok.
Pure Python 3 standard library.
"""
import hashlib
import json
import math
import sys

LIST_KEYS = ("congruences", "found", "covering", "best_cong")
# Do not attempt coverage on a period larger than this (bits).
MAX_PERIOD = 1 << 27


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def extract_pairs(data):
    if isinstance(data, list):
        return data, None
    if isinstance(data, dict):
        for k in LIST_KEYS:
            if k in data:
                return data[k], k
        return None, "object has none of keys %s" % (list(LIST_KEYS),)
    return None, "top-level JSON is neither a list nor an object"


def coverage_mask(congs, P):
    """Return the P-bit integer whose bit n is set iff n is covered."""
    full = (1 << P) - 1
    acc = 0
    for r, M in congs:
        r %= M
        if r >= P:
            continue  # can only happen if M does not divide P; nothing in range
        p = 1 << r
        span = M
        # After this loop, bits r + k*M are set for all k with r + k*M < r + span,
        # and span >= P, so every bit position < P of the form r+kM is set.
        while span < P:
            p |= p << span
            span <<= 1
        acc |= p & full
        if acc == full:
            break
    return acc, full


def first_set_bits(x, limit):
    out = []
    while x and len(out) < limit:
        low = x & -x
        out.append(low.bit_length() - 1)
        x ^= low
    return out


def popcount(x):
    try:
        return x.bit_count()
    except AttributeError:  # Python < 3.10
        return bin(x).count("1")


def main(argv):
    result = {
        "ok": False,
        "reasons": [],
        "uncovered_count": None,
        "first_uncovered": [],
        "n_congruences": 0,
        "L": None,
        "m": None,
        "sha256_of_input": None,
    }
    reasons = result["reasons"]

    def finish():
        result["ok"] = not reasons
        print(json.dumps(result))
        return 0 if result["ok"] else 1

    if len(argv) != 4:
        reasons.append("usage: verify_cover_cr.py FILE.json L m")
        return finish()
    path = argv[1]
    try:
        L = int(argv[2])
        m = int(argv[3])
    except ValueError:
        reasons.append("L and m must be integers")
        return finish()
    result["L"] = L
    result["m"] = m
    if L < 1:
        reasons.append("claimed L must be >= 1")
    if m < 2:
        reasons.append("claimed m must be >= 2")

    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError as e:
        reasons.append("cannot read input: %s" % e)
        return finish()
    result["sha256_of_input"] = hashlib.sha256(raw).hexdigest()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        reasons.append("invalid JSON: %s" % e)
        return finish()

    pairs, why = extract_pairs(data)
    if pairs is None:
        reasons.append(why)
        return finish()
    if not isinstance(pairs, list):
        reasons.append("congruence list is not a JSON list")
        return finish()

    congs = []
    for i, item in enumerate(pairs):
        if not (isinstance(item, (list, tuple)) and len(item) == 2):
            reasons.append("entry %d is not a [residue, modulus] pair: %r" % (i, item))
            continue
        r, M = item
        if not is_int(r) or not is_int(M):
            reasons.append("entry %d has non-integer residue or modulus: %r" % (i, item))
            continue
        if M < 2:
            reasons.append("entry %d has modulus %d < 2" % (i, M))
            continue
        congs.append((r, M))
    result["n_congruences"] = len(pairs)
    if len(congs) != len(pairs):
        # malformed entries already reported; still analyse the valid ones
        pass
    if not congs:
        reasons.append("no valid congruences")
        return finish()

    # (1) distinct moduli
    seen = {}
    dups = []
    for r, M in congs:
        seen[M] = seen.get(M, 0) + 1
    for M, c in sorted(seen.items()):
        if c > 1:
            dups.append(M)
    if dups:
        reasons.append("moduli not distinct; repeated: %s" % dups[:20])

    # (2) minimum modulus
    mn = min(M for _, M in congs)
    if mn != m:
        reasons.append("minimum modulus is %d, claimed m=%d" % (mn, m))

    # (3) lcm
    lcm = 1
    for _, M in congs:
        lcm = lcm // math.gcd(lcm, M) * M
    if lcm != L:
        if lcm < 10 ** 30:
            reasons.append("lcm of moduli is %d, claimed L=%d" % (lcm, L))
        else:
            reasons.append("lcm of moduli has %d digits, claimed L=%d" % (len(str(lcm)), L))

    # (4) coverage over one true period (lcm)
    P = lcm
    if P > MAX_PERIOD:
        reasons.append("coverage not checked: period lcm=%s exceeds limit %d"
                       % (P if P < 10 ** 30 else "huge", MAX_PERIOD))
        return finish()
    acc, full = coverage_mask(congs, P)
    missing = full ^ acc
    cnt = popcount(missing)
    result["uncovered_count"] = cnt
    result["first_uncovered"] = first_set_bits(missing, 10)
    if lcm != L:
        result["coverage_period_used"] = P
    if cnt:
        reasons.append("not a covering: %d of %d residues mod %d uncovered" % (cnt, P, P))
    return finish()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
