from pathlib import Path
import csv


# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Location of the source CSV files
DATA_FOLDER = PROJECT_ROOT / "data"


def read_csv(file_name):
    """
    Reads one CSV file and returns all rows as a list of dictionaries.
    """
    file_path = DATA_FOLDER / file_name

    with file_path.open(mode="r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    return rows


if __name__ == "__main__":
    members = read_csv("members.csv")
    eligibility = read_csv("eligibility.csv")
    providers = read_csv("providers.csv")
    claims = read_csv("claims.csv")

    print("=" * 45)
    print("EXTRACT STAGE COMPLETED")
    print("=" * 45)
    print("Members extracted:", len(members))
    print("Eligibility records extracted:", len(eligibility))
    print("Providers extracted:", len(providers))
    print("Claims extracted:", len(claims))