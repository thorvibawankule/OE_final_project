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
