"""
CDM engine implementing the exact specified formulas.

G(ui, P) = R(P) − Si  (we treat negative entries as 0 deficits)
Coverage(uj, ui, P) = Σ min(Sj_m, G_m)
CDM = Coverage / ||G|| × Trust(uj)

"""
import numpy as np


def compute_cdm(si, sj, R, trust_uj):
    """Compute CDM score for candidate uj given user ui and project R.

    si, sj, R are numpy arrays of length 120.
    trust_uj is in [0,1].
    Returns float score >= 0.
    """
    # ensure numpy arrays
    si = np.array(si, dtype=float)
    sj = np.array(sj, dtype=float)
    R = np.array(R, dtype=float)

    # Gap vector: deficits only
    G = R - si
    G = np.where(G > 0, G, 0.0)

    # Coverage: sum of min(sj_m, G_m)
    mins = np.minimum(sj, G)
    coverage = np.sum(mins)

    normG = np.linalg.norm(G)
    if normG == 0:
        return 0.0

    cdm = (coverage / normG) * float(trust_uj)
    return float(cdm)
