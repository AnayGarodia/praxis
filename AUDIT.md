# AUDIT — proposed diam-3 constraint (arXiv:2601.03572): REJECTED as unsound

Checked the primary source (arXiv abstract page, 2026-01-07, Pandey & Ravi,
"On structural properties of some probable R(3,10)-critical graphs").

The paper studies R(3,10)-CRITICAL graphs, defined there as graphs on
R(3,10)-1 vertices, UNDER THE ASSUMPTION R(3,10)=42 — i.e. 41-VERTEX
(3,10)-graphs. Its results (min degree = connectivity in {6,7,8}; diameter
2 or 3; 21 degree sequences for the diam-2 delta=6 case) are statements
about those 41-vertex graphs, not about (3,10;40)-graphs.

The coordinator's paraphrase — "any (3,10;40)-graph with diam=2 has
delta>=6" — is NOT what the paper proves. Therefore:

1. Do NOT add any diameter constraint to the d=5 rung encoding on the basis
   of this paper. No v2 CNF is published.
2. The v1 cube set (data/d5cubes_deep.icnf) remains the only authoritative
   workload.
3. Residual-novelty scoping: the paper does not overlap our target. Our d=5
   rung claim ("every (3,10;40)-graph has min degree >= 6") remains fully
   novel if completed; the paper's structural results live one vertex up
   (n=41) and under a different assumption (R=42, superseded by
   Angeltveit's R(3,10)<=41).

Separately, whether every (3,10;40)-graph has diameter <= 3 is plausible but
unproven here; if someone supplies a proof, an "exists distance>=3 pair"
constraint could only be added via auxiliary variables (a disjunction over
all pairs), NOT by fixing a labeled pair — fixing labels for a second
structure on top of the deg-5 vertex fixing is not a valid WLOG without a
new symmetry argument compatible with SMS minimality.
