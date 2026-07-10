import psycopg
from app.schemas.updates import Updates


class SQLHandler:
    def __init__(self, db_connection: psycopg.Connection):
        self.db_connection = db_connection

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id SERIAL PRIMARY KEY,
                company_name TEXT NOT NULL,
                job_title TEXT,
                reference_number TEXT,
                update_type TEXT NOT NULL,
                contact_person TEXT,
                contact_email TEXT,
                short_summary TEXT,
                confidence TEXT,
                date TEXT
            )
            """)
        self.db_connection.commit()

    def insert_email(self, email: Updates):
        self.create_table()
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO emails (company_name, job_title, reference_number, update_type, contact_person, contact_email, short_summary, confidence, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                email.company_name,
                email.job_title,
                email.reference_number,
                email.update_type,
                email.contact_person,
                email.contact_email,
                email.short_summary,
                email.confidence,
                email.email_sent_date,
            ),
        )
        self.db_connection.commit()

    def get_all_emails(self):
        self.create_table()
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM emails")

        rows = cursor.fetchall()
        column_names = [desc.name for desc in cursor.description]

        return {
            "columns": column_names,
            "rows": [
                dict(zip(column_names, row))
                for row in rows
            ],
        }
    def save_changes(self, rows: list[dict]):
        self.create_table()

        with self.db_connection.cursor() as cursor:
            incoming_ids = []

            for row in rows:
                row_id = row.get("id")

                values = (
                    row["company_name"],
                    row.get("job_title"),
                    row.get("reference_number"),
                    row["update_type"],
                    row.get("contact_person"),
                    row.get("contact_email"),
                    row.get("short_summary"),
                    row.get("confidence"),
                    row.get("date"),
                )

                if row_id is None:
                    cursor.execute(
                        """
                        INSERT INTO emails (
                            company_name,
                            job_title,
                            reference_number,
                            update_type,
                            contact_person,
                            contact_email,
                            short_summary,
                            confidence,
                            date
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        values,
                    )

                    new_id = cursor.fetchone()[0]
                    incoming_ids.append(new_id)

                    row["id"] = new_id

                else:
                    cursor.execute(
                        """
                        INSERT INTO emails (
                            id,
                            company_name,
                            job_title,
                            reference_number,
                            update_type,
                            contact_person,
                            contact_email,
                            short_summary,
                            confidence,
                            date
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id)
                        DO UPDATE SET
                            company_name = EXCLUDED.company_name,
                            job_title = EXCLUDED.job_title,
                            reference_number = EXCLUDED.reference_number,
                            update_type = EXCLUDED.update_type,
                            contact_person = EXCLUDED.contact_person,
                            contact_email = EXCLUDED.contact_email,
                            short_summary = EXCLUDED.short_summary,
                            confidence = EXCLUDED.confidence,
                            date = EXCLUDED.date
                        """,
                        (row_id,) + values,
                    )

                    incoming_ids.append(row_id)

            if incoming_ids:
                cursor.execute(
                    "DELETE FROM emails WHERE NOT (id = ANY(%s))",
                    (incoming_ids,),
                )
            else:
                cursor.execute("DELETE FROM emails")

        self.db_connection.commit()
