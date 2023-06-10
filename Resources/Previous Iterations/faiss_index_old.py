# faiss_index.py module

"""
faiss_index.py

This module provides a FaissIndex class for handling Faiss indexing of embeddings. The FaissIndex class creates an
index, performs search operations, and supports saving/loading of the index.

Usage:
    1. Create an instance of the FaissIndex class, providing the embeddings as input.
    2. Use the create_index method to create the Faiss index.
    3. Perform search operations using the search method.
    4. Save or load the index using the save_index and load_index methods.

Dependencies:
    - faiss
    - numpy as np

Notes:
    - The FaissIndex class handles the creation of the Faiss index and search operations.
    - The index is created with an L2 metric and supports IVFFlat indexing.
    - The index can be saved and loaded using the Faiss library functions.

Conceptual notes are below the code.
"""

import faiss
import numpy as np

# text-embedding-ada-002 embeddings = np.zeros((1, 1536))

# You might want to consider techniques such as the elbow method, silhouette analysis, or gap statistics to determine
# the optimal number of clusters for your specific dataset if accuracy is a key concern. n_list in the create_index
# method is the number of clusters. The default value is 100. The default value for nprobe is 10. nprobe is the number
# of clusters to search during a search operation. The default value for k is 5. k is the number of results to return
# during a search operation.


class FaissIndex:
    def __init__(self, embeddings):
        self.embeddings_np = np.array(embeddings, dtype=np.float32)
        if len(self.embeddings_np.shape) == 3:
            self.embeddings_np = self.embeddings_np.squeeze(axis=1)
        self.index = None

    def create_index(self, nlist=100, nprobe=10):
        print("Creating index in FaissIndex.create_index()")
        d = self.embeddings_np.shape[1]
        quantizer = faiss.IndexFlatL2(d)
        self.index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
        self.index.nprobe = nprobe
        print("Shape of embeddings_np:", self.embeddings_np.shape)
        if not self.index.is_trained:
            self.index.train(self.embeddings_np)
        self.index.add(self.embeddings_np)
        print("Index created in FaissIndex.create_index()")

    def search(self, query_embedding, k):
        if self.index is None:
            raise ValueError('Index has not been created')
        query_np = np.array(query_embedding, dtype=np.float32)
        if query_np.ndim == 2 and query_np.shape[1] == 1:
            query_np = query_np.squeeze(axis=1)
        print(query_np.shape)  # Add this line
        distances, indices = self.index.search(query_np, k)
        return indices, distances

    def save_index(self, index_path):
        if self.index is None:
            raise ValueError('Index has not been created')
        print("Saving Faiss index to", index_path)
        faiss.write_index(self.index, index_path)
        print("Faiss index saved to", index_path)

    def load_index(self, index_path):
        print("Loading Faiss index from", index_path)
        self.index = faiss.read_index(index_path)
        print("Faiss index loaded from", index_path)

    def get_index(self):
        return self.index


"""

When using Faiss, the quantizer and index are closely related components, but they are not specific to one another.
Let's understand the purpose and relationship between these components:

    Quantizer: The quantizer in Faiss is responsible for mapping vectors to a discrete set of centroids. It divides the
     vector space into smaller regions by creating a codebook of representative vectors called centroids. The quantizer
     compresses the vectors by assigning them to the nearest centroid. Faiss provides different quantization methods,
     such as Product Quantization (PQ) and Scalar Quantization (SQ), which can be chosen based on the application
     requirements.

    Index: The index in Faiss is the data structure used for efficient similarity search. It organizes the compressed
     vectors (quantized vectors) into a structure that enables fast search operations. Faiss provides various index
     types, including IVF (Inverted File), IVFADC (Inverted File with Asymmetric Distance Computation), and HNSW
     (Hierarchical Navigable Small World). Each index type has different characteristics in terms of memory usage,
     search speed, and accuracy.

The relationship between the quantizer and index in Faiss is as follows:

    The quantizer is used to transform the original vectors into quantized vectors, reducing the memory footprint and
     search complexity. The quantized vectors are then stored in the index structure.
     
    The index structure utilizes the quantized vectors for efficient search operations, such as nearest neighbor search
     or similarity search.

In summary, while the quantizer and index are interrelated components in Faiss, they serve distinct purposes. The
 quantizer compresses and quantizes the vectors, while the index organizes and facilitates fast search operations on the
 quantized vectors.

"""