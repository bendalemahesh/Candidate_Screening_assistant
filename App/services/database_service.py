import os
import sqlite3
import json

class DatabaseService:
    def __init__(self):

        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "App", "database", "recruiter_ai.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        # ---------------- Candidates ---------------- #

        self.cursor.execute("""

            CREATE TABLE IF NOT EXISTS candidates(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,

            linkedin TEXT,
            github TEXT,

            skills TEXT,
            education TEXT,
            experience TEXT,
            certifications TEXT,

            summary TEXT,

            resume_text TEXT,

            batch_id INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        
        """)

        # ---------------- Jobs ---------------- #

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_title TEXT,
            company TEXT,
            company_email TEXT,
            company_linkedin TEXT,

            company_location TEXT,
            work_mode TEXT,
            enrollment_type TEXT,

            salary_range TEXT,
            notice_period TEXT,

            experience_required TEXT,
            education_required TEXT,

            required_skills TEXT,
            responsibilities TEXT,

            job_description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ---------------- Screening Results ---------------- #

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS screening_results(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER,
            job_id INTEGER,

            match_score INTEGER,

            matched_skills TEXT,
            missing_skills TEXT,

            candidate_summary TEXT,
            strengths TEXT,
            weaknesses TEXT,

            recommendation TEXT,

            screened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(candidate_id)
                REFERENCES candidates(id),

            FOREIGN KEY(job_id)
                REFERENCES jobs(id)
        )
        """)

        self.conn.commit()


        #save Candidates

    def save_candidate(self, candidate):

            # Check whether candidate already exists
            self.cursor.execute(
                """
                SELECT id
                FROM candidates
                WHERE email = ?
                """,
                (candidate.email,)
            )

            existing = self.cursor.fetchone()

            if existing:
                return existing[0]

            self.cursor.execute(
                """
                INSERT INTO candidates(
                    full_name,
                    email,
                    phone,
                    location,
                    linkedin,
                    github,
                    skills,
                    education,
                    experience,
                    certifications,
                    summary,
                    resume_text
)

                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    candidate.full_name,
                    candidate.email,
                    candidate.phone,
                    candidate.location,
                    candidate.linkedin,
                    candidate.github,
                    json.dumps(candidate.skills),
                    json.dumps(
                        [e.model_dump() for e in candidate.education]
                    ),
                    json.dumps(
                        [e.model_dump() for e in candidate.experience]
                    ),
                    json.dumps(
                        [c.model_dump() for c in candidate.certifications]
                    ),
                    candidate.summary,
                    candidate.resume_text
                ),
            )

            self.conn.commit()

            return self.cursor.lastrowid


        #save Jobs
    def save_job(self, job):

            self.cursor.execute(
                """
                INSERT INTO jobs(
                    job_title,
                    company,
                    company_email,
                    company_linkedin,
                    company_location,
                    work_mode,
                    enrollment_type,
                    salary_range,
                    notice_period,
                    experience_required,
                    education_required,
                    required_skills,
                    responsibilities,
                    job_description
                )

                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
                    json.dumps(job.responsibilities),
                    job.job_description,
                ),
            )

            self.conn.commit()

            return self.cursor.lastrowid


        #save Screening_Results
    def save_screening_result(
            self,
            candidate_id,
            job_id,
            analysis,
            match_score,
            matched_skills,
            missing_skills,
        ):

            self.cursor.execute(
                """
                INSERT INTO screening_results(

                    candidate_id,
                    job_id,
                    match_score,

                    matched_skills,
                    missing_skills,

                    candidate_summary,
                    strengths,
                    weaknesses,
                    recommendation

                )

                VALUES(?,?,?,?,?,?,?,?,?)
                """,
                (
                    candidate_id,
                    job_id,
                    match_score,
                    json.dumps(matched_skills),
                    json.dumps(missing_skills),
                    analysis.candidate_summary,
                    json.dumps(analysis.strengths),
                    json.dumps(analysis.weaknesses),
                    analysis.recommendation,
                ),
            )

            self.conn.commit()

    def get_candidate_by_id(self, candidate_id):

            self.cursor.execute(
                """
                SELECT *
                FROM candidates
                WHERE id = ?
                """,
                (candidate_id,)
            )

            row = self.cursor.fetchone()

            if row is None:
                return None

            columns = [column[0] for column in self.cursor.description]

            return dict(zip(columns, row))


    def get_all_candidates(self):

            self.cursor.execute(
                """
                SELECT *
                FROM candidates
                """
            )

            rows = self.cursor.fetchall()

            columns = [column[0] for column in self.cursor.description]

            return [
                dict(zip(columns, row))
                for row in rows
            ]