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
            "rows": [dict(zip(column_names, row)) for row in rows],
        }
    def save_changes(self, rows: list[dict]) -> list[dict]:
        self.create_table()

        try:
            with self.db_connection.cursor() as cursor:
                incoming_ids: list[int] = []

                for row in rows:
                    row_id = row.get("id")

                    try:
                        row_id = int(row_id) 
                    except:
                        row_id = None

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

                    saved_id = None

                    if row_id is not None:
                        cursor.execute(
                            """
                            UPDATE emails
                            SET
                                company_name = %s,
                                job_title = %s,
                                reference_number = %s,
                                update_type = %s,
                                contact_person = %s,
                                contact_email = %s,
                                short_summary = %s,
                                confidence = %s,
                                date = %s
                            WHERE id = %s
                            RETURNING id
                            """,
                            values + (row_id,),
                        )

                        result = cursor.fetchone()

                        if result is not None:
                            saved_id = result[0]

                    if saved_id is None:
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

                        result = cursor.fetchone()

                        if result is None:
                            raise RuntimeError(
                                "Der Datensatz konnte nicht gespeichert werden."
                            )

                        saved_id = result[0]

                    # Eventuell falsche/fehlende ID durch echte DB-ID ersetzen
                    row["id"] = saved_id
                    incoming_ids.append(saved_id)

                # Datensätze löschen, die in der vollständigen Tabelle
                # nicht mehr enthalten sind
                if incoming_ids:
                    cursor.execute(
                        """
                        DELETE FROM emails
                        WHERE id <> ALL(%s)
                        """,
                        (incoming_ids,),
                    )
                else:
                    cursor.execute("DELETE FROM emails")

            self.db_connection.commit()
            return rows

        except Exception:
            self.db_connection.rollback()
            raise