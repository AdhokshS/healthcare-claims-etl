from src.extract import read_csv
from src.transform import validate_claims
from src.load import write_csv
from src.database import create_database
from src.analytics import run_analytics


def run_pipeline():
    print("=" * 60)
    print("HEALTHCARE CLAIMS ETL PIPELINE STARTED")
    print("=" * 60)

    # EXTRACT
    members = read_csv("members.csv")
    eligibility = read_csv("eligibility.csv")
    providers = read_csv("providers.csv")
    claims = read_csv("claims.csv")

    print("\nEXTRACT COMPLETED")
    print("Members:", len(members))
    print("Eligibility records:", len(eligibility))
    print("Providers:", len(providers))
    print("Claims:", len(claims))

    # TRANSFORM
    valid_claims, rejected_claims = validate_claims(
        members,
        eligibility,
        providers,
        claims,
    )

    print("\nTRANSFORM COMPLETED")
    print("Valid claims:", len(valid_claims))
    print("Rejected claims:", len(rejected_claims))

    # LOAD TO CSV
    write_csv("valid_claims.csv", valid_claims)
    write_csv("rejected_claims.csv", rejected_claims)

    print("\nCSV LOAD COMPLETED")

    # LOAD TO SQL DATABASE
    create_database()

    # RUN SQL ANALYTICS
    run_analytics()

    print("\n" + "=" * 60)
    print("HEALTHCARE CLAIMS ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()