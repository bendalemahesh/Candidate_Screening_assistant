import sqlite3
import os

# ==========================
# Database Path
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "recruiter_ai.db")

print("DATABASE PATH:", DB_PATH)

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# ==========================
# Candidates Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT,
    email TEXT,
    phone TEXT,
    linkedin TEXT,
    github TEXT,

    skills TEXT,
    education TEXT,
    experience TEXT,
    certifications TEXT,

    summary TEXT,
    resume_text TEXT,

    batch_id INTEGER
)
""")

# ==========================
# Jobs Table
# ==========================

cursor.execute("""
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

    preferred_skills TEXT,

    responsibilities TEXT,

    job_description TEXT
)
""")

# ==========================
# Screening Results
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS screening_results(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_id INTEGER,

    job_id INTEGER,

    match_score REAL,

    recommendation TEXT,

    matched_skills TEXT,

    missing_skills TEXT,

    FOREIGN KEY(candidate_id)
        REFERENCES candidates(id),

    FOREIGN KEY(job_id)
        REFERENCES jobs(id)

)
""")

conn.commit()

# ==========================
# Schema Updates
# ==========================

def add_column(table, column, definition):

    try:

        cursor.execute(
            f"""
            ALTER TABLE {table}
            ADD COLUMN {column} {definition}
            """
        )

        print(f"{column} added to {table}")

    except sqlite3.OperationalError:

        print(f"{column} already exists")

# Candidate Columns

add_column(
    "candidates",
    "resume_text",
    "TEXT"
)

add_column(
    "candidates",
    "batch_id",
    "INTEGER"
)

# Job Columns

add_column(
    "jobs",
    "preferred_skills",
    "TEXT"
)

conn.commit()

conn.close()

print("Database created successfully.")
print("Schema update completed.")