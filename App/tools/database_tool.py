from langchain_core.tools import tool

from services.database_service import DatabaseService

# =====================================================
# Candidate Tools
# =====================================================

@tool
def get_all_candidates():
    """
    Returns all candidates stored in the database.
    """
    db = DatabaseService()
    try:
        return db.get_all_candidates()
    finally:
        db.close()

@tool
def get_candidate_by_id(candidate_id: int):
    """
    Returns a candidate by their database ID.
    """
    db = DatabaseService()
    try:
        return db.get_candidate_by_id(candidate_id)
    finally:
        db.close()


@tool
def count_candidates():
    """
    Returns the total number of candidates.
    """
    db = DatabaseService()
    try:
        return len(db.get_all_candidates())
    finally:
        db.close()


@tool
def search_candidate(name: str):
    """
    Search candidates by full name.
    """
    db = DatabaseService()
    try:
        candidates = db.get_all_candidates()
        results = []

        for candidate in candidates:

            full_name = candidate.get("full_name", "")

            if name.lower() in full_name.lower():

                results.append(candidate)

        return results
    finally:
        db.close()


# =====================================================
# Job Tools
# =====================================================

@tool
def get_all_jobs():
    """
    Returns all jobs stored in the database.
    """
    db = DatabaseService()
    try:
        return db.get_all_jobs()
    finally:
        db.close()


@tool
def get_job_by_id(job_id: int):
    """
    Returns a job by its database ID.
    """
    db = DatabaseService()
    try:
        return db.get_job_by_id(job_id)
    finally:
        db.close()


@tool
def count_jobs():
    """
    Returns the total number of jobs.
    """
    db = DatabaseService()
    try:
        return len(db.get_all_jobs())
    finally:
        db.close()


@tool
def search_job(keyword: str):
    """
    Search jobs using job title.
    """
    db = DatabaseService()
    try:
        jobs = db.get_all_jobs()
        results = []

        for job in jobs:
            title = job.get("job_title", "")

            if keyword.lower() in title.lower():
                results.append(job)

        return results
    finally:
        db.close()