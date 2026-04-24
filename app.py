import streamlit as st
from agent import search_internships, judge_internships

st.set_page_config(page_title="AI Internship Finder")

st.title("🚀 AI Internship Opportunity Finder")

query = st.text_input("Enter field (AI, ML, Data Science)")

if st.button("Find Internships"):

    if not query.strip():
        st.warning("Please enter a search query")
        st.stop()

    with st.spinner("🔍 Searching internships..."):
        jobs = search_internships(query)

    if not jobs:
        st.error("No high-quality internships found. Try another query.")
    else:
        with st.spinner("🤖 Evaluating with AI..."):
            jobs = judge_internships(jobs)

        for job in jobs:
            st.subheader(job.get("title", "No Title"))

            st.markdown(f"[🔗 Apply Here]({job.get('url', '')})")

            st.markdown("### 🤖 AI Evaluation")
            st.info(job.get("llm_judge", "No evaluation"))

            st.markdown("---")
