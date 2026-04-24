import streamlit as st
from agent import search_internships, judge_internships

st.set_page_config(page_title="AI Internship Finder")

st.title("🚀 AI Internship Opportunity Finder")

query = st.text_input("Enter field (AI, ML, Data Science)")

if st.button("Find Internships"):

    with st.spinner("🔍 Searching internships..."):
        jobs = search_internships(query)

    if not jobs:
        st.error("No internships found.")
    else:
        with st.spinner("🤖 Evaluating with AI..."):
            jobs = judge_internships(jobs)

        for job in jobs:
            st.subheader(job["title"])
            st.write(job["url"])

            st.markdown("### 🤖 LLM-as-a-Judge")
            st.info(job["llm_judge"])

            st.markdown("---")