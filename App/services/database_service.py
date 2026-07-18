import json

from database.database import get_connection


class DatabaseService:

    def __init__(self):

        self.conn = get_connection()

        self.cursor = self.conn.cursor()

    # =====================================================
    # Candidate
    # =====================================================

    def save_candidate(self, candidate):

        self.cursor.execute(
            """
            INSERT INTO candidates(

                full_name,
                email,
                phone,
                linkedin,
                github,
                skills,
                education,
                experience,
                certifications,
                summary,
                resume_text,
                batch_id

            )

            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (

                candidate.full_name,
                candidate.email,
                candidate.phone,
                candidate.linkedin,
                candidate.github,
                json.dumps(candidate.skills),
                json.dumps(candidate.education),
                json.dumps(candidate.experience),
                json.dumps(candidate.certifications),
                candidate.summary,
                "",
                None

            ),
        )

        self.conn.commit()

        return self.cursor.lastrowid

    # =====================================================
    # Job
    # =====================================================

    def save_job(self, job):
        # Insert new job
        self.cursor.execute(
            """
            INSERT INTO jobs(
                job_title,
                company,
                company_email,
                company_linkedin,
                company_location,
                work_mode,
                employment_type,
                salary_range,
                notice_period,
                experience_required,
                education_required,
                required_skills,
                preferred_skills,
                responsibilities,
                job_description
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                job.job_title,
                job.company,
                job.company_email,
                job.company_linkedin,
                job.company_location,
                job.work_mode,
                job.employment_type,
                job.salary_range,
                job.notice_period,
                job.experience_required,
                job.education_required,
                json.dumps(job.required_skills),
                json.dumps(job.preferred_skills),
                json.dumps(job.responsibilities),
                job.job_description,
            ),
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def job_exists(self, job):

        self.cursor.execute(
            """
            SELECT id
            FROM jobs
            WHERE
                job_title = ?
                AND company = ?
                AND company_location = ?
            """,
            (
                job.job_title,
                job.company,
                job.company_location,
            ),
        )

        return self.cursor.fetchone()

    # =====================================================
    # Get Jobs
    # =====================================================

    def get_all_jobs(self):

        self.cursor.execute("""
            SELECT *
            FROM jobs
            ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()

        jobs = []

        for row in rows:

            job = dict(row)

            job["required_skills"] = json.loads(
                job["required_skills"] or "[]"
            )

            job["preferred_skills"] = json.loads(
                job["preferred_skills"] or "[]"
            )

            job["responsibilities"] = json.loads(
                job["responsibilities"] or "[]"
            )

            jobs.append(job)

        return jobs

    # =====================================================
    # Get Candidates
    # =====================================================

    def get_all_candidates(self):

        self.cursor.execute("""
            SELECT *
            FROM candidates
            ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()

        candidates = []

        for row in rows:

            candidate = dict(row)

            candidate["skills"] = json.loads(
                candidate["skills"] or "[]"
            )

            candidate["education"] = json.loads(
                candidate["education"] or "[]"
            )

            candidate["experience"] = json.loads(
                candidate["experience"] or "[]"
            )

            candidate["certifications"] = json.loads(
                candidate["certifications"] or "[]"
            )

            candidates.append(candidate)

        return candidates

    # =====================================================
    # Candidate By ID
    # =====================================================

    def get_candidate_by_id(self, candidate_id):

        self.cursor.execute(
            """
            SELECT *
            FROM candidates
            WHERE id = ?
            """,
            (candidate_id,),
        )

        row = self.cursor.fetchone()

        if row is None:

            return None

        return dict(row)

    # =====================================================
    # Close
    # =====================================================

    def close(self):

        self.conn.close()