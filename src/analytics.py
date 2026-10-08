from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / "healthcare_claims.db"


def run_analytics():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    print("=" * 55)
    print("HEALTHCARE CLAIMS SQL ANALYSIS")
    print("=" * 55)

    # Query 1: Claims by type
    print("\n1. VALID CLAIMS BY TYPE")

    cursor.execute(
        """
        SELECT
            claim_type,
            COUNT(*) AS claim_count,
            SUM(paid_amount) AS total_paid
        FROM valid_claims
        GROUP BY claim_type
        """
    )

    for claim_type, claim_count, total_paid in cursor.fetchall():
        print(
            claim_type,
            "- Claims:",
            claim_count,
            "- Total paid:",
            total_paid
        )

    # Query 2: Overall valid claim totals
    print("\n2. OVERALL VALID CLAIM TOTALS")

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_claims,
            SUM(billed_amount) AS total_billed,
            SUM(allowed_amount) AS total_allowed,
            SUM(paid_amount) AS total_paid
        FROM valid_claims
        """
    )

    total_claims, total_billed, total_allowed, total_paid = (
        cursor.fetchone()
    )

    print("Total valid claims:", total_claims)
    print("Total billed amount:", total_billed)
    print("Total allowed amount:", total_allowed)
    print("Total paid amount:", total_paid)

    # Query 3: Rejected claims and reasons
    print("\n3. REJECTED CLAIMS")

    cursor.execute(
        """
        SELECT
            claim_id,
            rejection_reason
        FROM rejected_claims
        """
    )

    for claim_id, rejection_reason in cursor.fetchall():
        print(claim_id, "-", rejection_reason)

    connection.close()


if __name__ == "__main__":
    run_analytics()