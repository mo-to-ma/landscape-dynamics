# Report: building a cell-state model from a single-cell atlas

## Goal

Given a single-cell atlas with a pseudotime ordering and a 2D visualization
embedding (UMAP), build a model that can answer two related questions:

1. **Query:** what is the gene expression state at an arbitrary point in
   the landscape, including points no real cell occupies?
2. **Dynamics:** starting from a point, how does that state plausibly
   evolve forward through pseudotime?

(1) is solved and robust. (2) is an ongoing effort, told below in the
order it was actually pursued — starting simple, then attempting full
continuous dynamics, and currently working on a method that trades some
flexibility for staying anchored entirely to real data.

## Pipeline shared by every stage

- **scVI** is trained once on raw counts to produce a 10D latent
  representation (`X_scVI`) and a frozen decoder (latent → gene
  expression). This is reused everywhere downstream.
- Every stage filters out cells with missing pseudotime (~2,500 of
  ~24,000 in this dataset) **once**, before any other step, so every
  model trains on an identical population.

## Stage 1: Interactive Explorer — direct query

`notebooks/interactive_explorer.ipynb`. A small feedforward network maps
any landscape coordinate `(pseudotime, UMAP1, UMAP2) → scVI latent
vector`, decoded through the frozen scVI decoder. Wrapped in a
slider-driven UI: move the dot, read off the corresponding gene
expression live. Includes a "distance to nearest real cell" confidence
readout, so it's clear in real time whether a queried point is close to
real data or being extrapolated into a region the model has no support
for.

This is the foundation everything else builds on.

## Stage 2: Greedy manifold-constrained walk

Built on top of Stage 1 (same notebook, final section). A lightweight way
to trace *a* plausible path through the landscape one step at a time,
without fitting any dynamics model: at each step, sample candidate points
nearby, reject any whose decoded latent vector falls too far from real
data, move to the most promising valid candidate. Useful for quick
exploration; not a substitute for a properly validated dynamics model.

## Stage 3: OT + a deterministic vector field

`notebooks/experiments/01_ot_deterministic.ipynb`. A proper attempt at
continuous dynamics: velocity at each cell estimated using optimal
transport (Sinkhorn) between consecutive pseudotime bins, cost computed
in scVI latent space, each cell's velocity taken as displacement toward
its *expected* (probability-weighted mean) future position. A single
continuous vector field is fit to these estimates and integrated forward
in time.

**This worked, until a cell sat near a genuine fate branch point.** The
mean of two diverging real futures is a point in between them that no
real cell occupies. The fitted vector field dutifully learned to point
toward that empty space, and simulated trajectories passing through such
regions drifted off the data manifold — confirmed directly by checking
trajectory points' nearest-neighbor distance to real cells in latent
space, which spiked exactly where trajectories passed near known branch
regions.

This limitation is what motivated Stage 4: a method that can't drift off
the manifold because it never leaves real cells in the first place.

## Stage 4 (current, in progress): kNN + correlation real-cell walk

Instead of fitting a continuous vector field, this walk restricts every single step to
**actual real cells** — bin pseudotime, restrict candidates to the k
nearest real cells (by distance, measured directly in the plotted
`(pseudotime, UMAP1, UMAP2)` space rather than the 10D latent space, so
the path stays visually coherent), and move to the best matching
candidate among them.

**Status: not yet producing satisfying results, actively being refined.**
Open questions currently being worked through:

- Is bin granularity (`N_BINS`) the right lever, or does the candidate
  pool size (`K_NEIGHBORS`) need to scale with it?
- Selecting in the visualized 3D space trades biological precision for
  visual coherence (UMAP doesn't preserve latent-space similarity) — is
  that the right tradeoff, or does it need to weigh both spaces somehow?
- Does the path's resulting smoothness depend heavily on the specific
  starting cell, or is the roughness systematic?

This section of the repo will be updated as this is resolved.

## Open questions for future work

- How does the eventual dynamics approach compare quantitatively to
  existing tools in this space, particularly Dynamo (Qiu et al. 2022),
  which fits a deterministic continuous vector field from RNA velocity for
  similar purposes? A direct head-to-head, especially at branch points,
  would be a natural validation step once Stage 4 is working well.
- Could Stage 1's query model and Stage 4's real-cell walk be combined —
  e.g. using the real-cell path as anchor points and the query model to
  interpolate smoothly between them?
