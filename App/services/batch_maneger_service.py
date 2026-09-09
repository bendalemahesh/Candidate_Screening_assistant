import sqlite3
import math
from database.update_schema import DB_PATH


BATCH_SIZE = 200

import os



class BatchManager:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DB_PATH = os.path.join(BASE_DIR, "database", "recruiter_ai.db")


    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


    def __init__(self, DB_PATH):

        self.conn = sqlite3.connect(DB_PATH,check_same_thread=False)
        self.cursor = self.conn.cursor()



    def calculate_batch_id(self, candidate_id):

        """
        Calculate batch number

        1-200     => Batch 1
        201-400   => Batch 2
        """

        return math.ceil(
            candidate_id / BATCH_SIZE
        )



    def assign_batch(self, candidate_id):

        batch_id = self.calculate_batch_id(
            candidate_id
        )


        self.cursor.execute(
            """
            UPDATE candidates

            SET batch_id = ?

            WHERE id = ?
            """,
            (
                batch_id,
                candidate_id
            )
        )


        self.conn.commit()


        return batch_id



    def update_all_candidates(self):

        self.cursor.execute(
            """
            SELECT id
            FROM candidates
            ORDER BY id
            """
        )


        candidates = self.cursor.fetchall()


        for candidate in candidates:

            candidate_id = candidate[0]

            batch_id = self.calculate_batch_id(
                candidate_id
            )


            self.cursor.execute(
                """
                UPDATE candidates

                SET batch_id = ?

                WHERE id = ?
                """,
                (
                    batch_id,
                    candidate_id
                )
            )


        self.conn.commit()


        print(
            f"Updated {len(candidates)} candidates"
        )



    def close(self):

        self.conn.close()



if __name__ == "__main__":


    manager = BatchManager()


    manager.update_all_candidates()


    manager.close()