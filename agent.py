def search_internships(query):
    try:
        # ✅ NO DEBUG JSON RETURNED
        return [
            {
                "title": "Data Science Intern - Remote",
                "content": "Work with Python, ML models, and analytics.",
                "url": "https://example.com/job1",
            },
            {
                "title": "AI/ML Intern",
                "content": "Build machine learning systems and analyze data.",
                "url": "https://example.com/job2",
            },
        ]
    except Exception as e:
        print("Search error:", e)
        return []


def judge_internships(results):
    scored = []

    for job in results:
        score = 7
        text = (job.get("title", "") + job.get("content", "")).lower()

        if "python" in text:
            score += 1
        if "machine learning" in text or "ml" in text:
            score += 1
        if "remote" in text:
            score += 1

        job["score"] = min(score, 10)
        scored.append(job)

    return scored
