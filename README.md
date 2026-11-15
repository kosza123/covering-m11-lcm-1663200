# A distinct covering system with minimum modulus 12 and lcm 1 663 200, and the bound L_min(11) ≤ 1 663 200

**Filip Majchrzak** (ORCID 0009-0007-3475-8900), independent researcher, Poland — 14 November 2026

> Archived on Zenodo — this version (1.0.1; same data files and verifier): **doi:[10.5281/zenodo.24241360](https://doi.org/10.5281/zenodo.24241360)**; all versions: doi:[10.5281/zenodo.24214001](https://doi.org/10.5281/zenodo.24214001)

## Result

A *distinct covering system* is a finite set of congruences x ≡ a_i (mod d_i), with pairwise distinct moduli d_i > 1,
such that every integer satisfies at least one of them. Following J. Zhang [1], let L_min(m) denote the least
possible lcm of the moduli of a distinct covering system whose minimum modulus is m.

**Theorem.** There is a distinct covering system with minimum modulus 12 whose moduli are exactly the 277 divisors
d ≥ 12 of

  L = 1 663 200 = 2^5 · 3^3 · 5^2 · 7 · 11.

Adding the congruence x ≡ 0 (mod 11) gives a distinct covering system with minimum modulus 11 and the same lcm.
Hence

  **L_min(11) ≤ 1 663 200.**

The adjoined congruence is valid because no modulus of the first system equals 11 (all are ≥ 12), 11 divides L, so
the lcm is unchanged, and adding a congruence to a covering system keeps it a covering system.

**Consequence.** Zhang [1, Conjecture 1] conjectured L_min(11) = 3 326 400. The system here has half that lcm, so the
m = 11 case of that conjecture is false. The m = 8, 9, 10 cases are not affected by this note.

## Files

| File | Content |
|---|---|
| `covering_m12_L1663200.txt` / `.json` | the 277 congruences (residue, modulus), minimum modulus 12 |
| `covering_m11_L1663200.txt` / `.json` | the same plus 0 (mod 11): 278 congruences, minimum modulus 11 |
| `verify.py` | standalone verifier (Python 3, standard library only) |
| `SHA256SUMS` | checksums of the files |

## How to verify

```
python3 verify.py covering_m12_L1663200.json 1663200 12
python3 verify.py covering_m11_L1663200.json 1663200 11
```

The verifier checks that the moduli are pairwise distinct, the minimum modulus and the lcm have the stated
values, and every residue 0, …, L − 1 is covered. Since the system is periodic with period L, this means every
integer is covered. Each check prints one JSON line with `"ok": true`. The verification takes well under a second on a laptop-class machine.

Before publication the two systems were also checked with two other programs written separately (one numpy sieve,
one pure-Python search per residue); all three agree.

## How it was found

By a heuristic computer search (local search over residue assignments on Z/LZ), run in the author's research
project with AI assistance (Claude, Anthropic). The search was for minimum modulus 12; the consequence for
minimum modulus 11 came from the monotonicity step above. The search method is not claimed to be new.

## What is not claimed

- That 1 663 200 is the least lcm for minimum modulus 11 or 12. No lower bound is given.
- Anything about minimum moduli 8, 9 or 10.
- Priority beyond the literature located. Searches of arXiv and the web (13–14 November 2026) and a direct check of
  Chapter V of Krukenberg's thesis [3] (coverings with smallest modulus up to 18) found no distinct covering with
  minimum modulus 11 and lcm below 3 326 400. The number
  1 663 200 itself is not new as an lcm: it is the lcm of Krukenberg's covering with minimum modulus **10**
  [3, Chapter V, table on pp. 38–39] and of W. Bosma's greedy construction with minimum modulus 10 [2]. For minimum
  modulus 11 and 12 the coverings in [3] have lcm 21 621 600 and 237 837 600 (86 486 400 and 951 350 400 in the
  second construction there). The system here has minimum modulus 12.

## Related

The author's earlier record on distinct coverings with minimum modulus 8 and 5-smooth lcm:
doi:10.5281/zenodo.24202654.

## References

[1] J. Zhang, *Small-LCM Distinct Covering Systems via Segmented Local Search*, arXiv:2611.01282v1 [math.NT], 2026.

[2] W. Bosma, *Some computational experiments in number theory*, in: W. Bosma, J. Cannon (eds.), Discovering
Mathematics with Magma, Springer, 2006, pp. 1–30 (as cited in [1], Table 1).

[3] C. E. Krukenberg, *Covering Sets of the Integers*, Ph.D. thesis, University of Illinois at Urbana-Champaign,
1971.

## Changes

- **1.0.1** (15 November 2026). Literature note corrected: the lcm 1 663 200 for minimum modulus 10 goes back to
  Krukenberg (1971) [3], not only to Bosma (2006) [2]; the thesis was checked for minimum modulus 11 and 12.
  The data files and the verifier are unchanged (same SHA-256 sums).
- **1.0.0** (14 November 2026). First version.

## License

Data and text: CC BY 4.0. `verify.py`: MIT.
