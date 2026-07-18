from database.database import get_connection


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # ---------------- Candidates ---------------- #

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

        batch_id INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ---------------- Jobs ---------------- #

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        job_title TEXT,

        company TEXT,

        company_email TEXT,

        company_linkedin TEXT,

        company_location TEXT,

        work_mode TEXT,

        employment_type TEXT,

        salary_range TEXT,

        notice_period TEXT,

        experience_required TEXT,

        education_required TEXT,

        required_skills TEXT,

        preferred_skills TEXT,

        responsibilities TEXT,

        job_description TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ---------------- Screening Results ---------------- #

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS screening_results(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        candidate_id INTEGER,

        job_id INTEGER,

        match_score REAL,

        recommendation TEXT,

        matched_skills TEXT,

        missing_skills TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- Document Batches ---------------- #

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_batches(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        batch_number INTEGER UNIQUE,

        start_candidate INTEGER,

        end_candidate INTEGER,

        document_name TEXT,

        status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()

    print("✅ Database tables created successfully.")