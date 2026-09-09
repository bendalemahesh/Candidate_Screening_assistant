import os
import sqlite3

from database.update_schema import DB_PATH

BATCH_FOLDER = "App/storage/batches"


class DocumentGenerator:
    def __init__(self):
        print("Document Generator DB:", DB_PATH)

        os.makedirs(BATCH_FOLDER, exist_ok=True)

        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def generate_batch_document(self, batch_id):

        self.cursor.execute(
            """
            SELECT *
            FROM candidates
            WHERE batch_id = ?
            """,
            (batch_id,)
        )


        candidates = self.cursor.fetchall()


        if not candidates:

            print(
                f"No candidates found in batch {batch_id}"
            )

            return None



        document = ""


        for candidate in candidates:

            document += f"""

============================

Candidate ID:
{candidate[0]}

Name:
{candidate[1]}

Email:
{candidate[2]}

Phone:
{candidate[3]}

Location:
{candidate[4]}

Skills:
{candidate[7]}

Education:
{candidate[8]}

Experience:
{candidate[9]}

Summary:
{candidate[11]}

============================

"""


        file_path = os.path.join(
            BATCH_FOLDER,
            f"batch_{batch_id:03}.txt"
        )


        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(document)



        print(
            f"Created {file_path}"
        )


        return file_path



    def close(self):

        self.conn.close()



if __name__ == "__main__":


    generator = DocumentGenerator()


    generator.generate_batch_document(
        1
    )


    generator.close()