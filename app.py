import streamlit as st
from agent import search_internships, judge_internships

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Internship Finder",
    page_icon="🚀",
    layout="wide"
)

# ------------------ TITLE ------------------
st.title("🚀 AI Internship Opportunity Finder")

# ------------------ INPUT ------------------
field = st.text_input(
    "Enter field (AI, ML, Data Science)",
    placeholder="e.g. data science"
)

# Optional toggles
show_debug = st.checkbox("Show Debug Data")
show_judge = st.checkbox("Show Judge Analysis")

# ------------------ BUTTON ------------------
if st.button("Search Internships"):

    # Validate input
    if not field.strip():
        st.warning("⚠️ Please enter a field")
    else:
        st.success(f"🔍 Searching internships for: {field}")

        # ✅ SAFE QUERY (no broken syntax)
        query = f"{field} internship AI ML remote"

        try:
            # ------------------ STEP 1: SEARCH ------------------
            results = search_internships(query)

            if not results:
                st.error("❌ No results found")
            else:
                # ------------------ DEBUG (SAFE) ------------------
                if show_debug:
                    st.subheader("🛠 Debug Data")
                    st.json(results)

                # ------------------ STEP 2: JUDGE ------------------
                scored_results = judge_internships(results)

                st.subheader("📊 Internship Results")

                # ------------------ DISPLAY ------------------
                for i, job in enumerate(scored_results, 1):

                    title = job.get("title", "No Title")
                    content = job.get("content", "No description available")
                    url = job.get("url", "#")
                    score = job.get("score", 0)
                    reason = job.get("reason", "No reasoning available")

                    with st.container():
                        st.markdown(f"### {i}. {title}")
                        st.write(content)
                        st.markdown(f"⭐ **Score:** {score}/10")
                        st.markdown(f"🔗 [Apply Here]({url})")

                        # ✅ Judge explanation (safe)
                        if show_judge:
                            with st.expander("🤖 Judge Analysis"):
                                st.write(reason)

                        st.markdown("---")

        except Exception as e:
            st.error("🚨 Something went wrong")
            st.code(str(e))
