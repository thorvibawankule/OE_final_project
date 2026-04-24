import requests
import os
import streamlit as st

# 🔹 SEARCH INTERNSHIPS
def search_internships(query):
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        st.error("❌ Missing TAVILY_API_KEY in Secrets")
        return []

    url = "https://api.tavily.com/search"

    # ✅ BETTER QUERY (real job links, not listing sites)
    query = f"{query} AI internship apply site:linkedin.com/jobs OR site:wellfound.com OR site:jobs.lever.co"

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 10
    }

    try:
        response = requests.post(url, json=payload, timeout=20)

        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)
            return []

        data = response.json()

        # 🔍 DEBUG (optional)
        st.write("DEBUG RESPONSE:", data)

    except Exception as e:
        st.error(f"Request failed: {e}")
        return []

    results = data.get("results", [])

    if not results:
        st.warning("No results returned")
        return []

    cleaned = []
    for item in results:
        cleaned.append({
            "title": item.get("title", "No Title"),
            "url": item.get("url", ""),
            "content": item.get("content", "")[:300]
        })

    # ❌ FILTER OUT JUNK SITES
    filtered = []
    for job in cleaned:
        url = job["url"]

        if any(x in url for x in ["glassdoor", "indeed", "remotive"]):
            continue

        if len(job["content"]) < 100:
            continue

        filtered.append(job)

    return filtered


# 🔹 LLM JUDGE
def judge_internships(jobs):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        for job in jobs:
            job["llm_judge"] = "❌ Missing OPENROUTER_API_KEY"
        return jobs

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    judged = []

    for job in jobs:

        prompt = f"""
Evaluate this SINGLE internship.

Return ONLY:
Score: X/10
Reason: 1-2 lines

Title: {job.get('title')}
Description: {job.get('content')[:300]}
"""

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=20
            )

            if res.status_code != 200:
                raise Exception(f"API error {res.status_code}")

            result = res.json()

            output = result["choices"][0]["message"]["content"]

        except Exception as e:
            output = f"❌ LLM Error: {str(e)}"

        job["llm_judge"] = output
        judged.append(job)

    return judged
