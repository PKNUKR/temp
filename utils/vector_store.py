import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self):
        self.docs = []
        self.embeds = []

    def add(self, text, embedding):
        self.docs.append(text)
        self.embeds.append(embedding)

    def search(self, query):
        if not self.docs:
            return "저장된 문서가 없습니다."

        q_embed = np.array(self.embeds[0])
        sims = cosine_similarity([q_embed], self.embeds)[0]
        idx = np.argmax(sims)
        return self.docs[idx]
