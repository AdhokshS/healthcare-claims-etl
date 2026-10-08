from pathlib import Path
import csv
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FOLDER = PROJECT_ROOT / "output"

DATABASE_FILE = PROJECT_ROOT / "healthcare_claims.db"


def read_output_file(file_name):
    """
    Reads a CSV file from the output folder.
    """
    file_path = OUTPUT_FOLDER / file_name

    with file_path.open(
        mode="r",
        encoding="utf-8",
        newline=""
    ) as file:
        return list(csv.DictReader(file))


def create_database():
    """
    Creates SQLite tables and loads valid and rejected claims.
    """
    valid_claims = read_output_file("valid_claims.csv")
    rejected_claims = read_output_file("rejected_claims.csv")

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Remove old tables so the script can be rerun safely
    cursor.execute("DROP TABLE IF EXISTS valid_claims")
    cursor.execute("DROP TABLE IF EXISTS rejected_claims")

    cursor.execute(
        """
        CREATE TABLE valid_claims (
            claim_id TEXT PRIMARY KEY,
            claim_type TEXT,
            member_id TEXT,
            provider_id TEXT,
            service_date TEXT,
            service_code TEXT,
            billed_amount REAL,
            allowed_amount REAL,
            paid_amount REAL,
            claim_status TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE rejected_claims (
            claim_id TEXT,
            claim_type TEXT,
            member_id TEXT,
            provider_id TEXT,
            service_date TEXT,
            service_code TEXT,
            billed_amount REAL,
            allowed_amount REAL,
            paid_amount REAL,
            claim_status TEXT,
            rejection_reason TEXT
        )
        """
    )

    for claim in valid_claims:
        cursor.execute(
            """
            INSERT INTO valid_claims VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                claim["claim_id"],
                claim["claim_type"],
                claim["member_id"],
                claim["provider_id"],
                claim["service_date"],
                claim["service_code"],
                float(claim["billed_amount"]),
                float(claim["allowed_amount"]),
                float(claim["paid_amount"]),
                claim["claim_status"],
            )
        )

    for claim in rejected_claims:
        cursor.execute(
            """
            INSERT INTO rejected_claims VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                claim["claim_id"],
                claim["claim_type"],
                claim["member_id"],
                claim["provider_id"],
                claim["service_date"],
                claim["service_code"],
                float(claim["billed_amount"]),
                float(claim["allowed_amount"]),
                float(claim["paid_amount"]),
                claim["claim_status"],
                claim["rejection_reason"],
            )
        )

    connection.commit()

    valid_count = cursor.execute(
        "SELECT COUNT(*) FROM valid_claims"
    ).fetchone()[0]

    rejected_count = cursor.execute(
        "SELECT COUNT(*) FROM rejected_claims"
    ).fetchone()[0]

    connection.close()

    print("=" * 50)
    print("SQL DATABASE LOAD COMPLETED")
    print("=" * 50)
    print("Database created:", DATABASE_FILE)
    print("Valid claims loaded:", valid_count)
    print("Rejected claims loaded:", rejected_count)


if __name__ == "__main__":
    create_database()