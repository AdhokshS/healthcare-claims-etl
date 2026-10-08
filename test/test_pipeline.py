import unittest

from src.extract import read_csv
from src.transform import validate_claims


class TestHealthcarePipeline(unittest.TestCase):

    def setUp(self):
        self.members = read_csv("members.csv")
        self.eligibility = read_csv("eligibility.csv")
        self.providers = read_csv("providers.csv")
        self.claims = read_csv("claims.csv")

        self.valid_claims, self.rejected_claims = validate_claims(
            self.members,
            self.eligibility,
            self.providers,
            self.claims,
        )

    def test_source_count_reconciles(self):
        self.assertEqual(
            len(self.claims),
            len(self.valid_claims) + len(self.rejected_claims),
        )

    def test_expected_valid_claim_count(self):
        self.assertEqual(len(self.valid_claims), 4)

    def test_expected_rejected_claim_count(self):
        self.assertEqual(len(self.rejected_claims), 6)

    def test_duplicate_claim_is_rejected(self):
        duplicate_found = any(
            claim["claim_id"] == "C1002"
            and "Duplicate claim ID" in claim["rejection_reason"]
            for claim in self.rejected_claims
        )

        self.assertTrue(duplicate_found)

    def test_unknown_member_is_rejected(self):
        unknown_member_found = any(
            claim["member_id"] == "M999"
            and "Unknown member" in claim["rejection_reason"]
            for claim in self.rejected_claims
        )

        self.assertTrue(unknown_member_found)


if __name__ == "__main__":
    unittest.main()