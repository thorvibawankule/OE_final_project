import streamlit as st
from agent import search_internships, judge_internships

# Page config
st.set_page_config(
    page_title="AI Internship Finder",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("🚀 AI Internship Opportunity Finder")

# Input
field = st.text_input("Enter field (AI, ML, Data Science)", placeholder="e.g. data science")

# Button
if st.button("Search Internships"):

    if not field.strip():
        st.warning("⚠️ Please enter a field")
    else:
        st.success(f"🔍 Searching internships for: {field}")

        # ✅ SAFE QUERY (fixes your previous crash)
        query = f"{field} internship AI ML remote"

        try:
            # Step 1: Search
            results = search_internships(query)

            if not results:
                st.error("❌ No results found")
            else:
                # Step 2: Judge / Score
                scored_results = judge_internships(results)

                st.subheader("📊 Results")

                for i, job in enumerate(scored_results, 1):
                    with st.container():
                        st.markdown(f"### {i}. {job.get('title', 'No Title')}")

                        st.write(job.get("content", "No description available"))

                        st.markdown(f"⭐ **Score:** {job.get('score', 0)}/10")

                        st.markdown(f"🔗 [Apply Here]({job.get('url', '#')})")

                        st.markdown("---")

        except Exception as e:
            st.error("🚨 Something went wrong")
            st.code(str(e))
