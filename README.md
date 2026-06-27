# Waddington Landscape Dynamics

A computational model of cell-state dynamics during mouse neural tube
differentiation, built on the Delile et al. (2019) single-cell atlas. Given
any point in the landscape (pseudotime + UMAP coordinates), the model
decodes the corresponding gene expression state — and a separate set of
experiments explores whether a continuous *dynamics* model (a vector field
over the landscape) can simulate how a cell's state evolves over time.

## Demo

**[Try the live interactive explorer →](https://github.com/mo-to-ma/landscape-dynamics/blob/main/landscape-/outputs/explorer_static.html)**

## The story, in order

1. **Interactive Explorer** (`notebooks/interactive_explorer.ipynb`) —
   the foundation. A small model maps any landscape coordinate
   (pseudotime + UMAP1 + UMAP2) to a scVI latent vector, decoded to gene
   expression through a frozen scVI decoder. Move a slider, read off the
   expression at that exact point, live.

2. **Greedy manifold-constrained walk** (same notebook, final section) —
   built on top of the explorer: a simple way to trace a plausible path
   through the landscape one step at a time, without fitting any dynamics
   model. Constrained to stay near real data so it can't wander into
   territory the model has no support for.

3. **OT + deterministic vector field**
   (`notebooks/experiments/01_ot_deterministic.ipynb`) — an attempt
   at continuous dynamics: velocity estimated between pseudotime bins via
   optimal transport, fit to a single continuous vector field, integrated
   forward in time. Works, but has a real limitation — a vector field
   that can only output one direction per point breaks down at genuine
   fate branch points. See `REPORT.md` for the full diagnosis.

4. **kNN + correlation real-cell walk**
   **current work.** 
   Restricts every step to actual real cells (so it structurally
   can't leave the data manifold), selecting the next step via a kNN
   search in the visualized 3D space. **Not yet producing satisfying
   results — actively being refined**, see `REPORT.md` for the open
   questions being worked through.

## Setup

Data is not included in this repo — see `data/README.md` for how to obtain
the Delile et al. (2019) dataset and where to place it.

## License

See `LICENSE`.
