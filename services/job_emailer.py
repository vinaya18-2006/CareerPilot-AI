from services.email_service import send_job_email


def send_matching_job_alert(jobs, minimum_score=70):
    """
    Send email only for jobs whose match score
    is equal to or above minimum_score.
    """

    matching_jobs = []

    for job in jobs:

        score = job.get("score", 0)

        try:
            score = float(score)
        except (ValueError, TypeError):
            score = 0

        if score >= minimum_score:
            matching_jobs.append({
                "title": job.get(
                    "title",
                    "Unknown Position"
                ),
                "company": job.get(
                    "company",
                    "Unknown Company"
                ),
                "location": job.get(
                    "location",
                    "Unknown"
                ),
                "url": job.get(
                    "url",
                    "#"
                ),
                "score": score
            })

    if not matching_jobs:
        return False, 0

    send_job_email(matching_jobs)

    return True, len(matching_jobs)