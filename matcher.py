def job_match_score(resume_text, job_text):

    resume_words = resume_text.lower().split()

    job_words = job_text.lower().split()

    match = 0

    for w in job_words:

        if w in resume_words:
            match += 1

    if len(job_words) == 0:
        return 0

    score = (match / len(job_words)) * 100

    return int(score)