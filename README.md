# Longevity Intervention Evidence Explorer

A searchable, plain-language tool that grades popular longevity interventions by how
strong the evidence actually is, using a transparent rubric, and makes the gap between
public hype and real evidence visible.

Version 1.0.0

## The result

It ships with 11 well-established interventions, graded by a fixed rule. The grade
distribution is deliberately sobering: **0 are grade A, 2 are B, 7 are C, 2 are D.**
The strongest evidence today (rapamycin, caloric restriction) earns a B. Nothing
earns an A, and that ceiling is enforced in code, not by opinion.

## In plain English

You do not need a science background to read this. Here is what it does and why it is
built the way it is.

**The problem it addresses.** The longevity space is full of confident claims:
supplements, diets, and drugs that supposedly slow aging. Some rest on decades of
animal studies; some rest on a single mouse experiment or a podcast. It is hard for a
non-specialist to tell which is which. This tool scores each one on the strength of
its evidence, in the open, so the reasoning is visible.

**How a grade is built.** Each intervention is scored on six *evidence axes*, plain
questions about the quality of the proof: does it extend lifespan in animals, has the
result been *replicated* (repeated by independent labs, the test of whether a finding
is real), is the effect consistent, is there *human* evidence, how close is it to
real-world use, and how safe is it. Each axis gets 0 to 3 points, summed to a 0-to-18
total, mapped to a letter grade.

**The honest ceiling.** Grade A requires a *human trial* (a controlled study in people)
showing longer lifespan or lower death rates. No longevity intervention has that yet,
so nothing can score an A. The code refuses to award one. That single rule is what
separates this from a hype list: it is honest about how thin even the best evidence is.

**Hype versus evidence, made visible.** Each item also carries an *attention* estimate,
clearly labeled as an editorial judgment, not a measurement. A scatter plot puts
attention against evidence, so you can see the hype gaps (loud but thin) and the
underrated cases (solid but quiet) at a glance.

**Why you can trust the citations.** The tool does not hardcode reference IDs, which
is how fake citations creep in. Each row carries a search query that is resolved
against the live PubMed database (the public index of biomedical literature). A wrong
or invented reference simply returns no match and gets flagged, instead of shipping a
fake.

This is a starting database written conservatively, not a finished reference. Verify
each row against its citation before relying on it.

## How it works (technical)

The scores live in data/interventions.csv (auditable); the grading lives in
src/rubric.py (consistent, with the grade-A gate hardcoded). src/pubmed.py resolves
each citation query via the NCBI E-utilities API, metadata only, no abstracts, to
respect copyright. The app is a Streamlit dashboard: a sortable table, a per-
intervention breakdown explaining every axis score in common language, and the
attention-versus-evidence scatter.

## What is in this repo

    run_all.py           validates the data, writes data/graded.csv
    src/rubric.py        the six-axis rubric and the enforced grade-A gate
    src/pubmed.py        resolves citation queries to real PubMed records
    app.py               the dashboard (Streamlit)
    data/interventions.csv  the 11 seed rows you can audit and extend

## Run (Windows)

    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    .venv\Scripts\python.exe run_all.py
    .venv\Scripts\python.exe run_all.py --pubmed
    .venv\Scripts\python.exe -m streamlit run app.py

run_all.py grades the data. The --pubmed pass resolves real citations into
data/citations.csv, which the app then shows directly.

## Limitations

Eleven hand-curated rows, not a comprehensive database. Attention scores are editorial
estimates, not measured. Grades reflect the rubric's design choices, which are stated
openly so they can be argued with. The tool grades evidence quality; it does not give
health advice.

## Glossary

- **Intervention**: anything proposed to slow aging (a drug, diet, or supplement).
- **Evidence axis**: one of six scored questions about the quality of the proof.
- **Replication**: an independent lab repeating a result; the core test of whether a
  finding is real.
- **Human trial / RCT**: a controlled study in people; required here for the top grade.
- **Lifespan vs healthspan**: how long you live vs how long you stay healthy.
- **PubMed**: the public US index of biomedical research articles.
- **Attention**: an editorial 1-to-5 estimate of public buzz, labeled as a judgment.

## Citation and disclaimer

Citations resolve live from PubMed (NCBI E-utilities). A conservative starting
reference, not medical advice.

## Project navigation

- [Engineering guide](ENGINEERING.md): directory map, development workflow and review standards.
