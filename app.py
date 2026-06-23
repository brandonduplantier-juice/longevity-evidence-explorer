"""
Longevity Intervention Evidence Explorer.

A searchable, plain-language guide to how strong the evidence really is for popular
longevity interventions, graded by a transparent rubric. Built for a general
audience: every grade is explained, and the gap between attention and evidence is
made visible. Not medical advice; nothing here is a recommendation to take anything.

Run locally:
  pip install -r requirements.txt
  python -m streamlit run app.py
"""

import os
import sys
import urllib.parse

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import rubric  # noqa: E402

APP_VERSION = "1.0.0"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "interventions.csv")
CITES = os.path.join(HERE, "data", "citations.csv")
GRADE_COLORS = {"A": "#1a9850", "B": "#66bd63", "C": "#fdae61", "D": "#f46d43", "F": "#a50026"}


@st.cache_data
def load():
    df = rubric.grade_frame(pd.read_csv(DATA))
    cites = pd.read_csv(CITES) if os.path.exists(CITES) else pd.DataFrame()
    return df, cites


df, cites = load()

st.title("Longevity intervention evidence explorer")
st.caption("How strong is the evidence, really, for popular anti-aging interventions. "
           "Graded by a transparent rubric. Not medical advice.")

with st.expander("New here? How grades work", expanded=False):
    st.markdown(
        "Every intervention is scored on six things, each from 0 to 3, then added up "
        "and turned into a letter grade. The scores live in the data so you can check "
        "them; the grading is fixed so it stays consistent.\n"
    )
    for key, label, levels in rubric.AXES:
        st.markdown("- **{}**: 0 = {}, 3 = {}".format(label, levels[0], levels[3]))
    st.markdown(
        "\n**The honest ceiling:** grade A requires a human trial showing longer "
        "lifespan or lower mortality. No intervention has that yet, so nothing is "
        "graded A. The best evidence today earns a B."
    )

best = df[df["grade"] == "B"]
c1, c2, c3 = st.columns(3)
c1.metric("Interventions", len(df), help="Number in this seed database. Extend it over time.")
c2.metric("Best grade reached", "B ({})".format(len(best)),
          help="No intervention reaches A, which needs a human lifespan trial.")
c3.metric("Graded A", 0, help="Reserved for human lifespan or mortality trial evidence. None yet.")

st.sidebar.header("Filter")
cats = st.sidebar.multiselect("Category", sorted(df["category"].unique()),
                              sorted(df["category"].unique()))
grades = st.sidebar.multiselect("Grade", ["B", "C", "D", "F"], ["B", "C", "D", "F"])
query = st.sidebar.text_input("Search name or mechanism", "").strip().lower()

f = df[df["category"].isin(cats) & df["grade"].isin(grades)]
if query:
    mask = (f["intervention"].str.lower().str.contains(query)
            | f["mechanism"].str.lower().str.contains(query))
    f = f[mask]

st.subheader("Attention vs evidence")
st.caption("Each dot is an intervention. Right means stronger evidence. Up means more "
           "public attention (an editorial estimate, not a measurement). Top-left is the "
           "hype gap: a lot of buzz, thin evidence. Bottom-right is underrated: solid "
           "evidence, little attention.")
if len(f):
    fig = px.scatter(f, x="evidence_total", y="attention", color="grade",
                     color_discrete_map=GRADE_COLORS, custom_data=["intervention", "grade"],
                     labels={"evidence_total": "evidence strength (0 to 18)",
                             "attention": "public attention (editorial, 1 to 5)"})
    fig.update_traces(marker=dict(size=13), hovertemplate="<b>%{customdata[0]}</b><br>"
                      "evidence: %{x} of 18<br>attention: %{y} of 5<br>grade %{customdata[1]}<extra></extra>")
    fig.add_vline(x=df["evidence_total"].median(), line_dash="dot", line_color="gray")
    fig.add_hline(y=df["attention"].median(), line_dash="dot", line_color="gray")
    fig.update_layout(height=480)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No interventions match the filter.")

st.subheader("All interventions")
view = f[["intervention", "category", "grade", "evidence_total", "attention",
          "sex_effect"]].sort_values(["grade", "evidence_total"], ascending=[True, False])
st.dataframe(view, use_container_width=True, height=360, hide_index=True)

st.subheader("Look at one intervention")
pick = st.selectbox("Choose", df["intervention"].tolist())
row = df[df["intervention"] == pick].iloc[0]
st.markdown("### {}  ({})".format(row["intervention"], row["grade"]))
st.write(row["evidence_summary"])
st.caption("Class: {}. Mechanism: {}. Sex effect in animals: {}.".format(
    row["category"], row["mechanism"], row["sex_effect"]))

st.markdown("**How it scored**")
for key, label, levels in rubric.AXES:
    score = int(row[key])
    st.markdown("- **{}**: {} of 3, {}".format(label, score, levels[score]))
st.caption("Total {} of {}. {}.".format(row["evidence_total"], rubric.MAX_TOTAL, row["grade_reason"]))

st.markdown("**Citation**")
cite_row = cites[cites["intervention"] == pick] if len(cites) else pd.DataFrame()
if len(cite_row):
    cr = cite_row.iloc[0]
    st.markdown("{}. {}, {}. [PubMed]({})".format(
        cr.get("title", ""), cr.get("journal", ""), cr.get("year", ""), cr.get("url", "")))
else:
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + urllib.parse.quote(row["citation_query"])
    st.markdown("[Search PubMed for this study]({})".format(url))
    st.caption("Run src/pubmed.py to resolve and cache exact references.")

st.caption("Attention is an editorial estimate, not a measurement. Evidence grades "
           "are reproducible from the scores in data/interventions.csv. Seed database, "
           "verify and extend before relying on it. Not medical advice. App v{}.".format(APP_VERSION))
