# Data

This project uses the mouse neural tube single-cell atlas from:

> Delile, J., Rayon, T., Melchionda, M., Edwards, A., Briscoe, J., & Sagner, A.
> (2019). *Single cell transcriptomics reveals spatial and temporal dynamics
> of gene expression in the developing mouse spinal cord.* Development,
> 146(12), dev173807. https://doi.org/10.1242/dev.173807

Raw data: deposited in **ArrayExpress under accession E-MTAB-7320**.
The original authors' analysis scripts are at
https://github.com/juliendelile/MouseSpinalCordAtlas.

**Provenance of the annotation columns** (`Pseudotime`, `Type_step1`,
`Type_step2`, `Neuron_subtypes`, `DV`): these are **not computed in this
repo**. They come directly from the original Delile et al. pipeline linked
above — `Type_step1`/`Type_step2` from their 2-step partitioning
algorithm, `Neuron_subtypes` from their per-neuronal-type subclustering,
and `Pseudotime` from their neurogenesis ordering. All credit for these
labels belongs to the original authors; this repo only converts their
output into an AnnData object for the modeling work that follows.

`data/prepare_adata.ipynb` documents exactly how that conversion was done.

To run the notebooks:

1. Obtain the original data/object from ArrayExpress (E-MTAB-7320) or the
   GitHub repo above.
2. Run `python data/prepare_adata.ipynb` (see that file for the exact inputs
   it expects) to produce `data/adata.h5ad`, with at minimum:
   - raw counts (`adata.X` or a specified layer)
   - `adata.obs['Pseudotime']`, `adata.obs['Type_step1']`, etc. (carried
     over from the original object, unmodified)
   - `adata.obs['replicate_id']` (or your batch key)
   - `adata.obsm['X_umap']`
3. Or place an already-prepared `adata.h5ad` directly at `data/adata.h5ad`.

Every notebook in this repo regenerates `artifacts/` (the trained scVI
model, latent representations, network weights) from this one file — none
of those intermediate artifacts, nor the original raw data, are committed.
