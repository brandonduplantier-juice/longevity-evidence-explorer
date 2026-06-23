"""
Validate the intervention data, compute grades, optionally resolve PubMed citations.

Usage:
  python run_all.py             validate and write data/graded.csv
  python run_all.py --pubmed    also resolve real citations into data/citations.csv
"""

import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))
import rubric  # noqa: E402

__version__ = "1.0.0"
DATA = os.path.join(HERE, "data", "interventions.csv")


def main():
    print("[run_all] longevity-evidence-explorer v{}".format(__version__))
    df = pd.read_csv(DATA)
    # validation: every axis score must be 0..3
    for _, r in df.iterrows():
        rubric.grade_row({k: r[k] for k in rubric.AXIS_KEYS})
    graded = rubric.grade_frame(df)
    graded.to_csv(os.path.join(HERE, "data", "graded.csv"), index=False)
    print("[run_all] graded {} interventions: {}".format(
        len(graded), graded["grade"].value_counts().to_dict()))
    if "--pubmed" in sys.argv:
        import pubmed
        pubmed.main()
    print("[run_all] done. Launch the app: python -m streamlit run app.py")


if __name__ == "__main__":
    main()
