"""
faiss_index.py Module

This module provides a FaissIndex class for handling Faiss indexing of embeddings. The FaissIndex class facilitates the
creation of an index, performs search operations, and supports saving/loading of the index.

Usage:
1. Create an instance of the FaissIndex class, providing the embeddings and the data type (node or sentence) as input.
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
- The class supports different data types, specifically nodes and sentences.

Conceptual notes are below the code.
"""

# faiss_index.py

import faiss
import numpy as np
from utils.log_config import setup_colored_logging
import logging

# Logging setup
setup_colored_logging()
logger = logging.getLogger(__name__)


# text-embedding-ada-002 embeddings = np.zeros((1, 1536))

# You might want to consider techniques such as the elbow method, silhouette analysis, or gap statistics to determine
# the optimal number of clusters for your specific dataset if accuracy is a key concern. n_list in the create_index
# method is the number of clusters. The default value is 100. The default value for nprobe is 10. nprobe is the number
# of clusters to search during a search operation. The default value for k is 5. k is the number of results to return
# during a search operation.


class FaissIndex:
    def __init__(self, embeddings, data_type):
        logger.info("Initializing FaissIndex object")
        """
        The constructor initializes a FaissIndex object using a set of embeddings and a data type. The embeddings is a
        list (or similar collection) of vectors, and data_type is a string describing the data (node, sentence, or
        keyword). The constructor converts the input embeddings into a numpy array of type float32, which is the
        required input format for FAISS. Because the text-embedding-ada-002 embeddings have three dimensions and Faiss
        just uses two dimensions, it removes the middle dimension by squeezing the numpy array.
        :param embeddings: A list of vectors to be indexed.
        :type: list
        :param data_type:  A string indicating the type of data in the index.
        :type: str
        """
        self.data_type = data_type
        self.embeddings_np = np.array(embeddings, dtype=np.float32)
        if len(self.embeddings_np.shape) == 3:
            self.embeddings_np = self.embeddings_np.squeeze(axis=1)
        self.index = None

    def create_index(self, nlist=100, nprobe=10):
        """
        Creates a Faiss IndexIVFFlat index with an L2 (Euclidean) metric and an IndexFlatL2 quantizer using the class's
        embeddings. The index is trained and the embeddings are added to it.
        User Guide: https://github.com/facebookresearch/faiss/wiki/Faiss-building-blocks:-clustering,-PCA,-quantization
        :param nlist: The number of clusters to use in the index.
        :type: int
        :param nprobe: The number of clusters to search during a search operation.
        :type: int
        :return: None
        :rtype: None
        """
        logger.info("Creating index in FaissIndex.create_index()")
        d = self.embeddings_np.shape[1]
        quantizer = faiss.IndexFlatL2(d)
        self.index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
        self.index.nprobe = nprobe
        logger.debug("Shape of embeddings_np:", self.embeddings_np.shape)
        if not self.index.is_trained:
            self.index.train(self.embeddings_np)
        self.index.add(self.embeddings_np)
        logger.info("Index created in FaissIndex.create_index()")

    def search(self, query_embedding, k) -> tuple[np.ndarray, np.ndarray]:
        """
        Performs a search operation on the index using the query_embedding and returns the indices and distances of the
        k nearest neighbors.
        :param query_embedding: The embedding vector to search for in the index.
        :type query_embedding: array_like
        :param k: The number of nearest neighbors to return.
        :type k: int
        :return: A tuple where the first element is the indices of the k nearest neighbors and the second element
             is their corresponding distances.
        :rtype: tuple of (numpy.ndarray, numpy.ndarray)
        """
        if self.index is None:
            logger.error('Index has not been created')
            raise ValueError('Index has not been created')
        query_np = np.array(query_embedding, dtype=np.float32)
        if query_np.ndim == 2 and query_np.shape[1] == 1:
            query_np = query_np.squeeze(axis=1)
        logger.debug(f"Query shape: {query_np.shape}")
        distances, indices = self.index.search(query_np, k)
        return indices, distances

    def save_index(self, index_path):
        """
        Saves the index to the specified path.
        :param index_path: The path to save the index to.
        :return: None
        """
        logger.info(f"Saving Faiss index for {self.data_type} to", index_path)
        faiss.write_index(self.index, index_path)
        logger.info(f"Faiss index for {self.data_type} saved to", index_path)

    def load_index(self, index_path):
        """
        Loads the index from the specified path.
        :param index_path: The path to load the index from.
        :return: None
        """
        logger.info(f"Loading Faiss index for {self.data_type} from", index_path)
        self.index = faiss.read_index(index_path)
        logger.info(f"Faiss index for {self.data_type} loaded from", index_path)

    def get_index(self):
        """
        Returns the index.
        :return: The index.
        """
        return self.index

"""
In Faiss, quantizers map vectors to discrete centroids, partitioning the vector space and compressing vectors for
reduced memory and complexity. Various quantization methods like Product Quantization (PQ) and Scalar Quantization (SQ)
are available. The quantized vectors are stored in the index, the data structure used for efficient similarity search.
Index types include IVF, IVFADC, and HNSW, each with different memory, speed, and accuracy characteristics.

The quantizer and index are interconnected but serve different roles. The quantizer manages vector compression and
quantization, while the index enables fast search operations on these quantized vectors.

IndexIVFFlat, a Faiss index, uses the Inverted File with Flat vectors (IVF) algorithm, balancing accuracy and
efficiency. IndexFlatL2, another index type, uses L2 distance for similarity and stores uncompressed vectors. It's used
as a quantizer for IndexIVFFlat in this code.

The quantizer also clusters vectors for an IVF index, with the number of clusters determined by 'nlist'. During a
search, Faiss examines a subset of clusters (controlled by 'nprobe') for efficiency. Before searching, an IVF index is
trained with a representative vector sample to learn the dataset's distribution.
"""