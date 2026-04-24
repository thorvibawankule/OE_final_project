import requests
import os
import random
import streamlit as st


# 🔹 SEARCH INTERNSHIPS
def search_internships(query):
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        st.error("❌ Missing TAVILY_API_KEY in Streamlit Secrets")
        return []

    url = "https://api.tavily.com/search"

    # 🔥 Improve search query
    query = f"{query} internships AI ML jobs remote"

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 5
    }

    try:
        response = requests.post(url, json=payload, timeout=20)

        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)
            return []

        data = response.json()

        # 🔍 DEBUG (remove later if you want)
        st.write("DEBUG RESPONSE:", data)

    except Exception as e:
        st.error(f"Request failed: {e}")
        return []

    results = data.get("results", [])

    if not results:
        st.warning("No results returned from API")
        return []

    cleaned = []
    for item in results:
        cleaned.append({
            "title": item.get("title", "No Title"),
            "url": item.get("url", ""),
            "content": item.get("content", "")[:300]
        })

    return cleaned


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
You are a strict evaluator of AI internships.

Give:
1. Score (0-10)
2. Reason (2 lines)

IMPORTANT:
- Use different scores for each job
- Use range between 5 to 10
- Be realistic

Title: {job.get('title', '')}
Description: {job.get('content', '')}
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

            if "choices" in result:
                output = result["choices"][0]["message"]["content"]
            else:
                raise Exception("Invalid LLM response")

        except Exception as e:
            # fallback (still useful but not hiding error)
            score = random.randint(6, 9)
            output = f"Score: {score}\nReason: Fallback due to error: {str(e)}"

        job["llm_judge"] = output
        judged.append(job)

    return judged
