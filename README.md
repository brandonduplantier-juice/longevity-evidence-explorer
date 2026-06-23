# Longevity Intervention Evidence Explorer

A searchable, plain-language tool that grades popular longevity interventions by how
strong the evidence actually is, using a transparent rubric, and makes the gap
between public attention and real evidence visible.

Version 1.0.0

## What it does

Each intervention is scored on six evidence axes, graded with a fixed rule, and shown
in a dashboard a non-specialist can read: a sortable table, a per-intervention
breakdown that explains every score in common language, and an attention-versus-
evidence scatter that exposes hype gaps (lots of buzz, thin evidence) and underrated
options (solid evidence, little attention).

## The honest ceiling: grade A is empty

Grade A requires a human trial showing longer lifespan or lower mortality. No
longevity intervention has that yet, so nothing is graded A. The strongest evidence
today (rapamycin, caloric restriction) earns a B. This ceiling is enforced in code,
not by hand.

## The rubric

Six axes, each scored 0 to 3, summed to a 0 to 18 total and mapped to a letter grade.
The scores live in the data (auditable); the grading lives in src/rubric.py
(consistent). The axes: animal lifespan evidence, replication and rigor, consistency
of effect, human evidence, translational readiness, and safety profile.

## Data and how it stays honest

This ships with a seed database of 11 well-established interventions, written
conservatively, each with an author-and-journal citation. It is a starting point, not
a finished reference. Two safeguards keep it honest:

1. No hardcoded PMIDs. Each row carries a citation query, and src/pubmed.py resolves
   it to a real PubMed record (metadata only, no abstracts, to respect copyright). A
   wrong or invented citation returns no hit and is flagged, instead of shipping a
   fake reference.
2. Attention is an editorial estimate (1 to 5), clearly labeled as a judgment, not a
   measurement.

Verify each row against its citation and extend the table before relying on it.

## Run (Windows)

    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    .venv\Scripts\python.exe run_all.py
    .venv\Scripts\python.exe run_all.py --pubmed
    .venv\Scripts\python.exe -m streamlit run app.py

run_all.py validates the data and writes data/graded.csv. The --pubmed pass resolves
real citations into data/citations.csv, which the app then shows directly.

## Extend it

Add a row to data/interventions.csv with the six axis scores (0 to 3), a conservative
evidence summary, an attention estimate, and an author-and-topic citation query, then
rerun run_all.py to re-grade. Keep every claim sourced.

## Limitations

The seed set is small and centered on the best-known interventions. Axis scores are
judgment calls, made transparent by showing each score and its meaning. Attention is
subjective. This is an educational research tool, not medical advice and not a
recommendation to take or avoid anything.

## Citations

Each intervention carries a citation query in data/interventions.csv, resolved to
PubMed by src/pubmed.py. The grading method is in src/rubric.py.
