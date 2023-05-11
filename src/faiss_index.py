# faiss_index.py module

import faiss
import numpy as np

# embedding = np.zeros((1, 1536))


class FaissIndex:
    def __init__(self, embeddings):
        self.embeddings_np = np.array(embeddings, dtype=np.float32)
        if len(self.embeddings_np.shape) == 3:
            self.embeddings_np = self.embeddings_np.squeeze(axis=1)
        self.index = None

    def create_index(self, nlist=100, nprobe=10):
        d = self.embeddings_np.shape[1]
        quantizer = faiss.IndexFlatL2(d)
        self.index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
        self.index.nprobe = nprobe
        print("Shape of embeddings_np:", self.embeddings_np.shape)  # Add this line
        self.index.train(self.embeddings_np)
        self.index.add(self.embeddings_np)

    def search(self, query_embedding, k):
        if self.index is None:
            raise ValueError('Index has not been created')
        query_np = np.array(query_embedding, dtype=np.float32)
        if len(query_np.shape) == 2:
            query_np = query_np.squeeze(axis=1)
        distances, indices = self.index.search(np.array([query_np], dtype=np.float32), k)
        return indices[0], distances[0]

    def save_index(self, index_path):
        if self.index is None:
            raise ValueError('Index has not been created')
        faiss.write_index(self.index, index_path)

    def load_index(self, index_path):
        self.index = faiss.read_index(index_path)

    def get_index(self):
        return self.index
