from pathlib import Path
import csv

from src.extract import read_csv
from src.transform import validate_claims

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FOLDER = PROJECT_ROOT / "output"


def write_csv(file_name, records):
    """
    Writes a list of dictionaries into a CSV file.
    """
    if not records:
        print(f"No records available for {file_name}")
        return

    OUTPUT_FOLDER.mkdir(exist_ok=True)

    file_path = OUTPUT_FOLDER / file_name
    column_names = records[0].keys()

    with file_path.open(
        mode="w",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=column_names
        )

        writer.writeheader()
        writer.writerows(records)

    print(f"Created: {file_path}")


if __name__ == "__main__":
    members = read_csv("members.csv")
    eligibility = read_csv("eligibility.csv")
    providers = read_csv("providers.csv")
    claims = read_csv("claims.csv")

    valid_claims, rejected_claims = validate_claims(
        members,
        eligibility,
        providers,
        claims,
    )

    write_csv(
        "valid_claims.csv",
        valid_claims,
    )

    write_csv(
        "rejected_claims.csv",
        rejected_claims,
    )

    print("=" * 45)
    print("LOAD STAGE COMPLETED")
    print("=" * 45)
    print("Valid claims loaded:", len(valid_claims))
    print("Rejected claims loaded:", len(rejected_claims))