from datetime import datetime

from src.extract import read_csv


def convert_to_date(date_text):
    """
    Converts text such as 2026-05-10 into a Python date.
    """
    return datetime.strptime(date_text, "%Y-%m-%d").date()


def check_eligibility(member_id, service_date, eligibility_records):
    """
    Returns True when the member had active coverage
    on the claim's service date.
    """
    for record in eligibility_records:
        if record["member_id"] != member_id:
            continue

        coverage_start = convert_to_date(record["coverage_start"])
        coverage_end = convert_to_date(record["coverage_end"])

        if (
            record["status"] == "ACTIVE"
            and coverage_start <= service_date <= coverage_end
        ):
            return True

    return False


def validate_claims(members, eligibility, providers, claims):
    """
    Separates claims into valid and rejected records.
    """
    valid_claims = []
    rejected_claims = []

    member_ids = {member["member_id"] for member in members}
    provider_ids = {provider["provider_id"] for provider in providers}

    seen_claim_ids = set()

    for claim in claims:
        reasons = []

        claim_id = claim["claim_id"]
        member_id = claim["member_id"]
        provider_id = claim["provider_id"]
        claim_type = claim["claim_type"]

        service_date = convert_to_date(claim["service_date"])
        paid_amount = float(claim["paid_amount"])

        # Check duplicate claim ID
        if claim_id in seen_claim_ids:
            reasons.append("Duplicate claim ID")
        else:
            seen_claim_ids.add(claim_id)

        # Check member
        if member_id not in member_ids:
            reasons.append("Unknown member")

        # Check provider
        if provider_id not in provider_ids:
            reasons.append("Unknown provider")

        # Check active eligibility
        if not check_eligibility(member_id, service_date, eligibility):
            reasons.append("Member not eligible on service date")

        # Check negative paid amount
        if paid_amount < 0:
            reasons.append("Negative paid amount")

        # Check pharmacy drug code
        if claim_type == "PHARMACY":
            service_code = claim["service_code"]

            if not service_code.isdigit() or len(service_code) != 11:
                reasons.append("Invalid pharmacy NDC code")

        if reasons:
            rejected_claim = claim.copy()
            rejected_claim["rejection_reason"] = "; ".join(reasons)
            rejected_claims.append(rejected_claim)
        else:
            valid_claims.append(claim)

    return valid_claims, rejected_claims


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

    print("=" * 55)
    print("TRANSFORM AND VALIDATION STAGE COMPLETED")
    print("=" * 55)
    print("Source claims:", len(claims))
    print("Valid claims:", len(valid_claims))
    print("Rejected claims:", len(rejected_claims))

    print("\nREJECTED CLAIM DETAILS")

    for claim in rejected_claims:
        print(
            claim["claim_id"],
            "-",
            claim["rejection_reason"],
        )