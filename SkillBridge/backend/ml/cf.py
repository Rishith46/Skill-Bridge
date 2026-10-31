"""
Collaborative Filtering using TruncatedSVD.
Builds an interaction matrix M (users x users) where entry is rating of responder by requester.
Applies TruncatedSVD to get low-rank factors and predicts scores.
"""
import numpy as np


class CFEngine:
    def __init__(self, db, n_components=20):
        self.db = db
        self.n_components = n_components
        self.user_index = {}
        self.index_user = {}
        self.U = None
        self.V = None
        self._fit()

    def _fit(self):
        from models import Collaboration, User
        cols = Collaboration.query.filter(Collaboration.rating != None).all()
        users = User.query.all()
        for i, u in enumerate(users):
            self.user_index[u.id] = i
            self.index_user[i] = u.id

        n = len(users)
        if n == 0:
            return
        M = np.zeros((n, n))
        for c in cols:
            if c.requester_id in self.user_index and c.responder_id in self.user_index and c.rating:
                i = self.user_index[c.requester_id]
                j = self.user_index[c.responder_id]
                M[i, j] = c.rating

        # apply TruncatedSVD
        k = min(self.n_components, n - 1) if n > 1 else 1
        try:
            from sklearn.decomposition import TruncatedSVD
            svd = TruncatedSVD(n_components=k)
            U = svd.fit_transform(M)
            V = svd.components_.T
            self.U = U
            self.V = V
        except Exception:
            self.U = None
            self.V = None

    def predict_score(self, user_i_id, user_j_id):
        if user_i_id not in self.user_index or user_j_id not in self.user_index:
            return 0.0
        i = self.user_index[user_i_id]
        j = self.user_index[user_j_id]
        if self.U is None or self.V is None:
            return 0.0
        try:
            return float(np.dot(self.U[i, :], self.V[j, :])) / 5.0
        except Exception:
            return 0.0
