# ------------------ STEP 2: SCORE ------------------
scored_results = judge_internships(results)

st.subheader("📊 Internship Results")

for i, job in enumerate(scored_results, 1):

    title = job.get("title", "No Title")
    content = job.get("content", "No description available")
    url = job.get("url", "#")
    score = job.get("score", 0)

    with st.container():
        st.markdown(f"### {i}. {title}")
        st.write(content)
        st.markdown(f"⭐ **Score:** {score}/10")
        st.markdown(f"🔗 [Apply Here]({url})")

        # ✅ SHOW JUDGE RESPONSE (SAFE)
        with st.expander("🤖 View Judge Analysis"):
            st.json({
                "title": title,
                "score": score,
                "reason": "Score based on keywords like Python, ML, Remote"
            })

        st.markdown("---")
