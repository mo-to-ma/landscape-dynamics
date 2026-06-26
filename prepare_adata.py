"""
Converts the original Delile et al. (2019) data/object into the
AnnData (`adata.h5ad`) used by the notebooks in this repo.

Source: Delile, J. et al. (2019). Single cell transcriptomics reveals
spatial and temporal dynamics of gene expression in the developing mouse
spinal cord. Development, 146(12), dev173807.
Raw data: ArrayExpress E-MTAB-7320
Original analysis code: https://github.com/juliendelile/MouseSpinalCordAtlas

"""
import scanpy as sc
import pandas as pd
import numpy as np
import anndata as ad
import scipy.sparse as sp

counts_path = "UMI_count.tsv"
pheno_path = "phenoData_annotated.csv"

pheno = pd.read_csv(pheno_path, sep="\t", index_col=0)

chunksize = 2000  
reader = pd.read_csv(counts_path, sep="\t", index_col=0, chunksize=chunksize)

gene_ids, chunks = [], []
for chunk in reader:
  gene_ids.extend(chunk.index.tolist())
  chunks.append(sp.csr_matrix(chunk.values))  # sparsify now, drop the dense chunk
del chunk

genes_by_cells = sp.vstack(chunks)
del chunks
counts = genes_by_cells.T.tocsr()  # transpose: AnnData wants cells x genes
del genes_by_cells

cell_ids = pd.read_csv(counts_path, sep="\t", nrows=0, index_col=0).columns.tolist()
adata = ad.AnnData(X=counts, obs=pheno.loc[cell_ids], var=pd.DataFrame(index=gene_ids))

neural_mask = adata.obs["Type_step1"].isin(["Neuron", "Progenitor"])
adata = adata[neural_mask].copy()

print(adata)
print(adata.obs["timepoint"].value_counts())

sc.pp.highly_variable_genes(adata, flavor="seurat_v3", n_top_genes=2000)

adata.write_h5ad("adata.h5ad")