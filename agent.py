def search_internships(query):
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


def judge_internships(results):
    scored = []

    for job in results:
        score = 5
        reasons = []

        text = (job.get("title", "") + job.get("content", "")).lower()

        if "python" in text:
            score += 1
            reasons.append("Mentions Python")

        if "machine learning" in text or "ml" in text:
            score += 2
            reasons.append("Includes Machine Learning")

        if "remote" in text:
            score += 1
            reasons.append("Remote opportunity")

        job["score"] = min(score, 10)
        job["reason"] = ", ".join(reasons) if reasons else "General relevance"

        scored.append(job)

    return scored
