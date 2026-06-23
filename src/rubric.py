"""
Transparent evidence-grading rubric for longevity interventions.

Six axes, each scored 0 to 3 against fixed criteria, summed to a 0 to 18 total and
mapped to a letter grade. The grade is fully reproducible from the axis scores; no
hidden weighting. One hard rule encodes scientific honesty: grade A requires direct
human lifespan or mortality randomized-trial evidence, which no longevity
intervention currently has, so grade A is intentionally unreachable today.

Each row in data/interventions.csv carries the six axis scores plus a written
justification and a citation. This module only turns scores into a grade, so the
judgment lives in the data (auditable) and the grading lives here (consistent).
"""

AXES = [
    ("axis_organism", "Animal lifespan evidence",
     ["none", "single study or organism", "multiple studies",
      "robust across labs or species"]),
    ("axis_replication", "Replication and rigor",
     ["none", "single lab", "independent replication",
      "multi-site program (for example NIA ITP)"]),
    ("axis_consistency", "Consistency of effect",
     ["none", "one sex or narrow condition", "mostly consistent",
      "robust in both sexes"]),
    ("axis_human", "Human evidence",
     ["none", "observational or biomarker only", "RCT on surrogate endpoints",
      "RCT on lifespan or mortality"]),
    ("axis_readiness", "Translational readiness",
     ["preclinical only", "human safety known", "approved for another use",
      "approved with aging-relevant dosing known"]),
    ("axis_safety", "Safety profile",
     ["serious concerns", "notable concerns", "manageable", "well tolerated"]),
]
AXIS_KEYS = [a[0] for a in AXES]
MAX_TOTAL = len(AXES) * 3


def grade_row(scores):
    """scores: dict with the six axis keys (ints 0..3). Returns (total, letter, reason)."""
    for k in AXIS_KEYS:
        v = int(scores[k])
        if v < 0 or v > 3:
            raise ValueError("{} out of range 0..3: {}".format(k, v))
    total = sum(int(scores[k]) for k in AXIS_KEYS)
    human = int(scores["axis_human"])

    # Hard honesty rule: A demands a human lifespan/mortality RCT.
    if human >= 3 and total >= 15:
        return total, "A", "human lifespan RCT plus strong overall evidence"
    if human < 3 and total >= 12:
        return total, "B", "strong evidence but no human lifespan RCT (A is gated on that)"
    if total >= 12:
        return total, "B", "strong overall evidence"
    if total >= 8:
        return total, "C", "moderate evidence"
    if total >= 4:
        return total, "D", "weak evidence"
    return total, "F", "minimal evidence"


def grade_frame(df):
    import pandas as pd
    out = df.apply(lambda r: grade_row({k: r[k] for k in AXIS_KEYS}),
                   axis=1, result_type="expand")
    out.columns = ["evidence_total", "grade", "grade_reason"]
    return pd.concat([df, out], axis=1)


def _selftest():
    rap = dict(axis_organism=3, axis_replication=3, axis_consistency=3,
               axis_human=1, axis_readiness=2, axis_safety=1)
    t, g, _ = grade_row(rap)
    print("rapamycin-like:", t, g)
    assert g == "B" and t == 13

    # Even a perfect non-human profile cannot reach A.
    perfect_animal = dict(axis_organism=3, axis_replication=3, axis_consistency=3,
                          axis_human=2, axis_readiness=3, axis_safety=3)
    t, g, _ = grade_row(perfect_animal)
    print("best-without-human-RCT:", t, g)
    assert g == "B", "A must be gated behind human lifespan RCT"

    # The gate: only a human lifespan RCT unlocks A.
    t, g, _ = grade_row(dict(axis_organism=3, axis_replication=3, axis_consistency=3,
                             axis_human=3, axis_readiness=2, axis_safety=1))
    print("hypothetical with human RCT:", t, g)
    assert g == "A"
    print("rubric selftest OK")


if __name__ == "__main__":
    _selftest()
